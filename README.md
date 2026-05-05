# Lava SDK for Python

![Python](https://img.shields.io/badge/python-%5E3.8-blue?style=plastic)
![License](https://img.shields.io/badge/license-MIT-green?style=plastic)

Python SDK for working with the [Lava Payment](https://lava.ru) API via the `LavaFacade` class.

## Installation

```bash
pip install -r requirements.txt
```

Or install directly into your project:

```bash
pip install requests
```

## Quick Start

### Initialization (shop methods only)

```python
from lava_sdk.http.lava_facade import LavaFacade

facade = LavaFacade(
    secret_key="shop_secret_key",
    shop_id="shop_id",
    webhook_additional_key="shop_webhook_additional_key",  # optional
)
```

### Initialization with profile/payoff methods

For profile and payoff methods (`create_payoff`, `get_status_payoff`, `get_payoff_tariffs`, `check_wallet`, `get_profile_balance`, `check_payoff_signature`) pass a `ProfileSecretDto`.

```python
from lava_sdk.http.lava_facade import LavaFacade
from lava_sdk.dto.secret.profile_secret_dto import ProfileSecretDto

profile_secret = ProfileSecretDto(
    profile_id="profile_id",
    secret_key="profile_secret_key",
    additional_key="profile_additional_key",  # optional, needed for check_payoff_signature
)

facade = LavaFacade(
    secret_key="shop_secret_key",
    shop_id="shop_id",
    webhook_additional_key="shop_webhook_additional_key",
    profile_secret=profile_secret,
)
```

## Facade Methods

### Invoices

#### Create invoice — `create_invoice`

```python
from lava_sdk.dto.request.invoice.create_invoice_dto import CreateInvoiceDto

dto = CreateInvoiceDto(
    sum="300.09",
    order_id="order-1001",
    hook_url="https://example.com/hook",
    success_url="https://example.com/success",
    fail_url="https://example.com/fail",
    expire=300,
    custom_fields='{"productId":39}',
    comment="Pay product",
)

response = facade.create_invoice(dto)
# response is a CreatedInvoiceDto
```

#### Invoice status — `check_status_invoice`

```python
from lava_sdk.dto.request.invoice.get_status_invoice_dto import GetStatusInvoiceDto

dto = GetStatusInvoiceDto(invoice_id="some-invoice-id")
response = facade.check_status_invoice(dto)
# response is a StatusInvoiceDto
```

#### Available tariffs — `get_availible_tariffs`

```python
tariffs = facade.get_availible_tariffs()
# returns a list of AvailibleTariffDto
```

### Refunds

#### Create refund — `create_refund`

```python
from lava_sdk.dto.request.refund.create_refund_dto import CreateRefundDto

dto = CreateRefundDto(
    invoice_id="invoice-id",
    amount=100.00,
)

response = facade.create_refund(dto)
# response is a CreatedRefundDto
```

#### Refund status — `check_status_refund`

```python
from lava_sdk.dto.request.refund.get_status_refund_dto import GetStatusRefundDto

dto = GetStatusRefundDto(refund_id="refund-id")
response = facade.check_status_refund(dto)
# response is a StatusRefundDto
```

### Balance

#### Profile balance — `get_profile_balance`

```python
balance = facade.get_profile_balance()
# returns a ProfileBalanceDto
```

#### Shop balance — `get_shop_balance` *(deprecated)*

```python
balance = facade.get_shop_balance()
# deprecated — use get_profile_balance() instead
```

### Payoffs (withdrawals)

#### Create payoff — `create_payoff`

```python
from lava_sdk.dto.request.payoff.create_payoff_dto import CreatePayoffDto

dto = CreatePayoffDto(
    order_id="withdraw-order-1",
    amount=10.00,
    service="lava_payoff",
)

response = facade.create_payoff(dto)
# response is a CreatedPayoffDto
```

#### Payoff status — `get_status_payoff`

```python
from lava_sdk.dto.request.payoff.get_payoff_status_dto import GetPayoffStatusDto

dto = GetPayoffStatusDto(payoff_id="payoff-id")
response = facade.get_status_payoff(dto)
# response is a StatusPayoffDto
```

#### Payoff tariffs — `get_payoff_tariffs`

```python
tariffs = facade.get_payoff_tariffs()
```

#### Check wallet — `check_wallet`

```python
from lava_sdk.dto.request.payoff.check_wallet_request_dto import CheckWalletRequestDto

dto = CheckWalletRequestDto(service="lava_payoff", wallet="wallet_value")
response = facade.check_wallet(dto)
# response is a CheckWalletResponseDto
```

### Webhooks & Signatures

#### Verify shop webhook signature — `check_sign_webhook`

```python
# In a Flask/FastAPI/Django handler:
body = request.get_data(as_text=True)       # raw JSON string from the request body
signature = request.headers.get("Authorization")

is_valid = facade.check_sign_webhook(body, signature)
if not is_valid:
    raise Exception("Invalid webhook signature")
```

#### Verify payoff webhook signature — `check_payoff_signature`

```python
body = request.get_data(as_text=True)
signature = request.headers.get("Authorization")

is_valid = facade.check_payoff_signature(body, signature)
```

## Exceptions

All API errors raise typed exceptions. Wrap facade calls in `try/except`:

```python
from lava_sdk.exceptions.invoice_exception import InvoiceException
from lava_sdk.exceptions.payoff_exception import PayoffException
from lava_sdk.exceptions.base_exception import LavaBaseException

try:
    response = facade.create_invoice(dto)
except InvoiceException as e:
    print(f"Invoice error {e.code}: {e.message}")
except LavaBaseException as e:
    print(f"SDK error {e.code}: {e.message}")
```

## Running Tests

```bash
pip install -r requirements-dev.txt
pytest
```

## Project Structure

```text
lava_sdk/
├── constants/          # API base URL and endpoint paths
├── dto/
│   ├── request/        # Request DTOs (invoice, payoff, refund, h2h, …)
│   ├── response/       # Response DTOs
│   └── secret/         # ProfileSecretDto, ShopSecretDto
├── exceptions/         # Typed exception classes
└── http/
    ├── client.py       # Low-level HTTP client (requests library)
    ├── handlers/       # Request/response mappers per domain
    └── lava_facade.py  # Main entry point — LavaFacade

tests/
├── Mocks/              # Mock HTTP clients (success / error)
├── test_invoice.py
├── test_payoff.py
├── test_refund.py
├── test_webhook.py
└── …
```
