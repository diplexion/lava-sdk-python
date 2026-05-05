# Lava Python SDK — Документация

> ⚠️ **Неофициальный порт.** Данный SDK является неофициальным портом официального PHP SDK Lava на Python, выполненным сообществом. Проект не аффилирован с компанией Lava Payment и не является официальным продуктом.

**Lava Python SDK** — неофициальный Python-порт PHP SDK Lava для работы с [Lava Payment API](https://dev.lava.ru).
SDK предоставляет удобный и типизированный интерфейс для приёма платежей, создания возвратов, выводов средств,
H2H-платежей, верификации вебхуков, получения баланса и курсов валют.

Весь функционал доступен через единую точку входа — класс **`LavaFacade`**, который инкапсулирует HTTP-транспорт,
генерацию подписей, верификацию входящих уведомлений и маппинг данных в типизированные DTO-объекты.

---

## Оглавление

1. [Установка и зависимости](installation.md)
2. [Инициализация и конфигурация](configuration.md)
3. [Инвойсы (приём платежей)](invoices.md)
4. [Возвраты](refunds.md)
5. [Выводы средств (Payoff)](payoffs.md)
6. [H2H-платежи](h2h.md)
7. [Вебхуки и верификация подписей](webhooks.md)
8. [Баланс](balance.md)
9. [Курсы валют](courses.md)
10. [Исключения и обработка ошибок](exceptions.md)
11. [Справочник классов и DTO](reference.md)

---

## Архитектура

SDK построен по принципу **фасадного паттерна**: `LavaFacade` является единственным публичным API для
пользователя библиотеки. Внутри он делегирует задачи специализированным компонентам.

### Компоненты

| Компонент | Расположение | Назначение |
|---|---|---|
| `LavaFacade` | `lava_sdk/http/lava_facade.py` | Главная точка входа. Оркестрирует все операции |
| `Client` | `lava_sdk/http/client/client.py` | Выполняет HTTP-запросы к Lava API, проверяет коды ответов и бросает исключения |
| `HttpClient` | `lava_sdk/http/client/http_client.py` | Низкоуровневая обёртка над библиотекой `requests` (POST/GET) |
| `ClientGenerateSignature` | `lava_sdk/http/client/client_generate_signature.py` | Вычисляет HMAC-SHA256 подпись запроса |
| `ClientCheckSignatureWebhook` | `lava_sdk/http/client/client_check_signature_webhook.py` | Верифицирует подпись входящего вебхука |
| Handler-классы | `lava_sdk/http/invoices/`, `payoffs/`, `refund/` и т.д. | Конвертируют DTO запроса в `dict` (`to_array`) и ответ API в DTO (`to_dto`) |
| DTO запросов | `lava_sdk/dto/request/` | Типизированные объекты параметров запросов |
| DTO ответов | `lava_sdk/dto/response/` | Типизированные объекты, возвращаемые методами фасада |
| `ProfileSecretDto` | `lava_sdk/dto/secret/profile_secret_dto.py` | Данные авторизации профиля (необходимы для payoff-методов) |

### Схема зависимостей

```text
LavaFacade
├── Client (HTTP-запросы)
│   └── HttpClient (requests library)
├── ClientGenerateSignature (HMAC-SHA256)
├── ClientCheckSignatureWebhook
└── Handler classes (to_array / to_dto)
```

### Поток выполнения запроса

Когда вы вызываете, например, `facade.create_invoice(dto)`, происходит следующее:

1. **Handler** (`CreateInvoice`) преобразует DTO в словарь (`to_array`), добавляя `shop_id`.
2. **`LavaFacade`** удаляет `None`-значения (`_clear_data`) и вычисляет подпись через `ClientGenerateSignature`.
3. **`Client`** отправляет POST-запрос через `HttpClient` на нужный URL-эндпоинт.
4. При HTTP-ошибке или ошибочном статусе в теле ответа `Client` бросает типизированное исключение (`InvoiceException`, `PayoffException` и т.д.).
5. **Handler** (`to_dto`) маппит словарь ответа обратно в типизированный DTO и возвращает его.

---

## Подпись запросов

Каждый исходящий запрос к Lava API подписывается с использованием алгоритма **HMAC-SHA256**.

### Алгоритм подписи

1. **Сортировка ключей** — все ключи словаря запроса сортируются в алфавитном порядке
   (аналог `ksort` в PHP).
2. **JSON-сериализация** — отсортированный словарь сериализуется в JSON без пробелов и отступов
   (параметры `separators=(",", ":")` и `ensure_ascii=True`).
3. **HMAC-SHA256** — JSON-строка подписывается с использованием секретного ключа (`secret_key` магазина
   или `secret_key` профиля, в зависимости от типа операции).
4. **Hex-дайджест** — результат возвращается в виде шестнадцатеричной строки и добавляется
   в тело запроса как поле `signature`.

### Пример

```python
import hashlib
import hmac
import json

data = {"shopId": "abc123", "amount": "100", "orderId": "order-1"}

# Шаг 1: Сортировка ключей
sorted_data = dict(sorted(data.items()))
# {"amount": "100", "orderId": "order-1", "shopId": "abc123"}

# Шаг 2: JSON без пробелов
payload = json.dumps(sorted_data, separators=(",", ":"), ensure_ascii=True)
# '{"amount":"100","orderId":"order-1","shopId":"abc123"}'

# Шаг 3 и 4: HMAC-SHA256 hex-дайджест
signature = hmac.new(
    "your_secret_key".encode("utf-8"),
    payload.encode("utf-8"),
    hashlib.sha256,
).hexdigest()
```

### Верификация вебхуков

Входящие вебхуки верифицируются по аналогичному алгоритму, но с использованием
`additional_key` (дополнительный ключ магазина или профиля). SDK автоматически
обрабатывает это через `ClientCheckSignatureWebhook`.

---

## Требования

| Требование | Версия |
|---|---|
| Python | >= 3.8 |
| `requests` | >= 2.28.0 |

> **Для тестирования** дополнительно требуются `pytest >= 7.0` и `pytest-cov >= 4.0`
> (см. `requirements-dev.txt`).

Для получения подробной информации об установке перейдите в раздел
[Установка и зависимости](installation.md).
