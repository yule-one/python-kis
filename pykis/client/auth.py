import json
from dataclasses import asdict, dataclass
from os import PathLike

from pykis.client.account import KisAccountNumber
from pykis.client.appkey import KisKey

__all__ = [
    "KisAuth",
]


@dataclass
class KisAuth:
    """한국투자증권 OpenAPI 계좌 및 인증 정보"""

    id: str
    """HTS 아이디"""
    appkey: str
    """앱 키"""
    secretkey: str
    """앱 시크릿"""
    account: str
    """계좌번호"""
    virtual: bool = False
    """모의투자 여부"""

    @property
    def key(self):
        """앱 키"""
        return KisKey(
            id=self.id,
            appkey=self.appkey,
            secretkey=self.secretkey,
        )

    @property
    def account_number(self):
        """계좌번호"""
        return KisAccountNumber(self.account)

    def save(self, path: str | PathLike[str]):
        """계좌 및 인증 정보를 JSON 파일로 저장합니다."""
        with open(path, "w") as f:
            json.dump(asdict(self), f)

    @classmethod
    def load(cls, path: str | PathLike[str]) -> "KisAuth":
        """JSON 파일에서 계좌 및 인증 정보를 불러옵니다."""
        try:
            with open(path) as f:
                return cls(**json.load(f))
        except Exception as e:
            raise ValueError("계좌 및 인증 정보를 불러오는데 실패했습니다.") from e

    def __repr__(self):
        return f"<KisAuth account={self.account} virtual={self.virtual}>"
