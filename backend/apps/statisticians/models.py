from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.game_schedule.models import Game
from apps.public_pages.models import Season
from apps.teams.models import (
    PlayerTeam,
)
from apps.teams.models import Team
from apps.authentication.models import User


class Stat(models.Model):
    STATS_TYPE = [
        ('P', 'Player'),
        ('T', 'Team'),
        ('TA', 'Time Analysis'),
        ('TG', 'Team Game'),
        ('PS', 'Player Season'),
        ('TP', 'Team Playoffs')
    ]

    stats_type = models.CharField(
        choices=STATS_TYPE,
        max_length=100
    )

    two_pts_att = models.IntegerField(
        default=0
    )

    two_pts_made = models.IntegerField(
        default=0
    )

    three_pts_att = models.IntegerField(
        default=0
    )

    three_pts_made = models.IntegerField(
        default=0
    )

    ft_att = models.IntegerField(
        default=0
    )

    ft_made = models.IntegerField(
        default=0
    )

    reb_off = models.IntegerField(
        default=0
    )

    reb_def = models.IntegerField(
        default=0
    )

    assists = models.IntegerField(
        default=0
    )

    steals = models.IntegerField(
        default=0
    )

    turnovers = models.IntegerField(
        default=0
    )

    blocks = models.IntegerField(
        default=0
    )

    fouls = models.IntegerField(
        default=0
    )

    is_ejected = models.BooleanField(
        default=False
    )

    is_disqualified = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    stats = models.Manager()

    @property
    def is_team_type(self):
        return self.stats_type == 'T'

    def is_player_type(self):
        return self.stats_type == 'P'

    @property
    def is_time_analysis(self):
        return self.stats_type == 'TA'

    @property
    def is_player(self):
        return self.stats_type == 'P'

    @property
    def is_time_analysis(self):
        return self.stats_type == 'TA'

    @property
    def is_team(self):
        return self.stats_type == 'T'

    @property
    def is_team_game(self):
        return self.stats_type == 'TG'

    @property
    def is_player_season_stat(self):
        return self.stats_type == 'PS'

    @property
    def total_points(self):
        two_points_total = self.two_pts_made * 2
        three_points_total = self.three_pts_made * 3
        return two_points_total + three_points_total + self.ft_made

    @property
    def two_pts_percentage(self):
        if self.two_pts_made == 0 or self.two_pts_att == 0:
            return 0

        percent = self.two_pts_made / self.two_pts_att
        return round(percent * 100, 2)

    @property
    def three_pts_percentage(self):
        if self.three_pts_made == 0 or self.three_pts_att == 0:
            return 0

        percent = self.three_pts_made / self.three_pts_att
        return round(percent * 100, 2)

    @property
    def ft_percentage(self):
        if self.ft_made == 0 or self.ft_att == 0:
            return 0

        percent = self.ft_made / self.ft_att
        return round(percent * 100, 2)

    @property
    def reb_total(self):
        return self.reb_def + self.reb_off

    @property
    def total_att(self):
        return self.three_pts_att + self.two_pts_att

    @property
    def total_made(self):
        return self.three_pts_made + self.two_pts_made

    @property
    def total_fg_percentage(self):
        if self.total_made == 0 or self.total_att == 0:
            return 0

        percent = self.total_made / self.total_att
        return round(percent * 100, 2)

    @property
    def total_shots_att(self):
        return self.three_pts_att + self.two_pts_att + self.ft_att

    @property
    def total_shots_made(self):
        return self.three_pts_made + self.two_pts_made + self.ft_made

    @property
    def total_shots_percentage(self):
        if self.total_shots_made == 0 or self.total_shots_att == 0:
            return 0

        percent = self.total_shots_made / self.total_shots_att
        return round(percent * 100, 2)

    def __str__(self):
        if self.stats_type == 'P':
            return self.player_game_stat.player.player.last_name

        if self.is_player_season_stat:
            return self.player_season_stat.player_team.player.last_name

        if self.is_time_analysis:
            return self.analysis.team.name

        if self.stats_type == 'TG':
            return self.team_game_stat.team.name

        if self.stats_type == 'T':
            return self.team_season_stat.team.name

        return 'no-name'


class PlayerStat(models.Model):
    stats = models.OneToOneField(
        Stat,
        on_delete=models.CASCADE,
        related_name='player_stats'
    )

    is_starter = models.BooleanField(
        default=False
    )

    seconds_played = models.IntegerField(
        default=0
    )

    games_played = models.IntegerField(
        default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    player_stats = models.Manager()

    @property
    def minutes_played(self):
        if self.seconds_played == 0:
            return 0
        minutes = self.seconds_played / 60
        return round(minutes, 1)

    @property
    def pts_per_game(self):
        if self.stats.total_points == 0 or self.games_played == 0:
            return 0

        ppg = self.stats.total_points / self.games_played
        return round(ppg, 2)

    @property
    def field_goal_made_per_game(self):
        if self.stats.total_made == 0 or self.games_played == 0:
            return 0

        fgm = self.stats.total_made / self.games_played
        return round(fgm, 2)

    @property
    def field_goals_att_per_game(self):
        if self.stats.total_att == 0 or self.games_played == 0:
            return 0

        fga = self.stats.total_att / self.games_played
        return round(fga, 2)

    @property
    def three_pts_made_per_game(self):
        if self.stats.three_pts_made == 0 or self.games_played == 0:
            return 0

        three_pts_made = self.stats.three_pts_made / self.games_played
        return round(three_pts_made, 2)

    @property
    def three_pts_att_per_game(self):
        if self.stats.three_pts_att == 0 or self.games_played == 0:
            return 0

        three_pts_made = self.stats.three_pts_att / self.games_played
        return round(three_pts_made, 2)

    @property
    def two_pts_made_per_game(self):
        if self.stats.two_pts_made == 0 or self.games_played == 0:
            return 0

        two_pts_made = self.stats.two_pts_made / self.games_played
        return round(two_pts_made, 2)

    @property
    def two_pts_att_per_game(self):
        if self.stats.two_pts_att == 0 or self.games_played == 0:
            return 0

        two_pts_att = self.stats.two_pts_att / self.games_played
        return round(two_pts_att, 2)

    @property
    def ft_made_per_game(self):
        if self.stats.ft_made == 0 or self.games_played == 0:
            return 0

        ft_made = self.stats.ft_made / self.games_played
        return round(ft_made, 2)

    @property
    def ft_att_per_game(self):
        if self.stats.ft_att == 0 or self.games_played == 0:
            return 0

        ft_made = self.stats.ft_att / self.games_played
        return round(ft_made, 2)

    @property
    def ftp_per_game(self):
        if self.ft_made_per_game == 0:
            return 0

        return self.ft_made_per_game / self.ft_att_per_game

    @property
    def reb_off_per_game(self):
        if self.stats.reb_off == 0 or self.games_played == 0:
            return 0

        reb_off = self.stats.reb_off / self.games_played
        return round(reb_off, 2)

    @property
    def reb_def_per_game(self):
        if self.stats.reb_def == 0 or self.games_played == 0:
            return 0

        reb_def = self.stats.reb_def / self.games_played
        return round(reb_def, 2)

    @property
    def reb_per_game(self):
        if self.stats.reb_total == 0 or self.games_played == 0:
            return 0

        reb_total = self.stats.reb_total / self.games_played
        return round(reb_total, 2)

    @property
    def assists_per_game(self):
        if self.stats.assists == 0 or self.games_played == 0:
            return 0

        apg = self.stats.assists / self.games_played
        return round(apg, 2)

    @property
    def steals_per_game(self):
        if self.stats.steals == 0 or self.games_played == 0:
            return 0

        steals = self.stats.steals / self.games_played
        return round(steals, 2)

    @property
    def blocks_per_game(self):
        if self.stats.blocks == 0 or self.games_played == 0:
            return 0

        blocks = self.stats.blocks / self.games_played
        return round(blocks, 2)

    @property
    def turnovers_per_game(self):
        if self.stats.turnovers == 0 or self.games_played == 0:
            return 0

        turnovers = self.stats.turnovers / self.games_played
        return round(turnovers)

    @property
    def team_stat(self):
        try:
            return TeamSeasonStat.stats.filter(
                team=self.stats.player_season_stat.player_team.team,
                season=self.stats.player_season_stat.season
            ).first().stat
        except TeamSeasonStat.player_season_stat.RelatedObjectDoesNotExist:
            return TeamSeasonStat.stats.filter(
                team=self.stats.player_playoffs_stat.player_team.team,
                season=self.stats.player_playoffs_stat.season
            ).first().stat

    @property
    def ppg_percentage(self):
        if self.stats.total_points == 0:
            return 0

        return self.stats.total_points / self.team_stat.total_points

    @property
    def rpg_percentage(self):
        if self.reb_per_game == 0:
            return 0

        team_rpg = self.team_stat.team_stats.reb_per_game
        return self.reb_per_game / team_rpg

    @property
    def apg_percentage(self):
        if self.assists_per_game == 0:
            return 0

        team_rpg = self.team_stat.team_stats.assists_per_game
        return self.assists_per_game / team_rpg

    @property
    def ftg_percentage(self):
        if self.ftp_per_game == 0:
            return 0
        print(self.ftp_per_game)
        print(self.team_stat.team_stats.ftp_per_game)
        return self.ftp_per_game / self.team_stat.team_stats.ftp_per_game


class TeamStat(models.Model):
    stat = models.OneToOneField(
        Stat,
        on_delete=models.CASCADE,
        related_name='team_stats'
    )

    win = models.IntegerField(
        default=0
    )

    lose = models.IntegerField(
        default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    team_stats = models.Manager()

    def __str__(self):
        return str(self.stat)

    @property
    def team_win_percentage(self):
        if self.win == 0:
            return 0

        percentage = self.win / self.games_played
        return round(percentage, 2)

    @property
    def games_played(self):
        return self.win + self.lose

    @property
    def pts_per_game(self):
        if self.stat.total_points == 0:
            return 0

        ppg = self.stat.total_points / self.games_played
        return round(ppg, 2)

    @property
    def field_goal_made_per_game(self):
        if self.stat.total_made == 0:
            return 0

        fgm = self.stat.total_made / self.games_played
        return round(fgm, 2)

    @property
    def field_goals_att_per_game(self):
        if self.stat.total_att == 0:
            return 0

        fga = self.stat.total_att / self.games_played
        return round(fga, 2)

    @property
    def three_pts_made_per_game(self):
        if self.stat.three_pts_made == 0:
            return 0

        three_pts_made = self.stat.three_pts_made / self.games_played
        return round(three_pts_made, 2)

    @property
    def three_pts_att_per_game(self):
        if self.stat.three_pts_att == 0:
            return 0

        three_pts_made = self.stat.three_pts_att / self.games_played
        return round(three_pts_made, 2)

    @property
    def two_pts_made_per_game(self):
        if self.stat.two_pts_made == 0:
            return 0

        two_pts_made = self.stat.two_pts_made / self.games_played
        return round(two_pts_made, 2)

    @property
    def two_pts_att_per_game(self):
        if self.stat.two_pts_att == 0:
            return 0

        two_pts_att = self.stat.two_pts_att / self.games_played
        return round(two_pts_att, 2)

    @property
    def ft_made_per_game(self):
        if self.stat.ft_made == 0:
            return 0

        ft_made = self.stat.ft_made / self.games_played
        return round(ft_made, 2)

    @property
    def ft_att_per_game(self):
        if self.stat.ft_att == 0:
            return 0

        ft_made = self.stat.ft_att / self.games_played
        return round(ft_made, 2)

    @property
    def ftp_per_game(self):
        if self.ft_made_per_game == 0:
            return 0

        return self.ft_made_per_game / self.ft_att_per_game

    @property
    def reb_off_per_game(self):
        if self.stat.reb_off == 0:
            return 0

        reb_off = self.stat.reb_off / self.games_played
        return round(reb_off, 2)

    @property
    def reb_def_per_game(self):
        if self.stat.reb_def == 0:
            return 0

        reb_def = self.stat.reb_def / self.games_played
        return round(reb_def, 2)

    @property
    def reb_per_game(self):
        if self.stat.reb_total == 0:
            return 0

        reb_total = self.stat.reb_total / self.games_played
        return round(reb_total, 2)


    @property
    def assists_per_game(self):
        if self.stat.assists == 0:
            return 0

        apg = self.stat.assists / self.games_played
        return round(apg, 2)

    @property
    def steals_per_game(self):
        if self.stat.steals == 0:
            return 0

        assists = self.stat.steals / self.games_played
        return round(assists, 2)

    @property
    def blocks_per_game(self):
        if self.stat.blocks == 0:
            return 0

        blocks = self.stat.blocks / self.games_played
        return round(blocks, 2)

    @property
    def turnovers_per_game(self):
        if self.stat.turnovers == 0:
            return 0

        turnovers = self.stat.turnovers / self.games_played
        return round(turnovers)


class PlayerGameStat(models.Model):
    player = models.ForeignKey(
        PlayerTeam,
        on_delete=models.CASCADE,
        related_name='player_game_stats'
    )

    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='player_game_stats'
    )

    stats = models.OneToOneField(
        Stat,
        on_delete=models.CASCADE,
        related_name='player_game_stat'
    )

    season = models.ForeignKey(
        Season,
        on_delete=models.CASCADE,
        related_name='player_game_stats'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    player_game_stats = models.Manager()


@receiver(post_delete, sender=PlayerGameStat)
def delete_related_stat(sender, instance, **kwargs):
    if instance.stats:
        instance.stats.delete()


class TeamGameStat(models.Model):
    season = models.ForeignKey(
        Season,
        on_delete=models.CASCADE,
        related_name='team_game_stats',
    )

    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='team_game_stats'
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='team_game_stats'
    )

    stat = models.OneToOneField(
        Stat,
        on_delete=models.CASCADE,
        related_name='team_game_stat'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    stats = models.Manager()

    def __str__(self) -> str:
        return '{} at {}'.format(
            self.team.name,
            self.game.schedule.match
        )

@receiver(post_delete, sender=TeamGameStat)
def delete_related_stat(sender, instance, **kwargs):
    if instance.stat:
        instance.stat.delete()


class TeamSeasonStat(models.Model):
    season = models.ForeignKey(
        Season,
        on_delete=models.CASCADE,
        related_name='team_season_stats'
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='seasons_stat'
    )

    stat = models.OneToOneField(
        Stat,
        on_delete=models.CASCADE,
        related_name='team_season_stat'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    stats = models.Manager()

    def __str__(self):
        return '{} - {}'.format(
            self.team.name,
            self.season.year
        )


class PlayerSeasonStat(models.Model):
    season = models.ForeignKey(
        Season,
        on_delete=models.CASCADE,
        related_name='player_seasons_stat'
    )

    player_team = models.ForeignKey(
        PlayerTeam,
        on_delete=models.CASCADE,
        related_name='player_seasons_stat',
        # remove
        default=None
    )

    stat = models.OneToOneField(
        Stat,
        on_delete=models.CASCADE,
        related_name='player_season_stat'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    stats = models.Manager()

    def __str__(self):
        return self.player_team.player.last_name


@receiver(post_delete, sender=PlayerSeasonStat)
def delete_stat(sender, instance, **kwargs):
    if instance.stat:
        instance.stat.delete()


@receiver(post_delete, sender=TeamSeasonStat)
def delete_stat(sender, instance, **kwargs):
    if instance.stat:
        instance.stat.delete()

class TeamPlayoffsStat(models.Model):
    season = models.ForeignKey(
        Season,
        on_delete=models.CASCADE,
        related_name='team_playoffs_stats'
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='playoffs_stat'
    )

    stat = models.OneToOneField(
        Stat,
        on_delete=models.CASCADE,
        related_name='team_playoffs_stat'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    stats = models.Manager()

    def __str__(self):
        return '{} - {}'.format(
            self.team.name,
            self.season.year
        )


class PlayerPlayoffsStat(models.Model):
    season = models.ForeignKey(
        Season,
        on_delete=models.CASCADE,
        related_name='player_playoffs_stat'
    )

    player_team = models.ForeignKey(
        PlayerTeam,
        on_delete=models.CASCADE,
        related_name='player_playoffs_stat',
    )

    stat = models.OneToOneField(
        Stat,
        on_delete=models.CASCADE,
        related_name='player_playoffs_stat'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    stats = models.Manager()

    def __str__(self):
        return self.player_team.player.last_name


class PointsClassification(models.Model):
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='points_classification',
        editable=False
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='points_classification',
        editable=False
    )

    off_turnover = models.IntegerField(default=0)

    fast_break = models.IntegerField(default=0)

    second_chance = models.IntegerField(default=0)

    starters = models.IntegerField(default=0)

    bench = models.IntegerField(default=0)

    is_time_analysis = models.BooleanField(
        default=False,
        editable=False
    )

    quarter = models.IntegerField(
        default=0,
        editable=False
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    classifications = models.Manager()

    class Meta:
        unique_together = ('quarter', 'game', 'team', 'is_time_analysis')


class Substitution(models.Model):
    SUBSTITUTION_STATUS = [
        ('I', 'In'),
        ('O', 'Out')
    ]

    player = models.ForeignKey(
        PlayerTeam,
        on_delete=models.CASCADE,
        related_name='substitutions'
    )

    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='substitutions'
    )

    minutes = models.IntegerField()

    seconds = models.IntegerField()

    status = models.CharField(
        choices=SUBSTITUTION_STATUS,
        max_length=10
    )

    quarter = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    substitutions = models.Manager()

    class Meta:
        ordering = ['quarter', '-minutes', '-seconds']

    def __str__(self):
        return ('{} - {}:{}').format(
            self.player.player.last_name,
            self.minutes,
            self.seconds
        )

    @property
    def is_sub_in(self):
        return self.status == 'I'

    @property
    def is_sub_out(self):
        return self.status == 'O'


class InGamePlayer(models.Model):
    game = models.OneToOneField(
        Game,
        on_delete=models.CASCADE,
        related_name='in_game_players'
    )

    # home_team = ListCharField(
    #     base_field=models.CharField(max_length=10),
    #     size=6,
    #     max_length=(6 * 11),
    #     default=[]
    # )

     # away_team = ListCharField(
    #     base_field=models.CharField(max_length=10),
    #     size=6,
    #     max_length=(6 * 11),
    #     default=[]
    # )

    home_team = ArrayField(
        models.CharField(max_length=100),
        default=list
    )

    away_team = ArrayField(
        models.CharField(max_length=100),
        default=list
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    players = models.Manager()


class PointsInAQuarter(models.Model):
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='quarter_points'
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='quarter_points'
    )

    quarter = models.IntegerField()
    points = models.IntegerField(
        default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    quarter_points = models.Manager()

    class Meta:
        ordering = ['quarter']

    def __str__(self):
        return 'Quarter {} - {}'.format(
            self.quarter,
            self.points
        )


class TeamTimeStatsAnalysis(models.Model):
    season = models.ForeignKey(
        Season,
        on_delete=models.CASCADE,
        related_name='time_analyses'
    )

    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='game_time_analyses'
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='time_analyses'
    )

    stat = models.OneToOneField(
        Stat,
        on_delete=models.CASCADE,
        related_name='analysis'
    )

    points_classification = models.OneToOneField(
        PointsClassification,
        on_delete=models.CASCADE,
        related_name='time_analysis',
    )

    time = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    analyses = models.Manager()

    class Meta:
        ordering = ['time']

    def __str__(self) -> str:
        return 'Analysis'


@receiver(post_delete, sender=TeamTimeStatsAnalysis)
def delete_related_stat(sender, instance, **kwargs):
    if instance.stat:
        instance.stat.delete()


class OfficiateHistory(models.Model):
    game = models.ForeignKey(
        Game,
        related_name='officiate_histories',
        on_delete=models.CASCADE
    )

    statistician = models.ForeignKey(
        User,
        related_name='officiate_histories',
        on_delete=models.CASCADE
    )

    actions = models.JSONField()

    next = models.OneToOneField(
        'OfficiateHistory',
        related_name='previous',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    is_current = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    histories = models.Manager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return 'History {}'.format(self.pk)