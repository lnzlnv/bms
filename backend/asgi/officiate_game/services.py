from django.core.exceptions import ObjectDoesNotExist
from channels.db import database_sync_to_async

from apis.statisticians.serializers import (
    StatsSerializer,
    SubstitutionSerializer,
    QuarterSerializer
)
from apps.statisticians.models import Stat
from apps.statisticians.services import get_game
from apis.statisticians.services import (
    ValidatedData,
    SubstitutionTime,
    PointsPerQuarter,
    update_game_quarter,
    set_game_starters
)
from apps.statisticians.models import OfficiateHistory


def get_stats(
        *,
        stat_id: int
):
    return Stat.stats.filter(pk=stat_id).first()


class Stats:
    def __init__(self, data):
        self.instance = None
        self.data = data

    @database_sync_to_async
    def update(self):
        self.instance = get_stats(stat_id=self.data['stat_id'])
        serializer = StatsSerializer(self.instance, data=self.data['content'], partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

    def perform_update(self, serializer):
        ValidatedData(
            game_id=self.data['game_id'],
            team_id=self.data['team_id'],
            data=self.data['content'],
            validated_data=serializer.validated_data,
            stats=self.instance
        ).update()

        serializer.save()


class SubstitutionsTime:
    def __init__(self, data):
        self.in_game_players = None
        self.data = data

    @database_sync_to_async
    def create(self):
        serializer = SubstitutionSerializer(data=self.data['content'])
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return self.in_game_players

    def perform_create(self, serializer):
        sub = SubstitutionTime(
            data=serializer.validated_data,
            game=get_game(game=self.data['game_id']),
            team_id=self.data['team_id']
        )

        sub.record()

        self.in_game_players = sub.in_game_player


class Quarter:
    def __init__(self, data):
        self.game = None
        self.data = data

    @database_sync_to_async
    def update(self):
        serializer = QuarterSerializer(data=self.data['content'])
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

    def perform_update(self, serializer):
        self.game = get_game(game=self.data['game_id'])
        self._game_quarter(serializer.validated_data['quarter'])
        print(self.data)
        delete_history(
            game=self.game,
            statistician=self.data['statistician']
        )

        if not self.game.starters_are_set:
            set_game_starters(game=self.game)

    def _game_quarter(self, quarter):
        PointsPerQuarter(
            game=self.game,
            quarter=quarter
        ).set()
        update_game_quarter(
            game=self.game,
            quarter=quarter
        )


class History:
    def __init__(self, data):
        self.instance = None
        self.history = None
        self.operation = data['operation']
        self.game = data['game_id']
        self.statistician = data['statistician']

    @database_sync_to_async
    def perform_operation(self):
        self.history = self._get_history()
        if self.history is None:
            return

        self._set_instance(self.history.actions['stat_id'])
        serializer = StatsSerializer(self.instance, data=self.history.actions['content'], partial=True)
        serializer.is_valid(raise_exception=True)
        self._perform_update(serializer)

    def _set_instance(self, pk):
        self.instance = Stat.stats.filter(pk=pk).first()

    def _perform_update(self, serializer):
        ValidatedData(
            game_id=self.history.actions['game_id'],
            team_id=self.history.actions['team_id'],
            data=self.history.actions['content'],
            validated_data=serializer.validated_data,
            stats=self.instance,
            operation=self.operation
        ).update()
        serializer.save()

    def _get_history(self):
        current = None
        previous_action = OfficiateHistory.histories.filter(
            game=self.game,
            statistician=self.statistician,
            is_current=True
        ).first()

        if previous_action is None:
            return

        match self.operation:
            case 'UNDO':
                try:
                    current = previous_action.previous
                except OfficiateHistory.previous.RelatedObjectDoesNotExist:
                    current = None
            case 'REDO':
                current = previous_action.next
            case _:
                pass

        if current is None:
            return None

        # change the current active history
        previous_action.is_current = False
        previous_action.save()

        current.is_current = True
        current.save()

        return previous_action


def get_id(
        *,
        string: str
):
    return string.split('-')[-1]


def delete_history(
    *,
    game: int or object,
    statistician: int or object
):
    OfficiateHistory.histories.filter(
        game=game,
        statistician=statistician
    ).delete()
    print('delete')
