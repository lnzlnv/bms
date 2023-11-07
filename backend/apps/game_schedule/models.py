from django.db import models
from django.utils.text import slugify
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.authentication.models import User
from apps.teams.models import Team
from apps.public_pages.models import Season


class GameSchedule(models.Model):
    creator = models.ForeignKey(
        User,
        related_name='schedules',
        on_delete=models.SET_NULL,
        null=True
    )
        
    season = models.ForeignKey(
        Season,
        related_name='schedules',
        on_delete=models.CASCADE
    )

    date = models.DateTimeField()

    division = models.CharField(
        choices=Team().DIVISIONS,
        max_length=10
    )

    venue = models.CharField(
        max_length=100
    )

    schedules = models.Manager()

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.match
    
    @property
    def match(self):
        home_team = self.game.home_team
        away_team = self.game.away_team

        home = home_team.name if home_team is not None else ''
        away = away_team.name if away_team is not None else ''

        return '{} vs {}'.format(
            home,
            away
        )
    
    @property
    def home_team(self):
        home_team = self.game.home_team
        
        id = home_team.id if home_team is not None else ''
        name = home_team.name if home_team is not None else ''

        return {
            'id': id,
            'name': name
        }

    @property
    def away_team(self):
        pass
        away_team = self.game.away_team

        id = away_team.id if away_team is not None else ''
        name = away_team.name if away_team is not None else ''

        return {
            'id': id,
            'name': name
        }


class Game(models.Model):
    GAME_TYPE = [
        ('E', 'Eliminations'),
        ('P', 'Playoffs'),
        ('F', 'Finals')
    ]
    
    season = models.ForeignKey(
        Season,
        on_delete=models.CASCADE,
        related_name='games',
    )

    schedule = models.OneToOneField(
        GameSchedule,
        on_delete=models.CASCADE,
        related_name='game'
    )

    home_team = models.ForeignKey(
        Team,
        related_name='home_games',
        on_delete=models.SET_NULL,
        null=True
    )

    away_team = models.ForeignKey(
        Team,
        related_name='away_games',
        on_delete=models.SET_NULL,
        null=True
    )

    player_stats_are_generated = models.BooleanField(
        default=False
    )

    in_game_players_are_generated = models.BooleanField(
        default=False
    )

    quarter = models.IntegerField(
        default=0
    )

    starters_are_set = models.BooleanField(
        default=False
    )

    winner = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        blank=True
    )

    game_type = models.CharField(
        choices=GAME_TYPE,
        # remove
        default='E'
    )

    is_approved_by_super_statistician = models.BooleanField(
        default=False
    )

    is_approved_by_admin = models.BooleanField(
        default=False
    )

    has_half_time_analysis = models.BooleanField(
        default=False
    )

    has_full_time_analysis = models.BooleanField(
        default=False
    )

    approved_by_super_statistician = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='approved_games_statistician',
        null=True,
        blank=True
    )

    approved_by_admin = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='approved_games_admin',
        null=True,
        blank=True
    )

    is_finished = models.BooleanField(
        default=False
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    games = models.Manager()

    def __str__(self) -> str:
        return '{} vs {}'.format(
            self.home_team.name,
            self.away_team.name
        )
    
    @property
    def is_eliminations(self):
        return self.game_type == 'E'
    
    @property
    def is_playoffs(self):
        return self.game_type == 'P'
    
    @property
    def is_finals(self):
        return self.game_type == 'F'


@receiver(post_save, sender=Game)
def create_game_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        match = '{}-vs-{}-{}'.format(
            instance.home_team.name,
            instance.away_team.name,
            instance.pk
        )
        instance.slug = slugify(match)
        instance.save()


@receiver(post_delete, sender=Game)
def delete_schedule(sender, instance, *args, **kwargs):
    if instance.schedule:
        instance.schedule.delete()
