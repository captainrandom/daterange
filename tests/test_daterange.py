import pendulum
import pytest

from date_range.daterange_cli import parse_args


class TestParseArgs:

    def setup(self):
        self.start_date = pendulum.datetime(2019, 1, 10)
        self.end_date = pendulum.datetime(2019, 1, 13)
        self.args_list = [
            '-s', '2019-01-10',
            '-e', '2019-01-13',
            '-i', '2d2h'
        ]

    def test_no_args(self):
        with pytest.raises(SystemExit):
            parse_args(args=[])

    def test_start_end_date_only(self):
        args = parse_args(args=self.args_list)
        assert args.start_date == self.start_date
        assert args.end_date == self.end_date
        assert args.sort_order == 'asc'
        assert args.increment == '2d2h'

    def test_start_end_date_invalid_date(self):
        with pytest.raises(SystemExit):
            parse_args(args=[
                '-s', '2019-01- 10 Tx',
                '-e', '2019-01- 11 tx'
            ])

    def test_start_end_date_invalid_sort_order(self):
        with pytest.raises(SystemExit):
            parse_args(args=[
                '-s', '2019-01-10',
                '-e', '2019-01-11',
                '-o', 'other'
            ])

    def test_start_end_date_with_sort_order(self):
        args = parse_args(args=[
            '-s', '2019-01-10',
            '-e', '2019-01-13',
            '-o', 'desc'
        ])
        assert args.start_date == self.start_date
        assert args.end_date == self.end_date
        assert args.sort_order == 'desc'
        assert args.increment is None
