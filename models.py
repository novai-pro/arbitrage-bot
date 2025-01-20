from pydantic import BaseModel
from typing import List, Tuple, Dict
from datetime import datetime

class ExchangeInfo(BaseModel):
    fundingRate: str
    nextFundingTime: int

class ExchangeData(BaseModel):
    exchange_name: str
    info: ExchangeInfo

    @classmethod
    def from_list(cls, data: List):
        return cls(
            exchange_name=data[0],
            info=ExchangeInfo(**data[1])
        )

class CoinFundingData(BaseModel):
    coin_name: str
    exchanges: List[ExchangeData]

    @classmethod
    def from_list(cls, data: List):
        return cls(
            coin_name=data[0],
            exchanges=[ExchangeData.from_list(exchange_data) for exchange_data in data[1]]
        )

class FundingResponse(BaseModel):
    coins: List[CoinFundingData]

    @classmethod
    def from_raw_response(cls, data: List):
        return cls(
            coins=[CoinFundingData.from_list(coin_data) for coin_data in data]
        )