import datetime

from studentvue import StudentVue

import pandas as pd


def get_all_events(user: StudentVue) -> list:
    raw_events = user.get_calendar()["CalendarListing"]["EventLists"]["EventList"]
    filtered_events = []
    # filtering events
    for event in raw_events:
        event = {
            "title": event["@Title"],
            'date': event['@Date'],
            'start_time': event["@StartTime"],
            "day_type": event["@DayType"],
        }
        filtered_events.append(event)
    return filtered_events


def get_event_df(user: StudentVue) -> pd.DataFrame:
    event_list = get_all_events(user)
    event_df = pd.DataFrame(event_list)

    event_df["date"] = pd.to_datetime(event_df["date"])
    event_df["title"] = event_df["title"].astype(str)
    event_df['start_time'] = event_df['start_time'].astype(str)
    event_df['day_type'] = event_df['day_type'].astype(str)
    return event_df


# this function will return the next seven days that there is an event
def get_next_seven_days(user: StudentVue):
    # I have to convert this, so I can compare it to the @Date column
    today = pd.to_datetime(datetime.date.today())
    event_df = get_event_df(user)

    dates_after_today = event_df[event_df["date"] >= today]["date"].head(n=7)
    return dates_after_today


def get_events(user: StudentVue) -> dict:
    event_df = get_event_df(user)
    event_dict = {}
    days = get_next_seven_days(user)
    for day in days:
        try:
            day_events = event_df[event_df["date"] == day].to_dict()

            # have to do this because the value will be a dictionary where the key is the item id and the value is
            # the actual value that we want
            for key, event in day_events.items():
                # getting the first value of the event because that is the actual content
                for event in event.values():
                    break
                day_events[key] = event

        # this is if the day is empty
        except ValueError:
            day_events = ""
        # assigning the date of the day to the events for that day
        event_dict[day.date().strftime("%m/%d/%Y")] = day_events
    return event_dict
