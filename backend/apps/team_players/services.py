from django.shortcuts import get_object_or_404

from apps.teams.models import Team


def get_team(
    *,
    slug: str,
    division: str
):
    return get_object_or_404(
        Team, 
        division=division, 
        slug=slug
    )
