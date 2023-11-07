import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from apps.statisticians.models import OfficiateHistory
from apps.game_schedule.models import Game
from apps.authentication.models import User

from .services import (
    Stats,
    SubstitutionsTime,
    Quarter,
    get_id,
    History,
)


class StatsUpdateConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = None
        self.game_room_name = None
        self.game_name = None

    async def connect(self):
        self.game_name = self.scope['url_route']['kwargs']['game_slug']
        self.game_room_name = 'officiate_{}'.format(self.game_name)
        await self.set_game_instance()
        await self.channel_layer.group_add(
            self.game_room_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.game_room_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        match data['type']:
            case 'stats':
                await self.type_stats(data)
            case 'substitution':
                await self.type_substitution(data)
            case 'quarter':
                await self.type_quarter(data)
            case 'game_winner':
                await self.type_game_winner(data)
            case 'history':
                await self.type_history(data)
            case _:  # do nothing
                pass

    @database_sync_to_async
    def set_game_instance(self):
        self.game = Game.games.filter(pk=get_id(string=self.game_name)).first()

    async def type_stats(self, data):
        stat = Stats(data)
        await stat.update()
        await self.create_history(data)
        await self.channel_group_send(data, 'update_stats')

    async def type_substitution(self, data):
        substitution = SubstitutionsTime(data)
        in_game_players = await substitution.create()
        data = self.get_data(in_game_players, data)
        await self.channel_group_send(data, 'substitution')

    async def type_quarter(self, data):
        quarter = Quarter(data)
        await quarter.update()
        await self.channel_layer.group_send(
            self.game_room_name,
            {
                'type': 'update_quarter',
                'data': data
            }
        )

    async def type_game_winner(self, data):
        await self.channel_group_send(data, 'game_winner')

    async def type_history(self, data):
        history = History(data)
        await history.perform_operation()

        if history.history is not None:
            data['history'] = history.history.actions

        await self.channel_group_send(data, 'history')

    @database_sync_to_async
    def create_history(self, data):
        current = OfficiateHistory.histories.filter(
            game=self.game,
            statistician=data['statistician'],
            is_current=True
        ).first()

        next_item = OfficiateHistory.histories.create(
            game=self.game,
            actions=data,
            statistician=User.objects.filter(pk=data['statistician']).first(),
            is_current=True
        )

        if current is None:
            return 
        
        current.next = next_item
        current.is_current = False
        current.save()

    async def update_stats(self, event):
        await self.send(text_data=json.dumps(event['data']))

    async def substitution(self, event):
        await self.send(text_data=json.dumps(event['data']))

    async def update_quarter(self, event):
        await self.send(text_data=json.dumps(event['data']))

    async def game_winner(self, event):
        await self.send(text_data=json.dumps(event['data']))

    async def history(self, event):
        await self.send(text_data=json.dumps(event['data']))

    async def channel_group_send(self, data, channel_type):
        await self.channel_layer.group_send(
            self.game_room_name,
            {
                'type': channel_type,
                'data': data
            }
        )

    def get_data(self, in_game_players, data):
        return {
            **data,
            'players': {
                'home_team': in_game_players.home_team,
                'away_team': in_game_players.away_team
            }
        }
