import pendulum

import pytest
from unittest.mock import MagicMock

from date_range.daterange import DateRange
from date_range.generate_dates import generate_dates, generate_date_range_and_output, format_date


class TestGenerateDates:

    def setup(self):
        self.start_date = pendulum.datetime(2019, 1, 10)
        self.end_date = pendulum.datetime(2019, 1, 13)
        self.date_range = DateRange(self.start_date, self.end_date, None, 'asc')

    def test_generate_date_range_ascending(self):
        date_list = list(generate_dates(self.date_range))
        expected_date_list = [
            pendulum.datetime(2019, 1, 10),
            pendulum.datetime(2019, 1, 11),
            pendulum.datetime(2019, 1, 12),
            pendulum.datetime(2019, 1, 13)
        ]
        assert date_list == expected_date_list

    def test_generate_date_range_descending(self):
        self.date_range = DateRange(self.start_date, self.end_date, None, 'desc')
        date_list = list(generate_dates(self.date_range))
        expected_date_list = [
            pendulum.datetime(2019, 1, 13),
            pendulum.datetime(2019, 1, 12),
            pendulum.datetime(2019, 1, 11),
            pendulum.datetime(2019, 1, 10)
        ]
        assert date_list == expected_date_list

    def test_generate_date_range_same_date(self):
        self.date_range = DateRange(self.start_date, self.start_date, None, 'asc')
        date_list = list(generate_dates(self.date_range))
        expected_date_list = [
            pendulum.datetime(2019, 1, 10)
        ]
        assert date_list == expected_date_list

    def test_generate_date_range_invalid_date_range(self):
        self.date_range = DateRange(self.end_date, self.start_date, None, 'asc')
        with pytest.raises(ValueError, match='invalid date range start date is after end date.'):
            for date in generate_dates(self.date_range):
                print(date)


class TestDateRangeOutput:

    def setup(self):
        self.start_date = pendulum.datetime(2019, 1, 10)
        self.end_date = pendulum.datetime(2019, 1, 13)

        self.args = MagicMock()
        self.args.start_date = self.start_date
        self.args.end_date = self.end_date
        self.args.sort_order = 'asc'
        self.args.date_format = None
        self.args.increment = None

        self.date_range_mock = MagicMock()
        self.date_range_mock.get_min_param.return_value = 'days'
        self.format_date = pendulum.datetime(2020, 1, 1, 5, 32, 20)

    def test_print_to_screen(self, capsys):
        generate_date_range_and_output(self.args)
        printed_ouptut = capsys.readouterr().out
        expected_output = '2019-01-10 2019-01-11 2019-01-12 2019-01-13 '
        assert printed_ouptut == expected_output

    def test_format_date__custom_format(self):
        formatted_date = format_date(self.format_date, 'MM/DD/YYYY', self.date_range_mock)
        assert formatted_date == '01/01/2020'

    def test_format_date__print_date(self):
        formatted_date = format_date(self.format_date, None, self.date_range_mock)
        assert formatted_date == '2020-01-01'

    def test_format_date__print_hour_precision(self):
        self.date_range_mock.get_min_param.return_value = 'hours'
        formatted_date = format_date(self.format_date, None, self.date_range_mock)
        assert formatted_date == '2020-01-01 05:32:20'

    def test_format_date__default_format(self):
        self.date_range_mock.get_min_param.return_value = 'milliseconds'
        formatted_date = format_date(self.format_date, None, self.date_range_mock)
        assert formatted_date == '2020-01-01T05:32:20+00:00'
