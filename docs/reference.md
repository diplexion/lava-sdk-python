# Справочник классов и DTO

> *Неофициальный Python-порт PHP SDK Lava. Не аффилирован с Lava Payment. [← Оглавление](index.md)*

## LavaFacade

**Модуль:** `lava_sdk.http.lava_facade`

`LavaFacade` — главная точка входа в Python Lava SDK. Все операции с API Lava выполняются через методы этого класса. Он инкапсулирует HTTP-клиент, генерацию подписей и маппинг ответов в DTO.

### Конструктор

```lava-sdk-python/lava_sdk/http/lava_facade.py#L52-70
LavaFacade(
    secret_key: str,
    shop_id: str,
    additional_key: Optional[str] = None,
    client: Optional[Client] = None,
    client_generate_sign: Optional[ClientGenerateSignature] = None,
    client_check_webhook: Optional[ClientCheckSignatureWebhook] = None,
    profile_secret_data: Optional[ProfileSecretDto] = None,
)
```

| Параметр | Тип | Обязательный | Описание |
|---|---|---|---|
| `secret_key` | `str` | Да | Секретный ключ магазина для подписи запросов к API инвойсов, возвратов, H2H и курсов |
| `shop_id` | `str` | Да | Идентификатор магазина в системе Lava |
| `additional_key` | `str \| None` | Нет | Ключ для верификации вебхуков инвойса; если не задан, `check_sign_webhook` упадёт с ошибкой |
| `client` | `Client \| None` | Нет | Пользовательский HTTP-клиент (для тестирования/мокирования) |
| `client_generate_sign` | `ClientGenerateSignature \| None` | Нет | Пользовательский генератор подписей |
| `client_check_webhook` | `ClientCheckSignatureWebhook \| None` | Нет | Пользовательский верификатор вебхуков |
| `profile_secret_data` | `ProfileSecretDto \| None` | Нет | Данные авторизации профиля; обязательны для методов выплат и баланса профиля |

### Таблица публичных методов

| Метод | Параметры | Возвращает | Описание |
|---|---|---|---|
| `create_invoice` | `CreateInvoiceDto` | `CreatedInvoiceDto` | Создать инвойс (счёт на оплату) |
| `check_status_invoice` | `GetStatusInvoiceDto` | `StatusInvoiceDto` | Получить текущий статус инвойса |
| `get_availible_tariffs` | — | `List[AvailableTariffDto]` | Получить список доступных тарифов для инвойсов магазина |
| `create_refund` | `CreateRefundDto` | `CreatedRefundDto` | Создать возврат по инвойсу |
| `check_status_refund` | `GetStatusRefundDto` | `StatusRefundDto` | Получить статус возврата |
| `create_payoff` | `CreatePayoffDto` | `CreatedPayoffDto` | Создать выплату (payout) на кошелёк |
| `get_status_payoff` | `GetPayoffStatusDto` | `StatusPayoffDto` | Получить статус выплаты |
| `get_payoff_tariffs` | — | `List[TariffResponseDto]` | Получить тарифы для выплат профиля |
| `check_wallet` | `CheckWalletRequestDto` | `CheckWalletResponseDto` | Проверить валидность кошелька для выплаты |
| `get_profile_balance` | — | `ProfileBalanceDto` | Получить баланс профиля |
| `get_shop_balance` | — | `ShopBalanceDto` | Получить баланс магазина *(устарело)* |
| `create_h2h_invoice` | `CreateH2hInvoiceDto` | `CreatedH2hInvoiceDto` | Создать H2H-инвойс для оплаты по карте |
| `create_h2h_spb_invoice` | `CreateSBPH2HDto` | `CreatedSBPH2hDto` | Создать H2H-инвойс для оплаты через СБП |
| `get_payment_course_list` | — | `List[CourseDto]` | Получить список курсов валют для платежей |
| `get_payoff_course_list` | — | `List[CourseDto]` | Получить список курсов валют для выплат |
| `check_sign_webhook` | `str, str` | `bool` | Верифицировать подпись вебхука инвойса |
| `check_payoff_signature` | `str, str` | `bool` | Верифицировать подпись вебхука выплаты |

> **Примечание о методах профиля:** `create_payoff`, `get_status_payoff`, `get_payoff_tariffs`, `check_wallet`, `get_profile_balance` и `check_payoff_signature` требуют передачи `ProfileSecretDto` в конструктор `LavaFacade`. При его отсутствии выбрасывается `ValueError`.

> **Устаревший метод:** `get_shop_balance` считается устаревшим. Используйте `get_profile_balance` для получения актуального баланса.

---

## Request DTOs

Request DTO (Data Transfer Object) — объекты для передачи параметров в методы `LavaFacade`. Все поля передаются через конструктор, данные доступны через методы `get_*()`.

### CreateInvoiceDto

**Модуль:** `lava_sdk.dto.request.invoice.create_invoice_dto`

DTO для создания инвойса. Передаётся в `facade.create_invoice()`.

| Параметр | Тип | Обязательный | Описание |
|---|---|---|---|
| `sum` | `str` | Да | Сумма платежа в виде строки (например `"100.50"`) |
| `order_id` | `str` | Да | Уникальный идентификатор заказа на вашей стороне |
| `hook_url` | `str \| None` | Нет | URL для получения вебхука при смене статуса инвойса |
| `success_url` | `str \| None` | Нет | URL для редиректа покупателя после успешной оплаты |
| `fail_url` | `str \| None` | Нет | URL для редиректа покупателя после отказа от оплаты |
| `expire` | `int \| None` | Нет | Время жизни инвойса в секундах |
| `custom_fields` | `str \| None` | Нет | Произвольные данные для передачи обратно в вебхуке (JSON-строка) |
| `comment` | `str \| None` | Нет | Комментарий к платежу, отображаемый покупателю |
| `exclude_service` | `List[str] \| None` | Нет | Список идентификаторов платёжных методов, которые нужно скрыть |
| `include_service` | `List[str] \| None` | Нет | Список идентификаторов платёжных методов, которые нужно показывать |

```lava-sdk-python/docs/reference.md#L1-1
from lava_sdk.dto.request.invoice.create_invoice_dto import CreateInvoiceDto

dto = CreateInvoiceDto(
    sum="500.00",
    order_id="order-789",
    hook_url="https://example.com/webhook/invoice",
    success_url="https://example.com/success",
    fail_url="https://example.com/fail",
    expire=3600,
    custom_fields='{"productId": 42}',
    comment="Оплата за подписку Premium",
)
invoice = facade.create_invoice(dto)
```

---

### GetStatusInvoiceDto

**Модуль:** `lava_sdk.dto.request.invoice.get_status_invoice_dto`

DTO для запроса статуса инвойса. Передаётся в `facade.check_status_invoice()`. Можно передать либо `order_id`, либо `invoice_id` — хотя бы одно поле обязательно.

| Параметр | Тип | Обязательный | Описание |
|---|---|---|---|
| `order_id` | `str \| None` | Нет* | Идентификатор заказа на вашей стороне |
| `invoice_id` | `str \| None` | Нет* | Идентификатор инвойса в системе Lava |

\* Хотя бы одно из двух полей должно быть задано.

```lava-sdk-python/docs/reference.md#L1-1
from lava_sdk.dto.request.invoice.get_status_invoice_dto import GetStatusInvoiceDto

# По идентификатору заказа
dto = GetStatusInvoiceDto(order_id="order-789")

# По идентификатору инвойса
dto = GetStatusInvoiceDto(invoice_id="inv-abc123")

status = facade.check_status_invoice(dto)
```

---

### CreateRefundDto

**Модуль:** `lava_sdk.dto.request.refund.create_refund_dto`

DTO для создания возврата по ранее оплаченному инвойсу. Передаётся в `facade.create_refund()`.

| Параметр | Тип | Обязательный | Описание |
|---|---|---|---|
| `invoice_id` | `str` | Да | Идентификатор инвойса, по которому выполняется возврат |
| `description` | `str \| None` | Нет | Причина возврата (отображается в личном кабинете) |
| `amount` | `float \| None` | Нет | Сумма частичного возврата; если `None`, возвращается полная сумма |

```lava-sdk-python/docs/reference.md#L1-1
from lava_sdk.dto.request.refund.create_refund_dto import CreateRefundDto

# Полный возврат
dto = CreateRefundDto(invoice_id="inv-abc123", description="Покупатель отказался от товара")

# Частичный возврат
dto = CreateRefundDto(invoice_id="inv-abc123", amount=150.00, description="Частичный возврат")

refund = facade.create_refund(dto)
```

---

### GetStatusRefundDto

**Модуль:** `lava_sdk.dto.request.refund.get_status_refund_dto`

DTO для запроса статуса возврата. Передаётся в `facade.check_status_refund()`.

| Параметр | Тип | Обязательный | Описание |
|---|---|---|---|
| `refund_id` | `str` | Да | Идентификатор возврата, полученный при его создании |

```lava-sdk-python/docs/reference.md#L1-1
from lava_sdk.dto.request.refund.get_status_refund_dto import GetStatusRefundDto

dto = GetStatusRefundDto(refund_id="refund-xyz")
status = facade.check_status_refund(dto)
```

---

### CreatePayoffDto

**Модуль:** `lava_sdk.dto.request.payoff.create_payoff_dto`

DTO для создания выплаты (вывода средств). Передаётся в `facade.create_payoff()`. Требует `ProfileSecretDto` в `LavaFacade`.

| Параметр | Тип | Обязательный | Описание |
|---|---|---|---|
| `order_id` | `str` | Да | Уникальный идентификатор операции вывода на вашей стороне |
| `amount` | `float` | Да | Сумма выплаты |
| `service` | `str` | Да | Идентификатор сервиса выплаты (например `"lava_payoff"`) |
| `subtract` | `int \| None` | Нет | Вычитать ли комиссию из суммы (`1` — да, `0` — нет) |
| `wallet_to` | `str \| None` | Нет | Кошелёк или реквизит получателя выплаты |
| `hook_url` | `str \| None` | Нет | URL для получения вебхука при смене статуса выплаты |

```lava-sdk-python/docs/reference.md#L1-1
from lava_sdk.dto.request.payoff.create_payoff_dto import CreatePayoffDto

dto = CreatePayoffDto(
    order_id="payout-001",
    amount=500.00,
    service="lava_payoff",
    wallet_to="recipient_wallet_id",
    hook_url="https://example.com/webhook/payoff",
    subtract=0,
)
payoff = facade.create_payoff(dto)
```

---

### GetPayoffStatusDto

**Модуль:** `lava_sdk.dto.request.payoff.get_payoff_status_dto`

DTO для запроса статуса выплаты. Передаётся в `facade.get_status_payoff()`. Можно использовать либо `order_id`, либо `payoff_id`.

| Параметр | Тип | Обязательный | Описание |
|---|---|---|---|
| `order_id` | `str \| None` | Нет* | Идентификатор операции на вашей стороне |
| `payoff_id` | `str \| None` | Нет* | Идентификатор выплаты в системе Lava |

\* Хотя бы одно из двух полей должно быть задано.

```lava-sdk-python/docs/reference.md#L1-1
from lava_sdk.dto.request.payoff.get_payoff_status_dto import GetPayoffStatusDto

dto = GetPayoffStatusDto(order_id="payout-001")
status = facade.get_status_payoff(dto)
```

---

### CheckWalletRequestDto

**Модуль:** `lava_sdk.dto.request.payoff.check_wallet_request_dto`

DTO для проверки валидности кошелька или реквизита получателя выплаты. Передаётся в `facade.check_wallet()`.

| Параметр | Тип | Обязательный | Описание |
|---|---|---|---|
| `service` | `str` | Да | Идентификатор сервиса выплаты |
| `wallet_to` | `str` | Да | Кошелёк или реквизит, который нужно проверить |

```lava-sdk-python/docs/reference.md#L1-1
from lava_sdk.dto.request.payoff.check_wallet_request_dto import CheckWalletRequestDto

dto = CheckWalletRequestDto(service="lava_payoff", wallet_to="wallet123")
result = facade.check_wallet(dto)
print(result.get_status())  # True если кошелёк валиден
```

---

### CreateH2hInvoiceDto

**Модуль:** `lava_sdk.dto.request.h2h.create_h2h_invoice_dto`

DTO для создания H2H-инвойса (host-to-host) для оплаты банковской картой. Передаётся в `facade.create_h2h_invoice()`. Данные карты передаются непосредственно в запросе.

| Параметр | Тип | Обязательный | Описание |
|---|---|---|---|
| `amount` | `float` | Да | Сумма платежа |
| `order_id` | `str` | Да | Уникальный идентификатор заказа на вашей стороне |
| `cvv` | `int` | Да | CVV/CVC код карты (3 цифры) |
| `month` | `int` | Да | Месяц срока действия карты (1–12) |
| `year` | `int` | Да | Год срока действия карты (последние 2 цифры) |
| `card_number` | `str` | Да | Номер банковской карты без пробелов |
| `hook_url` | `str \| None` | Нет | URL для получения вебхука при смене статуса |
| `custom_fields` | `str \| None` | Нет | Произвольные данные для передачи обратно в вебхуке |
| `comment` | `str \| None` | Нет | Комментарий к платежу |
| `success_url` | `str \| None` | Нет | URL для редиректа после успешной оплаты |
| `fail_url` | `str \| None` | Нет | URL для редиректа после неудачной оплаты |
| `expire` | `int \| None` | Нет | Время жизни инвойса в секундах (по умолчанию `300`) |

```lava-sdk-python/docs/reference.md#L1-1
from lava_sdk.dto.request.h2h.create_h2h_invoice_dto import CreateH2hInvoiceDto

dto = CreateH2hInvoiceDto(
    amount=1500.00,
    order_id="h2h-order-001",
    cvv=123,
    month=12,
    year=26,
    card_number="4111111111111111",
    hook_url="https://example.com/webhook/h2h",
    success_url="https://example.com/success",
    fail_url="https://example.com/fail",
)
result = facade.create_h2h_invoice(dto)
```

---

### CreateSBPH2HDto

**Модуль:** `lava_sdk.dto.request.h2h.create_sbp_h2h_dto`

DTO для создания H2H-инвойса через СБП (Систему Быстрых Платежей). Передаётся в `facade.create_h2h_spb_invoice()`.

| Параметр | Тип | Обязательный | Описание |
|---|---|---|---|
| `amount` | `float` | Да | Сумма платежа |
| `order_id` | `str` | Да | Уникальный идентификатор заказа на вашей стороне |
| `ip` | `str` | Да | IP-адрес плательщика |
| `hook_url` | `str \| None` | Нет | URL для получения вебхука при смене статуса |
| `custom_fields` | `str \| None` | Нет | Произвольные данные для передачи обратно в вебхуке |
| `comment` | `str \| None` | Нет | Комментарий к платежу |
| `success_url` | `str \| None` | Нет | URL для редиректа после успешной оплаты |
| `fail_url` | `str \| None` | Нет | URL для редиректа после неудачной оплаты |
| `expire` | `int \| None` | Нет | Время жизни инвойса в секундах (по умолчанию `300`) |

```lava-sdk-python/docs/reference.md#L1-1
from lava_sdk.dto.request.h2h.create_sbp_h2h_dto import CreateSBPH2HDto

dto = CreateSBPH2HDto(
    amount=299.00,
    order_id="sbp-order-001",
    ip="192.168.1.1",
    hook_url="https://example.com/webhook/sbp",
)
result = facade.create_h2h_spb_invoice(dto)
print(result.get_sbp_url())  # Ссылка для перехода в приложение банка
```

---

## Response DTOs

Response DTO — объекты, возвращаемые методами `LavaFacade`. Все поля доступны через методы `get_*()`.

### CreatedInvoiceDto

**Модуль:** `lava_sdk.dto.response.invoice.created_invoice_dto`

Возвращается методом `facade.create_invoice()`. Содержит данные созданного инвойса.

| Метод | Тип возврата | Описание |
|---|---|---|
| `get_invoice_id()` | `str` | Уникальный идентификатор инвойса в системе Lava |
| `get_amount()` | `float` | Сумма инвойса |
| `get_expired()` | `str` | Дата и время истечения инвойса в виде строки |
| `get_status()` | `int` | Числовой код текущего статуса инвойса |
| `get_shop_id()` | `str` | Идентификатор магазина |
| `get_url()` | `str` | URL страницы оплаты для перенаправления покупателя |

```lava-sdk-python/docs/reference.md#L1-1
invoice = facade.create_invoice(dto)
print(invoice.get_invoice_id())   # "inv-abc123"
print(invoice.get_url())          # "https://pay.lava.ru/..."
print(invoice.get_amount())       # 500.0
print(invoice.get_expired())      # "2024-01-01T12:00:00"
```

---

### StatusInvoiceDto

**Модуль:** `lava_sdk.dto.response.invoice.status_invoice_dto`

Возвращается методом `facade.check_status_invoice()`. Содержит подробную информацию о статусе инвойса.

| Метод | Тип возврата | Описание |
|---|---|---|
| `get_status()` | `str` | Текущий статус инвойса (`success`, `cancel`, `pending` и т.д.) |
| `get_error_message()` | `str \| None` | Сообщение об ошибке, если платёж не прошёл |
| `get_invoice_id()` | `str` | Идентификатор инвойса |
| `get_shop_id()` | `str` | Идентификатор магазина |
| `get_amount()` | `float` | Сумма инвойса |
| `get_expire()` | `str` | Дата и время истечения инвойса |
| `get_order_id()` | `str` | Идентификатор заказа, переданный при создании |
| `get_fail_url()` | `str \| None` | URL для редиректа при неудаче |
| `get_success_url()` | `str \| None` | URL для редиректа при успехе |
| `get_hook_url()` | `str \| None` | URL вебхука |
| `get_custom_fields()` | `str \| None` | Произвольные поля, переданные при создании |
| `get_include_service()` | `List[str] \| None` | Список разрешённых платёжных методов |
| `get_exclude_service()` | `List[str] \| None` | Список отключённых платёжных методов |

---

### AvailableTariffDto

**Модуль:** `lava_sdk.dto.response.invoice.available_tariff_dto`

Элемент списка, возвращаемого `facade.get_availible_tariffs()`. Описывает один доступный тариф оплаты.

| Метод | Тип возврата | Описание |
|---|---|---|
| `get_status()` | `int` | Статус тарифа (активен/неактивен) |
| `get_percent()` | `float` | Общий процент комиссии по тарифу |
| `get_user_percent()` | `float` | Доля комиссии, уплачиваемая покупателем |
| `get_shop_percent()` | `float` | Доля комиссии, уплачиваемая магазином |
| `get_service_name()` | `str` | Отображаемое название платёжного сервиса |
| `get_service_id()` | `str` | Машиночитаемый идентификатор платёжного сервиса |
| `get_currency()` | `str` | Валюта тарифа |

---

### CreatedRefundDto

**Модуль:** `lava_sdk.dto.response.refund.created_refund_dto`

Возвращается методом `facade.create_refund()`.

| Метод | Тип возврата | Описание |
|---|---|---|
| `get_status()` | `str` | Статус созданного возврата |
| `get_refund_id()` | `str` | Уникальный идентификатор возврата в системе Lava |
| `get_amount()` | `float` | Сумма возврата |
| `get_service()` | `str` | Идентификатор сервиса, через который выполняется возврат |
| `get_label()` | `str` | Метка или описание возврата |

---

### StatusRefundDto

**Модуль:** `lava_sdk.dto.response.refund.status_refund_dto`

Возвращается методом `facade.check_status_refund()`.

| Метод | Тип возврата | Описание |
|---|---|---|
| `get_status()` | `str` | Текущий статус возврата |
| `get_refund_id()` | `str` | Идентификатор возврата |
| `get_amount()` | `float` | Сумма возврата |

---

### CreatedPayoffDto

**Модуль:** `lava_sdk.dto.response.payoff.created_payoff_dto`

Возвращается методом `facade.create_payoff()`.

| Метод | Тип возврата | Описание |
|---|---|---|
| `get_payoff_id()` | `str` | Уникальный идентификатор выплаты в системе Lava |
| `get_status()` | `str` | Начальный статус созданной выплаты |

---

### StatusPayoffDto

**Модуль:** `lava_sdk.dto.response.payoff.status_payoff_dto`

Возвращается методом `facade.get_status_payoff()`. Содержит подробную информацию о ходе выплаты.

| Метод | Тип возврата | Описание |
|---|---|---|
| `get_id()` | `str` | Внутренний идентификатор выплаты |
| `get_order_id()` | `str` | Идентификатор заказа, переданный при создании |
| `get_status()` | `str` | Текущий статус выплаты |
| `get_wallet()` | `str \| None` | Кошелёк или реквизит получателя |
| `get_service()` | `str` | Идентификатор сервиса выплаты |
| `get_amount_pay()` | `float` | Сумма списания (с комиссией) |
| `get_commission()` | `float` | Сумма комиссии |
| `get_amount_receive()` | `float` | Сумма, которую получит адресат выплаты |
| `get_try_count()` | `int` | Количество попыток выполнения выплаты |
| `get_error_message()` | `str \| None` | Сообщение об ошибке, если выплата не удалась |

---

### CheckWalletResponseDto

**Модуль:** `lava_sdk.dto.response.payoff.check_wallet_response_dto`

Возвращается методом `facade.check_wallet()`.

| Метод | Тип возврата | Описание |
|---|---|---|
| `get_status()` | `bool` | `True` если кошелёк существует и принимает выплаты, `False` — иначе |

---

### TariffResponseDto

**Модуль:** `lava_sdk.dto.response.payoff.tariff_response_dto`

Элемент списка, возвращаемого `facade.get_payoff_tariffs()`. Описывает один тариф для выплат.

| Метод | Тип возврата | Описание |
|---|---|---|
| `get_service()` | `str` | Идентификатор сервиса выплаты |
| `get_title()` | `str \| None` | Отображаемое название сервиса |
| `get_currency()` | `str` | Валюта выплаты |
| `get_percent()` | `float \| None` | Процент комиссии (если применяется) |
| `get_fix()` | `float \| None` | Фиксированная комиссия (если применяется) |
| `get_min_sum()` | `float \| None` | Минимальная сумма выплаты по этому тарифу |
| `get_max_sum()` | `float \| None` | Максимальная сумма выплаты по этому тарифу |

```lava-sdk-python/docs/reference.md#L1-1
tariffs = facade.get_payoff_tariffs()
for tariff in tariffs:
    print(f"{tariff.get_service()} — {tariff.get_title()}")
    print(f"  Комиссия: {tariff.get_percent()}%, мин: {tariff.get_min_sum()}, макс: {tariff.get_max_sum()}")
```

---

### ProfileBalanceDto

**Модуль:** `lava_sdk.dto.response.profile.profile_balance_dto`

Возвращается методом `facade.get_profile_balance()`.

| Метод | Тип возврата | Описание |
|---|---|---|
| `get_total_balance()` | `float` | Общий баланс профиля (включая заморозку) |
| `get_available_balance()` | `float` | Доступный для вывода баланс |
| `get_freeze_balance()` | `float` | Замороженный баланс (в процессе выплат или споров) |

```lava-sdk-python/docs/reference.md#L1-1
balance = facade.get_profile_balance()
print(f"Доступно: {balance.get_available_balance()} руб.")
print(f"Заморожено: {balance.get_freeze_balance()} руб.")
print(f"Всего: {balance.get_total_balance()} руб.")
```

---

### ShopBalanceDto

**Модуль:** `lava_sdk.dto.response.shop.shop_balance_dto`

Возвращается устаревшим методом `facade.get_shop_balance()`. Рекомендуется использовать `get_profile_balance()`.

| Метод | Тип возврата | Описание |
|---|---|---|
| `get_balance()` | `float` | Доступный баланс магазина |
| `get_freeze_balance()` | `float` | Замороженный баланс магазина |

---

### CourseDto

**Модуль:** `lava_sdk.dto.response.course.course_dto`

Элемент списков, возвращаемых `facade.get_payment_course_list()` и `facade.get_payoff_course_list()`. Представляет курс одной валюты.

| Метод | Тип возврата | Описание |
|---|---|---|
| `get_currency()` | `CurrencyDto` | Объект с описанием валюты (название, символ, код) |
| `get_value()` | `float` | Текущий курс валюты относительно базовой |

```lava-sdk-python/docs/reference.md#L1-1
courses = facade.get_payment_course_list()
for course in courses:
    currency = course.get_currency()
    print(f"{currency.get_label()} ({currency.get_symbol()}): {course.get_value()}")
```

---

### CurrencyDto

**Модуль:** `lava_sdk.dto.response.course.currency_dto`

Вложенный объект внутри `CourseDto`. Описывает конкретную валюту.

| Метод | Тип возврата | Описание |
|---|---|---|
| `get_label()` | `str` | Читаемое название валюты (например, `"Russian Ruble"`) |
| `get_symbol()` | `str` | Символьный код валюты (например, `"RUB"`) |
| `get_value()` | `str` | Числовой или строковой идентификатор валюты |

---

### CreatedH2hInvoiceDto

**Модуль:** `lava_sdk.dto.response.h2h.created_h2h_invoice_dto`

Возвращается методом `facade.create_h2h_invoice()`.

| Метод | Тип возврата | Описание |
|---|---|---|
| `get_url()` | `str` | URL для 3DS-верификации или перенаправления покупателя |
| `get_invoice_id()` | `str` | Идентификатор созданного H2H-инвойса |
| `get_card_mask()` | `str` | Маска карты (например, `"411111****1111"`) |
| `get_amount()` | `float` | Исходная сумма платежа |
| `get_amount_pay()` | `float` | Сумма к оплате с учётом комиссии |
| `get_commission()` | `float` | Размер комиссии |
| `get_shop_id()` | `str` | Идентификатор магазина |

---

### CreatedSBPH2hDto

**Модуль:** `lava_sdk.dto.response.h2h.created_sbp_h2h_dto`

Возвращается методом `facade.create_h2h_spb_invoice()`.

| Метод | Тип возврата | Описание |
|---|---|---|
| `get_sbp_url()` | `str` | Deep link для открытия приложения банка через СБП |
| `get_qr_code()` | `str` | Данные QR-кода (base64 или ссылка) для сканирования |
| `is_fingerprint()` | `bool` | Признак того, нужна ли проверка отпечатка устройства |

```lava-sdk-python/docs/reference.md#L1-1
result = facade.create_h2h_spb_invoice(dto)
print(result.get_sbp_url())    # "https://qr.nspk.ru/..."
print(result.get_qr_code())    # base64-строка изображения QR
```

---

## Secret DTOs

Secret DTO содержат учётные данные для аутентификации на разных уровнях API Lava.

### ProfileSecretDto

**Модуль:** `lava_sdk.dto.secret.profile_secret_dto`

Хранит ключи уровня профиля для методов выплат и баланса. Передаётся в параметр `profile_secret_data` конструктора `LavaFacade`.

| Параметр | Тип | Обязательный | Описание |
|---|---|---|---|
| `profile_id` | `str` | Да | Идентификатор профиля в системе Lava |
| `secret_key` | `str` | Да | Секретный ключ профиля для подписи запросов |
| `additional_key` | `str \| None` | Нет | Ключ для верификации вебхуков выплат |

**Методы:**

| Метод | Тип возврата | Описание |
|---|---|---|
| `get_profile_id()` | `str` | Идентификатор профиля |
| `get_secret_key()` | `str` | Секретный ключ профиля |
| `get_additional_key()` | `str \| None` | Ключ вебхука выплат (`None` если не задан) |

```lava-sdk-python/docs/reference.md#L1-1
from lava_sdk.dto.secret.profile_secret_dto import ProfileSecretDto
import os

profile = ProfileSecretDto(
    profile_id=os.environ["LAVA_PROFILE_ID"],
    secret_key=os.environ["LAVA_PROFILE_SECRET"],
    additional_key=os.environ["LAVA_PAYOFF_WEBHOOK_KEY"],
)

print(profile.get_profile_id())     # "profile-xxx"
print(profile.get_additional_key()) # "webhook-key-xxx" или None
```

---

### ShopSecretDto

**Модуль:** `lava_sdk.dto.secret.shop_secret_dto`

Хранит учётные данные уровня магазина. Используется в устаревших методах; для новых интеграций используйте `ProfileSecretDto`.

| Параметр | Тип | Обязательный | Описание |
|---|---|---|---|
| `shop_id` | `str` | Да | Идентификатор магазина в системе Lava |
| `secret_key` | `str` | Да | Секретный ключ магазина для подписи запросов |
| `additional_key` | `str \| None` | Нет | Ключ для верификации вебхуков инвойсов магазина |

**Методы:**

| Метод | Тип возврата | Описание |
|---|---|---|
| `get_shop_id()` | `str` | Идентификатор магазина |
| `get_secret_key()` | `str` | Секретный ключ магазина |
| `get_additional_key()` | `str \| None` | Ключ вебхука (`None` если не задан) |

---

## Константы URL

Все URL-константы хранятся в отдельных классах-неймспейсах. Базовый URL указан в `ClientConstants.URL`; все пути формируются как `ClientConstants.URL + <константа>`.

| Класс | Модуль | Константа | Значение |
|---|---|---|---|
| `ClientConstants` | `lava_sdk.constants.client_constants` | `URL` | `https://api.lava.ru` |
| `InvoiceUrlConstants` | `lava_sdk.constants.invoice_url_constants` | `INVOICE_CREATE` | `/business/invoice/create` |
| `InvoiceUrlConstants` | `lava_sdk.constants.invoice_url_constants` | `INVOICE_STATUS` | `/business/invoice/status` |
| `InvoiceUrlConstants` | `lava_sdk.constants.invoice_url_constants` | `GET_AVAILIBLE_TARIFFS` | `/business/invoice/get-available-tariffs` |
| `PayoffUrlConstants` | `lava_sdk.constants.payoff_url_constants` | `CREATE_PAYOFF` | `/business/payoff/create` |
| `PayoffUrlConstants` | `lava_sdk.constants.payoff_url_constants` | `GET_PAYOFF_STATUS` | `/business/payoff/info` |
| `PayoffUrlConstants` | `lava_sdk.constants.payoff_url_constants` | `CHECK_USER_WALLET` | `/business/payoff/check-wallet` |
| `PayoffUrlConstants` | `lava_sdk.constants.payoff_url_constants` | `GET_PAYOFF_TARIFFS` | `/business/payoff/get-tariffs` |
| `RefundUrlConstants` | `lava_sdk.constants.refund_url_constants` | `CREATE_REFUND` | `/business/invoice/refund` |
| `RefundUrlConstants` | `lava_sdk.constants.refund_url_constants` | `GET_STATUS_REFUND` | `/business/invoice/get-refund-status` |
| `ProfileUrlConstants` | `lava_sdk.constants.profile_url_constants` | `GET_BALANCE` | `/business/profile/balance` |
| `ShopUrlConstants` | `lava_sdk.constants.shop_url_constants` | `GET_BALANCE` | `/business/shop/get-balance` |
| `H2hUrlConstants` | `lava_sdk.constants.h2h_url_constants` | `INVOICE_CREATE` | `/business/invoice/h2h` |
| `H2hUrlConstants` | `lava_sdk.constants.h2h_url_constants` | `SBP_INVOICE_CREATE` | `/business/invoice/pay-sbp-h2h` |
| `CourseUrlConstants` | `lava_sdk.constants.course_url_constants` | `GET_PAYMENT_COURSE_LIST` | `/business/course/list/payment` |
| `CourseUrlConstants` | `lava_sdk.constants.course_url_constants` | `GET_PAYOFF_COURSE_LIST` | `/business/course/list/payoff` |

### Пример использования констант напрямую

```lava-sdk-python/docs/reference.md#L1-1
from lava_sdk.constants.client_constants import ClientConstants
from lava_sdk.constants.invoice_url_constants import InvoiceUrlConstants

# Полный URL для создания инвойса:
full_url = ClientConstants.URL + InvoiceUrlConstants.INVOICE_CREATE
print(full_url)
# https://api.lava.ru/business/invoice/create
```

> **Примечание:** в обычном использовании SDK вам не нужно обращаться к константам напрямую — это делает внутренний HTTP-клиент. Константы полезны при написании собственных HTTP-клиентов или при отладке.
