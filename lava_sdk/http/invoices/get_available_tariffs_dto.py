from typing import Any, Dict, List

from lava_sdk.dto.response.invoice.available_tariff_dto import AvailableTariffDto


class GetAvailableTariffsDto:
    def to_dto(self, response_data: Dict[str, Any]) -> List[AvailableTariffDto]:
        tariffs = []
        for tariff in response_data.get("data", []):
            tariffs.append(
                AvailableTariffDto(
                    status=tariff["status"],
                    percent=tariff["percent"],
                    user_percent=tariff["user_percent"],
                    shop_percent=tariff["shop_percent"],
                    service_name=tariff["service_name"],
                    service_id=tariff["service_id"],
                    currency=tariff["currency"],
                )
            )
        return tariffs
