"""
File containing helper class to generate list of dictionaries (containing check-in, check-out, ...) to run through
"""

import datetime


def test_dates():
    return [("12.03.2019", "15.03.2019")]


class DateConstructionHelper:

    def __init__(self, dateformat=None):
        self.current_date = datetime.datetime.now()
        self.date_format = dateformat if dateformat else "%d.%m.%Y"

    def constant_delta_runner(self, delta):
        date_runner = self.current_date
        for i in range(366):

    def continuous_weeks(self):
        return self.constant_delta_runner(7)

    def standard_date_cycle(self):
        # reset standard date cycle list
        sdc = []
        sdc += self.continuous_weeks()
        print(sdc)
        return sdc

    def test_standard_date_cycle(self, full=True):
        for pair in self.standard_date_cycle():
            print("\n", pair[0], pair[1])
            if full:
                start_date = self.string_to_date(pair[0])
                end_date = self.string_to_date(pair[1])
                print("\t Start date:", "\t", start_date.strftime("%a"), pair[0])
                print("\t End date:  ", "\t", end_date.strftime("%a"), pair[1])
                diff = end_date - start_date
                print("\t Difference:", "\t", diff.days)

    def string_to_date(self, string):
        return datetime.datetime.strptime(string, self.date_format)

    def date_to_string(self, date_input: datetime.datetime):
        return date_input.strftime(self.date_format)


if __name__ == "__main__":
    dC = DateConstructionHelper()
    li = dC.standard_date_cycle()
    dC.test_standard_date_cycle()
