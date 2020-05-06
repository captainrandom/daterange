import pendulum


class DateRange:

    def __init__(
            self,
            start_date: pendulum.DateTime,
            end_date: pendulum.DateTime,
            increment: str,
            sort_order: str,
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.increment_duration: pendulum.Duration = self._parse_increment(increment, sort_order, start_date, end_date)
        self.sort_order = sort_order

    def get_min_param(self):
        pass

    def _parse_increment(self, increment: str, sort_order: str, start_date, end_date) -> pendulum.Duration:
        """
        :param increment: possible values (30dh, 2d3h, 2d, 2h, h ...)
        :param sort_order: ascending or descending
        :return:
        """
        order = 1 if sort_order == 'asc' else -1
        return order * pendulum.Duration(**self._compute_incremnt_times(increment, start_date, end_date))

    def _compute_incremnt_times(self, increment: str, start_date: pendulum.DateTime, end_date: pendulum.DateTime):
        if increment is None or increment == '':
            if start_date.second > 0 or end_date.second > 0:
                return {'seconds': 1}
            elif start_date.hour > 0 or end_date.hour > 0:
                return {'hours': 1}
            else:
                return {'days': 1}
        else:
            return self._parse_increment_times(increment)

    @staticmethod
    def _parse_increment_times(increment: str):
        # TODO: need to enforce the cfg a little bit more strictly here!! ex: 30 is not acceptable
        numberStr = ''
        full_name_by_char = {
            's': 'seconds',
            'h': 'hours',
            'd': 'days',
            'y': 'years'
        }
        times = {}
        for char in increment:
            if char.isdigit():
                numberStr += char
            if not char.isdigit():
                if char not in full_name_by_char:
                    raise ValueError(f'{char} is not a supported increment only: {full_name_by_char}')

                number = int(numberStr) if numberStr else 1
                times[full_name_by_char[char]] = number
                numberStr = ''
        if numberStr:
            raise ValueError(
                f'{increment} cannot have a leading number without date type designation. (ex: 30 bad but 30d good or 2d3 bad but 2d3h woudl work)')
        return times


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
    if date_range.sort_order == 'asc':
        # increment_days = 1
        current_dt = date_range.start_date
    else:
        # increment_days = -1
        current_dt = date_range.end_date
    return current_dt  # , increment_days


def format_date(date: pendulum.DateTime, format: str, date_range: DateRange):
    if format:
        return date.format(format)  # TODO: rename format
    if date_range.get_min_param() == 'days':
        return date.date()
    elif date_range.get_min_param() == 'hours':  # TODO: this needs to become an enum with a short form as well
        return date.format('YYYY-MM-DD HH:MM')
    else:
        return date


def generate_date_range_and_output(args):
    date_range = DateRange(args.start_date, args.end_date, args.increment, args.sort_order)
    for date in generate_dates(date_range):
        print(format_date(date), end=' ')
