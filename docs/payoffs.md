# Выводы средств (Payoff)

> *Неофициальный Python-порт PHP SDK Lava. Не аффилирован с Lava Payment. [← Оглавление](index.md)*

## Обзор

Методы выводов средств позволяют отправлять деньги на кошельки или счета пользователей через API Lava. С помощью этих методов можно автоматически переводить средства на банковские карты, электронные кошельки и другие платёжные системы, поддерживаемые Lava.

> **Важно:** Все методы раздела выводов требуют наличия объекта `ProfileSecretDto` с идентификатором профиля и секретным ключом профиля. Ключи профиля отличаются от ключей магазина и выдаются отдельно в личном кабинете Lava.

### Инициализация с ProfileSecretDto

Перед вызовом любого метода вывода необходимо создать экземпляр `ProfileSecretDto` и передать его в конструктор `LavaFacade` через параметр `profile_secret_data`:

```lava-sdk-python/docs/payoffs.md#L1-1
from lava_sdk.http.lava_facade import LavaFacade
from lava_sdk.dto.secret.profile_secret_dto import ProfileSecretDto

# Создаём объект с учётными данными профиля
profile_secret = ProfileSecretDto(
    profile_id="ваш-profile-id",           # ID профиля из личного кабинета Lava
    secret_key="ваш-profile-secret-key",   # Секретный ключ профиля
    additional_key="ваш-additional-key",   # Дополнительный ключ (нужен для проверки
                                           # подписи вебхуков вывода)
)

# Передаём profile_secret_data при инициализации фасада
facade = LavaFacade(
    secret_key="ваш-shop-secret-key",  # Секретный ключ магазина
    shop_id="ваш-shop-id",             # ID магазина
    profile_secret_data=profile_secret,
)
```

Если `profile_secret_data` не передан, при обращении к любому методу вывода будет выброшено исключение `ValueError: Profile Secret Data is None`.

---

## Создание вывода — `create_payoff`

> **Требует:** `ProfileSecretDto`

Метод создаёт заявку на вывод средств на указанный кошелёк получателя.

```lava-sdk-python/docs/payoffs.md#L1-1
facade.create_payoff(dto: CreatePayoffDto) -> CreatedPayoffDto
```

### Параметры CreatePayoffDto

| Параметр | Тип | Обязательный | Описание |
|---|---|---|---|
| `order_id` | `str` | Да | Уникальный ID операции в вашей системе. Используется для идентификации и защиты от дублирования. |
| `amount` | `float` | Да | Сумма вывода в рублях. |
| `service` | `str` | Да | Идентификатор сервиса вывода (например, `lava_payoff`). Полный список сервисов возвращает `get_payoff_tariffs()`. |
| `subtract` | `Optional[int]` | Нет | Способ списания комиссии: `0` — комиссия вычитается из суммы вывода, `1` — комиссия добавляется сверху к сумме. |
| `wallet_to` | `Optional[str]` | Нет | Адрес кошелька или номер телефона получателя. Формат зависит от выбранного сервиса. |
| `hook_url` | `Optional[str]` | Нет | URL для получения webhook-уведомлений об изменении статуса вывода. |

### Ответ: CreatedPayoffDto

| Поле | Тип | Описание |
|---|---|---|
| `payoff_id` | `str` | Уникальный ID вывода, присвоенный системой Lava. Используется для последующего запроса статуса. |
| `status` | `str` | Начальный статус вывода сразу после создания (обычно `pending`). |

Доступ к полям осуществляется через методы `get_payoff_id()` и `get_status()`.

### Пример использования

```lava-sdk-python/docs/payoffs.md#L1-1
from lava_sdk.http.lava_facade import LavaFacade
from lava_sdk.dto.secret.profile_secret_dto import ProfileSecretDto
from lava_sdk.dto.request.payoff.create_payoff_dto import CreatePayoffDto
from lava_sdk.exceptions.payoff.payoff_exception import PayoffException
from lava_sdk.exceptions.base_exception import LavaBaseException

# Инициализация
profile_secret = ProfileSecretDto(
    profile_id="ваш-profile-id",
    secret_key="ваш-profile-secret-key",
)

facade = LavaFacade(
    secret_key="ваш-shop-secret-key",
    shop_id="ваш-shop-id",
    profile_secret_data=profile_secret,
)

# Формируем DTO для создания вывода
dto = CreatePayoffDto(
    order_id="payoff-order-20240601-001",  # Уникальный ID в вашей системе
    amount=1500.00,                         # Сумма вывода: 1500 рублей
    service="lava_payoff",                  # Сервис вывода
    wallet_to="79001234567",                # Номер телефона или кошелька получателя
    subtract=0,                             # Комиссия вычитается из суммы
    hook_url="https://example.com/webhooks/payoff",
)

try:
    result = facade.create_payoff(dto)

    print(f"Вывод создан успешно!")
    print(f"  ID вывода:  {result.get_payoff_id()}")
    print(f"  Статус:     {result.get_status()}")

    # Сохраните payoff_id для последующей проверки статуса
    payoff_id = result.get_payoff_id()

except PayoffException as e:
    # Ошибка бизнес-логики API (неверные параметры, недостаточно средств и т.д.)
    print(f"Ошибка создания вывода [{e.code}]: {e}")
except LavaBaseException as e:
    # Любая другая ошибка SDK
    print(f"Ошибка SDK [{e.code}]: {e}")
```

---

## Статус вывода — `get_status_payoff`

> **Требует:** `ProfileSecretDto`

Метод возвращает текущий статус ранее созданного вывода, а также подробную информацию о суммах, комиссии и возможных ошибках.

```lava-sdk-python/docs/payoffs.md#L1-1
facade.get_status_payoff(dto: GetPayoffStatusDto) -> StatusPayoffDto
```

### Параметры GetPayoffStatusDto

| Параметр | Тип | Обязательный | Описание |
|---|---|---|---|
| `order_id` | `Optional[str]` | Нет | ID заказа в вашей системе, переданный при создании вывода. |
| `payoff_id` | `Optional[str]` | Нет | ID вывода, возвращённый системой Lava при создании (`CreatedPayoffDto.get_payoff_id()`). |

> **Примечание:** Необходимо передать хотя бы один из параметров — `order_id` или `payoff_id`. Если оба не указаны, API вернёт ошибку.

### Ответ: StatusPayoffDto

| Поле | Тип | Описание |
|---|---|---|
| `id` | `str` | ID вывода в системе Lava. |
| `order_id` | `str` | ID заказа из вашей системы. |
| `status` | `str` | Текущий статус вывода (см. таблицу статусов ниже). |
| `wallet` | `Optional[str]` | Адрес кошелька получателя (если был указан). |
| `service` | `str` | Идентификатор используемого сервиса вывода. |
| `amount_pay` | `float` | Сумма, которую отправил отправитель (с учётом комиссии). |
| `commission` | `float` | Размер комиссии за операцию. |
| `amount_receive` | `float` | Сумма, которую получит получатель. |
| `try_count` | `int` | Количество попыток обработки вывода. |
| `error_message` | `Optional[str]` | Сообщение об ошибке, если вывод завершился неудачей. |

Доступ к полям реализован через соответствующие геттеры: `get_id()`, `get_order_id()`, `get_status()`, `get_wallet()`, `get_service()`, `get_amount_pay()`, `get_commission()`, `get_amount_receive()`, `get_try_count()`, `get_error_message()`.

### Пример использования

```lava-sdk-python/docs/payoffs.md#L1-1
from lava_sdk.http.lava_facade import LavaFacade
from lava_sdk.dto.secret.profile_secret_dto import ProfileSecretDto
from lava_sdk.dto.request.payoff.get_payoff_status_dto import GetPayoffStatusDto
from lava_sdk.exceptions.payoff.payoff_exception import PayoffException
from lava_sdk.exceptions.base_exception import LavaBaseException

profile_secret = ProfileSecretDto(
    profile_id="ваш-profile-id",
    secret_key="ваш-profile-secret-key",
)

facade = LavaFacade(
    secret_key="ваш-shop-secret-key",
    shop_id="ваш-shop-id",
    profile_secret_data=profile_secret,
)

# ── Вариант 1: запрос статуса по payoff_id (ID вывода из Lava) ─────────────
dto_by_payoff_id = GetPayoffStatusDto(payoff_id="lava-payoff-id-abc123")

try:
    status = facade.get_status_payoff(dto_by_payoff_id)

    print(f"Статус вывода (по payoff_id):")
    print(f"  ID вывода:        {status.get_id()}")
    print(f"  ID заказа:        {status.get_order_id()}")
    print(f"  Статус:           {status.get_status()}")
    print(f"  Кошелёк:          {status.get_wallet()}")
    print(f"  Сервис:           {status.get_service()}")
    print(f"  Сумма отправки:   {status.get_amount_pay()} руб.")
    print(f"  Комиссия:         {status.get_commission()} руб.")
    print(f"  Сумма получения:  {status.get_amount_receive()} руб.")
    print(f"  Попыток:          {status.get_try_count()}")

    if status.get_error_message():
        print(f"  Ошибка:           {status.get_error_message()}")

except PayoffException as e:
    print(f"Ошибка получения статуса [{e.code}]: {e}")


# ── Вариант 2: запрос статуса по order_id (ID заказа из вашей системы) ─────
dto_by_order_id = GetPayoffStatusDto(order_id="payoff-order-20240601-001")

try:
    status = facade.get_status_payoff(dto_by_order_id)

    print(f"\nСтатус вывода (по order_id):")
    print(f"  Статус: {status.get_status()}")

    # Проверяем успешное завершение
    if status.get_status() == "success":
        print("  Вывод успешно выполнен.")
    elif status.get_status() == "error":
        print(f"  Вывод завершился ошибкой: {status.get_error_message()}")
    else:
        print("  Вывод ещё обрабатывается.")

except PayoffException as e:
    print(f"Ошибка получения статуса [{e.code}]: {e}")
except LavaBaseException as e:
    print(f"Ошибка SDK [{e.code}]: {e}")
```

### Возможные значения статуса

| Статус | Описание |
|---|---|
| `pending` | Заявка на вывод создана и ожидает начала обработки. |
| `process` | Вывод находится в процессе обработки платёжной системой. |
| `success` | Вывод успешно выполнен, средства зачислены получателю. |
| `error` | Вывод завершился ошибкой. Подробности — в поле `error_message`. |

---

## Тарифы вывода — `get_payoff_tariffs`

> **Требует:** `ProfileSecretDto`

Метод возвращает список доступных сервисов для вывода средств с информацией о комиссиях, минимальных и максимальных суммах. Рекомендуется вызывать этот метод перед созданием вывода, чтобы отобразить пользователю актуальные условия.

```lava-sdk-python/docs/payoffs.md#L1-1
facade.get_payoff_tariffs() -> List[TariffResponseDto]
```

### Ответ: List[TariffResponseDto]

| Поле | Тип | Описание |
|---|---|---|
| `service` | `str` | Уникальный идентификатор сервиса вывода. Используется в `CreatePayoffDto.service`. |
| `title` | `Optional[str]` | Человекочитаемое название сервиса (например, «QIWI», «ЮMoney»). |
| `currency` | `str` | Код валюты сервиса (например, `RUB`). |
| `percent` | `Optional[float]` | Процентная комиссия от суммы вывода. |
| `fix` | `Optional[float]` | Фиксированная комиссия за вывод в единицах валюты. |
| `min_sum` | `Optional[float]` | Минимальная сумма вывода для данного сервиса. |
| `max_sum` | `Optional[float]` | Максимальная сумма вывода для данного сервиса. |

Доступ к полям — через геттеры: `get_service()`, `get_title()`, `get_currency()`, `get_percent()`, `get_fix()`, `get_min_sum()`, `get_max_sum()`.

### Пример использования

```lava-sdk-python/docs/payoffs.md#L1-1
from lava_sdk.http.lava_facade import LavaFacade
from lava_sdk.dto.secret.profile_secret_dto import ProfileSecretDto
from lava_sdk.exceptions.payoff.error_get_payoff_tariff_exception import (
    ErrorGetPayoffTariffException,
)
from lava_sdk.exceptions.base_exception import LavaBaseException

profile_secret = ProfileSecretDto(
    profile_id="ваш-profile-id",
    secret_key="ваш-profile-secret-key",
)

facade = LavaFacade(
    secret_key="ваш-shop-secret-key",
    shop_id="ваш-shop-id",
    profile_secret_data=profile_secret,
)

try:
    tariffs = facade.get_payoff_tariffs()

    print(f"Доступные сервисы для вывода ({len(tariffs)} шт.):\n")

    for tariff in tariffs:
        title = tariff.get_title() or tariff.get_service()
        currency = tariff.get_currency()

        # Формируем строку с комиссией
        commission_parts = []
        if tariff.get_percent() is not None:
            commission_parts.append(f"{tariff.get_percent()}%")
        if tariff.get_fix() is not None:
            commission_parts.append(f"{tariff.get_fix()} {currency}")
        commission_str = " + ".join(commission_parts) if commission_parts else "нет данных"

        # Формируем строку с лимитами
        min_s = tariff.get_min_sum()
        max_s = tariff.get_max_sum()
        limits_str = ""
        if min_s is not None:
            limits_str += f"от {min_s} {currency}"
        if max_s is not None:
            limits_str += f" до {max_s} {currency}"
        limits_str = limits_str.strip() or "без ограничений"

        print(f"  Сервис:    {tariff.get_service()}")
        print(f"  Название:  {title}")
        print(f"  Валюта:    {currency}")
        print(f"  Комиссия:  {commission_str}")
        print(f"  Лимиты:    {limits_str}")
        print()

except ErrorGetPayoffTariffException as e:
    print(f"Не удалось получить тарифы [{e.code}]: {e}")
except LavaBaseException as e:
    print(f"Ошибка SDK [{e.code}]: {e}")
```

---

## Проверка кошелька — `check_wallet`

> **Требует:** `ProfileSecretDto`

Метод позволяет проверить корректность адреса кошелька или номера телефона перед созданием вывода. Рекомендуется использовать до вызова `create_payoff`, чтобы убедиться в валидности реквизитов получателя.

```lava-sdk-python/docs/payoffs.md#L1-1
facade.check_wallet(dto: CheckWalletRequestDto) -> CheckWalletResponseDto
```

### Параметры CheckWalletRequestDto

| Параметр | Тип | Обязательный | Описание |
|---|---|---|---|
| `service` | `str` | Да | Идентификатор сервиса, для которого производится проверка. Должен совпадать со значением из `TariffResponseDto.get_service()`. |
| `wallet_to` | `str` | Да | Адрес кошелька, номер телефона или иной идентификатор получателя в рамках указанного сервиса. |

### Ответ: CheckWalletResponseDto

| Поле | Тип | Описание |
|---|---|---|
| `status` | `bool` | `True` — кошелёк существует и является действительным для вывода. `False` — кошелёк недействителен или не найден. |

Доступ к полю через метод `get_status()`.

### Пример использования

```lava-sdk-python/docs/payoffs.md#L1-1
from lava_sdk.http.lava_facade import LavaFacade
from lava_sdk.dto.secret.profile_secret_dto import ProfileSecretDto
from lava_sdk.dto.request.payoff.check_wallet_request_dto import CheckWalletRequestDto
from lava_sdk.dto.request.payoff.create_payoff_dto import CreatePayoffDto
from lava_sdk.exceptions.payoff.check_wallet_exception import CheckWalletException
from lava_sdk.exceptions.payoff.payoff_exception import PayoffException
from lava_sdk.exceptions.base_exception import LavaBaseException

profile_secret = ProfileSecretDto(
    profile_id="ваш-profile-id",
    secret_key="ваш-profile-secret-key",
)

facade = LavaFacade(
    secret_key="ваш-shop-secret-key",
    shop_id="ваш-shop-id",
    profile_secret_data=profile_secret,
)

service = "lava_payoff"
wallet = "79001234567"

# Шаг 1: проверяем кошелёк перед выводом
check_dto = CheckWalletRequestDto(
    service=service,
    wallet_to=wallet,
)

try:
    check_result = facade.check_wallet(check_dto)

    if check_result.get_status():
        print(f"Кошелёк {wallet} действителен. Создаём вывод...")

        # Шаг 2: создаём вывод только при успешной проверке
        payoff_dto = CreatePayoffDto(
            order_id="verified-payoff-001",
            amount=2000.00,
            service=service,
            wallet_to=wallet,
            subtract=0,
        )

        try:
            result = facade.create_payoff(payoff_dto)
            print(f"Вывод создан: ID={result.get_payoff_id()}, статус={result.get_status()}")
        except PayoffException as e:
            print(f"Ошибка создания вывода [{e.code}]: {e}")

    else:
        print(f"Кошелёк {wallet} недействителен. Вывод не создан.")

except CheckWalletException as e:
    print(f"Ошибка проверки кошелька [{e.code}]: {e}")
except LavaBaseException as e:
    print(f"Ошибка SDK [{e.code}]: {e}")
```

---

## Обработка ошибок

Все методы раздела выводов могут выбрасывать следующие исключения:

| Исключение | Модуль | Описание |
|---|---|---|
| `PayoffException` | `lava_sdk.exceptions.payoff.payoff_exception` | Ошибка при создании вывода или запросе его статуса. |
| `CheckWalletException` | `lava_sdk.exceptions.payoff.check_wallet_exception` | Ошибка при проверке кошелька. |
| `ErrorGetPayoffTariffException` | `lava_sdk.exceptions.payoff.error_get_payoff_tariff_exception` | Ошибка при получении тарифов вывода. |

Все они наследуются от `LavaBaseException`, который содержит атрибуты `message` (текст ошибки) и `code` (числовой код).

```lava-sdk-python/docs/payoffs.md#L1-1
from lava_sdk.exceptions.payoff.payoff_exception import PayoffException
from lava_sdk.exceptions.payoff.check_wallet_exception import CheckWalletException
from lava_sdk.exceptions.payoff.error_get_payoff_tariff_exception import (
    ErrorGetPayoffTariffException,
)
from lava_sdk.exceptions.base_exception import LavaBaseException

# ── Обработка ошибок create_payoff ─────────────────────────────────────────
try:
    result = facade.create_payoff(payoff_dto)
    print(f"Вывод создан: {result.get_payoff_id()}")

except PayoffException as e:
    # Специфичная ошибка вывода (неверные реквизиты, недостаточно средств и т.д.)
    print(f"Ошибка вывода [{e.code}]: {e}")

except LavaBaseException as e:
    # Любая другая ошибка SDK (сетевая, авторизации и т.д.)
    print(f"Общая ошибка SDK [{e.code}]: {e}")


# ── Обработка ошибок check_wallet ──────────────────────────────────────────
try:
    check = facade.check_wallet(check_dto)
    print(f"Статус кошелька: {'действителен' if check.get_status() else 'недействителен'}")

except CheckWalletException as e:
    print(f"Ошибка проверки кошелька [{e.code}]: {e}")

except LavaBaseException as e:
    print(f"Общая ошибка SDK [{e.code}]: {e}")


# ── Обработка ошибок get_payoff_tariffs ────────────────────────────────────
try:
    tariffs = facade.get_payoff_tariffs()
    for t in tariffs:
        print(f"Сервис: {t.get_service()}, комиссия: {t.get_percent()}%")

except ErrorGetPayoffTariffException as e:
    print(f"Ошибка получения тарифов [{e.code}]: {e}")

except LavaBaseException as e:
    print(f"Общая ошибка SDK [{e.code}]: {e}")
```
