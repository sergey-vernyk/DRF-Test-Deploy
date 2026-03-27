import logging
import random
import socket

from django.db import DatabaseError
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import HttpRequest, Request
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView

from .models import Book
from .serializers import BookSerializer

logger = logging.getLogger(__name__)


def book_csrf_html_demo(request: HttpRequest) -> HttpResponse:
    """HTML сторінка для демонстрації CSRF атаки."""
    return render(request, template_name="books/csrf_demo.html")


class BookCSRFDemoView(APIView):
    """Ендпоінт для демонстрації CSRF атаки."""

    parser_classes = [FormParser]
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def post(self, request: Request) -> Response:
        title = request.data.get("title")

        return Response(
            {"message": f"Book '{title}' created"},
            status=status.HTTP_201_CREATED,
        )


@api_view(["GET"])
def check_pod_host(_: Request) -> Response:
    """Перевірка імені хосту (pod) який прийняв клієнтський запит."""
    return Response(
        {"hostname": socket.gethostname(), "random": random.randint(1, 100000)}
    )


class BookListCreateAPIView(APIView):
    """View для створення книги і для отримання списку книг."""

    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    http_method_names = ["options", "get", "post"]

    def get(self, _: Request) -> Response:
        books = Book.objects.select_related("publisher").prefetch_related("authors")
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = BookSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            logger.warning(e.detail, extra={"user": request.user.pk})
            raise e

        serializer.save()
        logger.info("New book created!", extra={"user": request.user.pk})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BookDetailAPIView(APIView):
    """View для оновлення, видалення та отримання книги."""

    http_method_names = ["options", "get", "put", "patch", "delete"]

    def get_object(self, pk: int) -> Book:
        try:
            return get_object_or_404(Book, pk=pk)
        except Http404 as e:
            logger.warning("Book with ID %d not found.", pk)
            raise e
        except DatabaseError as e:
            logger.error(str(e), exc_info=True)
            raise e

    def get(self, _: Request, pk: int) -> Response:
        book = self.get_object(pk)
        serializer = BookSerializer(instance=book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, pk: int) -> Response:
        book = self.get_object(pk)
        serializer = BookSerializer(instance=book, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request, pk: int) -> Response:
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request: Request, pk: int) -> Response:
        book = self.get_object(pk)
        try:
            book.delete()
        except DatabaseError as e:
            logger.error(
                "Database error while book deleting.",
                extra={"error": str(e)},
                exc_info=True,
            )
            raise e

        logger.info("Book with ID %d deleted!", pk, extra={"user": request.user.pk})
        return Response(status=status.HTTP_204_NO_CONTENT)
