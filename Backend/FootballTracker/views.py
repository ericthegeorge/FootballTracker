from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
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
from .serializers import (
    RegisterSerializer, LoginSerializer, UserProfileSerializer, LeagueSerializer, TeamSerializer, PlayerSerializer, OutfieldPlayerSerializer, GoalkeeperSerializer,
    PlayerNationalitySerializer, PlayerPositionSerializer, ManagerNationalitySerializer, MatchSerializer,
    MatchRefereeNationalitySerializer, TeamMatchDataSerializer, PlayerMatchDataSerializer,
    PlayerPlaysForTeamSerializer, TeamPlaysInLeagueSerializer, MatchHeldInLeagueSerializer,
    TeamMatchDataGoalSerializer, TeamMatchDataBookingSerializer, TeamMatchDataSubstitutionSerializer,
    PlayerMatchDataGoalSerializer, PlayerMatchDataBookingSerializer, PlayerMatchDataSubstitutionSerializer,
    AdminCanEditTeamMatchDataSerializer, AdminCanEditPlayerMatchDataSerializer, AdminCanEditPlayerSerializer,
    AdminCanEditTeamSerializer, AdminCanEditMatchSerializer, AdminCanEditLeagueSerializer,
    UserCanBrowseTeamMatchDataSerializer, UserCanBrowsePlayerMatchDataSerializer, UserCanBrowsePlayerSerializer,
    UserCanBrowseTeamSerializer, UserCanBrowseMatchSerializer, UserCanBrowseLeagueSerializer,
    TeamMatchSerializer, PlayerMatchSerializer, UserSerializer
)

import urllib.parse
from rest_framework.parsers import MultiPartParser, FormParser

# from rest_framework.permissions import AllowAny


# class RegisterView(APIView):
#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        
#         print(serializer.errors)  # <--- ADD THIS
#         return Response({
#             'token': token.key,
#             'username': user.username,
#             'is_staff': user.is_staff
#         })

class RegisterView(APIView):
    # permission_classes = [AllowAny]
    def post(self, request):
        print(request.data)
        print(request.FILES.get('picture'))
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            # Save the user first
            user = serializer.save()

            # Manually handle profile image
            picture = request.FILES.get('picture')
            if picture:
                # Assuming the UserProfile model has a FileField for profile_image
                profile, created = UserProfile.objects.get_or_create(user=user, defaults={'profile_image': picture})
                # You can also save the profile object if needed:
                profile.save()

            # Generate token
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'token': token.key,
                'username': user.username,
                'is_staff': user.is_staff
            }, status=status.HTTP_201_CREATED)

        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
    'token': token.key,
    'username': user.username,
    'is_staff': user.is_staff
}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        username = request.query_params.get('username')
        try:
            print(username)
            user = User.objects.get(username=username)
            user_profile = UserProfile.objects.get(user=user)
            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({"error": "User not found"}, status=404)


    def put(self, request):
        username = request.query_params.get('username')
        if not username:
            return Response({'error': 'Username required'}, status=400)

        try:
            user = User.objects.get(username=username)
            user_profile = UserProfile.objects.get(user=user)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=404)

        # Build a simple dict out of request.data + request.FILES
        data = {}

        # Nested user fields:
        user_data = {}
        for field in ('username', 'email', 'first_name', 'last_name'):
            key = f'user.{field}'
            if key in request.data:
                # .get() gives you the *first* value in the QueryDict list
                user_data[field] = request.data.get(key)[0]  # Get the first value

        if user_data:
            data['user'] = user_data

        # Profile image, if any
        if 'profile_image' in request.FILES:
            data['profile_image'] = request.FILES['profile_image']
        
        print("Request data:", request.data)
        print("Request FILES:", request.FILES)
        print("Cleaned user_data:", user_data)
        print("Cleaned profile image:", data.get('profile_image'))

        # Now run the serializer
        serializer = UserProfileSerializer(
            user_profile,
            data=data,
            partial=True,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request):
        username = request.query_params.get('username')
        try:
            print(username)
            user = User.objects.get(username=username)
            user_profile = UserProfile.objects.get(user=user)
            user_profile.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)


class UserView(APIView):

    def get(self, request):
        # Get the current authenticated user
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        # Get the current authenticated user
        username = request.query_params.get('username')
        user = User.objects.get(username=username)
        print(user)
        print(request.data)
        # Serialize the data to validate and save
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            print("Serializer is valid. Saving data...")  # Debugging message
            updated_user = serializer.save()  # Save the updated user data
            updated_user.refresh_from_db()

            # Check if the save was successful
            if updated_user:
                print("User updated successfully")
                print(updated_user)
                return Response(serializer.data)  # Return updated user data
            else:
                print("Failed to update the user")
                return Response({"error": "Failed to update user"}, status=400)
        else:
            print("Serializer is not valid")
            print(serializer.errors)  # Print errors for debugging
            return Response(serializer.errors, status=400)



class LeagueView(APIView):
    def get(self, request):
        leagues = League.objects.all()
        serializer = LeagueSerializer(leagues, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LeagueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, name):
        try:
            league = League.objects.get(name=name)
            serializer = LeagueSerializer(league, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except League.DoesNotExist:
            return Response({'error': 'League not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request,name):
        try:
            league = League.objects.get(name=name)
            league.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except League.DoesNotExist:
            return Response({'error': 'League not found'}, status=status.HTTP_404_NOT_FOUND)

class TeamView(APIView):
    def get(self, request):
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, name):
        try:
            decoded_name = urllib.parse.unquote(name)
            team = Team.objects.get(name=decoded_name)
            serializer = TeamSerializer(team, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Team.DoesNotExist:
            return Response({'error': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, name):
        # print(name)
        try:
            decoded_name = urllib.parse.unquote(name)
            print(decoded_name)
            team = Team.objects.get(name=decoded_name)
            team.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Team.DoesNotExist:
            return Response({'error': 'Team not found'}, status=status.HTTP_406_NOT_ACCEPTABLE)

class PlayerView(APIView):
    def get(self, request):
        players = Player.objects.all()
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            player = Player.objects.get(pk=pk)
            serializer = PlayerSerializer(player, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Player.DoesNotExist:
            return Response({'error': 'Player not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            player = Player.objects.get(pk=pk)
            player.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Player.DoesNotExist:
            return Response({'error': 'Player not found'}, status=status.HTTP_404_NOT_FOUND)

class OutfieldPlayerView(APIView):
    def get(self, request):
        outfield_players = OutfieldPlayer.objects.all()
        serializer = OutfieldPlayerSerializer(outfield_players, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OutfieldPlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            outfield_player = OutfieldPlayer.objects.get(pk=pk)
            serializer = OutfieldPlayerSerializer(outfield_player, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except OutfieldPlayer.DoesNotExist:
            return Response({'error': 'Outfield player not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            outfield_player = OutfieldPlayer.objects.get(pk=pk)
            outfield_player.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except OutfieldPlayer.DoesNotExist:
            return Response({'error': 'Outfield player not found'}, status=status.HTTP_404_NOT_FOUND)

class GoalkeeperView(APIView):
    def get(self, request):
        goalkeepers = Goalkeeper.objects.all()
        serializer = GoalkeeperSerializer(goalkeepers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GoalkeeperSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            goalkeeper = Goalkeeper.objects.get(pk=pk)
            serializer = GoalkeeperSerializer(goalkeeper, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Goalkeeper.DoesNotExist:
            return Response({'error': 'Goalkeeper not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            goalkeeper = Goalkeeper.objects.get(pk=pk)
            goalkeeper.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Goalkeeper.DoesNotExist:
            return Response({'error': 'Goalkeeper not found'}, status=status.HTTP_404_NOT_FOUND)

class PlayerNationalityView(APIView):
    def get(self, request):
        nationalities = PlayerNationality.objects.all()
        serializer = PlayerNationalitySerializer(nationalities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlayerNationalitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            nationalities = PlayerNationality.objects.get(pk=pk)
            serializer = PlayerNationalitySerializer(nationalities, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PlayerNationality.DoesNotExist:
            return Response({'error': 'Player Nationality not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            nationalities = PlayerNationality.objects.get(pk=pk)
            nationalities.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PlayerNationality.DoesNotExist:
            return Response({'error': 'Player Nationality not found'}, status=status.HTTP_404_NOT_FOUND)
        
class PlayerPositionView(APIView):
    def get(self, request):
        positions = PlayerPosition.objects.all()
        serializer = PlayerPositionSerializer(positions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlayerPositionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            positions = PlayerPosition.objects.get(pk=pk)
            serializer = PlayerPositionSerializer(positions, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PlayerPosition.DoesNotExist:
            return Response({'error': 'Player Position not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, pk):
        try:
            positions = PlayerPosition.objects.get(pk=pk)
            positions.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PlayerPosition.DoesNotExist:
            return Response({'error': 'Player Position not found'}, status=status.HTTP_404_NOT_FOUND)
    
class ManagerNationalityView(APIView):
    def get(self, request):
        nationalities = ManagerNationality.objects.all()
        serializer = ManagerNationalitySerializer(nationalities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ManagerNationalitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            nationalities = ManagerNationality.objects.get(pk=pk)
            serializer = ManagerNationalitySerializer(nationalities, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ManagerNationality.DoesNotExist:
            return Response({'error': 'Manager Nationality not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            nationalities = ManagerNationality.objects.get(pk=pk)
            nationalities.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ManagerNationality.DoesNotExist:
            return Response({'error': 'Manager Nationality not found'}, status=status.HTTP_404_NOT_FOUND)

class MatchView(APIView):
    def get(self, request):
        matches = Match.objects.all()
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, match_id):
        try:
            matches = Match.objects.get(match_id=match_id)
            serializer = MatchSerializer(matches, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Match.DoesNotExist:
            return Response({'error': 'Match not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, match_id):
        try:
            matches = Match.objects.get(match_id=match_id)
            matches.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Match.DoesNotExist:
            return Response({'error': 'Match not found'}, status=status.HTTP_404_NOT_FOUND)
        
class MatchRefereeNationalityView(APIView):
    def get(self, request):
        nationalities = MatchRefereeNationality.objects.all()
        serializer = MatchRefereeNationalitySerializer(nationalities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MatchRefereeNationalitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            nationalities = MatchRefereeNationality.objects.get(pk=pk)
            serializer = MatchRefereeNationalitySerializer(nationalities, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except MatchRefereeNationality.DoesNotExist:
            return Response({'error': 'Match Referee Nationality not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, pk):
        try:
            nationalities = MatchRefereeNationality.objects.get(pk=pk)
            nationalities.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except MatchRefereeNationality.DoesNotExist:
            return Response({'error': 'Match Referee Nationality not found'}, status=status.HTTP_404_NOT_FOUND)

class TeamMatchDataView(APIView):
    def get(self, request):
        team_match_data = TeamMatchData.objects.all()
        serializer = TeamMatchDataSerializer(team_match_data, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TeamMatchDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            team_match_data = TeamMatchData.objects.get(pk=pk)
            serializer = TeamMatchDataSerializer(team_match_data, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except TeamMatchData.DoesNotExist:
            return Response({'error': 'Team Match Data not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            team_match_data = TeamMatchData.objects.get(pk=pk)
            team_match_data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except TeamMatchData.DoesNotExist:
            return Response({'error': 'Team Match Data not found'}, status=status.HTTP_404_NOT_FOUND)
    
class PlayerMatchDataView(APIView):
    def get(self, request):
        player_match_data = PlayerMatchData.objects.all()
        serializer = PlayerMatchDataSerializer(player_match_data, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlayerMatchDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            player_match_data = PlayerMatchData.objects.get(pk=pk)
            serializer = PlayerMatchDataSerializer(player_match_data, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PlayerMatchData.DoesNotExist:
            return Response({'error': 'Player Match Data not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            player_match_data = PlayerMatchData.objects.get(pk=pk)
            player_match_data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PlayerMatchData.DoesNotExist:
            return Response({'error': 'Player Match Data not found'}, status=status.HTTP_404_NOT_FOUND)
    
class PlayerPlaysForTeamView(APIView):
    def get(self, request):
        player_plays_for_team = PlayerPlaysForTeam.objects.all()
        serializer = PlayerPlaysForTeamSerializer(player_plays_for_team, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlayerPlaysForTeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            player_plays_for_team = PlayerPlaysForTeam.objects.get(pk=pk)
            serializer = PlayerPlaysForTeamSerializer(player_plays_for_team, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PlayerPlaysForTeam.DoesNotExist:
            return Response({'error': 'Player Plays For Team not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            player_plays_for_team = PlayerPlaysForTeam.objects.get(pk=pk)
            player_plays_for_team.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PlayerPlaysForTeam.DoesNotExist:
            return Response({'error': 'Player Plays For Team not found'}, status=status.HTTP_404_NOT_FOUND)
    
class TeamPlaysInLeagueView(APIView):
    def get(self, request):
        team_plays_in_league = TeamPlaysInLeague.objects.all()
        # print(team_plays_in_league)
        if not team_plays_in_league:
            return Response({"error": "No teams or leagues found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TeamPlaysInLeagueSerializer(team_plays_in_league, many=True)
        # print(serializer.data)
        return Response(serializer.data)

    def post(self, request):
        serializer = TeamPlaysInLeagueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            team_plays_in_league = TeamPlaysInLeague.objects.get(pk=pk)
            serializer = TeamPlaysInLeagueSerializer(team_plays_in_league, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except TeamPlaysInLeague.DoesNotExist:
            return Response({'error': 'Team Plays In League not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            team_plays_in_league = TeamPlaysInLeague.objects.get(pk=pk)
            team_plays_in_league.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except TeamPlaysInLeague.DoesNotExist:
            return Response({'error': 'Team Plays In League not found'}, status=status.HTTP_404_NOT_FOUND)

class MatchHeldInLeagueView(APIView):
    def get(self, request):
        match_held_in_league = MatchHeldInLeague.objects.all()
        serializer = MatchHeldInLeagueSerializer(match_held_in_league, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MatchHeldInLeagueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            match_held_in_league = MatchHeldInLeague.objects.get(pk=pk)
            serializer = MatchHeldInLeagueSerializer(match_held_in_league, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except MatchHeldInLeague.DoesNotExist:
            return Response({'error': 'Match Held In League not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            match_held_in_league = MatchHeldInLeague.objects.get(pk=pk)
            match_held_in_league.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except MatchHeldInLeague.DoesNotExist:
            return Response({'error': 'Match Held In League not found'}, status=status.HTTP_404_NOT_FOUND)

class TeamMatchDataGoalView(APIView):
    def get(self, request):
        team_match_data_goals = TeamMatchDataGoal.objects.all()
        serializer = TeamMatchDataGoalSerializer(team_match_data_goals, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TeamMatchDataGoalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            team_match_data_goals = TeamMatchDataGoal.objects.get(pk=pk)
            serializer = TeamMatchDataGoalSerializer(team_match_data_goals, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except TeamMatchDataGoal.DoesNotExist:
            return Response({'error': 'Team Match Data Goal not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            team_match_data_goals = TeamMatchDataGoal.objects.get(pk=pk)
            team_match_data_goals.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except TeamMatchDataGoal.DoesNotExist:
            return Response({'error': 'Team Match Data Goal not found'}, status=status.HTTP_404_NOT_FOUND)
    
class TeamMatchDataBookingView(APIView):
    def get(self, request):
        team_match_data_bookings = TeamMatchDataBooking.objects.all()
        serializer = TeamMatchDataBookingSerializer(team_match_data_bookings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TeamMatchDataBookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            team_match_data_bookings = TeamMatchDataBooking.objects.get(pk=pk)
            serializer = TeamMatchDataBookingSerializer(team_match_data_bookings, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except TeamMatchDataBooking.DoesNotExist:
            return Response({'error': 'Team Match Data Booking not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            team_match_data_bookings = TeamMatchDataBooking.objects.get(pk=pk)
            team_match_data_bookings.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except TeamMatchDataBooking.DoesNotExist:
            return Response({'error': 'Team Match Data Booking not found'}, status=status.HTTP_404_NOT_FOUND)
        
class TeamMatchDataSubstitutionView(APIView):
    def get(self, request):
        team_match_data_substitutions = TeamMatchDataSubstitution.objects.all()
        serializer = TeamMatchDataSubstitutionSerializer(team_match_data_substitutions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TeamMatchDataSubstitutionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            team_match_data_substitutions = TeamMatchDataSubstitution.objects.get(pk=pk)
            serializer = TeamMatchDataSubstitutionSerializer(team_match_data_substitutions, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except TeamMatchDataSubstitution.DoesNotExist:
            return Response({'error': 'Team Match Data Substitution not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            team_match_data_substitutions = TeamMatchDataSubstitution.objects.get(pk=pk)
            team_match_data_substitutions.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except TeamMatchDataSubstitution.DoesNotExist:
            return Response({'error': 'Team Match Data Substitution not found'}, status=status.HTTP_404_NOT_FOUND)
        
class PlayerMatchDataGoalView(APIView):
    def get(self, request):
        player_match_data_goals = PlayerMatchDataGoal.objects.all()
        serializer = PlayerMatchDataGoalSerializer(player_match_data_goals, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlayerMatchDataGoalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            player_match_data_goals = PlayerMatchDataGoal.objects.get(pk=pk)
            serializer = PlayerMatchDataGoalSerializer(player_match_data_goals, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PlayerMatchDataGoal.DoesNotExist:
            return Response({'error': 'Player Match Data Goal not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            player_match_data_goals = PlayerMatchDataGoal.objects.get(pk=pk)
            player_match_data_goals.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PlayerMatchDataGoal.DoesNotExist:
            return Response({'error': 'Player Match Data Goal not found'}, status=status.HTTP_404_NOT_FOUND)

class PlayerMatchDataBookingView(APIView):
    def get(self, request):
        player_match_data_bookings = PlayerMatchDataBooking.objects.all()
        serializer = PlayerMatchDataBookingSerializer(player_match_data_bookings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlayerMatchDataBookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            player_match_data_bookings = PlayerMatchDataBooking.objects.get(pk=pk)
            serializer = PlayerMatchDataBookingSerializer(player_match_data_bookings, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PlayerMatchDataBooking.DoesNotExist:
            return Response({'error': 'Player Match Data Booking not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            player_match_data_bookings = PlayerMatchDataBooking.objects.get(pk=pk)
            player_match_data_bookings.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PlayerMatchDataBooking.DoesNotExist:
            return Response({'error': 'Player Match Data Booking not found'}, status=status.HTTP_404_NOT_FOUND)

class PlayerMatchDataSubstitutionView(APIView):
    def get(self, request):
        player_match_data_substitutions = PlayerMatchDataSubstitution.objects.all()
        serializer = PlayerMatchDataSubstitutionSerializer(player_match_data_substitutions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlayerMatchDataSubstitutionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            player_match_data_substitutions = PlayerMatchDataSubstitution.objects.get(pk=pk)
            serializer = PlayerMatchDataSubstitutionSerializer(player_match_data_substitutions, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PlayerMatchDataSubstitution.DoesNotExist:
            return Response({'error': 'Player Match Data Substitution not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            player_match_data_substitutions = PlayerMatchDataSubstitution.objects.get(pk=pk)
            player_match_data_substitutions.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PlayerMatchDataSubstitution.DoesNotExist:
            return Response({'error': 'Player Match Data Substitution not found'}, status=status.HTTP_404_NOT_FOUND)

class AdminCanEditTeamMatchDataView(APIView):
    def get(self, request):
        admin_can_edit_team_match_data = AdminCanEditTeamMatchData.objects.all()
        serializer = AdminCanEditTeamMatchDataSerializer(admin_can_edit_team_match_data, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AdminCanEditTeamMatchDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            admin_can_edit_team_match_data = AdminCanEditTeamMatchData.objects.get(pk=pk)
            serializer = AdminCanEditTeamMatchDataSerializer(admin_can_edit_team_match_data, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AdminCanEditTeamMatchData.DoesNotExist:
            return Response({'error': 'Admin Can Edit Team Match Data not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            admin_can_edit_team_match_data = AdminCanEditTeamMatchData.objects.get(pk=pk)
            admin_can_edit_team_match_data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AdminCanEditTeamMatchData.DoesNotExist:
            return Response({'error': 'Admin Can Edit Team Match Data not found'}, status=status.HTTP_404_NOT_FOUND)

class AdminCanEditPlayerMatchDataView(APIView):
    def get(self, request):
        admin_can_edit_player_match_data = AdminCanEditPlayerMatchData.objects.all()
        serializer = AdminCanEditPlayerMatchDataSerializer(admin_can_edit_player_match_data, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AdminCanEditPlayerMatchDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            admin_can_edit_player_match_data = AdminCanEditPlayerMatchData.objects.get(pk=pk)
            serializer = AdminCanEditPlayerMatchDataSerializer(admin_can_edit_player_match_data, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AdminCanEditPlayerMatchData.DoesNotExist:
            return Response({'error': 'Admin Can Edit Player Match Data not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            admin_can_edit_player_match_data = AdminCanEditPlayerMatchData.objects.get(pk=pk)
            admin_can_edit_player_match_data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AdminCanEditPlayerMatchData.DoesNotExist:
            return Response({'error': 'Admin Can Edit Player Match Data not found'}, status=status.HTTP_404_NOT_FOUND)

class AdminCanEditPlayerView(APIView):
    def get(self, request):
        admin_can_edit_player = AdminCanEditPlayer.objects.all()
        serializer = AdminCanEditPlayerSerializer(admin_can_edit_player, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AdminCanEditPlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            admin_can_edit_player = AdminCanEditPlayer.objects.get(pk=pk)
            serializer = AdminCanEditPlayerSerializer(admin_can_edit_player, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AdminCanEditPlayer.DoesNotExist:
            return Response({'error': 'Admin Can Edit Player not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            admin_can_edit_player = AdminCanEditPlayer.objects.get(pk=pk)
            admin_can_edit_player.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AdminCanEditPlayer.DoesNotExist:
            return Response({'error': 'Admin Can Edit Player not found'}, status=status.HTTP_404_NOT_FOUND)

class AdminCanEditTeamView(APIView):
    def get(self, request):
        admin_can_edit_team = AdminCanEditTeam.objects.all()
        serializer = AdminCanEditTeamSerializer(admin_can_edit_team, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AdminCanEditTeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            admin_can_edit_team = AdminCanEditTeam.objects.get(pk=pk)
            serializer = AdminCanEditTeamSerializer(admin_can_edit_team, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AdminCanEditTeam.DoesNotExist:
            return Response({'error': 'Admin Can Edit Team not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            admin_can_edit_team = AdminCanEditTeam.objects.get(pk=pk)
            admin_can_edit_team.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AdminCanEditTeam.DoesNotExist:
            return Response({'error': 'Admin Can Edit Team not found'}, status=status.HTTP_404_NOT_FOUND)

class AdminCanEditMatchView(APIView):
    def get(self, request):
        admin_can_edit_match = AdminCanEditMatch.objects.all()
        serializer = AdminCanEditMatchSerializer(admin_can_edit_match, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AdminCanEditMatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            admin_can_edit_match = AdminCanEditMatch.objects.get(pk=pk)
            serializer = AdminCanEditMatchSerializer(admin_can_edit_match, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AdminCanEditMatch.DoesNotExist:
            return Response({'error': 'Admin Can Edit Match not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            admin_can_edit_match = AdminCanEditMatch.objects.get(pk=pk)
            admin_can_edit_match.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AdminCanEditMatch.DoesNotExist:
            return Response({'error': 'Admin Can Edit Match not found'}, status=status.HTTP_404_NOT_FOUND)

class AdminCanEditLeagueView(APIView):
    def get(self, request):
        admin_can_edit_league = AdminCanEditLeague.objects.all()
        serializer = AdminCanEditLeagueSerializer(admin_can_edit_league, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AdminCanEditLeagueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            admin_can_edit_league = AdminCanEditLeague.objects.get(pk=pk)
            serializer = AdminCanEditLeagueSerializer(admin_can_edit_league, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AdminCanEditLeague.DoesNotExist:
            return Response({'error': 'Admin Can Edit League not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            admin_can_edit_league = AdminCanEditLeague.objects.get(pk=pk)
            admin_can_edit_league.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AdminCanEditLeague.DoesNotExist:
            return Response({'error': 'Admin Can Edit League not found'}, status=status.HTTP_404_NOT_FOUND)

class UserCanBrowseTeamMatchDataView(APIView):
    def get(self, request):
        user_can_browse_team_match_data = UserCanBrowseTeamMatchData.objects.all()
        serializer = UserCanBrowseTeamMatchDataSerializer(user_can_browse_team_match_data, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserCanBrowseTeamMatchDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            user_can_browse_team_match_data = UserCanBrowseTeamMatchData.objects.get(pk=pk)
            serializer = UserCanBrowseTeamMatchDataSerializer(user_can_browse_team_match_data, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserCanBrowseTeamMatchData.DoesNotExist:
            return Response({'error': 'User Can Browse Team Match Data not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            user_can_browse_team_match_data = UserCanBrowseTeamMatchData.objects.get(pk=pk)
            user_can_browse_team_match_data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserCanBrowseTeamMatchData.DoesNotExist:
            return Response({'error': 'User Can Browse Team Match Data not found'}, status=status.HTTP_404_NOT_FOUND)

class UserCanBrowsePlayerMatchDataView(APIView):
    def get(self, request):
        user_can_browse_player_match_data = UserCanBrowsePlayerMatchData.objects.all()
        serializer = UserCanBrowsePlayerMatchDataSerializer(user_can_browse_player_match_data, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserCanBrowsePlayerMatchDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            user_can_browse_player_match_data = UserCanBrowsePlayerMatchData.objects.get(pk=pk)
            serializer = UserCanBrowsePlayerMatchDataSerializer(user_can_browse_player_match_data, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserCanBrowsePlayerMatchData.DoesNotExist:
            return Response({'error': 'User Can Browse Player Match Data not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            user_can_browse_player_match_data = UserCanBrowsePlayerMatchData.objects.get(pk=pk)
            user_can_browse_player_match_data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserCanBrowsePlayerMatchData.DoesNotExist:
            return Response({'error': 'User Can Browse Player Match Data not found'}, status=status.HTTP_404_NOT_FOUND)
        
class UserCanBrowsePlayerView(APIView):
    def get(self, request):
        user_can_browse_player = UserCanBrowsePlayer.objects.all()
        serializer = UserCanBrowsePlayerSerializer(user_can_browse_player, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserCanBrowsePlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            user_can_browse_player = UserCanBrowsePlayer.objects.get(pk=pk)
            serializer = UserCanBrowsePlayerSerializer(user_can_browse_player, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserCanBrowsePlayer.DoesNotExist:
            return Response({'error': 'User Can Browse Player not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            user_can_browse_player = UserCanBrowsePlayer.objects.get(pk=pk)
            user_can_browse_player.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserCanBrowsePlayer.DoesNotExist:
            return Response({'error': 'User Can Browse Player not found'}, status=status.HTTP_404_NOT_FOUND)

class UserCanBrowseTeamView(APIView):
    def get(self, request):
        user_can_browse_team = UserCanBrowseTeam.objects.all()
        serializer = UserCanBrowseTeamSerializer(user_can_browse_team, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserCanBrowseTeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            user_can_browse_team = UserCanBrowseTeam.objects.get(pk=pk)
            serializer = UserCanBrowseTeamSerializer(user_can_browse_team, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserCanBrowseTeam.DoesNotExist:
            return Response({'error': 'User Can Browse Team not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            user_can_browse_team = UserCanBrowseTeam.objects.get(pk=pk)
            user_can_browse_team.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserCanBrowseTeam.DoesNotExist:
            return Response({'error': 'User Can Browse Team not found'}, status=status.HTTP_404_NOT_FOUND)

class UserCanBrowseMatchView(APIView):
    def get(self, request):
        user_can_browse_match = UserCanBrowseMatch.objects.all()
        serializer = UserCanBrowseMatchSerializer(user_can_browse_match, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserCanBrowseMatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            user_can_browse_match = UserCanBrowseMatch.objects.get(pk=pk)
            serializer = UserCanBrowseMatchSerializer(user_can_browse_match, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserCanBrowseMatch.DoesNotExist:
            return Response({'error': 'User Can Browse Match not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            user_can_browse_match = UserCanBrowseMatch.objects.get(pk=pk)
            user_can_browse_match.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserCanBrowseMatch.DoesNotExist:
            return Response({'error': 'User Can Browse Match not found'}, status=status.HTTP_404_NOT_FOUND)

class UserCanBrowseLeagueView(APIView):
    def get(self, request):
        user_can_browse_league = UserCanBrowseLeague.objects.all()
        serializer = UserCanBrowseLeagueSerializer(user_can_browse_league, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserCanBrowseLeagueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            user_can_browse_league = UserCanBrowseLeague.objects.get(pk=pk)
            serializer = UserCanBrowseLeagueSerializer(user_can_browse_league, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserCanBrowseLeague.DoesNotExist:
            return Response({'error': 'User Can Browse League not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            user_can_browse_league = UserCanBrowseLeague.objects.get(pk=pk)
            user_can_browse_league.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserCanBrowseLeague.DoesNotExist:
            return Response({'error': 'User Can Browse League not found'}, status=status.HTTP_404_NOT_FOUND)

class TeamMatchView(APIView):
    def get(self, request):
        team_match_data = TeamMatch.objects.all()
        serializer = TeamMatchSerializer(team_match_data, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TeamMatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            team_match_data = TeamMatch.objects.get(pk=pk)
            serializer = TeamMatchSerializer(team_match_data, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except TeamMatch.DoesNotExist:
            return Response({'error': 'Team Match Data not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            team_match_data = TeamMatch.objects.get(pk=pk)
            team_match_data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except TeamMatch.DoesNotExist:
            return Response({'error': 'Team Match Data not found'}, status=status.HTTP_404_NOT_FOUND)

class PlayerMatchView(APIView):
    def get(self, request):
        player_match_data = PlayerMatch.objects.all()
        serializer = PlayerMatchSerializer(player_match_data, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlayerMatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            player_match_data = PlayerMatch.objects.get(pk=pk)
            serializer = PlayerMatchSerializer(player_match_data, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PlayerMatch.DoesNotExist:
            return Response({'error': 'Player Match Data not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            player_match_data = PlayerMatch.objects.get(pk=pk)
            player_match_data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PlayerMatch.DoesNotExist:
            return Response({'error': 'Player Match Data not found'}, status=status.HTTP_404_NOT_FOUND)
