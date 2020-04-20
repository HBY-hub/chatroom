import datetime


def time_to_json(date):
    print(date)
    print(type(date))
    # date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    return {
        "year": date.year,
        "month": date.month,
        'day': date.day,
        "hour": date.hour,
        "minute": date.minute,
        "second": date.second

    }

#
# if __name__ == "__main__":
#     print(time_to_json("2020-03-23 22:33:23"))
