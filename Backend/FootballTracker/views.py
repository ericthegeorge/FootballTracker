from django.shortcuts import render

# Create your views here.


''' 
EXAMPLE CODE HERE

class RegisterView(APIView):
    def post(self, request, username):
        password = request.data.get('password', None)
        if not password or not username:
            return Response({"error": "Username and password is required", "success": False}, states = status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username = username).exists():
            return Response({"error": "Username is taken", "success": False}, status = status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.create_user(username = username, password = password)
            user_profile = UserProfile.objects.create(user = user)
            return Response(
                {"message": "User successfully registered", "success": True}, status = status.HTTP_201_CREATED
            )
        except Exception:
            return Response(
                {"error": "server error", "success": False}, status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )


'''