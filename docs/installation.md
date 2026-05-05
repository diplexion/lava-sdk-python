# Установка и зависимости

> *Неофициальный Python-порт PHP SDK Lava. Не аффилирован с Lava Payment. [← Оглавление](index.md)*

Данный раздел описывает требования к окружению и способы установки зависимостей для работы
с Lava Python SDK.

---

## Требования

Перед началом работы убедитесь, что в вашей системе установлены:

| Компонент | Минимальная версия | Назначение |
|---|---|---|
| Python | 3.8+ | Язык, на котором написан SDK |
| pip | любая актуальная | Менеджер пакетов Python |
| `requests` | >= 2.28.0 | HTTP-библиотека для запросов к Lava API |
| `pytest` | >= 7.0 | Фреймворк для запуска тестов *(только для разработки)* |
| `pytest-cov` | >= 4.0 | Измерение покрытия кода тестами *(только для разработки)* |

> **Примечание:** SDK использует только стандартную библиотеку Python и `requests`.
> Никаких тяжёлых фреймворков или дополнительных зависимостей не требуется.

---

## Установка зависимостей

Для установки зависимостей production-среды выполните в корне проекта:

```bash
pip install -r requirements.txt
```

Файл `requirements.txt` содержит:

```text
requests>=2.28.0
```

---

## Установка для разработки

Если вы работаете над SDK или хотите запускать тесты, установите расширенный набор зависимостей:

```bash
pip install -r requirements-dev.txt
```

Файл `requirements-dev.txt` содержит:

```text
requests>=2.28.0
pytest>=7.0
pytest-cov>=4.0
```

> **Рекомендация:** используйте виртуальное окружение (`venv`) для изоляции зависимостей проекта:
>
> ```bash
> python -m venv .venv
> source .venv/bin/activate        # Linux / macOS
> .venv\Scripts\activate           # Windows
> pip install -r requirements-dev.txt
> ```

---

## Ручная установка

Если вам нужна только библиотека `requests` без файла зависимостей:

```bash
pip install requests
```

---

## Проверка установки

После установки зависимостей убедитесь, что SDK доступен и корректно импортируется:

```python
from lava_sdk.http.lava_facade import LavaFacade

print("SDK готов к работе")
```

Ожидаемый вывод:

```text
SDK готов к работе
```

Если при импорте возникает ошибка `ModuleNotFoundError`, убедитесь, что:
1. Виртуальное окружение активировано.
2. Команда `pip install -r requirements.txt` была выполнена успешно.
3. Вы запускаете скрипт из корневой директории проекта `lava-sdk-python/`.

---

## Запуск тестов

SDK поставляется с набором автоматических тестов на базе `pytest`. Тесты используют
**mock-клиенты** (`ClientSuccessResponseMock`, `ClientErrorResponseMock`) и **не требуют
реальных API-ключей** или сетевого доступа.

### Запуск всех тестов

```bash
pytest
```

### Запуск с подробным выводом

```bash
pytest -v
```

Вывод будет показывать статус каждого теста отдельно:

```text
tests/test_invoice.py::test_create_invoice_success PASSED
tests/test_invoice.py::test_create_invoice_fail PASSED
tests/test_payoff.py::test_create_payoff_success PASSED
...
```

### Запуск конкретного тест-файла

```bash
pytest tests/test_invoice.py
```

### Запуск с отчётом о покрытии кода

```bash
pytest --cov=lava_sdk --cov-report=term-missing
```

### Доступные тест-файлы

| Файл | Что тестирует |
|---|---|
| `tests/test_invoice.py` | Создание и проверка статуса инвойсов |
| `tests/test_refund.py` | Создание возвратов и получение их статуса |
| `tests/test_payoff.py` | Выводы средств, статус, тарифы, проверка кошелька |
| `tests/test_h2h.py` | H2H-платежи по карте и через СБП |
| `tests/test_webhook.py` | Верификация подписей входящих вебхуков |
| `tests/test_profile.py` | Баланс профиля |
| `tests/test_shop.py` | Баланс магазина |
| `tests/test_course.py` | Курсы валют (платёжные и payoff) |

> **Важно:** все тесты внедряют mock-клиент напрямую в `LavaFacade` через параметр `client=`.
> Это означает, что HTTP-запросы к реальному API не выполняются. Подробнее о механизме
> внедрения зависимостей см. в разделе [Инициализация и конфигурация](configuration.md).

---

## Структура проекта

```text
lava-sdk-python/
├── lava_sdk/              # Основной пакет SDK
│   ├── constants/         # URL-константы эндпоинтов
│   ├── dto/
│   │   ├── request/       # DTO запросов
│   │   ├── response/      # DTO ответов
│   │   └── secret/        # Объекты с ключами авторизации
│   ├── exceptions/        # Типизированные исключения
│   └── http/
│       ├── client/        # HTTP-клиент и генерация подписи
│       ├── invoices/      # Обработчики инвойсов
│       ├── payoffs/       # Обработчики выводов
│       ├── refund/        # Обработчики возвратов
│       ├── h2h/           # Обработчики H2H
│       ├── profile/       # Обработчик баланса профиля
│       ├── shop/          # Обработчик баланса магазина
│       └── lava_facade.py # Главная точка входа
├── tests/                 # Тесты (pytest)
│   └── Mocks/             # Моки HTTP-клиентов
├── docs/                  # Документация
├── requirements.txt
├── requirements-dev.txt
└── pyproject.toml
```

### Описание ключевых директорий

**`lava_sdk/constants/`** — содержит константы URL для каждой группы эндпоинтов:
- `invoice_url_constants.py` — URL создания и проверки инвойсов
- `payoff_url_constants.py` — URL выводов, тарифов, проверки кошелька
- `refund_url_constants.py` — URL возвратов
- `h2h_url_constants.py` — URL H2H-платежей
- `profile_url_constants.py` — URL баланса профиля
- `shop_url_constants.py` — URL баланса магазина
- `course_url_constants.py` — URL курсов валют
- `client_constants.py` — базовый URL API (`https://api.lava.ru`)

**`lava_sdk/dto/`** — Data Transfer Objects:
- `request/` — объекты с параметрами запросов (например, `CreateInvoiceDto`, `CreatePayoffDto`)
- `response/` — объекты с данными ответов (например, `CreatedInvoiceDto`, `StatusPayoffDto`)
- `secret/` — объекты авторизации (`ProfileSecretDto`, `ShopSecretDto`)

**`lava_sdk/exceptions/`** — иерархия исключений, сгруппированных по типам операций:
- Базовый класс `LavaBaseException`
- Специализированные классы: `InvoiceException`, `PayoffException`, `RefundException`,
  `H2hException`, `CourseException`, `ProfileException`, `ShopException`

**`tests/Mocks/`** — mock-реализации клиента:
- `ClientSuccessResponseMock` — возвращает успешные ответы для всех методов
- `ClientErrorResponseMock` — возвращает ошибочные ответы для проверки обработки исключений
