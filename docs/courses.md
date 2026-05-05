# Курсы валют

> *Неофициальный Python-порт PHP SDK Lava. Не аффилирован с Lava Payment. [← Оглавление](index.md)*

## Обзор

SDK Lava предоставляет два метода для получения актуальных курсов обмена валют:

- **`get_payment_course_list`** — курсы для входящих платежей (инвойсов). Показывает, по какому курсу будет конвертирована сумма при приёме оплаты от покупателя.
- **`get_payoff_course_list`** — курсы для исходящих выводов (payoff). Показывает, по какому курсу будет конвертирована сумма при отправке средств получателю.

Оба метода возвращают список объектов `CourseDto`, каждый из которых содержит информацию о валюте (`CurrencyDto`) и соответствующий курс обмена. Курсы актуальны на момент запроса и могут изменяться в реальном времени в зависимости от рыночных условий.

**Ни один из методов не требует `ProfileSecretDto`** — достаточно инициализировать `LavaFacade` с ключами магазина.

---

## Курсы для платежей — `get_payment_course_list`

Метод возвращает список текущих курсов обмена для всех валют, поддерживаемых при приёме входящих платежей. Используйте этот метод, чтобы показать покупателю, сколько рублей он заплатит за товар или услугу, номинированную в иностранной валюте.

```lava-sdk-python/docs/courses.md#L1-1
facade.get_payment_course_list() -> List[CourseDto]
```

### Ответ: List[CourseDto]

Каждый элемент списка — объект `CourseDto` со следующими полями:

| Поле | Тип | Описание |
|---|---|---|
| `currency` | `CurrencyDto` | Объект с описанием валюты: название, символ и код. |
| `value` | `float` | Курс обмена: количество рублей за одну единицу данной валюты. |

Доступ — через геттеры `get_currency()` и `get_value()`.

**Поля `CurrencyDto`:**

| Поле | Тип | Описание |
|---|---|---|
| `label` | `str` | Полное название валюты (например, `"Доллар США"` или `"US Dollar"`). |
| `symbol` | `str` | Символ валюты для отображения (например, `"$"`, `"€"`, `"₽"`). |
| `value` | `str` | Буквенный код валюты по стандарту ISO 4217 (например, `"USD"`, `"EUR"`, `"RUB"`). |

Доступ — через геттеры `get_label()`, `get_symbol()`, `get_value()`.

### Пример использования

```lava-sdk-python/docs/courses.md#L1-1
from typing import List

from lava_sdk.http.lava_facade import LavaFacade
from lava_sdk.dto.response.course.course_dto import CourseDto
from lava_sdk.dto.response.course.currency_dto import CurrencyDto
from lava_sdk.exceptions.course.course_exception import CourseException
from lava_sdk.exceptions.base_exception import LavaBaseException

# Инициализация фасада (ProfileSecretDto не нужен)
facade = LavaFacade(
    secret_key="ваш-shop-secret-key",
    shop_id="ваш-shop-id",
)

try:
    courses: List[CourseDto] = facade.get_payment_course_list()

    print(f"Курсы для входящих платежей ({len(courses)} валют):\n")

    for course in courses:
        currency: CurrencyDto = course.get_currency()

        code   = currency.get_value()   # Код валюты, например "USD"
        symbol = currency.get_symbol()  # Символ, например "$"
        label  = currency.get_label()   # Название, например "US Dollar"
        rate   = course.get_value()     # Курс в рублях

        print(f"  {code} ({symbol})  —  {label}")
        print(f"    Курс: 1 {code} = {rate} RUB")

    print()

    # Пример практического использования: пересчёт суммы из USD в RUB
    amount_usd = 25.00
    usd_course = next(
        (c for c in courses if c.get_currency().get_value() == "USD"),
        None
    )

    if usd_course:
        amount_rub = amount_usd * usd_course.get_value()
        print(f"  Конвертация: {amount_usd} USD = {amount_rub:.2f} RUB")
        print(f"  (по курсу 1 USD = {usd_course.get_value()} RUB)")
    else:
        print("  Курс USD не найден в списке.")

except CourseException as e:
    print(f"Ошибка получения курсов платежей [{e.code}]: {e}")
except LavaBaseException as e:
    print(f"Ошибка SDK [{e.code}]: {e}")
```

---

## Курсы для выводов — `get_payoff_course_list`

Метод возвращает список текущих курсов обмена для всех валют, поддерживаемых при выводе средств. Используйте этот метод, чтобы заранее рассчитать, сколько рублей будет списано с профиля при выводе суммы в иностранной валюте.

```lava-sdk-python/docs/courses.md#L1-1
facade.get_payoff_course_list() -> List[CourseDto]
```

Структура ответа идентична `get_payment_course_list` — список объектов `CourseDto` с вложенными объектами `CurrencyDto`.

### Пример использования

```lava-sdk-python/docs/courses.md#L1-1
from typing import List

from lava_sdk.http.lava_facade import LavaFacade
from lava_sdk.dto.response.course.course_dto import CourseDto
from lava_sdk.exceptions.course.course_exception import CourseException
from lava_sdk.exceptions.base_exception import LavaBaseException

facade = LavaFacade(
    secret_key="ваш-shop-secret-key",
    shop_id="ваш-shop-id",
)

try:
    courses: List[CourseDto] = facade.get_payoff_course_list()

    print(f"Курсы для выводов средств ({len(courses)} валют):\n")

    for course in courses:
        currency = course.get_currency()
        print(
            f"  {currency.get_value():>6}  {currency.get_symbol():<3}  "
            f"{currency.get_label():<25}  "
            f"1 {currency.get_value()} = {course.get_value():.4f} RUB"
        )

    print()

    # Пример: рассчитаем, сколько рублей нужно иметь на балансе,
    # чтобы вывести 100 EUR
    amount_eur = 100.00
    eur_course = next(
        (c for c in courses if c.get_currency().get_value() == "EUR"),
        None
    )

    if eur_course:
        needed_rub = amount_eur * eur_course.get_value()
        print(f"  Для вывода {amount_eur} EUR потребуется ~{needed_rub:.2f} RUB на балансе.")
        print(f"  (курс: 1 EUR = {eur_course.get_value()} RUB)")
    else:
        print("  Курс EUR для выводов не найден.")

    # Сравнение курсов для двух валют
    print("\n  Топ-3 валюты по убыванию курса:")
    sorted_courses = sorted(courses, key=lambda c: c.get_value(), reverse=True)
    for i, course in enumerate(sorted_courses[:3], start=1):
        cur = course.get_currency()
        print(f"  {i}. {cur.get_value()} ({cur.get_symbol()}) — {course.get_value():.2f} RUB")

except CourseException as e:
    print(f"Ошибка получения курсов выводов [{e.code}]: {e}")
except LavaBaseException as e:
    print(f"Ошибка SDK [{e.code}]: {e}")
```

---

## Обработка ошибок

Оба метода курсов выбрасывают исключение `CourseException` при любой ошибке на стороне API или при получении некорректного ответа (например, отсутствие обязательного поля `data` в теле ответа).

| Исключение | Модуль | Описание |
|---|---|---|
| `CourseException` | `lava_sdk.exceptions.course.course_exception` | Ошибка при запросе курсов валют: недоступность API, некорректный ответ, ошибка авторизации. |

`CourseException` наследуется от `LavaBaseException` и содержит атрибуты `code` (числовой код ошибки) и `message` (текстовое описание).

```lava-sdk-python/docs/courses.md#L1-1
from lava_sdk.http.lava_facade import LavaFacade
from lava_sdk.exceptions.course.course_exception import CourseException
from lava_sdk.exceptions.base_exception import LavaBaseException

facade = LavaFacade(
    secret_key="ваш-shop-secret-key",
    shop_id="ваш-shop-id",
)

# ── Обработка ошибок get_payment_course_list ───────────────────────────────
try:
    payment_courses = facade.get_payment_course_list()
    for course in payment_courses:
        cur = course.get_currency()
        print(f"Платёж: {cur.get_value()} = {course.get_value()} RUB")

except CourseException as e:
    # Возможные причины:
    #   - API Lava временно недоступно
    #   - Неверный shop_id или secret_key
    #   - Ответ от API не содержит ожидаемого поля "data"
    print(f"Ошибка курсов платежей [{e.code}]: {e}")

except LavaBaseException as e:
    print(f"Общая ошибка SDK [{e.code}]: {e}")


# ── Обработка ошибок get_payoff_course_list ────────────────────────────────
try:
    payoff_courses = facade.get_payoff_course_list()
    for course in payoff_courses:
        cur = course.get_currency()
        print(f"Вывод: {cur.get_value()} = {course.get_value()} RUB")

except CourseException as e:
    print(f"Ошибка курсов выводов [{e.code}]: {e}")

except LavaBaseException as e:
    print(f"Общая ошибка SDK [{e.code}]: {e}")
```
