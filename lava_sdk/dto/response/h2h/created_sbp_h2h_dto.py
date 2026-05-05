class CreatedSBPH2hDto:
    """Response DTO for a created SBP H2H invoice."""

    def __init__(self, sbp_url: str, fingerprint: bool, qr_code: str):
        self.sbp_url = sbp_url
        self._fingerprint = fingerprint
        self._qr_code = qr_code

    def is_fingerprint(self) -> bool: return self._fingerprint
    def get_qr_code(self) -> str: return self._qr_code
    def get_sbp_url(self) -> str: return self.sbp_url
