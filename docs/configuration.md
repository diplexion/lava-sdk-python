# Инициализация и конфигурация

> *Неофициальный Python-порт PHP SDK Lava. Не аффилирован с Lava Payment. [← Оглавление](index.md)*

Данный раздел описывает, как правильно создать и настроить экземпляр `LavaFacade` для работы
с Lava Payment API.

---

## LavaFacade — главный класс

`LavaFacade` — это единственная точка входа в SDK. Все операции с API (создание инвойсов,
выводы средств, возвраты, H2H-платежи, проверка балансов, получение курсов валют и верификация
вебхуков) выполняются через методы этого класса.

Вы **не должны** напрямую создавать экземпляры `Client`, `ClientGenerateSignature` или
других внутренних компонентов — это происходит автоматически при инициализации `LavaFacade`.

```python
from lava_sdk.http.lava_facade import LavaFacade

facade = LavaFacade(
    secret_key="ваш_секретный_ключ",
    shop_id="ваш_shop_id",
)
```

---

## Параметры конструктора

Конструктор `LavaFacade.__init__` принимает 7 параметров:

| Параметр | Тип | Обязательный | Описание |
|---|---|---|---|
| `secret_key` | `str` | Да | Секретный ключ магазина для подписи запросов |
| `shop_id` | `str` | Да | Идентификатор магазина |
| `additional_key` | `Optional[str]` | Нет | Дополнительный ключ для верификации входящих webhook-уведомлений инвойсов |
| `client` | `Optional[Client]` | Нет | Кастомный HTTP-клиент (используется в тестах) |
| `client_generate_sign` | `Optional[ClientGenerateSignature]` | Нет | Кастомный генератор подписи |
| `client_check_webhook` | `Optional[ClientCheckSignatureWebhook]` | Нет | Кастомный верификатор вебхуков |
| `profile_secret_data` | `Optional[ProfileSecretDto]` | Нет | Данные профиля — обязательны для payoff/profile методов |

### Поведение по умолчанию

Если необязательные внутренние компоненты (`client`, `client_generate_sign`,
`client_check_webhook`) не переданы, `LavaFacade` автоматически создаёт их стандартные
реализации:

- `Client()` — стандартный HTTP-клиент, использующий `HttpClient` (библиотека `requests`)
- `ClientGenerateSignature(secret_key)` — генератор подписей для переданного `secret_key`
- `ClientCheckSignatureWebhook(additional_key)` — верификатор вебхуков для `additional_key`

---

## Инициализация только с методами магазина

Если вам нужны только операции на уровне магазина (создание инвойсов, возвраты, H2H, баланс
магазина, курсы валют), достаточно указать `secret_key` и `shop_id`.

Параметр `additional_key` рекомендуется указывать, если вы планируете проверять подписи
входящих вебхуков инвойсов.

```python
from lava_sdk.http.lava_facade import LavaFacade

# Минимальная инициализация — только операции магазина
facade = LavaFacade(
    secret_key="shop_secret_key_here",
    shop_id="shop_id_here",
)

# С поддержкой верификации вебхуков инвойсов
facade = LavaFacade(
    secret_key="shop_secret_key_here",
    shop_id="shop_id_here",
    additional_key="webhook_additional_key_here",
)
```

### Доступные методы при такой инициализации

| Метод | Описание |
|---|---|
| `create_invoice(dto)` | Создать платёжный инвойс |
| `check_status_invoice(dto)` | Проверить статус инвойса |
| `get_availible_tariffs()` | Получить доступные тарифы инвойсов |
| `create_refund(dto)` | Создать возврат |
| `check_status_refund(dto)` | Проверить статус возврата |
| `create_h2h_invoice(dto)` | Создать H2H-инвойс (оплата картой) |
| `create_h2h_spb_invoice(dto)` | Создать H2H-инвойс через СБП |
| `get_shop_balance()` | Получить баланс магазина *(устаревший метод)* |
| `get_payment_course_list()` | Получить курсы валют для платежей |
| `get_payoff_course_list()` | Получить курсы валют для выводов |
| `check_sign_webhook(body, sig)` | Верифицировать подпись вебхука инвойса |

---

## ProfileSecretDto — данные профиля

Для операций с выводами средств (Payoff) и профильным балансом необходимо дополнительно
передать объект `ProfileSecretDto`. Это требуется, потому что payoff-операции выполняются
от имени **профиля**, а не магазина, и используют отдельный набор ключей.

### Методы, требующие ProfileSecretDto

- `create_payoff(dto)` — создать вывод средств
- `get_status_payoff(dto)` — проверить статус вывода
- `get_payoff_tariffs()` — получить тарифы для выводов
- `check_wallet(dto)` — проверить корректность реквизитов кошелька
- `get_profile_balance()` — получить баланс профиля
- `check_payoff_signature(body, sig)` — верифицировать подпись payoff-вебхука

### Параметры ProfileSecretDto

| Параметр | Тип | Обязательный | Описание |
|---|---|---|---|
| `profile_id` | `str` | Да | Идентификатор профиля |
| `secret_key` | `str` | Да | Секретный ключ профиля |
| `additional_key` | `Optional[str]` | Нет | Дополнительный ключ для верификации payoff-вебхуков |

### Создание ProfileSecretDto

```python
from lava_sdk.dto.secret.profile_secret_dto import ProfileSecretDto

profile_data = ProfileSecretDto(
    profile_id="ваш_profile_id",
    secret_key="ваш_profile_secret_key",
    additional_key="ваш_profile_additional_key",  # необязательно
)
```

---

## Полная инициализация с ProfileSecretDto

Для использования всех возможностей SDK, включая выводы средств и управление балансом
профиля, передайте `ProfileSecretDto` при создании `LavaFacade`:

```python
from lava_sdk.dto.secret.profile_secret_dto import ProfileSecretDto
from lava_sdk.http.lava_facade import LavaFacade

# Объект с данными профиля
profile_data = ProfileSecretDto(
    profile_id="your_profile_id",
    secret_key="your_profile_secret_key",
    additional_key="your_profile_additional_key",
)

# Полная инициализация фасада
facade = LavaFacade(
    secret_key="your_shop_secret_key",
    shop_id="your_shop_id",
    additional_key="your_shop_webhook_key",
    profile_secret_data=profile_data,
)

# Теперь доступны все методы, включая payoff и баланс профиля
balance = facade.get_profile_balance()
print(f"Баланс: {balance.get_balance()} руб.")
```

---

## Безопасность ключей

> ⚠️ **Внимание!** Никогда не храните секретные ключи непосредственно в исходном коде.
> Жёсткое кодирование ключей в коде (hardcode) создаёт серьёзные риски безопасности:
> ключи могут попасть в систему контроля версий (Git) и стать доступны посторонним.
>
> Используйте **переменные окружения** или специализированные хранилища секретов
> (например, AWS Secrets Manager, HashiCorp Vault, Docker Secrets).

### Рекомендуемый способ: переменные окружения

```python
import os
from lava_sdk.http.lava_facade import LavaFacade

facade = LavaFacade(
    secret_key=os.environ["LAVA_SECRET_KEY"],
    shop_id=os.environ["LAVA_SHOP_ID"],
    additional_key=os.environ.get("LAVA_WEBHOOK_KEY"),
)
```

Обратите внимание:
- `os.environ["KEY"]` — обязательная переменная, при отсутствии выбрасывает `KeyError`
- `os.environ.get("KEY")` — необязательная переменная, возвращает `None` если не задана

### Полный пример с ProfileSecretDto через переменные окружения

```python
import os
from lava_sdk.dto.secret.profile_secret_dto import ProfileSecretDto
from lava_sdk.http.lava_facade import LavaFacade

profile_data = ProfileSecretDto(
    profile_id=os.environ["LAVA_PROFILE_ID"],
    secret_key=os.environ["LAVA_PROFILE_SECRET_KEY"],
    additional_key=os.environ.get("LAVA_PROFILE_ADDITIONAL_KEY"),
)

facade = LavaFacade(
    secret_key=os.environ["LAVA_SECRET_KEY"],
    shop_id=os.environ["LAVA_SHOP_ID"],
    additional_key=os.environ.get("LAVA_WEBHOOK_KEY"),
    profile_secret_data=profile_data,
)
```

---

## Пример .env файла

Для удобной работы с переменными окружения в локальной разработке используйте файл `.env`
в корне проекта (загружается библиотеками типа `python-dotenv`):

```bash
LAVA_SECRET_KEY=your_shop_secret_key
LAVA_SHOP_ID=your_shop_id
LAVA_WEBHOOK_KEY=your_webhook_additional_key
LAVA_PROFILE_ID=your_profile_id
LAVA_PROFILE_SECRET_KEY=your_profile_secret_key
LAVA_PROFILE_ADDITIONAL_KEY=your_profile_additional_key
```

> **Важно:** добавьте `.env` в `.gitignore`, чтобы файл с секретами не попал в репозиторий:
>
> ```text
> # .gitignore
> .env
> .env.local
> ```

Для автоматической загрузки `.env` в Python установите `python-dotenv`:

```bash
pip install python-dotenv
```

```python
from dotenv import load_dotenv
load_dotenv()  # загружает переменные из .env в os.environ

import os
from lava_sdk.http.lava_facade import LavaFacade

facade = LavaFacade(
    secret_key=os.environ["LAVA_SECRET_KEY"],
    shop_id=os.environ["LAVA_SHOP_ID"],
)
```

---

## Внедрение зависимостей (для тестирования)

`LavaFacade` поддерживает внедрение зависимостей (Dependency Injection) через параметры
конструктора `client`, `client_generate_sign` и `client_check_webhook`. Это позволяет
подменять реальные компоненты mock-объектами в тестах без каких-либо изменений в коде SDK.

### Архитектурный принцип

`Client`, `ClientGenerateSignature` и `ClientCheckSignatureWebhook` не привязаны жёстко
к `LavaFacade`. Любой объект с совместимым интерфейсом (duck typing) может быть передан
на их место.

### Пример внедрения mock-клиента в тестах

```python
import uuid
import pytest
from lava_sdk.dto.request.invoice.create_invoice_dto import CreateInvoiceDto
from lava_sdk.dto.response.invoice.created_invoice_dto import CreatedInvoiceDto
from lava_sdk.http.lava_facade import LavaFacade
from tests.Mocks.client_success_response_mock import ClientSuccessResponseMock
from tests.Mocks.client_error_response_mock import ClientErrorResponseMock


def test_create_invoice_success():
    # Передаём mock-клиент вместо реального HTTP-клиента
    facade = LavaFacade(
        secret_key=str(uuid.uuid4()),
        shop_id=str(uuid.uuid4()),
        client=ClientSuccessResponseMock(),  # <-- mock
    )
    response = facade.create_invoice(CreateInvoiceDto("300", str(uuid.uuid4())))
    assert isinstance(response, CreatedInvoiceDto)


def test_create_invoice_fail():
    facade = LavaFacade(
        secret_key=str(uuid.uuid4()),
        shop_id=str(uuid.uuid4()),
        client=ClientErrorResponseMock(),  # <-- mock с ошибками
    )
    with pytest.raises(Exception) as exc_info:
        facade.create_invoice(CreateInvoiceDto("300", str(uuid.uuid4())))
    assert "OrderId must be uniq" in str(exc_info.value)
```

### Создание собственного mock-клиента

Чтобы создать свой mock, достаточно реализовать методы с теми же именами, что и у класса `Client`:

```python
class MyCustomMockClient:
    """Минимальный mock для тестирования создания инвойса."""

    def create_invoice(self, data):
        return {
            "data": {
                "id": "test-invoice-id-123",
                "amount": 500,
                "expired": "2025-12-31 23:59:59",
                "status": 0,
                "shop_id": data.get("shopId"),
                "url": "https://pay.lava.ru/invoice/test-invoice-id-123",
                "comment": None,
                "merchantName": "Тестовый магазин",
                "exclude_service": None,
                "include_service": None,
            },
            "status": 200,
            "status_check": True,
        }


# Использование в тесте
facade = LavaFacade(
    secret_key="any-key",
    shop_id="any-shop-id",
    client=MyCustomMockClient(),
)
```

### Внедрение кастомного генератора подписи

В редких случаях может понадобиться заменить и генератор подписи — например, для
тестирования самого алгоритма подписи:

```python
from lava_sdk.http.client.client_generate_signature import ClientGenerateSignature
from lava_sdk.http.lava_facade import LavaFacade

# Кастомный генератор с известным ключом для воспроизводимых тестов
custom_signer = ClientGenerateSignature(secret_key="known-test-secret-key")

facade = LavaFacade(
    secret_key="known-test-secret-key",
    shop_id="test-shop-id",
    client_generate_sign=custom_signer,
)
```

> **Итог:** возможность внедрения зависимостей делает `LavaFacade` полностью тестируемым
> без необходимости реальных сетевых запросов к Lava API, что ускоряет тесты и делает
> их воспроизводимыми в любом окружении.
