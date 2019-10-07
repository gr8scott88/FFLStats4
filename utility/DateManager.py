from datetime import datetime, timedelta


class DateManager:
    def __init__(self, week_1_date: datetime):
        self.start_date = week_1_date

    def get_current_week(self):
        now = datetime.now()
        delta = now - self.start_date
        week = delta.days / 7
        return week
        # monday1 = (d1 - timedelta(days=d1.weekday()))
        # monday2 = (d2 - timedelta(days=d2.weekday()))
        # print('Weeks:', (monday2 - monday1).days / 7)

    def get_start_of_week_x(self, x):
        pass

    def get_week_breakdown(self, x):
        pass
