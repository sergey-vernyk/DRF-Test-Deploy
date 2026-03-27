from django.urls import path

from . import views

urlpatterns = [
    path("", views.BookListCreateAPIView.as_view(), name="book_list_create"),
    path("<int:pk>/", views.BookDetailAPIView.as_view(), name="book_detail"),
    path("csrf_html/", views.book_csrf_html_demo, name="book_csrf_html"),
    path("csrf_api/", views.BookCSRFDemoView.as_view(), name="book_csrf_api"),
]
