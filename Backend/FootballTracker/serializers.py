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

'''
EXAMPLE SERIALIZERS


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'
class UserProfileSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many =True)
    class Meta:
        model = UserProfile
        fields = ['user', 'cards']
        # no other user details
'''

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    picture = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'picture']
        extra_kwargs = {'password': {'write_only':True}}
    
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

        return data
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'picture']

class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

class OutfieldPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutfieldPlayer
        fields = '__all__'

class GoalkeeperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goalkeeper
        fields = '__all__'

class PlayerNationalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerNationality
        fields = '__all__'

class PlayerPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerPosition
        fields = '__all__'

class ManagerNationalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerNationality
        fields = '__all__'

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'

class MatchRefereeNationalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchRefereeNationality
        fields = '__all__'

class TeamMatchDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMatchData
        fields = '__all__'

class PlayerMatchDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerMatchData
        fields = '__all__'

class PlayerPlaysForTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerPlaysForTeam
        fields = '__all__'

class TeamPlaysInLeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamPlaysInLeague
        fields = '__all__'

class MatchHeldInLeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchHeldInLeague
        fields = '__all__'

class TeamMatchDataGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMatchDataGoal
        fields = '__all__'

class TeamMatchDataBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMatchDataBooking
        fields = '__all__'

class TeamMatchDataSubstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMatchDataSubstitution
        fields = '__all__'

class PlayerMatchDataGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerMatchDataGoal
        fields = '__all__'

class PlayerMatchDataBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerMatchDataBooking
        fields = '__all__'

class PlayerMatchDataSubstitutionSerializer(serializers.ModelSerializer):
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
