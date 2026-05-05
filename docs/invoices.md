# Инвойсы (приём платежей)

> *Неофициальный Python-порт PHP SDK Lava. Не аффилирован с Lava Payment. [← Оглавление](index.md)*

## Обзор

Инвойс — это основной инструмент приёма платежей в Lava SDK. Принцип работы прост: вы создаёте инвойс на своём сервере, получаете в ответ уникальную ссылку на страницу оплаты Lava и перенаправляете на неё пользователя. После того как пользователь завершает оплату, Lava отправляет POST-запрос (webhook) на указанный вами `hook_url` с информацией о транзакции.

**Жизненный цикл инвойса:**

```
Создание инвойса  →  Перенаправление пользователя  →  Оплата на странице Lava
       ↓                                                         ↓
 CreatedInvoiceDto                                  Webhook на hook_url (POST)
 (url → перенаправить)                              + Редирект на success_url / fail_url
```

> **Важно:** Каждый инвойс должен иметь уникальный `order_id` в рамках вашего магазина. Повторное использование одного и того же `order_id` приведёт к ошибке.

---

## Создание инвойса — `create_invoice`

```python
facade.create_invoice(dto: CreateInvoiceDto) -> CreatedInvoiceDto
```

Метод отправляет запрос к API Lava, создаёт инвойс и возвращает объект `CreatedInvoiceDto` с данными для перенаправления пользователя.

### Параметры CreateInvoiceDto

| Параметр | Тип | Обязательный | Описание |
|---|---|---|---|
| `sum` | `str` | Да | Сумма платежа в рублях (например `"300.09"`) |
| `order_id` | `str` | Да | Уникальный идентификатор заказа в вашей системе |
| `hook_url` | `Optional[str]` | Нет | URL для отправки webhook-уведомлений после оплаты |
| `success_url` | `Optional[str]` | Нет | URL редиректа после успешной оплаты |
| `fail_url` | `Optional[str]` | Нет | URL редиректа при неудачной оплате или истечении инвойса |
| `expire` | `Optional[int]` | Нет | Время жизни инвойса в секундах (например `300` = 5 минут) |
| `custom_fields` | `Optional[str]` | Нет | Произвольные данные в формате JSON-строки — вернутся в webhook |
| `comment` | `Optional[str]` | Нет | Комментарий к платежу, отображаемый пользователю |
| `include_service` | `Optional[List[str]]` | Нет | Список разрешённых способов оплаты (остальные скрыты) |
| `exclude_service` | `Optional[List[str]]` | Нет | Список исключённых способов оплаты |

### Ответ: CreatedInvoiceDto

| Поле | Тип | Описание |
|---|---|---|
| `invoice_id` | `str` | Уникальный ID инвойса, присвоенный системой Lava |
| `amount` | `float` | Сумма инвойса |
| `expired` | `str` | Дата и время истечения инвойса в формате ISO 8601 |
| `status` | `int` | Статус инвойса на момент создания |
| `shop_id` | `str` | ID магазина, которому принадлежит инвойс |
| `url` | `str` | Ссылка на страницу оплаты — **перенаправьте пользователя сюда** |

Доступ к полям осуществляется через геттеры: `get_invoice_id()`, `get_amount()`, `get_expired()`, `get_status()`, `get_shop_id()`, `get_url()`.

### Пример использования

```python
from lava_sdk import LavaFacade
from lava_sdk.dto.request.invoice.create_invoice_dto import CreateInvoiceDto
from lava_sdk.exceptions.invoice.invoice_exception import InvoiceException
from lava_sdk.exceptions.base_exception import LavaBaseException

# Инициализация фасада
facade = LavaFacade(
    secret_key="ваш_секретный_ключ",
    shop_id="ваш_идентификатор_магазина",
    additional_key="ваш_дополнительный_ключ",  # для проверки подписи webhook
)

# Формирование DTO с параметрами инвойса
dto = CreateInvoiceDto(
    sum="1500.00",
    order_id="order-20240101-0042",
    hook_url="https://example.com/webhooks/lava",
    success_url="https://example.com/payment/success",
    fail_url="https://example.com/payment/fail",
    expire=600,                           # инвойс истечёт через 10 минут
    custom_fields='{"user_id": 99, "product_id": 7}',
    comment="Оплата заказа #0042",
)

try:
    response = facade.create_invoice(dto)

    invoice_id  = response.get_invoice_id()
    payment_url = response.get_url()
    expires_at  = response.get_expired()
    amount      = response.get_amount()

    print(f"Инвойс создан:  {invoice_id}")
    print(f"Сумма:          {amount} руб.")
    print(f"Истекает:       {expires_at}")
    print(f"Ссылка оплаты:  {payment_url}")

    # В веб-фреймворке выполните редирект:
    # return redirect(payment_url)           # Flask
    # return RedirectResponse(payment_url)   # FastAPI

except InvoiceException as e:
    # Ошибка на стороне API (неверные параметры, дублирующий order_id и т.д.)
    print(f"Ошибка инвойса [{e.code}]: {e}")

except LavaBaseException as e:
    # Общая ошибка SDK (сетевые проблемы, неверная подпись и т.д.)
    print(f"Ошибка SDK [{e.code}]: {e}")
```

### Управление способами оплаты

Параметры `include_service` и `exclude_service` позволяют гибко управлять тем, какие способы оплаты будут доступны пользователю. Список доступных идентификаторов сервисов можно получить через [`get_availible_tariffs()`](#доступные-тарифы--get_availible_tariffs).

> **Примечание:** `include_service` и `exclude_service` нельзя использовать одновременно — укажите только один из параметров.

```python
from lava_sdk.dto.request.invoice.create_invoice_dto import CreateInvoiceDto
from lava_sdk.exceptions.invoice.invoice_exception import InvoiceException

# include_service — показываем только выбранные методы оплаты
dto_only_cards = CreateInvoiceDto(
    sum="500.00",
    order_id="order-cards-only-001",
    hook_url="https://example.com/webhooks/lava",
    include_service=["card", "sbp"],  # идентификаторы из get_availible_tariffs()
)

# exclude_service — скрываем конкретные методы, все остальные доступны
dto_no_crypto = CreateInvoiceDto(
    sum="500.00",
    order_id="order-no-crypto-001",
    hook_url="https://example.com/webhooks/lava",
    exclude_service=["bitcoin", "usdt_trc20"],
)

try:
    response_cards = facade.create_invoice(dto_only_cards)
    print(f"Ссылка (только карты/СБП): {response_cards.get_url()}")

    response_no_crypto = facade.create_invoice(dto_no_crypto)
    print(f"Ссылка (без крипты):       {response_no_crypto.get_url()}")

except InvoiceException as e:
    print(f"Ошибка [{e.code}]: {e}")
```

---

## Статус инвойса — `check_status_invoice`

```python
facade.check_status_invoice(dto: GetStatusInvoiceDto) -> StatusInvoiceDto
```

Метод возвращает текущее состояние инвойса. Необходимо передать хотя бы один из параметров: `order_id` (ID заказа в вашей системе) или `invoice_id` (ID инвойса Lava).

### Параметры GetStatusInvoiceDto

| Параметр | Тип | Обязательный | Описание |
|---|---|---|---|
| `order_id` | `Optional[str]` | Нет | ID заказа в вашей системе |
| `invoice_id` | `Optional[str]` | Нет | ID инвойса Lava |

> **Обязательное условие:** необходимо передать хотя бы один из параметров — `order_id` или `invoice_id`. Если не передан ни один — API вернёт ошибку.

### Ответ: StatusInvoiceDto

| Поле | Тип | Описание |
|---|---|---|
| `status` | `str` | Текущий статус инвойса (`success`, `pending`, `error`, `cancel`) |
| `error_message` | `Optional[str]` | Описание ошибки (заполнено только при статусе `error`) |
| `invoice_id` | `str` | Уникальный ID инвойса в системе Lava |
| `shop_id` | `str` | ID магазина |
| `amount` | `float` | Сумма инвойса |
| `expire` | `str` | Дата и время истечения инвойса |
| `order_id` | `str` | ID заказа из вашей системы |
| `fail_url` | `Optional[str]` | URL редиректа при неудачной оплате |
| `success_url` | `Optional[str]` | URL редиректа при успешной оплате |
| `hook_url` | `Optional[str]` | URL для webhook-уведомлений |
| `custom_fields` | `Optional[str]` | Произвольные данные, переданные при создании инвойса |
| `include_service` | `Optional[List[str]]` | Список разрешённых способов оплаты |
| `exclude_service` | `Optional[List[str]]` | Список исключённых способов оплаты |

### Возможные значения статуса

| Статус | Описание |
|---|---|
| `success` | Платёж успешно выполнен — деньги зачислены |
| `pending` | Инвойс ожидает оплаты |
| `error` | Ошибка при обработке платежа |
| `cancel` | Инвойс отменён или истёк срок его действия |

### Пример использования

**Проверка по `invoice_id` (рекомендуется — сохраняйте ID после создания):**

```python
from lava_sdk.dto.request.invoice.get_status_invoice_dto import GetStatusInvoiceDto
from lava_sdk.exceptions.invoice.invoice_exception import InvoiceException

dto = GetStatusInvoiceDto(invoice_id="lava-inv-00001abc")

try:
    status = facade.check_status_invoice(dto)

    print(f"Статус инвойса:  {status.get_status()}")
    print(f"Сумма:           {status.get_amount()} руб.")
    print(f"Заказ:           {status.get_order_id()}")
    print(f"Истекает:        {status.get_expire()}")

    match status.get_status():
        case "success":
            print("Платёж успешно завершён — выдаём товар/услугу.")
        case "pending":
            print("Ожидаем оплату...")
        case "cancel":
            print("Инвойс истёк или отменён.")
        case "error":
            print(f"Ошибка платежа: {status.get_error_message()}")

except InvoiceException as e:
    print(f"Ошибка API [{e.code}]: {e}")
```

**Проверка по `order_id` (когда `invoice_id` не был сохранён):**

```python
from lava_sdk.dto.request.invoice.get_status_invoice_dto import GetStatusInvoiceDto
from lava_sdk.exceptions.invoice.invoice_exception import InvoiceException
import json

dto = GetStatusInvoiceDto(order_id="order-20240101-0042")

try:
    status = facade.check_status_invoice(dto)

    print(f"Invoice ID: {status.get_invoice_id()}")
    print(f"Статус:     {status.get_status()}")

    # Распаковка custom_fields, если были переданы при создании
    if status.get_custom_fields():
        fields = json.loads(status.get_custom_fields())
        print(f"user_id:    {fields.get('user_id')}")
        print(f"product_id: {fields.get('product_id')}")

except InvoiceException as e:
    print(f"Ошибка API [{e.code}]: {e}")
```

---

## Доступные тарифы — `get_availible_tariffs`

```python
facade.get_availible_tariffs() -> List[AvailableTariffDto]
```

Метод возвращает список всех доступных способов оплаты для вашего магазина вместе с информацией о комиссиях. Используйте его для:
- формирования списков `include_service` / `exclude_service` при создании инвойсов;
- отображения доступных способов оплаты и их комиссий в интерфейсе.

### Ответ: List[AvailableTariffDto]

| Поле | Тип | Описание |
|---|---|---|
| `status` | `int` | Статус тарифа (`1` — активен, `0` — отключён) |
| `percent` | `float` | Суммарный процент комиссии по тарифу |
| `user_percent` | `float` | Процент комиссии, который оплачивает пользователь |
| `shop_percent` | `float` | Процент комиссии, который оплачивает магазин |
| `service_name` | `str` | Отображаемое название способа оплаты (например `"Банковская карта"`) |
| `service_id` | `str` | Идентификатор для передачи в `include_service` / `exclude_service` |
| `currency` | `str` | Валюта тарифа |

### Пример использования

```python
from lava_sdk.exceptions.invoice.invoice_exception import InvoiceException

try:
    tariffs = facade.get_availible_tariffs()

    print(f"Доступных способов оплаты: {len(tariffs)}")
    print("-" * 70)

    for tariff in tariffs:
        label = "активен" if tariff.get_status() == 1 else "отключён"
        print(
            f"[{label:8s}] {tariff.get_service_name():<25s}"
            f"  ID: {tariff.get_service_id():<20s}"
            f"  Комиссия: {tariff.get_percent():5.2f}%"
            f"  (магазин: {tariff.get_shop_percent():.2f}%,"
            f" пользователь: {tariff.get_user_percent():.2f}%)"
            f"  Валюта: {tariff.get_currency()}"
        )

    # Отбираем идентификаторы только активных тарифов
    active_ids = [t.get_service_id() for t in tariffs if t.get_status() == 1]
    print(f"\nАктивные сервисы ({len(active_ids)}): {active_ids}")

except InvoiceException as e:
    print(f"Ошибка получения тарифов [{e.code}]: {e}")
```

---

## Обработка ошибок

Все ошибки при работе с инвойсами приводят к выбросу исключения `InvoiceException`. Оно наследует базовый класс `LavaBaseException`, который предоставляет:

- `e.code` — числовой код ошибки от API Lava
- `str(e)` — текстовое описание причины ошибки

Рекомендуется перехватывать `InvoiceException` точечно, а `LavaBaseException` использовать как запасной обработчик для неожиданных системных ошибок SDK:

```python
from lava_sdk.exceptions.invoice.invoice_exception import InvoiceException
from lava_sdk.exceptions.base_exception import LavaBaseException
from lava_sdk.dto.request.invoice.create_invoice_dto import CreateInvoiceDto

dto = CreateInvoiceDto(
    sum="250.00",
    order_id="order-err-example-001",
    hook_url="https://example.com/webhooks/lava",
)

try:
    response = facade.create_invoice(dto)
    print(f"Инвойс создан: {response.get_invoice_id()}")
    print(f"Ссылка:        {response.get_url()}")

except InvoiceException as e:
    # Бизнес-ошибки API:
    #   — неверные параметры запроса
    #   — дублирующий order_id в рамках магазина
    #   — магазин не найден или деактивирован
    #   — неверная подпись запроса
    print(f"Ошибка инвойса [{e.code}]: {e}")

except LavaBaseException as e:
    # Инфраструктурные ошибки SDK:
    #   — сетевой сбой или таймаут
    #   — неожиданный формат ответа от API
    print(f"Ошибка SDK [{e.code}]: {e}")

except Exception as e:
    # Непредвиденные исключения
    print(f"Неожиданная ошибка: {e}")
```
