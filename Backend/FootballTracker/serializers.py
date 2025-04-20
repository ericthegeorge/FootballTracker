from django.contrib.auth.models import User
from .models import UserProfile
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

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