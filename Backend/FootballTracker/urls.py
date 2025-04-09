from django.urls import path
from .views import PackOpenerView, UserDecksListAndCreateView, UserDeckDetailView
from .views import AllCardsView, UserProfileView, LoginView, RegisterView, UserCardsView


urlpatterns = [
    # EXAMPLE URL using the view as response
    # path('user/<str:username>/register/', RegisterView.as_view(), name = 'user_register'),
]