"""
File containing helper class to generate list of dictionaries (containing check-in, check-out, ...) to run through
"""

import datetime


def test_dates():
    return [("12.03.2019", "15.03.2019")]


class DateConstructionHelper:

    def __init__(self, dateformat=None):
        """
        In the whole class we work with a list of tuples of (datetime.checkin, datetime.checkout). Only in the ende,
        right before returning, the dictionary is constructed with all information desired.
        :param dateformat: Optional string specifing the string date format.
        """
        self.current_date = datetime.datetime.now()
        self.date_format = dateformat if dateformat else "%d.%m.%Y"

    def date_runner(self, delta, split=1):
        result = []
        check_in_runner = self.current_date
        check_out_runner = self.current_date + datetime.timedelta(days=delta)
        for i in range(365):
            result.append((check_in_runner, check_out_runner))
            check_in_runner = check_in_runner + datetime.timedelta(days=split)
            check_out_runner = check_out_runner + datetime.timedelta(days=split)
        return result

    def continuous_weeks(self):
        return self.date_runner(7)

    def standard_date_cycle(self):
        # reset standard date cycle list
        sdc = []
        week_split = self.continuous_weeks()
        three_day_split = self.date_runner(3)
        one_day_split = self.date_runner(1)
        for a, b, c in zip(week_split, three_day_split, one_day_split):
            sdc.append(a)
            sdc.append(b)
            sdc.append(c)
        print(sdc)
        return self.tuples_to_dic(sdc)

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

    def tuples_to_dic(self, sdc):
        result = []
        for pair in sdc:
            result.append((self.date_to_string(pair[0]), self.date_to_string(pair[1])))
        return result


if __name__ == "__main__":
    dC = DateConstructionHelper()
    li = dC.standard_date_cycle()
    dC.test_standard_date_cycle()
