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
        specific_part_start_dt = self._most_specific_part(self.start_date)
        specific_part_end_dt = self._most_specific_part(self.end_date)
        if specific_part_start_dt[1] < specific_part_end_dt[1]:
            return specific_part_start_dt[0]
        else:
            return specific_part_end_dt[0]

    @staticmethod
    def _most_specific_part(dt: pendulum.DateTime):
        if dt.microsecond != 0:
            return 'microseconds', 0
        elif dt.second != 0:
            return 'seconds', 1
        elif dt.minute != 0:
            return 'minutes', 1
        elif dt.hour != 0:
            return 'hours', 1
        elif dt.day != 0:
            return 'days', 1
        elif dt.month != 0:
            return 'months', 1
        elif dt.year != 0:
            return 'years', 1

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
