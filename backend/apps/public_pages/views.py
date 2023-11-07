from typing import Any, Dict

from django.views.generic import TemplateView

from apps.teams.services import (
    get_all_participating_schools,
)
from apps.landing.models import (
    MainImage,
    News
)
from apis.generate_account.selectors import get_activation_requests

from .models import Season
from .services import (
    NextGameSchedule,
    get_latest_announcement
)


class LandingPageView(TemplateView):
    template_name = 'public_pages/landing.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        seasons = Season.seasons.all()[:2]
        self.is_landing = 'active'
        self.previous_season = seasons[1] if seasons.count == 2 else seasons.first()
        self.season = seasons.first()
        self.main_image = MainImage.images.all().first()
        self.news = News.images.all().first()
        self.unupdated_accounts = get_activation_requests().first()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return {'self': self}


class AboutPageView(TemplateView):
    template_name = 'public_pages/about.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_about = 'active'
        self.schools = list(get_all_participating_schools())
        self.season = Season.seasons.all().first()
        self.unupdated_accounts = get_activation_requests().first()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return {'self': self}


class SchedulePageView(TemplateView):
    template_name = 'public_pages/schedule.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_schedule = 'active'
        self.schedules = NextGameSchedule().get_next_game()
        self.announcement = get_latest_announcement()
        self.season = Season.seasons.all().first()
        self.unupdated_accounts = get_activation_requests().first()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return {'self': self}


class RecapsView(TemplateView):
    template_name = 'public_pages/recaps.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_recap = 'active'
        self.season = Season.seasons.all().first()
        self.unupdated_accounts = get_activation_requests().first()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return {'self': self}


class SchedulesPublicView(TemplateView):
    template_name = 'public_pages/all-schedules.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.season = Season.seasons.all().first()
        self.unupdated_accounts = get_activation_requests().first()

    def get_context_data(self, **kwargs):
        return {'self': self}
