from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.public_pages.models import Season


class UpdateUserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'user_profile/update.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.season = Season.seasons.all().first()

    def get_context_data(self, **kwargs):
        return {'self': self}
