#!/bin/bash/python

import argparse

import pendulum

def parse_args(args=None):
    date_parser = lambda dt: pendulum.parse(dt).date()
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start-date', required=True, type=date_parser)
    parser.add_argument('-e', '--end-date', required=True, type=date_parser)
    parser.add_argument('-o', '--sort-order', choices=['asc', 'desc'], default='asc')
    return parser.parse_args(args=args)


def generate_dates(start_date, end_date, sort_order):
    """
    This should be an inclusive date range
    """
    if start_date > end_date:
        raise ValueError('invalid date range start date is after end date.')

    current_dt, increment_days = find_current_date_and_direction(end_date, sort_order, start_date)
    while start_date <= current_dt <= end_date:
        yield current_dt
        current_dt = current_dt.add(days=increment_days)


def find_current_date_and_direction(end_date, sort_order, start_date):
    if sort_order == 'asc':
        increment_days = 1
        current_dt = start_date
    else:
        increment_days = -1
        current_dt = end_date
    return current_dt, increment_days


def generate_date_range_and_output(args):
    for date in generate_dates(args.start_date, args.end_date, args.sort_order):
        print(date, end=' ')


if __name__ == '__main__':
    args = parse_args()
    generate_date_range_and_output(args)
