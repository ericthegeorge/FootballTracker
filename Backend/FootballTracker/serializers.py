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