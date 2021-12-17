import datetime


def get_current_datetime():
    return datetime.date.today()

def get_future_datetime():
    td = datetime.timedelta(days=365)
    return datetime.date.today() + td


print(get_current_datetime())
print(get_future_datetime())