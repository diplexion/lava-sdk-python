# H2H-платежи (Host-to-Host)

> *Неофициальный Python-порт PHP SDK Lava. Не аффилирован с Lava Payment. [← Оглавление](index.md)*

## Обзор

H2H (Host-to-Host) — это режим приёма платежей, при котором карточные данные или реквизиты СБП передаются напрямую с вашего сервера в API Lava, без перенаправления пользователя на страницу оплаты. Это обеспечивает полный контроль над интерфейсом и платёжным потоком, однако накладывает дополнительные требования безопасности.

**Ключевые особенности H2H:**

- **Без редиректа** — пользователь остаётся на вашем сайте или в приложении на протяжении всего процесса оплаты.
- **Два варианта оплаты:** по номеру банковской карты или через СБП (Систему быстрых платежей).
- **3DS-аутентификация** — при оплате картой может потребоваться 3DS-подтверждение, URL для которого возвращается в ответе.
- **Требует специального разрешения** — функция H2H активируется по отдельному соглашению с Lava. Свяжитесь с поддержкой для подключения.

> **Важно:** Использование H2H-платежей обязывает вас соответствовать стандарту **PCI DSS** (Payment Card Industry Data Security Standard), так как карточные данные проходят через ваш сервер. Убедитесь, что вы выполнили все требования стандарта и получили необходимые сертификаты перед запуском в продакшн.

---

## H2H по карте — `create_h2h_invoice`

Метод создаёт платёжный инвойс с передачей полных карточных данных непосредственно в запросе. Если банк-эмитент требует 3DS-подтверждения, в ответе будет возвращён URL для перенаправления пользователя на страницу верификации.

```lava-sdk-python/docs/h2h.md#L1-1
facade.create_h2h_invoice(dto: CreateH2hInvoiceDto) -> CreatedH2hInvoiceDto
```

> **Требование:** H2H-платежи требуют соответствия стандарту PCI DSS и заключения отдельного соглашения с Lava. Использование без разрешения невозможно.

### Параметры CreateH2hInvoiceDto

| Параметр | Тип | Обязательный | Описание |
|---|---|---|---|
| `amount` | `float` | Да | Сумма платежа в рублях. |
| `order_id` | `str` | Да | Уникальный ID заказа в вашей системе. Используется для идентификации и предотвращения дублирования. |
| `card_number` | `str` | Да | Номер банковской карты (без пробелов и дефисов). |
| `cvv` | `int` | Да | CVV/CVC-код карты (3 или 4 цифры). |
| `month` | `int` | Да | Месяц истечения срока действия карты (числом, например `7` или `12`). |
| `year` | `int` | Да | Год истечения срока действия карты (4 цифры, например `2027`). |
| `hook_url` | `Optional[str]` | Нет | URL для получения webhook-уведомлений о статусе платежа. |
| `success_url` | `Optional[str]` | Нет | URL для редиректа пользователя после успешной оплаты (или успешного 3DS). |
| `fail_url` | `Optional[str]` | Нет | URL для редиректа пользователя в случае ошибки оплаты или 3DS. |
| `expire` | `Optional[int]` | Нет | Время жизни инвойса в секундах. По умолчанию `300` (5 минут). |
| `custom_fields` | `Optional[str]` | Нет | Произвольные данные в виде строки. Возвращаются в webhook-уведомлениях без изменений. |
| `comment` | `Optional[str]` | Нет | Комментарий к платежу. Может отображаться в личном кабинете. |

### Ответ: CreatedH2hInvoiceDto

| Поле | Тип | Описание |
|---|---|---|
| `invoice_id` | `str` | Уникальный ID инвойса, присвоенный системой Lava. |
| `url` | `str` | URL для прохождения 3DS-аутентификации. Если 3DS не требуется, возвращается пустая строка или служебный URL. |
| `card_mask` | `str` | Маскированный номер карты для отображения пользователю (например, `4276 **** **** 7891`). |
| `amount` | `float` | Запрошенная сумма платежа. |
| `amount_pay` | `float` | Итоговая сумма к списанию с карты (с учётом комиссии). |
| `commission` | `float` | Размер комиссии за транзакцию. |
| `shop_id` | `str` | ID магазина, которому принадлежит инвойс. |

Доступ к полям — через геттеры: `get_invoice_id()`, `get_url()`, `get_card_mask()`, `get_amount()`, `get_amount_pay()`, `get_commission()`, `get_shop_id()`.

### Пример использования

```lava-sdk-python/docs/h2h.md#L1-1
from lava_sdk.http.lava_facade import LavaFacade
from lava_sdk.dto.request.h2h.create_h2h_invoice_dto import CreateH2hInvoiceDto
from lava_sdk.exceptions.h2h.h2h_exception import H2hException
from lava_sdk.exceptions.base_exception import LavaBaseException

# Инициализация фасада (H2H не требует ProfileSecretDto — используются ключи магазина)
facade = LavaFacade(
    secret_key="ваш-shop-secret-key",
    shop_id="ваш-shop-id",
)

# Формируем DTO с карточными данными
# ВАЖНО: никогда не храните карточные данные в открытом виде на сервере!
# Получайте их напрямую из формы пользователя по защищённому каналу (HTTPS).
dto = CreateH2hInvoiceDto(
    amount=999.00,                              # Сумма: 999 рублей
    order_id="h2h-order-20240601-042",          # Уникальный ID в вашей системе
    card_number="4276000000000000",             # Номер карты (16 цифр)
    cvv=123,                                    # CVV-код
    month=9,                                    # Месяц: сентябрь
    year=2027,                                  # Год истечения
    hook_url="https://example.com/webhooks/h2h",
    success_url="https://example.com/payment/success",
    fail_url="https://example.com/payment/fail",
    expire=600,                                 # Время жизни: 10 минут
    comment="Оплата заказа №042",
)

try:
    result = facade.create_h2h_invoice(dto)

    print(f"H2H-инвойс создан!")
    print(f"  ID инвойса:         {result.get_invoice_id()}")
    print(f"  Карта (маска):      {result.get_card_mask()}")
    print(f"  Сумма заказа:       {result.get_amount()} руб.")
    print(f"  Сумма к списанию:   {result.get_amount_pay()} руб.")
    print(f"  Комиссия:           {result.get_commission()} руб.")
    print(f"  ID магазина:        {result.get_shop_id()}")

    # Если требуется 3DS — перенаправляем пользователя
    if result.get_url():
        print(f"\n  Требуется 3DS-подтверждение!")
        print(f"  Перенаправьте пользователя на: {result.get_url()}")
        # В вашем веб-приложении: redirect(result.get_url())
    else:
        print("\n  3DS не требуется. Ожидаем webhook о статусе платежа.")

except H2hException as e:
    # Ошибка H2H: неверные карточные данные, карта заблокирована, недостаточно средств
    print(f"Ошибка H2H-платежа [{e.code}]: {e}")
except LavaBaseException as e:
    # Сетевая ошибка, ошибка авторизации и т.д.
    print(f"Ошибка SDK [{e.code}]: {e}")
```

---

## H2H через СБП — `create_h2h_spb_invoice`

Метод создаёт платёжный инвойс через Систему быстрых платежей (СБП). В ответе возвращается ссылка для перехода в банковское приложение и QR-код для сканирования. Пользователь подтверждает платёж самостоятельно в своём банковском приложении.

```lava-sdk-python/docs/h2h.md#L1-1
facade.create_h2h_spb_invoice(dto: CreateSBPH2HDto) -> CreatedSBPH2hDto
```

### Параметры CreateSBPH2HDto

| Параметр | Тип | Обязательный | Описание |
|---|---|---|---|
| `amount` | `float` | Да | Сумма платежа в рублях. |
| `order_id` | `str` | Да | Уникальный ID заказа в вашей системе. |
| `ip` | `str` | Да | IP-адрес пользователя, инициировавшего платёж. Используется для защиты от мошенничества. |
| `hook_url` | `Optional[str]` | Нет | URL для получения webhook-уведомлений о статусе платежа. |
| `success_url` | `Optional[str]` | Нет | URL для редиректа после успешной оплаты. |
| `fail_url` | `Optional[str]` | Нет | URL для редиректа при ошибке или истечении времени. |
| `expire` | `Optional[int]` | Нет | Время жизни инвойса в секундах. По умолчанию `300` (5 минут). |
| `custom_fields` | `Optional[str]` | Нет | Произвольные данные в виде строки. Возвращаются в webhook-уведомлениях без изменений. |
| `comment` | `Optional[str]` | Нет | Комментарий к платежу. |

### Ответ: CreatedSBPH2hDto

| Поле | Тип | Описание |
|---|---|---|
| `sbp_url` | `str` | Deep-link ссылка для перехода в банковское приложение пользователя через СБП. Передаётся на клиент для открытия в браузере или приложении. |
| `qr_code` | `str` | Строка с данными QR-кода (base64 или URL). Отображается пользователю для сканирования в банковском приложении. |
| `fingerprint` | `bool` | Флаг наличия fingerprint-данных для дополнительной верификации транзакции. |

Доступ к полям — через методы `get_sbp_url()`, `get_qr_code()`, `is_fingerprint()`.

### Пример использования

```lava-sdk-python/docs/h2h.md#L1-1
from lava_sdk.http.lava_facade import LavaFacade
from lava_sdk.dto.request.h2h.create_sbp_h2h_dto import CreateSBPH2HDto
from lava_sdk.exceptions.h2h.h2h_exception import H2hException
from lava_sdk.exceptions.base_exception import LavaBaseException

# Инициализация фасада
facade = LavaFacade(
    secret_key="ваш-shop-secret-key",
    shop_id="ваш-shop-id",
)

# IP-адрес пользователя нужно получать из входящего HTTP-запроса
user_ip = "95.173.136.12"   # Пример: request.remote_addr (Flask) или request.META['REMOTE_ADDR'] (Django)

dto = CreateSBPH2HDto(
    amount=350.50,                               # Сумма: 350.50 рублей
    order_id="sbp-order-20240601-088",           # Уникальный ID заказа
    ip=user_ip,                                  # IP-адрес пользователя
    hook_url="https://example.com/webhooks/sbp",
    success_url="https://example.com/payment/success",
    fail_url="https://example.com/payment/fail",
    expire=300,                                  # Время жизни: 5 минут
    comment="Оплата через СБП",
)

try:
    result = facade.create_h2h_spb_invoice(dto)

    print("СБП-инвойс создан!")
    print(f"  Fingerprint:   {result.is_fingerprint()}")

    # Отображаем QR-код пользователю (в браузере или приложении)
    print(f"\n  QR-код для оплаты:")
    print(f"  {result.get_qr_code()}")

    # Для мобильных устройств — ссылка для открытия банковского приложения
    sbp_url = result.get_sbp_url()
    if sbp_url:
        print(f"\n  Ссылка для открытия банковского приложения:")
        print(f"  {sbp_url}")
        # В мобильном приложении: open_url(sbp_url)
        # В браузере: redirect(sbp_url) для мобильных UA, или показать QR на десктопе

    print("\n  Ожидаем подтверждение оплаты через webhook...")

except H2hException as e:
    # Ошибка создания СБП-инвойса (неверные параметры, сервис недоступен и т.д.)
    print(f"Ошибка H2H СБП [{e.code}]: {e}")
except LavaBaseException as e:
    print(f"Ошибка SDK [{e.code}]: {e}")
```

---

## Обработка ошибок

Оба H2H-метода выбрасывают исключение `H2hException` в случае ошибки на стороне API Lava. Оно наследуется от `LavaBaseException` и содержит атрибуты `code` (числовой код ошибки) и `message` (текстовое описание).

| Исключение | Модуль | Описание |
|---|---|---|
| `H2hException` | `lava_sdk.exceptions.h2h.h2h_exception` | Общая ошибка H2H-платежа: неверные карточные данные, отказ банка, недоступность сервиса, нарушение лимитов и т.д. |

```lava-sdk-python/docs/h2h.md#L1-1
from lava_sdk.http.lava_facade import LavaFacade
from lava_sdk.dto.request.h2h.create_h2h_invoice_dto import CreateH2hInvoiceDto
from lava_sdk.dto.request.h2h.create_sbp_h2h_dto import CreateSBPH2HDto
from lava_sdk.exceptions.h2h.h2h_exception import H2hException
from lava_sdk.exceptions.base_exception import LavaBaseException

facade = LavaFacade(
    secret_key="ваш-shop-secret-key",
    shop_id="ваш-shop-id",
)

# ── Обработка ошибок H2H по карте ──────────────────────────────────────────
card_dto = CreateH2hInvoiceDto(
    amount=500.00,
    order_id="h2h-err-demo-001",
    card_number="4276000000000000",
    cvv=123,
    month=9,
    year=2027,
)

try:
    response = facade.create_h2h_invoice(card_dto)
    print(f"Инвойс создан: {response.get_invoice_id()}")

    if response.get_url():
        print(f"Требуется 3DS: {response.get_url()}")

except H2hException as e:
    # Возможные причины:
    #   - Неверный номер карты или срок действия
    #   - Карта заблокирована или недостаточно средств
    #   - H2H не активирован для данного магазина
    #   - Нарушение лимитов транзакции
    print(f"Ошибка H2H-платежа [{e.code}]: {e}")

except LavaBaseException as e:
    # Сетевая ошибка, ошибка подписи, неверные учётные данные и т.д.
    print(f"Общая ошибка SDK [{e.code}]: {e}")


# ── Обработка ошибок H2H через СБП ────────────────────────────────────────
sbp_dto = CreateSBPH2HDto(
    amount=150.00,
    order_id="sbp-err-demo-001",
    ip="95.173.136.12",
)

try:
    sbp_response = facade.create_h2h_spb_invoice(sbp_dto)
    print(f"СБП-инвойс создан. QR: {sbp_response.get_qr_code()[:40]}...")

except H2hException as e:
    # Возможные причины:
    #   - Неверный IP-адрес пользователя
    #   - СБП H2H не активирован для магазина
    #   - Нарушение лимитов суммы
    print(f"Ошибка H2H СБП [{e.code}]: {e}")

except LavaBaseException as e:
    print(f"Общая ошибка SDK [{e.code}]: {e}")
```
