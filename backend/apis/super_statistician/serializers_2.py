from rest_framework import serializers
from apps.statisticians.models import Stat

class StatsSerializer(serializers.ModelSerializer):
    minutes_played = serializers.SerializerMethodField()
    minutes = serializers.DecimalField(
        decimal_places=1,
        max_digits=10,
        default=0
    )

    class Meta:
        model = Stat
        fields = [
            'id',
            'stats_type',
            'two_pts_att',
            'two_pts_made',
            'two_pts_percentage',
            'three_pts_att',
            'three_pts_made',
            'three_pts_percentage',
            'total_att',
            'total_made',
            'total_fg_percentage',
            'ft_att',
            'ft_made',
            'ft_percentage',
            'reb_off',
            'reb_def',
            'reb_total',
            'assists',
            'steals',
            'blocks',
            'turnovers',
            'total_shots_att',
            'total_shots_made',
            'total_shots_percentage',
            'total_points',
            'minutes_played',
            'minutes',
            'fouls',
            'is_ejected',
            'is_disqualified',
            'total_points'
        ]

    def get_is_starter(self, instance):
        if type(instance) != Stat or not instance.is_player:
            return None
        
        return instance.player_stats.is_starter
    
    def get_minutes_played(self, instance):
        if type(instance) != Stat or not instance.is_player:
            return None
        
        return instance.player_stats.minutes_played