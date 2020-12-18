from django.urls import path
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword
from .views.game_views import Games, GameDetail
from .views.review_views import Reviews, ReviewDetail

urlpatterns = [
  	# Restful routing
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw'),
    path('games/', Games.as_view(), name='games'),
    path('games/<int:pk>/', GameDetail.as_view(), name='game_detail'),
    path('reviews/', Reviews.as_view(), name='reviews'),
    path('reviews/<int:pk>/', ReviewDetail.as_view(), name='review_detail'),
]
