from typing import Any, Dict, List, Optional

from lava_sdk.dto.request.h2h.create_h2h_invoice_dto import CreateH2hInvoiceDto
from lava_sdk.dto.request.h2h.create_sbp_h2h_dto import CreateSBPH2HDto
from lava_sdk.dto.request.invoice.create_invoice_dto import CreateInvoiceDto
from lava_sdk.dto.request.invoice.get_status_invoice_dto import GetStatusInvoiceDto
from lava_sdk.dto.request.payoff.check_wallet_request_dto import CheckWalletRequestDto
from lava_sdk.dto.request.payoff.create_payoff_dto import CreatePayoffDto
from lava_sdk.dto.request.payoff.get_payoff_status_dto import GetPayoffStatusDto
from lava_sdk.dto.request.refund.create_refund_dto import CreateRefundDto
from lava_sdk.dto.request.refund.get_status_refund_dto import GetStatusRefundDto
from lava_sdk.dto.response.course.course_dto import CourseDto
from lava_sdk.dto.response.course.currency_dto import CurrencyDto
from lava_sdk.dto.response.h2h.created_h2h_invoice_dto import CreatedH2hInvoiceDto
from lava_sdk.dto.response.h2h.created_sbp_h2h_dto import CreatedSBPH2hDto
from lava_sdk.dto.response.invoice.available_tariff_dto import AvailableTariffDto
from lava_sdk.dto.response.invoice.created_invoice_dto import CreatedInvoiceDto
from lava_sdk.dto.response.invoice.status_invoice_dto import StatusInvoiceDto
from lava_sdk.dto.response.payoff.check_wallet_response_dto import CheckWalletResponseDto
from lava_sdk.dto.response.payoff.created_payoff_dto import CreatedPayoffDto
from lava_sdk.dto.response.payoff.status_payoff_dto import StatusPayoffDto
from lava_sdk.dto.response.payoff.tariff_response_dto import TariffResponseDto
from lava_sdk.dto.response.profile.profile_balance_dto import ProfileBalanceDto
from lava_sdk.dto.response.refund.created_refund_dto import CreatedRefundDto
from lava_sdk.dto.response.refund.status_refund_dto import StatusRefundDto
from lava_sdk.dto.response.shop.shop_balance_dto import ShopBalanceDto
from lava_sdk.dto.secret.profile_secret_dto import ProfileSecretDto
from lava_sdk.exceptions.course.course_exception import CourseException
from lava_sdk.http.client.client import Client
from lava_sdk.http.client.client_check_signature_webhook import ClientCheckSignatureWebhook
from lava_sdk.http.client.client_generate_signature import ClientGenerateSignature
from lava_sdk.http.h2h.create_h2h_invoice import CreateH2hInvoice
from lava_sdk.http.h2h.create_h2h_sbp import CreateH2HSbp
from lava_sdk.http.invoices.create_invoice import CreateInvoice
from lava_sdk.http.invoices.get_available_tariffs_dto import GetAvailableTariffsDto
from lava_sdk.http.invoices.get_status_invoice import GetStatusInvoice
from lava_sdk.http.payoffs.check_wallet_dto import CheckWalletDto
from lava_sdk.http.payoffs.create_payoff import CreatePayoff
from lava_sdk.http.payoffs.get_status_payoff import GetStatusPayoff
from lava_sdk.http.payoffs.tariff_dto import TariffDto
from lava_sdk.http.profile.get_profile_balance import GetProfileBalance
from lava_sdk.http.refund.create_refund import CreateRefund
from lava_sdk.http.refund.get_refund_status import GetRefundStatus
from lava_sdk.http.shop.get_shop_balance import GetShopBalance


class LavaFacade:
    """
    Main facade for the Lava Payment API.

    Provides all API operations: invoices, payoffs, refunds, H2H payments,
    webhook verification, balance queries and currency exchange rates.
    """

    def __init__(
        self,
        secret_key: str,
        shop_id: str,
        additional_key: Optional[str] = None,
        client: Optional[Client] = None,
        client_generate_sign: Optional[ClientGenerateSignature] = None,
        client_check_webhook: Optional[ClientCheckSignatureWebhook] = None,
        profile_secret_data: Optional[ProfileSecretDto] = None,
    ):
        self._shop_id = shop_id
        self._client = client if client is not None else Client()
        self._client_generate_sign = (
            client_generate_sign
            if client_generate_sign is not None
            else ClientGenerateSignature(secret_key)
        )
        self._client_check_webhook = (
            client_check_webhook
            if client_check_webhook is not None
            else ClientCheckSignatureWebhook(additional_key)
        )
        self._profile_secret_data = profile_secret_data

    # ── helpers ────────────────────────────────────────────────────────────

    @staticmethod
    def _clear_data(request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Remove None values from the request dict (mirrors PHP clearData)."""
        return {k: v for k, v in request_data.items() if v is not None}

    def _set_signature(self, request_data: Dict[str, Any], secret_key: str) -> Dict[str, Any]:
        """Remove None values, then generate and inject the signature."""
        request_data = self._clear_data(request_data)
        signer = ClientGenerateSignature(secret_key)
        request_data["signature"] = signer.generate_signature(request_data)
        return request_data

    def _require_profile_secret(self) -> ProfileSecretDto:
        if self._profile_secret_data is None:
            raise ValueError("Profile Secret Data is None")
        return self._profile_secret_data

    # ── Invoice operations ─────────────────────────────────────────────────

    def create_invoice(self, invoice: CreateInvoiceDto) -> CreatedInvoiceDto:
        """Create a payment invoice."""
        handler = CreateInvoice()
        request_data = handler.to_array(invoice, self._shop_id)
        request_data = self._clear_data(request_data)
        request_data["signature"] = self._client_generate_sign.generate_signature(request_data)
        return handler.to_dto(self._client.create_invoice(request_data))

    def check_status_invoice(self, status_invoice: GetStatusInvoiceDto) -> StatusInvoiceDto:
        """Check the status of an invoice."""
        handler = GetStatusInvoice()
        request_data = handler.to_array(status_invoice, self._shop_id)
        request_data = self._clear_data(request_data)
        request_data["signature"] = self._client_generate_sign.generate_signature(request_data)
        return handler.to_dto(self._client.get_invoice_status(request_data))

    def get_availible_tariffs(self) -> List[AvailableTariffDto]:
        """Get available invoice tariffs for the shop."""
        request_data: Dict[str, Any] = {"shopId": self._shop_id}
        request_data["signature"] = self._client_generate_sign.generate_signature(request_data)
        return GetAvailableTariffsDto().to_dto(self._client.get_availible_tariffs(request_data))

    # ── Refund operations ──────────────────────────────────────────────────

    def create_refund(self, refund_dto: CreateRefundDto) -> CreatedRefundDto:
        """Create a refund for an invoice."""
        handler = CreateRefund()
        request_data = handler.to_array(refund_dto, self._shop_id)
        request_data = self._clear_data(request_data)
        request_data["signature"] = self._client_generate_sign.generate_signature(request_data)
        return handler.to_dto(self._client.create_refund(request_data))

    def check_status_refund(self, refund_dto: GetStatusRefundDto) -> StatusRefundDto:
        """Check the status of a refund."""
        handler = GetRefundStatus()
        request_data = handler.to_array(refund_dto, self._shop_id)
        request_data = self._clear_data(request_data)
        request_data["signature"] = self._client_generate_sign.generate_signature(request_data)
        return handler.response_to_dto(self._client.get_refund_status(request_data))

    # ── Shop balance (deprecated) ──────────────────────────────────────────

    def get_shop_balance(self) -> ShopBalanceDto:
        """Get the shop balance. Deprecated: use get_profile_balance() instead."""
        handler = GetShopBalance()
        request_data = handler.to_array(self._shop_id)
        request_data = self._clear_data(request_data)
        request_data["signature"] = self._client_generate_sign.generate_signature(request_data)
        return handler.to_dto(self._client.get_shop_balance(request_data))

    # ── H2H operations ─────────────────────────────────────────────────────

    def create_h2h_invoice(self, h2h_invoice_dto: CreateH2hInvoiceDto) -> CreatedH2hInvoiceDto:
        """Create a host-to-host card payment invoice."""
        handler = CreateH2hInvoice()
        request_data = handler.to_array(h2h_invoice_dto, self._shop_id)
        request_data = self._clear_data(request_data)
        request_data["signature"] = self._client_generate_sign.generate_signature(request_data)
        return handler.to_dto(self._client.create_h2h_invoice(request_data))

    def create_h2h_spb_invoice(self, h2h_invoice_dto: CreateSBPH2HDto) -> CreatedSBPH2hDto:
        """Create a host-to-host SBP (Faster Payments System) invoice."""
        handler = CreateH2HSbp()
        request_data = handler.to_array(h2h_invoice_dto, self._shop_id)
        request_data = self._clear_data(request_data)
        request_data["signature"] = self._client_generate_sign.generate_signature(request_data)
        return handler.to_dto(self._client.create_h2h_sbp(request_data))

    # ── Payoff operations (require ProfileSecretDto) ───────────────────────

    def create_payoff(self, payoff: CreatePayoffDto) -> CreatedPayoffDto:
        """Create a payoff (payout)."""
        profile = self._require_profile_secret()
        handler = CreatePayoff()
        request_data = self._set_signature(handler.to_array(payoff, profile.get_profile_id()),
                                           profile.get_secret_key())
        return handler.to_dto(self._client.create_payoff(request_data))

    def get_status_payoff(self, payoff_status: GetPayoffStatusDto) -> StatusPayoffDto:
        """Get the status of a payoff."""
        profile = self._require_profile_secret()
        handler = GetStatusPayoff()
        request_data = self._set_signature(handler.to_array(payoff_status, profile.get_profile_id()),
                                           profile.get_secret_key())
        return handler.to_dto(self._client.get_payoff_status(request_data))

    def get_payoff_tariffs(self) -> List[TariffResponseDto]:
        """Get available payoff tariffs."""
        profile = self._require_profile_secret()
        request_data: Dict[str, Any] = {"profileId": profile.get_profile_id()}
        request_data = self._set_signature(request_data, profile.get_secret_key())
        return TariffDto().to_dto(self._client.get_payoff_tariffs(request_data))

    def check_wallet(self, check_wallet: CheckWalletRequestDto) -> CheckWalletResponseDto:
        """Check if a wallet/account is valid for payoff."""
        profile = self._require_profile_secret()
        handler = CheckWalletDto()
        request_data = self._set_signature(handler.to_array(check_wallet, profile.get_profile_id()),
                                           profile.get_secret_key())
        return handler.to_dto(self._client.check_wallet(request_data))

    # ── Profile balance ────────────────────────────────────────────────────

    def get_profile_balance(self) -> ProfileBalanceDto:
        """Get the profile balance."""
        profile = self._require_profile_secret()
        handler = GetProfileBalance()
        request_data = self._set_signature(handler.to_array(profile.get_profile_id()),
                                           profile.get_secret_key())
        return handler.to_dto(self._client.get_profile_balance(request_data))

    # ── Course (exchange rate) operations ──────────────────────────────────

    def get_payment_course_list(self) -> List[CourseDto]:
        """Get the list of payment currency exchange rates."""
        request_data: Dict[str, Any] = {"shopId": self._shop_id}
        request_data["signature"] = self._client_generate_sign.generate_signature(request_data)
        result = self._client.get_payment_course_list(request_data)
        if not isinstance(result.get("data"), list):
            raise CourseException("Invalid response data")
        return [self._parse_course(v) for v in result["data"]]

    def get_payoff_course_list(self) -> List[CourseDto]:
        """Get the list of payoff currency exchange rates."""
        request_data: Dict[str, Any] = {"shopId": self._shop_id}
        request_data["signature"] = self._client_generate_sign.generate_signature(request_data)
        result = self._client.get_payoff_course_list(request_data)
        if not isinstance(result.get("data"), list):
            raise CourseException("Invalid response data")
        return [self._parse_course(v) for v in result["data"]]

    # ── Webhook signature verification ────────────────────────────────────

    def check_sign_webhook(self, webhook_response: str, signature: str) -> bool:
        """Verify an incoming invoice webhook signature."""
        return self._client_check_webhook.check_sign_webhook(webhook_response, signature)

    def check_payoff_signature(self, webhook_response: str, signature: str) -> bool:
        """Verify an incoming payoff webhook signature."""
        profile = self._require_profile_secret()
        if profile.get_additional_key() is None:
            raise ValueError("Payoff Additional Key is None")
        return ClientCheckSignatureWebhook(profile.get_additional_key()).check_sign_webhook(
            webhook_response, signature
        )

    # ── Private helpers ────────────────────────────────────────────────────

    @staticmethod
    def _parse_course(value: Dict[str, Any]) -> CourseDto:
        for key, fields in {"currency": ["label", "symbol", "value"], "value": []}.items():
            if key not in value:
                raise ValueError(f"Field '{key}' is required.")
            for field in fields:
                if field not in value[key]:
                    raise ValueError(f"Field '{key}.{field}' is required.")
        currency = CurrencyDto(
            label=value["currency"]["label"],
            symbol=value["currency"]["symbol"],
            value=value["currency"]["value"],
        )
        return CourseDto(currency=currency, value=value["value"])
