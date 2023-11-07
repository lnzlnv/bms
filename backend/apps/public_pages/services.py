from datetime import datetime

from apps.announcements.models import Announcement

from .models import ScheduleBanner


class NextGameSchedule():
    def get_next_game(self) -> dict:
        """get the next game schedule for senior and junior

        Returns:
            _type_: dictionary of the junior and senior
        """
        return {
            'senior': self.__get_schedule('S'),
            'junior': self.__get_schedule('J')
        }

    def __get_schedule(self, division: str) -> ScheduleBanner:
        """get the next game schedule

        Args:
            division (_type_): division shedule

        Returns:
            _type_: the first schedule which will be the next schedule
        """
        now = datetime.now().date()
        return ScheduleBanner.schedules.filter(
            division=division,
            date__gte=now
        ).first()


def get_latest_announcement():
    now = datetime.now().date()
    return Announcement.announcements.filter(
        publish_date__date__lte=now
    ).first()
