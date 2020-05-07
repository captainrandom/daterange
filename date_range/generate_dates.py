import pendulum

from date_range.daterange import DateRange


def generate_dates(date_range: DateRange):
    """
    This should be an inclusive date range
    """
    if date_range.start_date > date_range.end_date:
        raise ValueError('invalid date range start date is after end date.')

    current_dt = find_current_date(date_range)
    while date_range.start_date <= current_dt <= date_range.end_date:
        yield current_dt
        current_dt = current_dt + date_range.increment_duration


def find_current_date(date_range: DateRange):
    return date_range.start_date if date_range.sort_order == 'asc' else date_range.end_date


def format_date(date: pendulum.DateTime, format: str, date_range: DateRange):
    if format:
        return date.format(format)  # TODO: rename format
    if date_range.get_min_param() in ('days', 'months', 'years'):
        return date.date().isoformat()
    elif date_range.get_min_param() in ('hours', 'seconds'):  # TODO: this needs to become an enum with a short form as well
        return date.format('YYYY-MM-DD HH:mm:ss')
    else:
        return date.isoformat()


def generate_date_range_and_output(args):
    date_range = DateRange(args.start_date, args.end_date, args.increment, args.sort_order)
    for date in generate_dates(date_range):
        print(format_date(date, args.date_format, date_range), end=' ')
