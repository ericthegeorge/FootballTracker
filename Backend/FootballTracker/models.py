from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
# from django_countries import 
# Create your models here.

# EXAMPLE HERE YOUR MOST WELCOME:

'''
class Card(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255, blank=True, null=True)
    object_id = models.TextField(blank=True, null=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="decks")
'''

# country field for nationality example use:
'''
{{ player.nationality.name }}  <!-- e.g., "Germany" -->
{{ player.nationality.code }}  <!-- e.g., "DE" -->
{{ player.nationality.flag }}  <!-- 🌍 URL or emoji-like flag -->

'''

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/profile_images/<username>/<filename>
    return f'profile_images/{instance.user.username}/{filename}'

# specifically for pf image to Django premade user relation
class UserProfile(models.Model):
    # includes username, password, email, and more
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="profile")
    profile_image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"

class League(models.Model):
    name = models.CharField(primary_key=True, max_length=100)


def team_image_upload_path(instance, filename):
    return f'profile_images/teams/{instance.name}/{filename}'


class Team(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    home_ground = models.CharField(max_length=100)
    manager_dob = models.DateField()
    manager_name = models.CharField(max_length=100)
    manager_seasons_headed = models.IntegerField()
    manager_date_joined = models.DateField()
    image = models.CharField(max_length=255)


class Player(models.Model):
    player_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    dob = models.DateField()
    minutes_played = models.IntegerField()
    matches_played = models.IntegerField()
    market_value = models.FloatField()
    preferred_foot = models.CharField(max_length=10)
    height = models.FloatField()
    yellow_cards = models.IntegerField()
    red_cards = models.IntegerField()
    playing_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name='playing_players')
    owning_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name='owning_players')
    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['player_id', 'name'], name='unique_player_id_name')
    #     ]


class OutfieldPlayer(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE, primary_key=True, related_name='outfield_players')
    goals = models.IntegerField()
    assists = models.IntegerField()
    penalties_scored = models.IntegerField()


class Goalkeeper(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE, primary_key=True, related_name='goalkeeper_players')
    goals_conceded = models.IntegerField()
    goals_saved = models.IntegerField()
    clean_sheets = models.IntegerField()
    penalties_saved = models.IntegerField()


class PlayerNationality(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    nationality = CountryField(default='US')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['player', 'nationality'], name='unique_player_nationality')
        ]

class Position(models.TextChoices):
    GOALKEEPER = 'GK', 'Goalkeeper'
    DEFENDER = 'DF', 'Defender'
    MIDFIELDER = 'MF', 'Midfielder'
    FORWARD = 'FW', 'Forward'

class PlayerPosition(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    position = models.CharField(max_length=2,
                                choices=Position.choices,
                                default=Position.MIDFIELDER)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['player', 'position'], name='unique_player_position')
        ]



class ManagerNationality(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    nationality = CountryField(default='US')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['team', 'nationality'], name='unique_team_manager_nationality')
        ]



class Match(models.Model):
    match_id = models.AutoField(primary_key=True)
    date = models.DateField()
    location = models.CharField(max_length=100)
    start_time = models.TimeField()
    referee_name = models.CharField(max_length=100)
    end_time = models.TimeField()



class MatchRefereeNationality(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    nationality = CountryField(default='US')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['match', 'nationality'], name='unique_match_referee_nationality')
        ]



class TeamMatchData(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    stoppage_time = models.IntegerField()
    had_extra_time = models.BooleanField()
    had_penalties = models.BooleanField()
    goals_conceded = models.IntegerField()
    saves = models.IntegerField()
    offsides = models.IntegerField()
    goals_scored = models.IntegerField()
    shots_on_target = models.IntegerField()
    possession_percentage = models.FloatField()
    completed_passes = models.IntegerField()
    total_passes = models.IntegerField()
    match_outcome = models.CharField(max_length=10)
    team_formation = models.CharField(max_length=20)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['match', 'team'], name='unique_match_data_match_team')
        ]


class PlayerMatchData(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    stoppage_time = models.IntegerField()
    had_extra_time = models.BooleanField()
    had_penalties = models.BooleanField()
    assists = models.IntegerField()
    completed_passes = models.IntegerField()
    total_passes = models.IntegerField()
    minutes_played = models.IntegerField()
    goals_scored = models.IntegerField()
    shots_on_target = models.IntegerField()
    total_shots = models.IntegerField()
    fouls = models.IntegerField()
    goals_conceded = models.IntegerField()
    saves = models.IntegerField()
    position = models.CharField(max_length=2,
                                choices=Position.choices,
                                default=Position.MIDFIELDER)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['match', 'player'], name='unique_player_match_data_match_player')
        ]

class PlayerPlaysForTeam(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    shirt_number = models.IntegerField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['player', 'team'], name='unique_player_plays_for_team_player_team')
        ]


class TeamPlaysInLeague(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['team', 'league'], name='unique_team_plays_in_league_team_league')
        ]


class MatchHeldInLeague(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['match', 'league'], name='unique_match_held_in_league_match_league')
        ]


class TeamMatchDataGoal(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    goal_type = models.CharField(max_length=50)
    assisting_player = models.CharField(max_length=100)
    time_scored = models.TimeField()
    scoring_player = models.CharField(max_length=100)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['match', 'team', 'goal_type', 'assisting_player', 'time_scored', 'scoring_player'], name='unique_team_match_data_goal')
        ]


class TeamMatchDataBooking(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    time_booked = models.TimeField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['match', 'team', 'time_booked'], name='unique_team_match_data_booking')
        ]


class TeamMatchDataSubstitution(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player_on = models.CharField(max_length=100)
    player_off = models.CharField(max_length=100)
    time_subbed = models.TimeField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['match', 'team', 'player_on', 'player_off', 'time_subbed'], name='unique_team_match_data_substitution')
        ]


class PlayerMatchDataGoal(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    goal_type = models.CharField(max_length=50)
    assisting_player = models.CharField(max_length=100)
    time_scored = models.TimeField()
    scoring_player = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['match', 'player', 'goal_type', 'assisting_player', 'time_scored', 'scoring_player'], name='unique_player_match_data_goal')
        ]

class PlayerMatchDataBooking(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    time_booked = models.TimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['match', 'player', 'time_booked'], name='unique_player_match_data_booking')
        ]


class PlayerMatchDataSubstitution(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    player_on = models.CharField(max_length=100)
    player_off = models.CharField(max_length=100)
    time_subbed = models.TimeField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['match', 'player', 'player_on', 'player_off', 'time_subbed'], name='unique_player_match_data_substitution')
        ]


class AdminCanEditTeamMatchData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team_match_data = models.ForeignKey(TeamMatchData, on_delete=models.CASCADE)
    # team = models.ForeignKey(Team, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'team_match_data'], name='unique_admin_edit_team_match_data')
        ]

class AdminCanEditPlayerMatchData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    player_match_data = models.ForeignKey(PlayerMatchData, on_delete=models.CASCADE)
    # player = models.ForeignKey(Player, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'player_match_data'], name='unique_admin_edit_player_match_data')
        ]

class AdminCanEditPlayer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'player'], name='unique_admin_edit_player')
        ]

class AdminCanEditTeam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'team'], name='unique_admin_edit_team')
        ]

class AdminCanEditMatch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'match'], name='unique_admin_edit_match')
        ]


class AdminCanEditLeague(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'league'], name='unique_admin_edit_league')
        ]

''''''

class UserCanBrowseTeamMatchData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team_match_data = models.ForeignKey(TeamMatchData, on_delete=models.CASCADE)
    # team = models.ForeignKey(Team, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'team_match_data',], name='unique_user_browse_team_match_data')
        ]

class UserCanBrowsePlayerMatchData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    player_match_data = models.ForeignKey(PlayerMatchData, on_delete=models.CASCADE)
    # player = models.ForeignKey(Player, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'player_match_data'], name='unique_user_browse_player_match_data')
        ]

class UserCanBrowsePlayer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'player'], name='unique_user_browse_player')
        ]

class UserCanBrowseTeam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'team'], name='unique_user_browse_team')
        ]

class UserCanBrowseMatch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'match'], name='unique_user_browse_match')
        ]


class UserCanBrowseLeague(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'league'], name='unique_user_browse_league')
        ]

''''''

class TeamMatch(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['team', 'match'], name='unique_team_match')
        ]

class PlayerMatch(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['player', 'match'], name='unique_player_match')
        ]