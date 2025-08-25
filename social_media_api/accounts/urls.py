from django.urls import path
from .views import RegisterView, LoginView, ProfileView
from .views import RegisterView, LoginView, ProfileView, FollowUserView, FollowingListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    # same endpoint supports DELETE for unfollow
    path('following/', FollowingListView.as_view(), name='following-list'),
]