from django.db import models
from django.contrib.auth.models import User
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

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/profile_images/<username>/<filename>
    return f'profile_images/{instance.user.username}/{filename}'


class UserProfile(models.Model):
    # includes username, password, email, and more
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"

class League(models.Model):
    name = models.CharField(primary_key=True, max_length=100)


class Team(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    home_ground = models.CharField(max_length=100)
    manager_dob = models.DateField()
    manager_name = models.CharField(max_length=100)
    manager_seasons_headed = models.IntegerField()
    manager_date_joined = models.DateField()


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


class OutfieldPlayer(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE, primary_key=True)
    goals = models.IntegerField()
    assists = models.IntegerField()
    penalties_scored = models.IntegerField()


class Goalkeeper(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE, primary_key=True)
    goals_conceded = models.IntegerField()
    goals_saved = models.IntegerField()
    clean_sheets = models.IntegerField()
    penalties_saved = models.IntegerField()


class PlayerNationality(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    nationality = models.CharField(max_length=50)


class PlayerPosition(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    position = models.CharField(max_length=50)


class ManagerNationality(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    nationality = models.CharField(max_length=50)


class Match(models.Model):
    match_id = models.AutoField(primary_key=True)
    date = models.DateField()
    location = models.CharField(max_length=100)
    start_time = models.TimeField()
    referee_name = models.CharField(max_length=100)
    end_time = models.TimeField()



class MatchRefereeNationality(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    nationality = models.CharField(max_length=50)


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
    position = models.CharField(max_length=50)


class PlayerPlaysForTeam(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    shirt_number = models.IntegerField()


class TeamPlaysInLeague(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)


class MatchHeldInLeague(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)


class TeamMatchDataGoal(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    goal_type = models.CharField(max_length=50)
    assisting_player = models.CharField(max_length=100)
    time_scored = models.TimeField()
    scoring_player = models.CharField(max_length=100)


class TeamMatchDataBooking(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    time_booked = models.TimeField()


class TeamMatchDataSubstitution(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player_on = models.CharField(max_length=100)
    player_off = models.CharField(max_length=100)
    time_subbed = models.TimeField()


class PlayerMatchDataGoal(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    goal_type = models.CharField(max_length=50)
    assisting_player = models.CharField(max_length=100)
    time_scored = models.TimeField()
    scoring_player = models.CharField(max_length=100)


class PlayerMatchDataBooking(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    time_booked = models.TimeField()


class PlayerMatchDataSubstitution(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    player_on = models.CharField(max_length=100)
    player_off = models.CharField(max_length=100)
    time_subbed = models.TimeField()


class AdminCanEditTeamMatchData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

class AdminCanEditPlayerMatchData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)


class AdminCanEditPlayer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)


class AdminCanEditTeam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)


class AdminCanEditMatch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)


class AdminCanEditLeague(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)


class UserCanBrowseMatchData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


class UserCanBrowsePlayer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)


class UserCanBrowseTeam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)


class UserCanBrowseMatch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)


class UserCanBrowseLeague(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)


class TeamMatch(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)


class PlayerMatch(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
