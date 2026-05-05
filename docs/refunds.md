# Возвраты

> *Неофициальный Python-порт PHP SDK Lava. Не аффилирован с Lava Payment. [← Оглавление](index.md)*

## Обзор

Возврат (refund) позволяет вернуть деньги покупателю за ранее оплаченный инвойс. SDK поддерживает как **полный возврат** (вся сумма инвойса), так и **частичный возврат** (произвольная сумма, не превышающая сумму оплаченного инвойса).

Для создания возврата вам потребуется `invoice_id` — идентификатор инвойса Lava, по которому прошёл платёж. Этот ID возвращается при [создании инвойса](./invoices.md#создание-инвойса--create_invoice) и доступен в теле webhook-уведомления.

> **Важно:** Создать возврат можно только по инвойсу со статусом `success`. Попытка возврата по незавершённому или отменённому инвойсу приведёт к ошибке.

---

## Создание возврата — `create_refund`

```python
facade.create_refund(dto: CreateRefundDto) -> CreatedRefundDto
```

Метод инициирует операцию возврата средств и возвращает объект `CreatedRefundDto` с идентификатором созданного возврата и его начальным статусом.

### Параметры CreateRefundDto

| Параметр | Тип | Обязательный | Описание |
|---|---|---|---|
| `invoice_id` | `str` | Да | ID инвойса Lava, по которому создаётся возврат |
| `description` | `Optional[str]` | Нет | Описание причины возврата |
| `amount` | `Optional[float]` | Нет | Сумма возврата в рублях; если не указана — выполняется полный возврат |

### Ответ: CreatedRefundDto

| Поле | Тип | Описание |
|---|---|---|
| `status` | `str` | Статус операции возврата сразу после создания |
| `refund_id` | `str` | Уникальный ID возврата — сохраните для последующей проверки статуса |
| `amount` | `float` | Сумма, которая будет возвращена покупателю |
| `service` | `str` | Способ оплаты, через который проводится возврат |
| `label` | `str` | Метка операции возврата |

Доступ к полям: `get_status()`, `get_refund_id()`, `get_amount()`, `get_service()`, `get_label()`.

### Примеры использования

**Полный возврат** (параметр `amount` не указывается):

```python
from lava_sdk import LavaFacade
from lava_sdk.dto.request.refund.create_refund_dto import CreateRefundDto
from lava_sdk.exceptions.refund.refund_exception import RefundException
from lava_sdk.exceptions.base_exception import LavaBaseException

facade = LavaFacade(
    secret_key="ваш_секретный_ключ",
    shop_id="ваш_идентификатор_магазина",
)

# Полный возврат — amount не передаём
dto = CreateRefundDto(
    invoice_id="lava-inv-00001abc",
    description="Покупатель отказался от товара",
)

try:
    refund = facade.create_refund(dto)

    print(f"Возврат создан:  {refund.get_refund_id()}")
    print(f"Сумма возврата:  {refund.get_amount()} руб.")
    print(f"Статус:          {refund.get_status()}")
    print(f"Сервис:          {refund.get_service()}")
    print(f"Метка:           {refund.get_label()}")

    # Сохраните refund_id для проверки статуса
    saved_refund_id = refund.get_refund_id()

except RefundException as e:
    print(f"Ошибка возврата [{e.code}]: {e}")

except LavaBaseException as e:
    print(f"Ошибка SDK [{e.code}]: {e}")
```

**Частичный возврат** (параметр `amount` с нужной суммой):

```python
from lava_sdk.dto.request.refund.create_refund_dto import CreateRefundDto
from lava_sdk.exceptions.refund.refund_exception import RefundException
from lava_sdk.exceptions.base_exception import LavaBaseException

# Частичный возврат — возвращаем 300 руб. из 1500 руб.
dto = CreateRefundDto(
    invoice_id="lava-inv-00002xyz",
    description="Частичный возврат: покупатель вернул 1 из 5 товаров",
    amount=300.00,
)

try:
    refund = facade.create_refund(dto)

    print(f"Частичный возврат создан: {refund.get_refund_id()}")
    print(f"Возвращаемая сумма:       {refund.get_amount()} руб.")
    print(f"Статус:                   {refund.get_status()}")

except RefundException as e:
    # Возможные причины ошибки:
    #   — инвойс не найден или не оплачен
    #   — сумма возврата превышает доступный остаток
    #   — возврат по данному инвойсу уже был создан
    print(f"Ошибка возврата [{e.code}]: {e}")

except LavaBaseException as e:
    print(f"Ошибка SDK [{e.code}]: {e}")
```

---

## Статус возврата — `check_status_refund`

```python
facade.check_status_refund(dto: GetStatusRefundDto) -> StatusRefundDto
```

Метод возвращает текущий статус операции возврата по её `refund_id`, полученному при создании.

### Параметры GetStatusRefundDto

| Параметр | Тип | Обязательный | Описание |
|---|---|---|---|
| `refund_id` | `str` | Да | ID возврата, полученный при создании через `create_refund` |

### Ответ: StatusRefundDto

| Поле | Тип | Описание |
|---|---|---|
| `status` | `str` | Текущий статус возврата (`pending`, `success`, `error`) |
| `refund_id` | `str` | ID возврата |
| `amount` | `float` | Сумма возврата |

Доступ к полям: `get_status()`, `get_refund_id()`, `get_amount()`.

### Возможные значения статуса

| Статус | Описание |
|---|---|
| `pending` | Возврат принят и обрабатывается |
| `success` | Возврат успешно выполнен — деньги отправлены покупателю |
| `error` | Ошибка при выполнении возврата |

### Пример использования

```python
from lava_sdk.dto.request.refund.get_status_refund_dto import GetStatusRefundDto
from lava_sdk.exceptions.refund.refund_exception import RefundException
from lava_sdk.exceptions.base_exception import LavaBaseException
import time

refund_id = "refund-abc-00001"  # ID, полученный из create_refund()

dto = GetStatusRefundDto(refund_id=refund_id)

try:
    # Опрос статуса с повтором (polling)
    for attempt in range(1, 6):
        result = facade.check_status_refund(dto)
        current_status = result.get_status()

        print(f"Попытка {attempt}: статус = {current_status}, сумма = {result.get_amount()} руб.")

        if current_status == "success":
            print("Возврат успешно завершён.")
            break
        elif current_status == "error":
            print("Возврат завершился с ошибкой.")
            break
        elif current_status == "pending":
            print("Возврат обрабатывается, ждём 5 секунд...")
            time.sleep(5)
    else:
        print("Возврат всё ещё в обработке после 5 попыток.")

except RefundException as e:
    print(f"Ошибка проверки статуса [{e.code}]: {e}")

except LavaBaseException as e:
    print(f"Ошибка SDK [{e.code}]: {e}")
```

---

## Обработка ошибок

Все ошибки при работе с возвратами приводят к выбросу исключения `RefundException`. Оно наследует базовый класс `LavaBaseException`:

- `e.code` — числовой код ошибки от API Lava
- `str(e)` — текстовое описание причины ошибки

```python
from lava_sdk.exceptions.refund.refund_exception import RefundException
from lava_sdk.exceptions.base_exception import LavaBaseException
from lava_sdk.dto.request.refund.create_refund_dto import CreateRefundDto

dto = CreateRefundDto(
    invoice_id="lava-inv-00003",
    description="Тест обработки ошибок",
    amount=100.00,
)

try:
    refund = facade.create_refund(dto)
    print(f"ID возврата: {refund.get_refund_id()}")
    print(f"Статус:      {refund.get_status()}")

except RefundException as e:
    # Бизнес-ошибки возвратов:
    #   — инвойс не найден
    #   — инвойс не оплачен (статус не success)
    #   — сумма возврата превышает оплаченную сумму
    #   — возврат по этому инвойсу уже обрабатывается
    #   — неверный формат параметров
    print(f"Ошибка возврата [{e.code}]: {e}")

except LavaBaseException as e:
    # Инфраструктурные ошибки:
    #   — сетевой сбой или таймаут
    #   — неожиданный формат ответа от API
    print(f"Ошибка SDK [{e.code}]: {e}")

except Exception as e:
    # Непредвиденные исключения
    print(f"Неожиданная ошибка: {e}")
```
