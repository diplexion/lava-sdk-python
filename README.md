# Lava SDK для Python

![Python](https://img.shields.io/badge/python-%5E3.8-blue?style=plastic)
![License](https://img.shields.io/badge/license-MIT-green?style=plastic)
![Unofficial Port](https://img.shields.io/badge/неофициальный-порт-orange?style=plastic)

> ⚠️ **Это неофициальный порт.** Данный пакет является неофициальным портом официального PHP SDK Lava на Python, выполненным сообществом. Проект не аффилирован с компанией Lava Payment и не является официальным продуктом. Используйте на свой страх и риск.

Неофициальный Python-порт PHP SDK Lava. Предоставляет полный функционал для работы с API [Lava Payment](https://lava.ru) через класс `LavaFacade`.

## Документация

- [Установка и зависимости](docs/installation.md)
- [Инициализация и конфигурация](docs/configuration.md)
- [Инвойсы](docs/invoices.md)
- [Возвраты](docs/refunds.md)
- [Выводы средств](docs/payoffs.md)
- [H2H-платежи](docs/h2h.md)
- [Вебхуки и подписи](docs/webhooks.md)
- [Баланс](docs/balance.md)
- [Курсы валют](docs/courses.md)
- [Исключения](docs/exceptions.md)
- [Справочник классов](docs/reference.md)

## Быстрый старт

### Инициализация (только методы магазина)

```python
from lava_sdk.http.lava_facade import LavaFacade

facade = LavaFacade(
    secret_key="shop_secret_key",
    shop_id="shop_id",
    webhook_additional_key="shop_webhook_additional_key",  # optional
)
```

### Инициализация с методами профиля и выводов

Для методов профиля и выводов (`create_payoff`, `get_status_payoff`, `get_payoff_tariffs`, `check_wallet`, `get_profile_balance`, `check_payoff_signature`) необходимо передать `ProfileSecretDto`.

```python
from lava_sdk.http.lava_facade import LavaFacade
from lava_sdk.dto.secret.profile_secret_dto import ProfileSecretDto

profile_secret = ProfileSecretDto(
    profile_id="profile_id",
    secret_key="profile_secret_key",
    additional_key="profile_additional_key",  # optional, needed for check_payoff_signature
)

facade = LavaFacade(
    secret_key="shop_secret_key",
    shop_id="shop_id",
    webhook_additional_key="shop_webhook_additional_key",
    profile_secret=profile_secret,
)
```

## Основные методы

### Инвойсы

- `create_invoice(dto)` — создать новый инвойс (счёт на оплату)
- `check_status_invoice(dto)` — получить статус инвойса по его идентификатору
- `get_availible_tariffs()` — получить список доступных тарифов для оплаты

### Возвраты

- `create_refund(dto)` — создать возврат средств по инвойсу
- `check_status_refund(dto)` — получить статус возврата по его идентификатору

### Баланс

- `get_profile_balance()` — получить баланс профиля
- `get_shop_balance()` *(устарело)* — получить баланс магазина; используйте `get_profile_balance()`

### Выводы средств

- `create_payoff(dto)` — создать заявку на вывод средств
- `get_status_payoff(dto)` — получить статус вывода по его идентификатору
- `get_payoff_tariffs()` — получить список доступных тарифов для выводов
- `check_wallet(dto)` — проверить валидность кошелька перед выводом

### Вебхуки и подписи

- `check_sign_webhook(body, signature)` — проверить подпись входящего вебхука магазина
- `check_payoff_signature(body, signature)` — проверить подпись вебхука вывода средств

## Исключения

Все ошибки API выбрасываются в виде типизированных исключений. Оборачивайте вызовы фасада в `try/except`:

```python
from lava_sdk.exceptions.invoice_exception import InvoiceException
from lava_sdk.exceptions.payoff_exception import PayoffException
from lava_sdk.exceptions.base_exception import LavaBaseException

try:
    response = facade.create_invoice(dto)
except InvoiceException as e:
    print(f"Invoice error {e.code}: {e.message}")
except LavaBaseException as e:
    print(f"SDK error {e.code}: {e.message}")
```

## Тесты

```bash
pip install -r requirements-dev.txt
pytest
```

## Структура проекта

```text
lava_sdk/
├── constants/          # API base URL and endpoint paths
├── dto/
│   ├── request/        # Request DTOs (invoice, payoff, refund, h2h, …)
│   ├── response/       # Response DTOs
│   └── secret/         # ProfileSecretDto, ShopSecretDto
├── exceptions/         # Typed exception classes
└── http/
    ├── client.py       # Low-level HTTP client (requests library)
    ├── handlers/       # Request/response mappers per domain
    └── lava_facade.py  # Main entry point — LavaFacade

tests/
├── Mocks/              # Mock HTTP clients (success / error)
├── test_invoice.py
├── test_payoff.py
├── test_refund.py
├── test_webhook.py
└── …
```

## Лицензия

MIT
