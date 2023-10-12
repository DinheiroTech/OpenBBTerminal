from datetime import datetime

import pytest
from openbb_core.app.service.user_service import UserService
from openbb_tradingeconomics.models.economic_calendar import TEEarningsCalendarFetcher

test_credentials = UserService().default_user_settings.credentials.dict()


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_headers": [("User-Agent", None)],
        "filter_query_parameters": [
            ("api_key", "mock_api_key"),
        ],
    }


@pytest.mark.record_http
def test_te_earnings_calendar_fetcher(credentials=test_credentials):
    params = {
        "start_date": "2023-01-01",
        "end_date": "2023-10-10",
    }

    fetcher = TEEarningsCalendarFetcher()
    result = fetcher.test(params, credentials)
    assert result is None
