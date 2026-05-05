from typing import Any, Dict, List

from lava_sdk.dto.response.payoff.tariff_response_dto import TariffResponseDto


class TariffDto:
    def to_dto(self, response: Dict[str, Any]) -> List[TariffResponseDto]:
        tariffs = []
        for tariff in (response.get("data") or {}).get("tariffs", []):
            tariffs.append(
                TariffResponseDto(
                    percent=tariff.get("percent"),
                    max_sum=tariff.get("max_sum"),
                    service=tariff["service"],
                    fix=tariff.get("fix"),
                    title=tariff.get("title"),
                    currency=tariff["currency"],
                    min_sum=tariff.get("min_sum"),
                )
            )
        return tariffs
