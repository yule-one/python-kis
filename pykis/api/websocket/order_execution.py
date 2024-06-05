from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Protocol
from zoneinfo import ZoneInfo

from pykis.__env__ import TIMEZONE
from pykis.api.account.order import (
    ORDER_CONDITION,
    ORDER_EXECUTION,
    ORDER_TYPE,
    KisOrder,
    KisOrderNumber,
    resolve_domestic_order_condition,
)
from pykis.api.base.account_product import KisAccountProductBase
from pykis.client.account import KisAccountNumber
from pykis.responses.types import KisAny, KisDecimal, KisString, KisTimeToDatetime
from pykis.responses.websocket import KisWebsocketResponse, KisWebsocketResponseProtocol
from pykis.utils.repr import kis_repr
from pykis.utils.typing import Checkable

if TYPE_CHECKING:
    from pykis.api.stock.market import MARKET_TYPE


class KisRealtimeOrderExecution(KisWebsocketResponseProtocol, Protocol):
    """한국투자증권 실시간 체결"""

    @property
    def time(self) -> datetime:
        """주문시각"""
        raise NotImplementedError

    @property
    def time_kst(self) -> datetime:
        """주문시각(KST)"""
        raise NotImplementedError

    @property
    def timezone(self) -> ZoneInfo:
        """시간대"""
        raise NotImplementedError

    @property
    def order_number(self) -> KisOrderNumber:
        """주문번호"""
        raise NotImplementedError

    @property
    def type(self) -> ORDER_TYPE:
        """주문유형"""
        raise NotImplementedError

    @property
    def price(self) -> Decimal:
        """체결단가"""
        raise NotImplementedError

    @property
    def unit_price(self) -> Decimal | None:
        """주문단가"""
        raise NotImplementedError

    @property
    def order_price(self) -> Decimal | None:
        """주문단가"""
        raise NotImplementedError

    @property
    def quantity(self) -> Decimal:
        """주문수량"""
        raise NotImplementedError

    @property
    def qty(self) -> Decimal:
        """주문수량"""
        raise NotImplementedError

    @property
    def executed_quantity(self) -> Decimal:
        """체결수량"""
        raise NotImplementedError

    @property
    def executed_qty(self) -> Decimal:
        """체결수량"""
        raise NotImplementedError

    @property
    def executed_amount(self) -> Decimal:
        """체결금액"""
        raise NotImplementedError

    @property
    def condition(self) -> ORDER_CONDITION | None:
        """주문조건"""
        raise NotImplementedError

    @property
    def execution(self) -> ORDER_EXECUTION | None:
        """체결조건"""
        raise NotImplementedError

    @property
    def receipt(self) -> bool:
        """접수여부"""
        raise NotImplementedError

    @property
    def canceled(self) -> bool:
        """취소여부 (IOC/FOK)"""
        raise NotImplementedError

    @property
    def rejected(self) -> bool:
        """거부여부"""
        raise NotImplementedError

    @property
    def rejected_reason(self) -> str | None:
        """거부사유"""
        raise NotImplementedError


@kis_repr(
    "account_number",
    "market",
    "symbol",
    "time",
    "type",
    "price",
    "executed_qty",
    lines="single",
)
class KisRealtimeOrderExecutionRepr:
    """한국투자증권 실시간 체결"""


class KisRealtimeOrderExecutionBase(
    KisRealtimeOrderExecutionRepr, KisWebsocketResponse, KisAccountProductBase
):
    """한국투자증권 실시간 체결"""

    symbol: str
    """종목코드"""
    market: "MARKET_TYPE"
    """상품유형타입"""

    account_number: KisAccountNumber
    """계좌번호"""

    time: datetime
    """체결시각"""
    time_kst: datetime
    """체결시각(KST)"""
    timezone: ZoneInfo
    """시간대"""

    order_number: KisOrderNumber
    """주문번호"""

    type: ORDER_TYPE
    """주문유형"""

    price: Decimal
    """체결단가"""
    unit_price: Decimal | None
    """주문단가"""

    @property
    def order_price(self) -> Decimal | None:
        """주문단가"""
        return self.unit_price

    quantity: Decimal
    """주문수량"""

    @property
    def qty(self) -> Decimal:
        """주문수량"""
        return self.quantity

    executed_quantity: Decimal
    """체결수량"""

    @property
    def executed_qty(self) -> Decimal:
        """체결수량"""
        return self.executed_quantity

    executed_amount: Decimal
    """체결금액"""

    condition: ORDER_CONDITION | None
    """주문조건"""
    execution: ORDER_EXECUTION | None
    """체결조건"""

    receipt: bool
    """접수여부"""

    canceled: bool
    """취소여부 (IOC/FOK)"""
    rejected: bool
    """거부여부"""
    rejected_reason: str | None
    """거부사유"""


class KisDomesticRealtimeOrderExecution(KisRealtimeOrderExecutionBase):
    """한국투자증권 국내주식 실시간 체결"""

    __fields__ = [
        None,  # 0 CUST_ID 고객 ID
        KisAny(lambda x: KisAccountNumber(x))["account_number"],  # 1 ACNT_NO 계좌번호
        None,  # 2 ODER_NO 주문번호
        None,  # 3 OODER_NO 원주문번호
        KisAny(lambda x: "sell" if x == "01" else "buy")[
            "type"
        ],  # 4 SELN_BYOV_CLS 매도매수구분 01 : 매도 02 : 매수
        None,  # 5 RCTF_CLS 정정구분
        None,  # 6 ODER_KIND 주문종류 00 : 지정가 01 : 시장가 02 : 조건부지정가 03 : 최유리지정가 04 : 최우선지정가 05 : 장전 시간외 06 : 장후 시간외 07 : 시간외 단일가 08 : 자기주식 09 : 자기주식S-Option 10 : 자기주식금전신탁 11 : IOC지정가 (즉시체결,잔량취소) 12 : FOK지정가 (즉시체결,전량취소) 13 : IOC시장가 (즉시체결,잔량취소) 14 : FOK시장가 (즉시체결,전량취소) 15 : IOC최유리 (즉시체결,잔량취소) 16 : FOK최유리 (즉시체결,전량취소)
        None,  # 7 ODER_COND 주문조건
        KisString["symbol"],  # 8 STCK_SHRN_ISCD 주식 단축 종목코드
        KisDecimal["executed_quantity"],  # 9 CNTG_QTY 체결 수량
        KisDecimal["price"],  # 10 CNTG_UNPR 체결단가
        KisTimeToDatetime("%H%M%S", timezone=TIMEZONE)["time"],  # 11 STCK_CNTG_HOUR 주식 체결 시간
        KisAny(lambda x: x == "1")["rejected"],  # 12 RFUS_YN 거부여부 0 : 승인 1 : 거부
        None,  # 13 CNTG_YN 체결여부 1 : 주문,정정,취소,거부 2 : 체결 (★ 체결만 보실경우 2번만 보시면 됩니다)
        None,  # 14 ACPT_YN 접수여부 1 : 주문접수 2 : 확인 3: 취소(FOK/IOC)
        None,  # 15 BRNC_NO 지점번호
        KisDecimal["quantity"],  # 16 ODER_QTY 주문수량
        None,  # 17 ACNT_NAME 계좌명
        None,  # 18 CNTG_ISNM 체결종목명
        None,  # 19 CRDT_CLS 신용구분
        None,  # 20 CRDT_LOAN_DATE 신용대출일자
        None,  # 21 CNTG_ISNM40 체결종목명40
        KisDecimal["unit_price"],  # 22 ODER_PRC 주문가격
    ]

    symbol: str  # 8 STCK_SHRN_ISCD 주식 단축 종목코드
    """종목코드"""
    market: "MARKET_TYPE" = "KRX"
    """상품유형타입"""

    account_number: KisAccountNumber  # 1 ACNT_NO 계좌번호
    """계좌번호"""

    time: datetime  # 11 STCK_CNTG_HOUR 주식 체결 시간
    """체결시각"""
    time_kst: datetime  # 11 STCK_CNTG_HOUR 주식 체결 시간
    """체결시각(KST)"""
    timezone: ZoneInfo = TIMEZONE
    """시간대"""

    order_number: KisOrderNumber  # 2 ODER_NO 주문번호, 15 BRNC_NO 지점번호
    """주문번호"""

    type: ORDER_TYPE  # 4 SELN_BYOV_CLS 매도매수구분
    """주문유형"""

    price: Decimal  # 10 CNTG_UNPR 체결단가
    """체결단가"""
    unit_price: Decimal | None  # 22 ODER_PRC 주문가격
    """주문단가"""

    quantity: Decimal  # 16 ODER_QTY 주문수량
    """주문수량"""

    executed_quantity: Decimal  # 9 CNTG_QTY 체결 수량
    """체결수량"""

    @property
    def executed_amount(self) -> Decimal:
        """체결수량"""
        return self.executed_quantity * (self.price or 0)

    condition: ORDER_CONDITION | None  # 6 ODER_KIND 주문종류
    """주문조건"""
    execution: ORDER_EXECUTION | None  # 6 ODER_KIND 주문종류
    """체결조건"""

    receipt: bool  # 14 ACPT_YN 접수여부
    """접수여부"""
    canceled: bool  # 14 ACPT_YN 접수여부
    """취소여부 (IOC/FOK)"""
    rejected: bool  # 12 RFUS_YN 거부여부
    """거부여부"""
    rejected_reason: str | None = None
    """거부사유"""

    _has_price: bool = True
    """주문단가 유무"""

    def __pre_init__(self, data: list[str]):
        super().__pre_init__(data)
        self._has_price, self.condition, self.execution = resolve_domestic_order_condition(data[6])

        self.canceled = data[14] == "3"
        self.receipt = data[14] == "1"

    def __post_init__(self):
        super().__post_init__()
        self.time_kst = self.time.astimezone(TIMEZONE)

        if not self._has_price:
            self.unit_price = None

        if self.receipt:
            self.quantity = self.executed_quantity
            self.executed_quantity = Decimal(0)

    def __kis_post_init__(self):
        super().__kis_post_init__()

        self.order_number = KisOrder.from_order(
            kis=self.kis,
            symbol=self.symbol,
            market=self.market,
            account_number=self.account_number,
            branch=self.__data__[15],  # 지점번호
            number=self.__data__[2],  # 주문번호
            time_kst=self.time_kst,
        )


# IDE Type Checker
if TYPE_CHECKING:
    Checkable[KisRealtimeOrderExecution](KisDomesticRealtimeOrderExecution)
