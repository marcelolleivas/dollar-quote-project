from datetime import timedelta


def get_workdays(start, end):
    # get list of all days
    all_days = (start + timedelta(x + 1) for x in range((end - start).days))

    # filter business days
    # weekday from 0 to 4. 0 is monday adn 4 is friday
    # increase counter in each iteration if it is a weekday
    count = sum(1 for day in all_days if day.weekday() < 5)
    return count
