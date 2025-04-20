from django.urls import path
from .views import RegisterView, LoginView
# from .views import ...


urlpatterns = [
    # EXAMPLE URL using the view as response
    path('register/', RegisterView.as_view(), name = 'register'),
    path('login/', LoginView.as_view(), name = 'login'),

]