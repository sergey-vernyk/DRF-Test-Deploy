## Загальні відомості про SSL (TLS)

`SSL` (точніше сучасна версія називається `TLS`) — це механізм, який дозволяє браузеру і серверу обмінюватися даними у зашифрованому вигляді. Коли користувач відкриває сайт через HTTPS, його браузер хоче бути впевненим у двох речах: що він дійсно підключився до правильного сервера, і що ніхто по дорозі не може прочитати передані дані.

Для цього використовуються два ключі: `public key` і `private key`. Вони працюють у парі. `Public key` можна вільно показувати всім - він входить до складу HTTPS сертифіката і передається браузеру під час встановлення HTTPS-з’єднання. `Private key`, навпаки, завжди залишається тільки на сервері (часто в Nginx) і нікому не передається.

Ідея в тому, що дані, зашифровані `public key`, можна розшифрувати тільки за допомогою `private key`. Тому навіть якщо хтось перехопить трафік, без `private key` він не зможе його прочитати.

Зазвичай ці ключі мають такий формат:
- Сертифікат (про це нижче), який містить public key + інформацію про домен (в цьому випадку localhost), термін його дії і підпис CA (про це нижче)
```sh
-----BEGIN CERTIFICATE-----
MIIEHjCCAoagAwIBAgIQbSFynY90Fefy/xG2TkQTojANBgkqhkiG9w0BAQsFADBr
MR4wHAYDVQQKExVta2NlcnQgZGV2ZWxvcG1lbnQgQ0ExIDAeBgNVBAsMF3Nlcmdl
eUBsZW5vdm8tdGhpbmtib29rMScwJQYDVQQDDB5ta2NlcnQgc2VyZ2V5QGxlbm92
by10aGlua2Jvb2swHhcNMjYwMzMxMDkyMTAyWhcNMjgwNzAxMDkyMTAyWjBLMScw
JQYDVQQKEx5ta2NlcnQgZGV2ZWxvcG1lbnQgY2VydGlmaWNhdGUxIDAeBgNVBAsM
F3NlcmdleUBsZW5vdm8tdGhpbmtib29rMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A
MIIBCgKCAQEA17HgukAE/LJYFvAHN4pyb+8qlT1RakgNcq1chqbD2DoTfde7MM/D
W2FsVS3pAPoDcIFFdW200hatyhsC4VBL+DoO9svrZYQW8zREVkymGs4PTmznBgtV
O0m++8sl4nDG7rQvcQ0mpufM9nyNpeHL5R3KGgGz1vYTC6RXP2Hl/qXuJzTCB8eX
vPMIh7rXZF8d2Nlou6lhoOW40PABckKOKAtTsaxmh6UFahSKOhaJrbFfkt62p2Fh
5n8SrvFjBjU6C4idbiF8WYWasdEKe6UpGMbP6o9yAnoEvjlW3Hxey3mscoI9sooa
o0VfOjQDwH17o+nGKPd/pidGFcN7dpuzuQIDAQABo14wXDAOBgNVHQ8BAf8EBAMC
BaAwEwYDVR0lBAwwCgYIKwYBBQUHAwEwHwYDVR0jBBgwFoAUb3bAAb9TWjLTfDcr
xMLsUkDVTeEwFAYDVR0RBA0wC4IJbG9jYWxob3N0MA0GCSqGSIb3DQEBCwUAA4IB
gQC7JHbtCY4ZgfHYQJX2l7C8MPMc/P8ff7aDyLxIdxWlx9rmvK4o7GvhkolPxXiV
LpHmfMd+xnn27eLC077CfgGE3WvprM5Y8z+lUc9eOZ4uc/zoCUK6FRn/dwenKDgY
Agc5fiVsSAnRVrWhztTj+pyTVOjEOSAFIkO6YOmfgmz9/u8yxFNt6wZFCLDXN9oQ
gZQNCIxbhQ8DAsGqeNDkrJ3lJRr3sPlwf2gwL1ByRujcHg62Yne6cnhTfbCVN7Ue
4h39ge3yWl4jK5PTptiHleUB2USj0uS2VLuob+1Bak4RhMHcinikc3j8Uy/IJrkF
CQK3hrKYhiSbpbxTX0MVQ9u9NxoHwb1tsmhQhVjWr1SgElR93PZpBvCpAjm2F0ot
y9o+C/gfp9S6361AA2ulLALlfl+RGhu6wcphtIOuCSvG19mrpu3frb9DJINpI+BI
wgJMgiFdQTbbh4c1Bq2/LElYhz+KS8rFnQfSv+jd/tjM6dgFp3Ihwhy2G4EPm559
Hi4=
-----END CERTIFICATE-----
```

- private key
```sh
-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDXseC6QAT8slgW
8Ac3inJv7yqVPVFqSA1yrVyGpsPYOhN917swz8NbYWxVLekA+gNwgUV1bbTSFq3K
GwLhUEv4Og72y+tlhBbzNERWTKYazg9ObOcGC1U7Sb77yyXicMbutC9xDSam58z2
fI2l4cvlHcoaAbPW9hMLpFc/YeX+pe4nNMIHx5e88wiHutdkXx3Y2Wi7qWGg5bjQ
8AFyQo4oC1OxrGaHpQVqFIo6FomtsV+S3ranYWHmfxKu8WMGNToLiJ1uIXxZhZqx
0Qp7pSkYxs/qj3ICegS+OVbcfF7Leaxygj2yihqjRV86NAPAfXuj6cYo93+mJ0YV
w3t2m7O5AgMBAAECggEBALqXQGcetrG7voSpRDUB6Zl3dokAMIwWpLuNyTsazNUi
+HWmyGKjeMZ2cvcE7kpP/eW3jtTVANW1lMX/s/AiPHYSE5vgMFTzfb8KeguF5zPN
CmS3xOrvpt3RIAxGYxGOqikZaukLjWJZqG+atBbKTE56BLmWu3K8ESHDG07Ta9lr
LuhMzykvByAd+7JGFecLCDO3WbXWcBUSkjAAXar8bS4r8j4tauiyLcGRXTtXwJYP
9iCZnjtVm5pHbHjwsZQ20z4oDFoXfj1awghi9mngsLJDUuWJVWl3ofuKVcejoOMM
8I0GL8AimGfRwldP0PUTTYr5thHj5xDasxFNJMa6JXkCgYEA8j8eBlb7YHkeic9w
1xXkButQ9ggtSxd3hBIFc7GptFpfJG+sAyUQMx+jhqDAZrcEj+vNfORyXheQwyDU
m4DKA5L9j+ftgpCDofE/piSc8KejJE6RILI7NbfddbReZbyZh7xELkCupTjVWCl4
LQhMVKYGKmDPcIU3lwoe2B33Th8CgYEA4/DZn4zc3habbemCN848vk3LuNtrOkZD
s2SfVibanQNyXd2tqPDb3aTRamwKuDNel+SfkUj2aDAN00mrs155vvpkqPbPfKqv
s9465ifpqD2b1K2cm42daQYtRh9p90IEv2KKVQbUfkzjPAuH/azI5XiWN7raoe6i
j1Z9loONkycCgYBtRlGJ9JTCiQBglAXH0GUjReUohrm/xN8x4Vs6PCtcYuPGMOW8
KWzsUtpWMY95Bhf1wB3at8ZrcV/o1Zdyah82i4j78FgwbHYkiAn5LUzqNgSerR5E
TIHvEnjAztNCO1haZW+wGZduinuaoGJIlhSwno/rb+5DSKSx6mvNe38CawKBgQCA
YNNA4EY5M0RhGCYGJjrh99DokXQIAzD4JZD0Jbf0vM85/LNlNhqu77gelzFGY3BA
XjxcyFo3ffEbch+pS2mIXWA6JZ/gmAWTaXOE0y/vWJueohVVKuJgF2GCYAj/gIhJ
/kbo8orVg5pr5Ba4kgsn6s24H54pm8ykrFLZZchj+wKBgG6BROS51+WV9ljPOQpU
hmuT4GLZ/n9abxBX28E2vgfBknwq6+U1PxlnPu/NDWKk1En+Ql7yxMIEyp8TekGR
i5gImRdCxfDsA7nQPyxxG59SS8ulr0j5XoBTDoYR1PgPNoOvIsZ59g7Oos/i/jSN
tdTFIH2updFozxhoUFG8LPzF
-----END PRIVATE KEY-----
```

Але тут виникає важливе питання: як браузер розуміє, що `public key` дійсно належить саме цьому сайту, а не комусь іншому? Саме для цього існує сертифікат.

Сертифікат — це файл, у якому зберігається `public key`, доменне ім’я сайту і цифровий підпис організації, яка підтверджує справжність цього сертифіката. Такі організації називаються `Certificate Authorities (CA)`. Однією з найвідоміших сьогодні є `Let's Encrypt`.

Коли браузер отримує сертифікат, він перевіряє:

- чи збігається домен у сертифікаті з адресою сайту
- чи не закінчився термін дії сертифіката
- чи підписаний він довіреним CA

Якщо все правильно — браузер показує замочок 🔒 і встановлює захищене HTTPS з’єднання.

У production зазвичай використовується `Let's Encrypt`, тому що це безкоштовний сервіс, який автоматично видає сертифікати для доменів (в основному на термін 90 днів). Щоб отримати сертифікат, сервер повинен довести, що він реально контролює домен. Найчастіше це робиться через `HTTP challenge`: спеціальний файл тимчасово розміщується на сервері, а CA перевіряє, чи доступний він за потрібною адресою. Нижче це налаштування є в нашому `default.conf` файлі для `nginx`.

```conf
    # default.conf
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;    # шлях до тимчасових файлів certbot
        allow all;                # дозволяємо доступ з інтернету
    }
```

Після успішної перевірки сервер отримує два важливі файли:

- `fullchain.pem` — сам сертифікат і ланцюжок довіри
- `privkey.pem` — приватний ключ

Саме ці файли потім використовуються у `nginx`:

```conf
# default.conf
ssl_certificate     fullchain.pem
ssl_certificate_key privkey.pem
```

У нашій архітектурі `nginx` бере на себе всю роботу з `HTTPS`: браузер встановлює захищене з’єднання саме з `nginx`, а вже `nginx` передає запит у backend всередині Docker network звичайним `HTTP`. Це зручно, тому що backend не потрібно окремо налаштовувати для `SSL`.

Сучасний HTTPS працює дуже швидко, хоча раніше SSL вважався дорогим по ресурсах. Сьогодні майже весь інтернет працює через `HTTPS`, тому що це вже стандарт безпеки.

Якщо пояснити дуже абстрактно:

- `Public key` можна всім показати.
- `Private key` знає тільки сервер.
- `CA` підтверджує, що ключ справжній.
- `HTTPS` робить з’єднання безпечним.

Саме тому сьогодні майже кожен production-сайт починається з правильного `SSL` налаштування.

- `HTTP` — це як лист з вашими даними.
- `HTTPS` — це запечатаний конверт і тільки ви його можете відкрити і прочитати.