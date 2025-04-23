from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import (
    UserProfile, League, Team, Player, OutfieldPlayer, Goalkeeper,
    PlayerNationality, PlayerPosition, ManagerNationality, Match,
    MatchRefereeNationality, TeamMatchData, PlayerMatchData,
    PlayerPlaysForTeam, TeamPlaysInLeague, MatchHeldInLeague,
    TeamMatchDataGoal, TeamMatchDataBooking, TeamMatchDataSubstitution,
    PlayerMatchDataGoal, PlayerMatchDataBooking, PlayerMatchDataSubstitution,
    AdminCanEditTeamMatchData, AdminCanEditPlayerMatchData, AdminCanEditPlayer,
    AdminCanEditTeam, AdminCanEditMatch, AdminCanEditLeague,
    UserCanBrowseTeamMatchData, UserCanBrowsePlayerMatchData, UserCanBrowsePlayer,
    UserCanBrowseTeam, UserCanBrowseMatch, UserCanBrowseLeague,
    TeamMatch, PlayerMatch
)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    picture = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'picture', 'is_staff']
        # read_only_fields = ['is_staff']
        extra_kwargs = {'password': {'write_only':True}, 'is_staff': {'write_only':True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            # picture=validated_data['picture'],
        )
        # picture = validated_data['picture']
        picture = validated_data.pop('picture', None)  # <- pop to prevent issues
        if picture:
                profile, _ = UserProfile.objects.get_or_create(user=user)
                profile.picture = picture
                profile.save()
        is_staff = validated_data.pop('is_staff', None)
        user.is_staff = is_staff
        user.save()
        if (is_staff):
            # here make relation instances of this admin with all teams, players, matches, and match_data
            # except for leagues
            # relevant models: AdminCanEditTeamMatchData, AdminCanEditPlayerMatchData,
            # AdminCanEditPlayer, AdminCanEditTeam, AdminCanEditMatch, AdminCanEditLeague...
        # Grant access to edit all teams
            for team in Team.objects.all():
                AdminCanEditTeam.objects.create(user=user, team=team)

            # Grant access to edit all players
            for player in Player.objects.all():
                AdminCanEditPlayer.objects.create(user=user, player=player)

            # Grant access to edit all matches
            for match in Match.objects.all():
                AdminCanEditMatch.objects.create(user=user, match=match)

            # Grant access to edit all team match data
            for team_data in TeamMatchData.objects.all():
                AdminCanEditTeamMatchData.objects.create(user=user, team_match_data=team_data)

            # Grant access to edit all player match data
            for player_data in PlayerMatchData.objects.all():
                AdminCanEditPlayerMatchData.objects.create(user=user, player_match_data=player_data)
        # grant access to view all
        for team in Team.objects.all():
            UserCanBrowseTeam.objects.create(user=user, team=team)

        # Grant access to view all players
        for player in Player.objects.all():
            UserCanBrowsePlayer.objects.create(user=user, player=player)

        # Grant access to view all matches
        for match in Match.objects.all():
            UserCanBrowseMatch.objects.create(user=user, match=match)

        # Grant access to view all team match data
        for team_data in TeamMatchData.objects.all():
            UserCanBrowseTeamMatchData.objects.create(user=user, team_match_data=team_data)

        # Grant access to view all player match data
        for player_data in PlayerMatchData.objects.all():
            UserCanBrowsePlayerMatchData.objects.create(user=user, player_match_data=player_data)

        # Grant access to view all league data
        for league in League.objects.all():
            UserCanBrowseLeague.objects.create(user=user, league=league)

        
        user.save()
        print(user.is_staff)
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError("Username and password are required.")

        user = User.objects.filter(username=username).first()

        if user is None or not user.check_password(password):
            raise serializers.ValidationError("Invalid username or password.")
        is_staff = user.is_staff
        if (is_staff):
            # here make relation instances of this admin with all teams, players, matches, and match_data
            # except for leagues
            # relevant models: AdminCanEditTeamMatchData, AdminCanEditPlayerMatchData,
            # AdminCanEditPlayer, AdminCanEditTeam, AdminCanEditMatch, AdminCanEditLeague...
        # Grant access to edit all teams
            for team in Team.objects.all():
                AdminCanEditTeam.objects.get_or_create(user=user, team=team)

            # Grant access to edit all players
            for player in Player.objects.all():
                AdminCanEditPlayer.objects.get_or_create(user=user, player=player)

            # Grant access to edit all matches
            for match in Match.objects.all():
                AdminCanEditMatch.objects.get_or_create(user=user, match=match)

            # Grant access to edit all team match data
            for team_data in TeamMatchData.objects.all():
                AdminCanEditTeamMatchData.objects.get_or_create(user=user, team_match_data=team_data)

            # Grant access to edit all player match data
            for player_data in PlayerMatchData.objects.all():
                AdminCanEditPlayerMatchData.objects.get_or_create(user=user, player_match_data=player_data)
        # grant access to view all
        for team in Team.objects.all():
            UserCanBrowseTeam.objects.get_or_create(user=user, team=team)

        # Grant access to view all players
        for player in Player.objects.all():
            UserCanBrowsePlayer.objects.get_or_create(user=user, player=player)

        # Grant access to view all matches
        for match in Match.objects.all():
            UserCanBrowseMatch.objects.get_or_create(user=user, match=match)

        # Grant access to view all team match data
        for team_data in TeamMatchData.objects.all():
            UserCanBrowseTeamMatchData.objects.get_or_create(user=user, team_match_data=team_data)

        # Grant access to view all player match data
        for player_data in PlayerMatchData.objects.all():
            UserCanBrowsePlayerMatchData.objects.get_or_create(user=user, player_match_data=player_data)

        # Grant access to view all league data
        for league in League.objects.all():
            UserCanBrowseLeague.objects.get_or_create(user=user, league=league)


        return data
    
class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'picture']

class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    # league = LeagueSerializer(read_only=True)
    # league_id = serializers.PrimaryKeyRelatedField(
    #     queryset=League.objects.all(), source='league', write_only=True, required=False
    # )
    class Meta:
        model = Team
        fields = '__all__'

class PlayerNationalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerNationality
        fields = '__all__'

class PlayerPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerPosition
        fields = '__all__'

class PlayerSerializer(serializers.ModelSerializer):
    nationality = PlayerNationalitySerializer(read_only=True)
    nationality_id = serializers.PrimaryKeyRelatedField(
        queryset=PlayerNationality.objects.all(), source='nationality', write_only=True, required=False
    )
    position = PlayerPositionSerializer(read_only=True)
    position_id = serializers.PrimaryKeyRelatedField(
        queryset=PlayerPosition.objects.all(), source='position', write_only=True, required=False
    )
    class Meta:
        model = Player
        fields = '__all__'

class OutfieldPlayerSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(read_only=True)
    player_id = serializers.PrimaryKeyRelatedField(
        queryset=Player.objects.all(), source='player', write_only=True, required=False
    )
    class Meta:
        model = OutfieldPlayer
        fields = '__all__'

class GoalkeeperSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(read_only=True)
    player_id = serializers.PrimaryKeyRelatedField(
        queryset=Player.objects.all(), source='player', write_only=True, required=False
    )
    class Meta:
        model = Goalkeeper
        fields = '__all__'

class ManagerNationalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerNationality
        fields = '__all__'

class MatchSerializer(serializers.ModelSerializer):
    home_team = TeamSerializer(read_only=True)
    away_team = TeamSerializer(read_only=True)
    home_team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(), source='home_team', write_only=True, required=False
    )
    away_team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(), source='away_team', write_only=True, required=False
    )
    class Meta:
        model = Match
        fields = '__all__'

class MatchRefereeNationalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchRefereeNationality
        fields = '__all__'

class TeamMatchDataSerializer(serializers.ModelSerializer):
    match = MatchSerializer(read_only=True)
    match_id = serializers.PrimaryKeyRelatedField(
        queryset=Match.objects.all(), source='match', write_only=True, required=False
    )
    team = TeamSerializer(read_only=True)
    team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(), source='team', write_only=True, required=False
    )
    class Meta:
        model = TeamMatchData
        fields = '__all__'

class PlayerMatchDataSerializer(serializers.ModelSerializer):
    match = MatchSerializer(read_only=True)
    match_id = serializers.PrimaryKeyRelatedField(
        queryset=Match.objects.all(), source='match', write_only=True, required=False
    )
    player = PlayerSerializer(read_only=True)
    player_id = serializers.PrimaryKeyRelatedField(
        queryset=Player.objects.all(), source='player', write_only=True, required=False
    )
    class Meta:
        model = PlayerMatchData
        fields = '__all__'

class PlayerPlaysForTeamSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(read_only=True)
    player_id = serializers.PrimaryKeyRelatedField(
        queryset=Player.objects.all(), source='player', write_only=True, required=False
    )
    team = TeamSerializer(read_only=True)
    team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(), source='team', write_only=True, required=False
    )
    class Meta:
        model = PlayerPlaysForTeam
        fields = '__all__'

class TeamPlaysInLeagueSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(), source='team', write_only=True, required=False
    )
    league = LeagueSerializer(read_only=True)
    league_id = serializers.PrimaryKeyRelatedField(
        queryset=League.objects.all(), source='league', write_only=True, required=False
    )
    class Meta:
        model = TeamPlaysInLeague
        fields = '__all__'

class MatchHeldInLeagueSerializer(serializers.ModelSerializer):
    match = MatchSerializer(read_only=True)
    match_id = serializers.PrimaryKeyRelatedField(
        queryset=Match.objects.all(), source='match', write_only=True, required=False
    )
    league = LeagueSerializer(read_only=True)
    league_id = serializers.PrimaryKeyRelatedField(
        queryset=League.objects.all(), source='league', write_only=True, required=False
    )
    class Meta:
        model = MatchHeldInLeague
        fields = '__all__'

class TeamMatchDataGoalSerializer(serializers.ModelSerializer):
    team_match_data = TeamMatchDataSerializer(read_only=True)
    team_match_data_id = serializers.PrimaryKeyRelatedField(
        queryset=TeamMatchData.objects.all(), source='team_match_data', write_only=True, required=False
    )
    class Meta:
        model = TeamMatchDataGoal
        fields = '__all__'

class TeamMatchDataBookingSerializer(serializers.ModelSerializer):
    team_match_data = TeamMatchDataSerializer(read_only=True)
    team_match_data_id = serializers.PrimaryKeyRelatedField(
        queryset=TeamMatchData.objects.all(), source='team_match_data', write_only=True, required=False
    )
    class Meta:
        model = TeamMatchDataBooking
        fields = '__all__'

class TeamMatchDataSubstitutionSerializer(serializers.ModelSerializer):
    team_match_data = TeamMatchDataSerializer(read_only=True)
    team_match_data_id = serializers.PrimaryKeyRelatedField(
        queryset=TeamMatchData.objects.all(), source='team_match_data', write_only=True, required=False
    )
    class Meta:
        model = TeamMatchDataSubstitution
        fields = '__all__'

class PlayerMatchDataGoalSerializer(serializers.ModelSerializer):
    player_match_data = PlayerMatchDataSerializer(read_only=True)
    player_match_data_id = serializers.PrimaryKeyRelatedField(
        queryset=PlayerMatchData.objects.all(), source='player_match_data', write_only=True, required=False
    )
    class Meta:
        model = PlayerMatchDataGoal
        fields = '__all__'

class PlayerMatchDataBookingSerializer(serializers.ModelSerializer):
    player_match_data = PlayerMatchDataSerializer(read_only=True)
    player_match_data_id = serializers.PrimaryKeyRelatedField(
        queryset=PlayerMatchData.objects.all(), source='player_match_data', write_only=True, required=False
    )
    class Meta:
        model = PlayerMatchDataBooking
        fields = '__all__'

class PlayerMatchDataSubstitutionSerializer(serializers.ModelSerializer):
    player_match_data = PlayerMatchDataSerializer(read_only=True)
    player_match_data_id = serializers.PrimaryKeyRelatedField(
        queryset=PlayerMatchData.objects.all(), source='player_match_data', write_only=True, required=False
    )
    class Meta:
        model = PlayerMatchDataSubstitution
        fields = '__all__'

class AdminCanEditTeamMatchDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminCanEditTeamMatchData
        fields = '__all__'

class AdminCanEditPlayerMatchDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminCanEditPlayerMatchData
        fields = '__all__'

class AdminCanEditPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminCanEditPlayer
        fields = '__all__'

class AdminCanEditTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminCanEditTeam
        fields = '__all__'

class AdminCanEditMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminCanEditMatch
        fields = '__all__'

class AdminCanEditLeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminCanEditLeague
        fields = '__all__'

class UserCanBrowseTeamMatchDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCanBrowseTeamMatchData
        fields = '__all__'

class UserCanBrowsePlayerMatchDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCanBrowsePlayerMatchData
        fields = '__all__'

class UserCanBrowsePlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCanBrowsePlayer
        fields = '__all__'

class UserCanBrowseTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCanBrowseTeam
        fields = '__all__'

class UserCanBrowseMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCanBrowseMatch
        fields = '__all__'

class UserCanBrowseLeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCanBrowseLeague
        fields = '__all__'

class TeamMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMatch
        fields = '__all__'

class PlayerMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerMatch
        fields = '__all__'
