from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.mixins import (
    ListModelMixin,
    DestroyModelMixin
)

from apis.statisticians.serializers import GameSerializer
from apis.statisticians.services import set_winner
from apps.statisticians.services import get_game
from apps.game_schedule.models import Game

from .serializers import GamesForAdminApprovalOptionsSerializer
from .selectors import get_games_stats_reports
from .services import (
    update_game_is_approved_by_admin,
    update_teams_win_or_lose,
    PlayerSeasonStatComputation,
    TeamSeasonStatComputation,
    PlayoffStats
)


class GamesForAdminApprovalOptionsAPIView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        serializer = GamesForAdminApprovalOptionsSerializer(
            request.user
        )
        return Response(serializer.data)
    

class GamesForAdminApprovalAPIView(
    GenericAPIView,
    ListModelMixin,
    DestroyModelMixin
):
    serializer_class = GameSerializer

    def dispatch(self, request, *args, **kwargs):
        self.is_delete = request.method == 'DELETE'
        self.is_approved = request.GET.get('is_approved', False)
        self.season = request.GET.get('season', None)
        self.division = request.GET.get('division', None)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        game = get_game(game=kwargs['pk'])

        if game is None:
            return Response({'message': 'Game not found.'}, status=404)

        if game.is_approved_by_admin:
            return Response({'message': 'Already approved by admin.'})

        update_game_is_approved_by_admin(
            game=game,
            user=request.user
        )

        set_winner(game=game)

        if game.is_playoffs:
            PlayoffStats(game=game).set_playoffs_stats()

        if game.is_eliminations or game.is_playoffs:
            PlayerSeasonStatComputation(game=game).compute_both_teams()
            TeamSeasonStatComputation(game=game).compute_both_teams()
            update_teams_win_or_lose(game=game)


        return Response({'message': 'success'})

    def delete(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)

        return Response({'message': 'success'})
    
    def get_queryset(self):
        if self.is_delete:
            return Game.games.all()

        return get_games_stats_reports(
            is_approved=self.is_approved,
            season=self.season,
            division=self.division
        )