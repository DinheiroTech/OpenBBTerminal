"""Polygon types helpers."""


from datetime import date, datetime, timedelta
from enum import Enum
from typing import Literal, Optional, Union

from openbb_provider.abstract.data import Data
from openbb_provider.abstract.query_params import QueryParams
from openbb_provider.models.income_statement import IncomeStatementQueryParams
from pydantic import Field, NonNegativeInt, PositiveFloat, PositiveInt, validator


class Timespan(str, Enum):
    minute = "minute"
    hour = "hour"
    day = "day"
    week = "week"
    month = "month"
    quarter = "quarter"
    year = "year"


class PolygonFundamentalQueryParams(IncomeStatementQueryParams):
    """Polygon Fundamental QueryParams.

    Source: https://polygon.io/docs/stocks#!/get_vx_reference_financials
    """

    class Config:
        fields = {
            "symbol": "ticker",
            "period": "timeframe",
        }

    limit: Optional[NonNegativeInt] = Field(
        default=1, description="The limit of the income statement."
    )

    company_name: Optional[str] = Field(description="The name of the company.")
    company_name_search: Optional[str] = Field(
        description="The name of the company to search."
    )
    sic: Optional[str] = Field(
        description="The Standard Industrial Classification (SIC) of the company."
    )
    filing_date: Optional[date] = Field(
        description="The filing date of the financial statement."
    )
    filing_date_lt: Optional[date] = Field(
        description="The filing date less than the given date."
    )
    filing_date_lte: Optional[date] = Field(
        description="The filing date less than or equal to the given date.",
    )
    filing_date_gt: Optional[date] = Field(
        description="The filing date greater than the given date.",
    )
    filing_date_gte: Optional[date] = Field(
        description="The filing date greater than or equal to the given date.",
    )
    period_of_report_date: Optional[date] = Field(
        description="The period of report date of the financial statement."
    )
    period_of_report_date_lt: Optional[date] = Field(
        description="The period of report date less than the given date.",
    )
    period_of_report_date_lte: Optional[date] = Field(
        description="The period of report date less than or equal to the given date.",
    )
    period_of_report_date_gt: Optional[date] = Field(
        description="The period of report date greater than the given date.",
    )
    period_of_report_date_gte: Optional[date] = Field(
        description="The period of report date greater than or equal to the given date.",
    )
    include_sources: Optional[bool] = Field(
        description="Whether to include the sources of the financial statement."
    )
    order: Optional[Literal["asc", "desc"]] = Field(
        description="The order of the financial statement."
    )
    sort: Optional[Literal["filing_date", "period_of_report_date"]] = Field(
        description="The sort of the financial statement."
    )


class BaseStockQueryParams(QueryParams):
    stocksTicker: str = Field(alias="symbol")
    start_date: Union[date, datetime] = Field(
        default=datetime.now().date() - timedelta(days=8)
    )
    end_date: Union[date, datetime] = Field(
        default=datetime.now().date() - timedelta(days=1)
    )
    timespan: Timespan = Field(default=Timespan.day)
    sort: Literal["asc", "desc"] = Field(default="desc")
    limit: PositiveInt = Field(default=49999)
    adjusted: bool = Field(default=True)
    multiplier: PositiveInt = Field(default=1)


class BaseStockData(Data):
    c: PositiveFloat = Field(alias="close")
    o: PositiveFloat = Field(alias="open")
    h: PositiveFloat = Field(alias="high")
    l: PositiveFloat = Field(alias="low")  # noqa: E741
    t: datetime = Field(alias="date")

    @validator("t", pre=True)
    def time_validate(cls, v):  # pylint: disable=E0213
        return datetime.fromtimestamp(v / 1000)
