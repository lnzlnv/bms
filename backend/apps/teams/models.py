from typing import Any
from django.db import models
from django.utils.text import slugify
from django.core.validators import MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


from apps.public_pages.models import Season


def team_logo_upload_path(instance, filename):
    folder_name = 'team_logo'
    new_filename = '{}/{}'.format(
        instance.get_division_display().lower(),
        filename
    )
    return '{}/{}'.format(folder_name, new_filename)


class Team(models.Model):
    DIVISIONS = [
        ('J', 'Junior'),
        ('S', 'Senior')
    ]

    name = models.CharField(
        max_length=100
    )

    division = models.CharField(
        max_length=100,
        choices=DIVISIONS
    )

    logo = models.ImageField(
        upload_to=team_logo_upload_path,
    )

    slug = models.SlugField(
        unique=True,
        blank=True  
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    teams = models.Manager()

    class Meta:
        ordering = ['name']
        unique_together = ('name', 'division')

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        if not self.slug:
            self.slug = slugify(''.format(
                self.name,
                self.division
            ))
       

    def __str__(self) -> str:
        return self.name
    

    @property
    def logo_name(self):
        return self.logo.name.split('/')[-1]

@receiver(post_save, sender=Team)
def create_team_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = '{}-{}'.format(
            instance.name,
            instance.id
        )
        instance.slug = slugify(slug)
        instance.save()


class Player(models.Model):
    height_feet = models.IntegerField(
        default=0
    )

    height_inches = models.IntegerField(
        validators=[MaxValueValidator(11)],
        default=0
    )

    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    players = models.Manager()

    def __str__(self):
        return '{} {}'.format(
            self.first_name,
            self.last_name
        )
    
    @property
    def height(self):
        return "{}'{}".format(
            self.height_feet,
            self.height_inches
        )

    @property
    def full_name(self):
        return '{} {}'.format(
            self.first_name,
            self.last_name
        )

class PlayerTeam(models.Model):
    player = models.ForeignKey(
        Player,
        related_name='teams',
        on_delete=models.CASCADE
    )

    team = models.ForeignKey(
        Team,
        related_name='players',
        on_delete=models.CASCADE
    )

    season = models.ForeignKey(
        Season,
        related_name='players',
        on_delete=models.CASCADE
    )

    position = models.CharField(
        max_length=100
    )

    slug = models.SlugField(
        default=None,
        null=True,
        blank=True
    )

    number = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    players = models.Manager()

    class Meta:
        unique_together = ('team', 'season', 'number')
        ordering = ['number']
    

    def __str__(self):
        return str(self.player)


@receiver(post_save, sender=PlayerTeam)
def set_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify('{}-{}-{}'.format(
            instance.player.first_name,
            instance.player.last_name,
            instance.id
        ))

class SeasonTeam(models.Model):
    season = models.ForeignKey(
        Season,
        on_delete=models.CASCADE,
        related_name='season_teams'
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='participated_season'
    )

    has_playoffs_stats = models.BooleanField(
        default=False
    )

    teams = models.Manager()

    def __str__(self) -> str:
        return '{} @ {}'.format(
            self.team.name,
            self.season.year
        )