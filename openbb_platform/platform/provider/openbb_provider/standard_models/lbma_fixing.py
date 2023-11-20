"""LBMA Fixing Standard Model."""

from datetime import (
    date as dateType,
    datetime,
)
from typing import Optional

from pydantic import Field, field_validator

from openbb_provider.abstract.data import Data
from openbb_provider.abstract.query_params import QueryParams
from openbb_provider.utils.descriptions import DATA_DESCRIPTIONS, QUERY_DESCRIPTIONS


class LbmaFixingQueryParams(QueryParams):
    """
    LBMA Fixing Query Params.

    Source: https://www.lbma.org.uk/prices-and-data/precious-metal-prices#/table
    """

    asset: str = Field(
        description="The metal to get price fixing rates for.",
        default="gold",
    )
    start_date: Optional[dateType] = Field(
        default=None,
        description=QUERY_DESCRIPTIONS.get("start_date", ""),
    )
    end_date: Optional[dateType] = Field(
        default=None,
        description=QUERY_DESCRIPTIONS.get("end_date", ""),
    )


class LbmaFixingData(Data):
    """
    LBMA Fixing Data.  Historical fixing prices in USD, GBP and EUR.
    """

    date: dateType = Field(description=DATA_DESCRIPTIONS.get("date", ""))
    usd_am: Optional[float] = Field(
        default=None,
        description="AM fixing price in USD.",
    )
    usd_pm: Optional[float] = Field(
        default=None,
        description="PM fixing price in USD.",
    )
    gbp_am: Optional[float] = Field(
        default=None,
        description="AM fixing price in GBP.",
    )
    gbp_pm: Optional[float] = Field(
        default=None,
        description="PM fixing price in GBP.",
    )
    euro_am: Optional[float] = Field(
        default=None,
        description="AM fixing price in EUR.",
    )
    euro_pm: Optional[float] = Field(
        default=None,
        description="PM fixing price in EUR.",
    )
    usd: Optional[float] = Field(
        default=None,
        description="Daily fixing price in USD.",
    )
    gbp: Optional[float] = Field(
        default=None,
        description="Daily fixing price in GBP.",
    )
    eur: Optional[float] = Field(
        default=None,
        description="Daily fixing price in EUR.",
    )

    @field_validator("date", mode="before", check_fields=False)
    def validate_date(cls, v) -> dateType:
        """Validate date."""
        if isinstance(v, datetime):
            return v.date()
        return datetime.strptime(v, "%Y-%m-%d").date()
