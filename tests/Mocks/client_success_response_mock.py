import random
from typing import Any, Dict


class ClientSuccessResponseMock:
    """Mock client returning successful responses for all endpoints."""

    def create_refund(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "data": {
                "status": "success",
                "refund_id": "5b7d4464-d375-41d4-95b1-bb9786fbbac6",
                "amount": 10.53,
                "service": "card",
                "label": "Банковская карта",
            },
            "status": 200,
            "status_check": True,
        }

    def get_refund_status(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "data": {
                "status": "success",
                "refund_id": "5b7d4464-d375-41d4-95b1-bb9786fbbac6",
                "amount": 10.53,
            },
            "status": 200,
            "status_check": True,
        }

    def create_invoice(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "data": {
                "id": "01fc840d-a0b1-43ca-b65d-ca713d8a1f95",
                "amount": 300,
                "expired": "2022-11-07 13:46:37",
                "status": 0,
                "shop_id": "some-shop-id",
                "url": "https://pay.lava.ru/invoice/01fc840d-a0b1-43ca-b65d-ca713d8a1f95",
                "comment": None,
                "merchantName": "name",
                "exclude_service": None,
                "include_service": None,
            },
            "status": 200,
            "status_check": True,
        }

    def get_invoice_status(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "data": {
                "status": "created",
                "error_message": None,
                "id": "01fc840d-a0b1-43ca-b65d-ca713d8a1f95",
                "shop_id": "4e48b574-48c4-4d35-a64d-6a0bb169d4fb",
                "amount": 300,
                "expire": "2022-11-07 13:46:37",
                "order_id": "6368c5ed3e7521.67590325",
                "fail_url": None,
                "success_url": None,
                "hook_url": None,
                "custom_fields": None,
                "include_service": None,
                "exclude_service": None,
            },
            "status": 200,
            "status_check": True,
        }

    def get_shop_balance(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "data": {"balance": 37500.08, "freeze_balance": 375000.08},
            "status": 200,
            "status_check": True,
        }

    def create_payoff(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "data": {
                "payoff_id": "cc3bcb98-5c10-4eeb-8aab-1da96e6575c2",
                "payoff_status": "created",
            },
            "status": 200,
            "status_check": True,
        }

    def get_payoff_status(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "data": {
                "id": "cc3bcb98-5c10-4eeb-8aab-1da96e6575c1",
                "orderId": "636915c4707440",
                "status": "success",
                "wallet": None,
                "service": "lava_payoff",
                "amountPay": 10,
                "commission": 0,
                "amountReceive": 10,
                "tryCount": 1,
                "errorMessage": None,
            },
            "status": 200,
            "status_check": True,
        }

    def create_h2h_invoice(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "data": {
                "url": "https://lava.ru/tds?t=f109ddc5-e65c-a3b4-6f7a-579ee7f8b452",
                "invoiceId": "681b780b-cb7e-430b-a503-b7aefb834399",
                "cardMask": "553691******8079",
                "amount": 100,
                "amountPay": 100,
                "commission": 5,
                "shopId": "some-shop-id",
            },
            "status": 200,
            "status_check": True,
        }

    def create_h2h_sbp(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "data": {
                "sbp_url": "https://pay.lava.ru/sbp/f78ea11f-cd8a-4752-b8b1-36bc312ff886",
                "fingerprint": False,
                "qr_code": "data:image/png;base64,abc123",
            },
            "status": 200,
            "status_check": True,
        }

    def check_wallet(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {"data": {"status": True}, "status": 200, "status_check": True}

    def get_payoff_tariffs(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "data": {
                "tariffs": [
                    {
                        "percent": 2.5,
                        "min_sum": 10.0,
                        "max_sum": 100000.0,
                        "service": "lava_payoff",
                        "fix": None,
                        "title": "Lava",
                        "currency": "RUB",
                    }
                ]
            },
            "status": 200,
            "status_check": True,
        }

    def get_availible_tariffs(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "data": [
                {
                    "percent": 10,
                    "user_percent": 5,
                    "shop_percent": 5,
                    "service_id": "1",
                    "service_name": "Банковская карта",
                    "status": 1,
                    "currency": "RUB",
                }
            ],
            "status": 200,
            "status_check": True,
        }

    def get_profile_balance(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "data": {
                "freeze_balance": 2000,
                "active_balance": 8000,
                "balance": 10000,
            },
            "status": 200,
            "status_check": True,
        }

    def get_payoff_course_list(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "data": [
                {"currency": {"symbol": "₽", "value": "RUB", "label": "Российский рубль"}, "value": 1.0},
                {"currency": {"symbol": "USDT", "value": "USDT", "label": "Tether USD"}, "value": float(random.randint(90, 120))},
                {"currency": {"symbol": "BTC", "value": "BTC", "label": "Bitcoin"}, "value": float(random.randint(40000, 120000))},
            ],
            "status": 200,
            "status_check": True,
        }

    def get_payment_course_list(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "data": [
                {"currency": {"symbol": "₽", "value": "RUB", "label": "Российский рубль"}, "value": 1.0},
                {"currency": {"symbol": "USDT", "value": "USDT", "label": "Tether USD"}, "value": float(random.randint(90, 120))},
                {"currency": {"symbol": "BTC", "value": "BTC", "label": "Bitcoin"}, "value": float(random.randint(40000, 120000))},
            ],
            "status": 200,
            "status_check": True,
        }
