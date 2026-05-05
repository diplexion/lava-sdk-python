# Вебхуки и верификация подписей

> *Неофициальный Python-порт PHP SDK Lava. Не аффилирован с Lava Payment. [← Оглавление](index.md)*

## Обзор

Платёжная система Lava отправляет **HTTP POST-запросы (вебхуки)** на указанный вами URL каждый раз, когда меняется статус инвойса (счёта на оплату) или выплаты (payoff). Это позволяет вашему серверу в режиме реального времени реагировать на события — например, выдавать товар после успешной оплаты или помечать заказ как отменённый.

Ключевые характеристики вебхуков Lava:

- **Тело запроса** — JSON-строка с полями, описывающими событие.
- **Метод** — всегда `POST`.
- **Подпись** — HMAC-SHA256 от отсортированного JSON-тела, передаётся в заголовке `Authorization`.
- **Ключ подписи** — для инвойсов используется `additional_key` из конструктора `LavaFacade`; для выплат — `additional_key` из `ProfileSecretDto`.

> **Важно:** Всегда верифицируйте подпись перед обработкой вебхука. Запросы с неверной подписью необходимо отклонять с кодом HTTP 403.

---

## Алгоритм верификации подписи

Lava применяет единый алгоритм подписи как для вебхуков инвойсов, так и для вебхуков выплат. Ниже приведено пошаговое описание того, что происходит внутри `ClientCheckSignatureWebhook.check_sign_webhook`.

**Шаг 1 — Получить тело запроса как строку (raw JSON)**

Необходимо считать тело HTTP-запроса как «сырую» строку, **не разбирая** её заранее. Многие веб-фреймворки предоставляют для этого специальный метод (например, `request.get_data(as_text=True)` во Flask или `await request.body()` в FastAPI). Если тело было считано ранее, его нужно сохранить до вызова метода верификации.

**Шаг 2 — Разобрать JSON в словарь**

Строка парсится стандартным `json.loads`, результатом является обычный словарь Python.

**Шаг 3 — Отсортировать ключи словаря по алфавиту**

Ключи сортируются в лексикографическом порядке (`sorted(data.items())`). Это необходимо потому, что порядок ключей в JSON не гарантирован, а HMAC-подпись чувствительна к порядку символов в строке.

**Шаг 4 — Сериализовать обратно в JSON без пробелов**

Используется `json.dumps` с параметром `separators=(",", ":")`, чтобы исключить пробелы после запятых и двоеточий, и `ensure_ascii=True`, чтобы не-ASCII символы были экранированы в формате `\uXXXX`. Это гарантирует побайтовое совпадение результата на любой платформе.

**Шаг 5 — Вычислить HMAC-SHA256 с секретным ключом**

Полученная строка кодируется в UTF-8, затем вычисляется HMAC-SHA256. В качестве ключа используется секретный ключ вебхука, тоже закодированный в UTF-8.

**Шаг 6 — Сравнить с переданной подписью из заголовка Authorization**

Результат вычисления (`hexdigest`) сравнивается с подписью из заголовка `Authorization`. Если они совпадают — запрос подлинный.

```lava-sdk-python/lava_sdk/http/client/client_check_signature_webhook.py#L1-35
import hashlib
import hmac
import json

data = json.loads(webhook_response)
sorted_data = dict(sorted(data.items()))
payload = json.dumps(sorted_data, separators=(",", ":"), ensure_ascii=True)
computed = hmac.new(
    secret_key.encode("utf-8"),
    payload.encode("utf-8"),
    hashlib.sha256,
).hexdigest()
is_valid = computed == signature
```

---

## Верификация вебхука инвойса — `check_sign_webhook`

**Сигнатура метода:**

```lava-sdk-python/lava_sdk/http/lava_facade.py#L1-1
facade.check_sign_webhook(webhook_response: str, signature: str) -> bool
```

Метод верифицирует подпись входящего вебхука инвойса. Для вычисления HMAC используется `additional_key`, переданный в конструктор `LavaFacade` (параметр `additional_key`). Этот ключ хранится в `ClientCheckSignatureWebhook` и не совпадает с основным секретным ключом API.

### Параметры

| Параметр | Тип | Описание |
|---|---|---|
| `webhook_response` | `str` | Тело запроса в виде строки (raw JSON), считанное напрямую из HTTP-запроса |
| `signature` | `str` | Подпись из заголовка `Authorization` входящего запроса |

### Возвращаемое значение

- `True` — подпись корректна, запрос подлинный.
- `False` — подпись не совпадает, запрос следует отклонить.

### Пример использования

```lava-sdk-python/lava_sdk/http/lava_facade.py#L1-1
from lava_sdk.http.lava_facade import LavaFacade

facade = LavaFacade(
    secret_key="ваш_секретный_ключ",
    shop_id="ваш_shop_id",
    additional_key="ваш_ключ_вебхука",
)

raw_body = '{"invoiceId":"inv-xxx","status":"success","amount":300.09}'
auth_header = "a3f9d1..."  # значение из заголовка Authorization

if facade.check_sign_webhook(raw_body, auth_header):
    print("Подпись верна — обрабатываем вебхук")
else:
    print("Подпись неверна — отклоняем запрос")
```

---

## Интеграция с Flask

Ниже приведён полный пример обработчика вебхука инвойса на базе Flask. Обратите внимание на использование `request.get_data(as_text=True)` — это единственный способ получить «сырое» тело запроса без его предварительной обработки фреймворком.

```lava-sdk-python/docs/webhooks.md#L1-1
from flask import Flask, request, abort
from lava_sdk.http.lava_facade import LavaFacade
import os

app = Flask(__name__)

facade = LavaFacade(
    secret_key=os.environ["LAVA_SECRET_KEY"],
    shop_id=os.environ["LAVA_SHOP_ID"],
    additional_key=os.environ["LAVA_WEBHOOK_KEY"],
)

@app.route("/webhook/invoice", methods=["POST"])
def invoice_webhook():
    body = request.get_data(as_text=True)
    signature = request.headers.get("Authorization", "")

    if not facade.check_sign_webhook(body, signature):
        abort(403, "Invalid signature")

    import json
    data = json.loads(body)
    status = data.get("status")
    order_id = data.get("orderId")

    # Обработайте смену статуса
    if status == "success":
        print(f"Заказ {order_id} оплачен!")

    return {"status": "ok"}, 200
```

**Важные замечания для Flask:**

- Не вызывайте `request.json` или `request.get_json()` до обращения к `request.get_data()`, так как это может израсходовать поток данных.
- Убедитесь, что переменная окружения `LAVA_WEBHOOK_KEY` содержит именно ключ вебхука (не основной секрет API).
- Возвращайте HTTP 200, только если обработка прошла успешно — иначе Lava будет повторно отправлять вебхук.

---

## Интеграция с FastAPI

Следующий пример демонстрирует обработку вебхука в асинхронном приложении FastAPI. Тело запроса считывается через `await request.body()`, что возвращает байты; их нужно декодировать в UTF-8 строку.

```lava-sdk-python/docs/webhooks.md#L1-1
from fastapi import FastAPI, Request, HTTPException
from lava_sdk.http.lava_facade import LavaFacade
import os, json

app = FastAPI()

facade = LavaFacade(
    secret_key=os.environ["LAVA_SECRET_KEY"],
    shop_id=os.environ["LAVA_SHOP_ID"],
    additional_key=os.environ["LAVA_WEBHOOK_KEY"],
)

@app.post("/webhook/invoice")
async def invoice_webhook(request: Request):
    body = (await request.body()).decode("utf-8")
    signature = request.headers.get("Authorization", "")

    if not facade.check_sign_webhook(body, signature):
        raise HTTPException(status_code=403, detail="Invalid signature")

    data = json.loads(body)
    status = data.get("status")
    order_id = data.get("orderId")

    # Обработайте событие...
    if status == "success":
        print(f"Заказ {order_id} оплачен!")

    return {"status": "ok"}
```

**Важные замечания для FastAPI:**

- Используйте `Request` из `fastapi`, а не модели Pydantic, в качестве параметра эндпоинта — иначе FastAPI сам разберёт JSON и вы потеряете «сырое» тело.
- `await request.body()` можно вызвать несколько раз в рамках одного запроса — FastAPI кэширует результат.
- Для production-окружения рекомендуется добавить логирование подписей для упрощения отладки.

---

## Верификация вебхука выплаты — `check_payoff_signature`

**Сигнатура метода:**

```lava-sdk-python/lava_sdk/http/lava_facade.py#L1-1
facade.check_payoff_signature(webhook_response: str, signature: str) -> bool
```

Метод верифицирует подпись входящего вебхука выплаты. В отличие от `check_sign_webhook`, для вычисления HMAC здесь используется `additional_key` из `ProfileSecretDto`, переданного в конструктор `LavaFacade`.

> **Предупреждение:** Если `profile_secret_data` не передан в конструктор `LavaFacade`, или если `ProfileSecretDto.additional_key` равен `None`, метод выбросит `ValueError`. Убедитесь, что оба значения установлены перед вызовом `check_payoff_signature`.

### Параметры

| Параметр | Тип | Описание |
|---|---|---|
| `webhook_response` | `str` | Тело запроса в виде строки (raw JSON), считанное напрямую из HTTP-запроса |
| `signature` | `str` | Подпись из заголовка `Authorization` входящего запроса |

### Возвращаемое значение

- `True` — подпись корректна, запрос подлинный.
- `False` — подпись не совпадает, запрос следует отклонить.

### Пример обработчика вебхука выплаты (Flask)

```lava-sdk-python/docs/webhooks.md#L1-1
from flask import Flask, request, abort
from lava_sdk.http.lava_facade import LavaFacade
from lava_sdk.dto.secret.profile_secret_dto import ProfileSecretDto
import os, json

app = Flask(__name__)

profile = ProfileSecretDto(
    profile_id=os.environ["LAVA_PROFILE_ID"],
    secret_key=os.environ["LAVA_PROFILE_SECRET_KEY"],
    additional_key=os.environ["LAVA_PAYOFF_WEBHOOK_KEY"],
)

facade = LavaFacade(
    secret_key=os.environ["LAVA_SECRET_KEY"],
    shop_id=os.environ["LAVA_SHOP_ID"],
    profile_secret_data=profile,
)

@app.route("/webhook/payoff", methods=["POST"])
def payoff_webhook():
    body = request.get_data(as_text=True)
    signature = request.headers.get("Authorization", "")

    if not facade.check_payoff_signature(body, signature):
        abort(403, "Invalid payoff signature")

    data = json.loads(body)
    status = data.get("status")
    order_id = data.get("orderId")
    payoff_id = data.get("payoffId")

    if status == "success":
        print(f"Выплата {payoff_id} для заказа {order_id} выполнена успешно")
    elif status == "error":
        error = data.get("errorMessage", "Неизвестная ошибка")
        print(f"Выплата {payoff_id} завершилась ошибкой: {error}")

    return {"status": "ok"}, 200
```

### Пример обработчика вебхука выплаты (FastAPI)

```lava-sdk-python/docs/webhooks.md#L1-1
from fastapi import FastAPI, Request, HTTPException
from lava_sdk.http.lava_facade import LavaFacade
from lava_sdk.dto.secret.profile_secret_dto import ProfileSecretDto
import os, json

app = FastAPI()

profile = ProfileSecretDto(
    profile_id=os.environ["LAVA_PROFILE_ID"],
    secret_key=os.environ["LAVA_PROFILE_SECRET_KEY"],
    additional_key=os.environ["LAVA_PAYOFF_WEBHOOK_KEY"],
)

facade = LavaFacade(
    secret_key=os.environ["LAVA_SECRET_KEY"],
    shop_id=os.environ["LAVA_SHOP_ID"],
    profile_secret_data=profile,
)

@app.post("/webhook/payoff")
async def payoff_webhook(request: Request):
    body = (await request.body()).decode("utf-8")
    signature = request.headers.get("Authorization", "")

    if not facade.check_payoff_signature(body, signature):
        raise HTTPException(status_code=403, detail="Invalid payoff signature")

    data = json.loads(body)
    # Обработайте событие выплаты...
    return {"status": "ok"}
```

---

## Структура тела вебхука

### Вебхук инвойса

Lava отправляет примерно следующее тело при изменении статуса инвойса:

```lava-sdk-python/docs/webhooks.md#L1-1
{
  "invoiceId": "inv-xxx",
  "orderId": "order-123",
  "status": "success",
  "amount": 300.09,
  "shopId": "shop-xxx",
  "customFields": "{\"productId\":39}"
}
```

| Поле | Тип | Описание |
|---|---|---|
| `invoiceId` | `string` | Уникальный идентификатор инвойса в системе Lava |
| `orderId` | `string` | Идентификатор заказа, переданный при создании инвойса |
| `status` | `string` | Новый статус инвойса (`success`, `cancel`, `pending` и т.д.) |
| `amount` | `number` | Сумма платежа |
| `shopId` | `string` | Идентификатор магазина |
| `customFields` | `string` | Произвольные поля, переданные при создании инвойса (JSON-строка) |

### Вебхук выплаты

Тело вебхука при изменении статуса выплаты:

```lava-sdk-python/docs/webhooks.md#L1-1
{
  "payoffId": "payoff-xxx",
  "orderId": "order-456",
  "status": "success",
  "amount": 10.00,
  "service": "lava_payoff"
}
```

| Поле | Тип | Описание |
|---|---|---|
| `payoffId` | `string` | Уникальный идентификатор выплаты в системе Lava |
| `orderId` | `string` | Идентификатор заказа, переданный при создании выплаты |
| `status` | `string` | Новый статус выплаты (`success`, `error` и т.д.) |
| `amount` | `number` | Сумма выплаты |
| `service` | `string` | Идентификатор сервиса выплаты |

---

## Частые ошибки

### 1. Повторное считывание тела запроса

**Проблема:** некоторые фреймворки позволяют считать тело запроса только один раз — после чего поток данных исчерпывается. Если вы уже вызвали `request.json` или `request.get_json()` до `request.get_data()`, тело окажется пустым строкой.

**Решение:** всегда считывайте «сырое» тело самым первым действием в обработчике и сохраняйте его в переменную. Последующие разборы JSON делайте уже из этой переменной.

```lava-sdk-python/docs/webhooks.md#L1-1
# Правильно
body = request.get_data(as_text=True)     # считываем один раз
signature = request.headers.get("Authorization", "")
is_valid = facade.check_sign_webhook(body, signature)  # передаём исходную строку
data = json.loads(body)                   # повторно парсим из той же строки

# Неправильно
data = request.get_json()                 # тело уже израсходовано!
body = request.get_data(as_text=True)     # вернёт пустую строку
```

### 2. Передача уже разобранного JSON вместо «сырой» строки

**Проблема:** метод `check_sign_webhook` ожидает строку с исходным JSON (`str`), но не принимает уже разобранный словарь или повторно сериализованный JSON. Пересериализация может изменить порядок ключей или форматирование, что сломает подпись.

**Решение:** передавайте строку, считанную непосредственно из HTTP-запроса, без каких-либо промежуточных преобразований.

```lava-sdk-python/docs/webhooks.md#L1-1
# Правильно
raw = request.get_data(as_text=True)
facade.check_sign_webhook(raw, signature)

# Неправильно
parsed = json.loads(request.get_data(as_text=True))
raw_again = json.dumps(parsed)            # порядок ключей может отличаться!
facade.check_sign_webhook(raw_again, signature)
```

### 3. Не установлен `additional_key`

**Проблема:** `check_sign_webhook` использует `additional_key`, переданный в конструктор `LavaFacade`. Если он не задан (`None`), `ClientCheckSignatureWebhook` попытается вызвать `None.encode("utf-8")` и упадёт с `AttributeError`.

**Решение:** всегда передавайте `additional_key` при создании `LavaFacade`:

```lava-sdk-python/docs/webhooks.md#L1-1
facade = LavaFacade(
    secret_key="...",
    shop_id="...",
    additional_key="ключ_вебхука_из_личного_кабинета",  # обязательно!
)
```

### 4. Перепутаны ключи магазина и профиля

**Проблема:** у Lava существуют два разных уровня ключей: ключ магазина (`shop`) и ключ профиля (`profile`). Для верификации вебхука инвойса используется ключ вебхука магазина (`additional_key` в `LavaFacade`), а для верификации вебхука выплаты — ключ вебхука профиля (`additional_key` в `ProfileSecretDto`). Если перепутать их местами, подпись всегда будет неверной.

**Решение:** в личном кабинете Lava найдите раздельные ключи для вебхуков и убедитесь, что каждый из них передаётся в правильный объект:

```lava-sdk-python/docs/webhooks.md#L1-1
from lava_sdk.dto.secret.profile_secret_dto import ProfileSecretDto
from lava_sdk.http.lava_facade import LavaFacade

profile = ProfileSecretDto(
    profile_id="id_профиля",
    secret_key="секрет_профиля",
    additional_key="ключ_вебхука_ВЫПЛАТЫ",  # ключ от профиля
)

facade = LavaFacade(
    secret_key="секрет_магазина",
    shop_id="id_магазина",
    additional_key="ключ_вебхука_ИНВОЙСА",  # ключ от магазина
    profile_secret_data=profile,
)
```
