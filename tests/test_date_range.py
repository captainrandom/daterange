import pendulum

import pytest
from unittest.mock import MagicMock

from daterange import generate_dates, generate_date_range_and_output, parse_args

start_date = pendulum.date(2019, 1, 10)
end_date = pendulum.date(2019, 1, 13)


def test_generate_date_range_ascending():
    date_list = list(generate_dates(start_date, end_date, 'asc'))
    expected_date_list = [
        pendulum.date(2019, 1, 10),
        pendulum.date(2019, 1, 11),
        pendulum.date(2019, 1, 12),
        pendulum.date(2019, 1, 13)
    ]
    assert date_list == expected_date_list


def test_generate_date_range_descending():
    date_list = list(generate_dates(start_date, end_date, 'desc'))
    expected_date_list = [
        pendulum.date(2019, 1, 13),
        pendulum.date(2019, 1, 12),
        pendulum.date(2019, 1, 11),
        pendulum.date(2019, 1, 10)
    ]
    assert date_list == expected_date_list


def test_generate_date_range_same_date():
    date_list = list(generate_dates(start_date, start_date, 'asc'))
    expected_date_list = [
        pendulum.date(2019, 1, 10)
    ]
    assert date_list == expected_date_list


def test_generate_date_range_invalid_date_range():
    with pytest.raises(ValueError, match='invalid date range start date is after end date.'):
        for date in generate_dates(end_date, start_date, 'asc'):
            print(date)


def test_print_to_screen(capsys):
    args = MagicMock()
    args.start_date = start_date
    args.end_date = end_date
    args.sort_order = 'asc'

    generate_date_range_and_output(args)
    printed_ouptut = capsys.readouterr().out
    expected_output = '2019-01-10 2019-01-11 2019-01-12 2019-01-13 '
    assert printed_ouptut == expected_output


def test_no_args():
    with pytest.raises(SystemExit):
        parse_args(args=[])


def test_start_end_date_only():
    args = parse_args(args=[
        '-s', '2019-01-10',
        '-e', '2019-01-13'
    ])
    assert args.start_date == start_date
    assert args.end_date == end_date
    assert args.sort_order == 'asc'


def test_start_end_date_invalid_date():
    with pytest.raises(SystemExit):
        parse_args(args=[
        '-s', '2019-01- 10 Tx',
        '-e', '2019-01- 11 tx'
    ])


def test_start_end_date_invalid_sort_order():
    with pytest.raises(SystemExit):
        parse_args(args=[
        '-s', '2019-01-10',
        '-e', '2019-01-11',
        '-o', 'other'
    ])


def test_start_end_date_with_sort_order():
    args = parse_args(args=[
        '-s', '2019-01-10',
        '-e', '2019-01-13',
        '-o', 'desc'
    ])
    assert args.start_date == start_date
    assert args.end_date == end_date
    assert args.sort_order == 'desc'