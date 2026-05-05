# Баланс

> *Неофициальный Python-порт PHP SDK Lava. Не аффилирован с Lava Payment. [← Оглавление](index.md)*

Lava SDK предоставляет два метода для получения баланса: `get_profile_balance()` — актуальный метод на основе профиля, и `get_shop_balance()` — устаревший метод на основе магазина. Рекомендуется использовать `get_profile_balance()`.

---

## Баланс профиля — `get_profile_balance`

```python
facade.get_profile_balance() -> ProfileBalanceDto
```

Метод возвращает балансовые данные профиля Lava. Профиль — это учётная запись более высокого уровня, которая может объединять несколько магазинов.

> **Требование:** для вызова этого метода при инициализации `LavaFacade` необходимо передать объект `ProfileSecretDto` через параметр `profile_secret_data`. Если он не передан — метод выбросит `ValueError`.

### Ответ: ProfileBalanceDto

| Поле | Тип | Описание |
|---|---|---|
| `total_balance` | `float` | Общий баланс профиля (включает заморозку) |
| `available_balance` | `float` | Баланс, доступный для вывода прямо сейчас |
| `freeze_balance` | `float` | Замороженный баланс (средства в обработке или удержании) |

Доступ к полям: `get_total_balance()`, `get_available_balance()`, `get_freeze_balance()`.

### Пример использования

```python
from lava_sdk import LavaFacade, ProfileSecretDto
from lava_sdk.exceptions.profile.profile_exception import ProfileException
from lava_sdk.exceptions.base_exception import LavaBaseException

# ProfileSecretDto содержит учётные данные профиля (не магазина)
profile_secret = ProfileSecretDto(
    profile_id="ваш_идентификатор_профиля",
    secret_key="ваш_секретный_ключ_профиля",
    additional_key="ваш_дополнительный_ключ",  # опционально
)

# Передаём profile_secret_data при инициализации фасада
facade = LavaFacade(
    secret_key="ваш_секретный_ключ_магазина",
    shop_id="ваш_идентификатор_магазина",
    profile_secret_data=profile_secret,
)

try:
    balance = facade.get_profile_balance()

    total     = balance.get_total_balance()
    available = balance.get_available_balance()
    frozen    = balance.get_freeze_balance()

    print(f"Общий баланс:     {total:.2f} руб.")
    print(f"Доступно:         {available:.2f} руб.")
    print(f"Заморожено:       {frozen:.2f} руб.")

    # Пример: проверяем, достаточно ли средств для вывода
    payout_amount = 5000.00
    if available >= payout_amount:
        print(f"Достаточно средств для вывода {payout_amount:.2f} руб.")
    else:
        shortfall = payout_amount - available
        print(f"Недостаточно средств — не хватает {shortfall:.2f} руб.")

except ProfileException as e:
    print(f"Ошибка профиля [{e.code}]: {e}")

except LavaBaseException as e:
    print(f"Ошибка SDK [{e.code}]: {e}")
```

---

## Баланс магазина — `get_shop_balance` *(устарело)*

> **Deprecated:** Этот метод устарел. Используйте [`get_profile_balance()`](#баланс-профиля--get_profile_balance) вместо него. Метод может быть удалён в будущих версиях SDK.

```python
facade.get_shop_balance() -> ShopBalanceDto
```

Метод возвращает баланс конкретного магазина. Не требует `ProfileSecretDto` — работает на основе `shop_id` и `secret_key`, переданных при инициализации `LavaFacade`.

### Ответ: ShopBalanceDto

| Поле | Тип | Описание |
|---|---|---|
| `balance` | `float` | Текущий баланс магазина |
| `freeze_balance` | `float` | Замороженный баланс магазина |

Доступ к полям: `get_balance()`, `get_freeze_balance()`.

### Пример использования

```python
from lava_sdk import LavaFacade
from lava_sdk.exceptions.shop.shop_exception import ShopException
from lava_sdk.exceptions.base_exception import LavaBaseException

# Для get_shop_balance() достаточно стандартной инициализации
facade = LavaFacade(
    secret_key="ваш_секретный_ключ_магазина",
    shop_id="ваш_идентификатор_магазина",
)

try:
    # Deprecated: рекомендуется get_profile_balance()
    balance = facade.get_shop_balance()

    print(f"Баланс магазина:  {balance.get_balance():.2f} руб.")
    print(f"Заморожено:       {balance.get_freeze_balance():.2f} руб.")

except ShopException as e:
    print(f"Ошибка магазина [{e.code}]: {e}")

except LavaBaseException as e:
    print(f"Ошибка SDK [{e.code}]: {e}")
```

---

## Обработка ошибок

### ProfileException

Выбрасывается методом `get_profile_balance()` при ошибках, связанных с профилем.

```python
from lava_sdk import LavaFacade, ProfileSecretDto
from lava_sdk.exceptions.profile.profile_exception import ProfileException
from lava_sdk.exceptions.base_exception import LavaBaseException

profile_secret = ProfileSecretDto(
    profile_id="ваш_идентификатор_профиля",
    secret_key="ваш_секретный_ключ_профиля",
)

facade = LavaFacade(
    secret_key="ваш_секретный_ключ_магазина",
    shop_id="ваш_идентификатор_магазина",
    profile_secret_data=profile_secret,
)

try:
    balance = facade.get_profile_balance()
    print(f"Доступный баланс: {balance.get_available_balance():.2f} руб.")

except ValueError as e:
    # profile_secret_data не был передан при инициализации LavaFacade
    print(f"Ошибка конфигурации: {e}")

except ProfileException as e:
    # Бизнес-ошибки профиля:
    #   — профиль не найден
    #   — неверный секретный ключ профиля
    #   — недостаточно прав для запроса баланса
    print(f"Ошибка профиля [{e.code}]: {e}")

except LavaBaseException as e:
    # Инфраструктурные ошибки SDK
    print(f"Ошибка SDK [{e.code}]: {e}")
```

### ShopException

Выбрасывается устаревшим методом `get_shop_balance()` при ошибках, связанных с магазином.

```python
from lava_sdk import LavaFacade
from lava_sdk.exceptions.shop.shop_exception import ShopException
from lava_sdk.exceptions.base_exception import LavaBaseException

facade = LavaFacade(
    secret_key="ваш_секретный_ключ_магазина",
    shop_id="ваш_идентификатор_магазина",
)

try:
    # Deprecated: используйте get_profile_balance()
    balance = facade.get_shop_balance()
    print(f"Баланс: {balance.get_balance():.2f} руб.")

except ShopException as e:
    # Бизнес-ошибки магазина:
    #   — магазин не найден
    #   — неверный секретный ключ
    #   — магазин деактивирован
    print(f"Ошибка магазина [{e.code}]: {e}")

except LavaBaseException as e:
    # Инфраструктурные ошибки SDK
    print(f"Ошибка SDK [{e.code}]: {e}")

except Exception as e:
    print(f"Неожиданная ошибка: {e}")
```
