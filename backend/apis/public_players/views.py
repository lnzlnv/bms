from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from apis.team_players.serializers import PlayerTeamSerializer
from apps.teams.models import PlayerTeam

from .serializers import PlayersPublicOptionsSerializer


class PlayersPublicOptionsAPIView(GenericAPIView):
	permission_classes = []
	authentication_classes = []

	def get(self, request, *args, **kwargs):
		serializer = PlayersPublicOptionsSerializer(request.user)
		return Response(serializer.data)


class PlayersPublicAPIView(
	GenericAPIView,
	ListModelMixin
):
	permission_classes = []
	authentication_classes = []
	paginator = None
	serializer_class = PlayerTeamSerializer

	def get(self, request, *args, **kwargs):
		self.kwargs = kwargs
		return super().list(request, *args, **kwargs)

	def get_queryset(self, *args, **kwargs):
		return PlayerTeam.players.filter(
			team=self.kwargs['team'],
			season=self.kwargs['season']
		)
