# Исключения и обработка ошибок

> *Неофициальный Python-порт PHP SDK Lava. Не аффилирован с Lava Payment. [← Оглавление](index.md)*

## Иерархия исключений

Все исключения Python Lava SDK наследуются от стандартного класса `Exception`. Библиотека разделяет ошибки на два независимых дерева: `LavaBaseException` охватывает все предметные ошибки API, тогда как `UnauthorizedException` выделен отдельно для ошибок авторизации.

```lava-sdk-python/docs/exceptions.md#L1-1
Exception
└── LavaBaseException                     (все SDK-исключения)
    ├── InvoiceException                  (ошибки инвойсов)
    ├── RefundException                   (ошибки возвратов)
    ├── PayoffException                   (ошибки выводов)
    ├── CheckWalletException              (ошибки проверки кошелька)
    ├── ErrorGetPayoffTariffException     (ошибки получения тарифов вывода)
    ├── PayoffServiceException            (ошибки payoff-сервиса)
    ├── ProfileException                  (ошибки профиля)
    ├── ShopException                     (ошибки магазина, устарело)
    ├── H2hException                      (ошибки H2H-платежей)
    └── CourseException                   (ошибки курсов валют)

Exception
└── UnauthorizedException                 (ошибки авторизации, HTTP 401)
```

Обратите внимание: `UnauthorizedException` **не наследуется** от `LavaBaseException`. Это значит, что перехват `LavaBaseException` не защитит вас от `UnauthorizedException` — её нужно обрабатывать явно или через базовый `Exception`.

---

## LavaBaseException

**Модуль:** `lava_sdk.exceptions.base_exception`

`LavaBaseException` — корневой класс всех предметных ошибок SDK. Он расширяет стандартный `Exception` двумя дополнительными атрибутами:

| Атрибут | Тип | Описание |
|---|---|---|
| `message` | `str` | Текстовое описание ошибки. Доступно через `str(exception)` или `exception.args[0]`. Соответствует тексту, переданному в конструктор. |
| `code` | `int` | HTTP-статус ответа сервера Lava, вызвавшего исключение. Равен `0`, если код недоступен или неприменим. |

### Конструктор

```lava-sdk-python/lava_sdk/exceptions/base_exception.py#L1-8
LavaBaseException(message: str = "", code: int = 0)
```

### Пример использования

```lava-sdk-python/docs/exceptions.md#L1-1
from lava_sdk.exceptions.base_exception import LavaBaseException

try:
    response = facade.create_invoice(dto)
except LavaBaseException as e:
    print(f"Код: {e.code}, Сообщение: {e}")
    # Например: "Код: 422, Сообщение: Validation error"
```

---

## Справочник исключений

| Класс | Модуль | Вызывается при |
|---|---|---|
| `LavaBaseException` | `lava_sdk.exceptions.base_exception` | Базовое исключение SDK; перехватывает любую предметную ошибку |
| `InvoiceException` | `lava_sdk.exceptions.invoice.invoice_exception` | Ошибка при работе с инвойсами: создание, проверка статуса, тарифы |
| `RefundException` | `lava_sdk.exceptions.refund.refund_exception` | Ошибка при создании возврата или проверке его статуса |
| `PayoffException` | `lava_sdk.exceptions.payoff.payoff_exception` | Ошибка при создании или получении статуса выплаты |
| `CheckWalletException` | `lava_sdk.exceptions.payoff.check_wallet_exception` | Ошибка при проверке валидности кошелька получателя выплаты |
| `ErrorGetPayoffTariffException` | `lava_sdk.exceptions.payoff.error_get_payoff_tariff_exception` | Ошибка при получении списка тарифов для выплат |
| `PayoffServiceException` | `lava_sdk.exceptions.payoff.payoff_service_exception` | Ошибка на уровне payoff-сервиса (например, недоступный сервис) |
| `ProfileException` | `lava_sdk.exceptions.profile.profile_exception` | Ошибка профиля: получение баланса профиля |
| `ShopException` | `lava_sdk.exceptions.shop.shop_exception` | Ошибка магазина (устарело — используйте `ProfileException`) |
| `H2hException` | `lava_sdk.exceptions.h2h.h2h_exception` | Ошибка H2H-платежа по карте или через СБП |
| `CourseException` | `lava_sdk.exceptions.course.course_exception` | Ошибка при получении курсов валют или некорректная структура ответа |
| `UnauthorizedException` | `lava_sdk.exceptions.unauthorized_exception` | Ошибка авторизации (HTTP 401) — неверный или просроченный ключ API |

---

## Паттерны обработки ошибок

### Перехват конкретного исключения

Если вы хотите по-разному реагировать на ошибки разных операций, перехватывайте конкретные типы исключений. Это позволяет точно понять контекст ошибки и применить нужную логику повторной попытки или уведомления.

```lava-sdk-python/docs/exceptions.md#L1-1
from lava_sdk.exceptions.invoice.invoice_exception import InvoiceException
from lava_sdk.exceptions.unauthorized_exception import UnauthorizedException

try:
    invoice = facade.create_invoice(dto)
    print(f"Инвойс создан: {invoice.get_invoice_id()}")
except UnauthorizedException as e:
    # Неверный API-ключ — нет смысла повторять запрос
    print(f"Ошибка авторизации (код {e.code}): {e}")
except InvoiceException as e:
    # Ошибка конкретно при работе с инвойсом
    print(f"Ошибка инвойса (код {e.code}): {e}")
```

Аналогичным образом можно перехватывать `PayoffException`, `RefundException`, `H2hException` и другие специфичные классы.

### Перехват всех SDK-исключений

Если вам нужна единая точка обработки любой ошибки от Lava SDK, используйте `LavaBaseException`. Помните, что `UnauthorizedException` не входит в это дерево и требует отдельной обработки.

```lava-sdk-python/docs/exceptions.md#L1-1
from lava_sdk.exceptions.base_exception import LavaBaseException
from lava_sdk.exceptions.unauthorized_exception import UnauthorizedException

try:
    invoice = facade.create_invoice(dto)
except UnauthorizedException as e:
    # Всегда обрабатываем UnauthorizedException отдельно
    print(f"Авторизация не пройдена: {e}")
except LavaBaseException as e:
    # Любая другая ошибка Lava SDK
    print(f"Ошибка Lava SDK — код: {e.code}, сообщение: {e}")
```

### Обработка по HTTP-коду

Поле `code` содержит HTTP-статус ответа от сервера Lava. Это позволяет разделить логику обработки по типу ошибки — клиентская она или серверная.

```lava-sdk-python/docs/exceptions.md#L1-1
from lava_sdk.exceptions.base_exception import LavaBaseException
from lava_sdk.exceptions.unauthorized_exception import UnauthorizedException

try:
    invoice = facade.create_invoice(dto)
except UnauthorizedException as e:
    print(f"Неверный ключ API (HTTP {e.code})")
except LavaBaseException as e:
    if e.code == 422:
        print("Ошибка валидации — проверьте параметры запроса")
    elif e.code == 400:
        print("Некорректный запрос — проверьте обязательные поля")
    elif e.code == 404:
        print("Ресурс не найден — проверьте идентификаторы")
    elif e.code == 429:
        print("Превышен лимит запросов — повторите позже")
    elif e.code == 500:
        print("Внутренняя ошибка сервера Lava — повторите запрос")
    elif e.code == 503:
        print("Сервис Lava временно недоступен")
    else:
        print(f"Неожиданная ошибка с кодом {e.code}: {e}")
```

### Логирование ошибок

Для production-окружения рекомендуется использовать стандартный модуль `logging` вместо `print`. Это позволяет направлять логи в системы мониторинга (Sentry, Datadog, ELK и т.д.).

```lava-sdk-python/docs/exceptions.md#L1-1
import logging
from lava_sdk.exceptions.base_exception import LavaBaseException
from lava_sdk.exceptions.unauthorized_exception import UnauthorizedException

logger = logging.getLogger(__name__)

try:
    response = facade.create_invoice(dto)
except UnauthorizedException as e:
    logger.critical(
        "Lava API: ошибка авторизации",
        extra={"code": e.code, "message": str(e)},
    )
    raise
except LavaBaseException as e:
    logger.error(
        "Lava API error",
        extra={"code": e.code, "message": str(e)},
        exc_info=True,
    )
    raise
```

### Повторная попытка при временных ошибках

Ошибки с кодами 500, 502, 503 и 504 обычно временные. Приведённый ниже пример демонстрирует простую стратегию повторных попыток с экспоненциальной задержкой.

```lava-sdk-python/docs/exceptions.md#L1-1
import time
import logging
from lava_sdk.exceptions.base_exception import LavaBaseException

logger = logging.getLogger(__name__)

def create_invoice_with_retry(facade, dto, max_attempts: int = 3):
    """Создать инвойс с повторными попытками при серверных ошибках."""
    retryable_codes = {500, 502, 503, 504}

    for attempt in range(1, max_attempts + 1):
        try:
            return facade.create_invoice(dto)
        except LavaBaseException as e:
            if e.code not in retryable_codes or attempt == max_attempts:
                logger.error(f"Не удалось создать инвойс после {attempt} попыток: {e}")
                raise
            delay = 2 ** attempt  # 2, 4, 8 секунд...
            logger.warning(f"Попытка {attempt} не удалась (код {e.code}), повтор через {delay}с")
            time.sleep(delay)
```

---

## ValueError

Помимо исключений SDK, некоторые методы `LavaFacade` выбрасывают стандартный `ValueError` (не наследник `LavaBaseException`) в случае неверной конфигурации. Это сигнализирует о программной ошибке, а не об ошибке API.

### Когда возникает `ValueError`

**1. `profile_secret_data` не передан в `LavaFacade`, но вызывается метод, требующий профиля**

Методы `create_payoff`, `get_status_payoff`, `get_payoff_tariffs`, `check_wallet`, `get_profile_balance` и `check_payoff_signature` требуют, чтобы в конструктор `LavaFacade` был передан объект `ProfileSecretDto`. Если он не задан, будет выброшен `ValueError("Profile Secret Data is None")`.

```lava-sdk-python/docs/exceptions.md#L1-1
from lava_sdk.http.lava_facade import LavaFacade
from lava_sdk.dto.request.payoff.create_payoff_dto import CreatePayoffDto

# Создание фасада БЕЗ profile_secret_data
facade = LavaFacade(secret_key="...", shop_id="...")

dto = CreatePayoffDto(order_id="order-1", amount=100.0, service="lava_payoff")

try:
    result = facade.create_payoff(dto)
except ValueError as e:
    print(f"Ошибка конфигурации: {e}")
    # Вывод: "Ошибка конфигурации: Profile Secret Data is None"
```

**Решение:** передайте `ProfileSecretDto` в конструктор `LavaFacade`:

```lava-sdk-python/docs/exceptions.md#L1-1
from lava_sdk.dto.secret.profile_secret_dto import ProfileSecretDto
from lava_sdk.http.lava_facade import LavaFacade

profile = ProfileSecretDto(
    profile_id="ваш_profile_id",
    secret_key="ваш_profile_secret_key",
    additional_key="ваш_payoff_webhook_key",  # нужен для check_payoff_signature
)

facade = LavaFacade(
    secret_key="ваш_shop_secret_key",
    shop_id="ваш_shop_id",
    profile_secret_data=profile,
)
```

**2. `additional_key` равен `None` при вызове `check_payoff_signature`**

Если `ProfileSecretDto` передан, но его `additional_key` равен `None`, метод `check_payoff_signature` выбросит `ValueError("Payoff Additional Key is None")`.

```lava-sdk-python/docs/exceptions.md#L1-1
from lava_sdk.dto.secret.profile_secret_dto import ProfileSecretDto
from lava_sdk.http.lava_facade import LavaFacade

# additional_key НЕ задан
profile = ProfileSecretDto(
    profile_id="...",
    secret_key="...",
    # additional_key не передан — по умолчанию None
)

facade = LavaFacade(
    secret_key="...",
    shop_id="...",
    profile_secret_data=profile,
)

try:
    is_valid = facade.check_payoff_signature(raw_body, signature)
except ValueError as e:
    print(f"Ошибка конфигурации: {e}")
    # Вывод: "Ошибка конфигурации: Payoff Additional Key is None"
```

### Рекомендованный шаблон обработки конфигурационных ошибок

Оборачивайте `ValueError` отдельно от исключений SDK, чтобы отличать ошибки конфигурации от ошибок API:

```lava-sdk-python/docs/exceptions.md#L1-1
from lava_sdk.exceptions.base_exception import LavaBaseException
from lava_sdk.exceptions.unauthorized_exception import UnauthorizedException

try:
    result = facade.create_payoff(dto)
except ValueError as e:
    # Ошибка конфигурации приложения — нужно исправить код или окружение
    logger.critical(f"Неверная конфигурация Lava SDK: {e}")
    raise RuntimeError(f"Lava SDK не сконфигурирован: {e}") from e
except UnauthorizedException as e:
    logger.error(f"Неверный ключ API: {e}")
    raise
except LavaBaseException as e:
    logger.error(f"Ошибка Lava API (код {e.code}): {e}")
    raise
```
