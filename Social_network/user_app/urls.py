from django.urls import path
from .views import *

urlpatterns = [
    path('settings/', SettingsView.as_view(), name='settings_view'),
    path('registration/', CheckRegistration.as_view(), name='check_registration'),
    path('logout/', LogoutView.as_view(), name='logout_view'),
    path('check_login/', CheckLogin.as_view(), name='check_login_view'),
    path('confirm_email/', ConfirmEmail.as_view(), name='confirm_email'),
    path('auth/', AuthUser.as_view(), name='auth_view'),

    path('friends/', FriendsView.as_view(), name='friends_view'),
    path('friends/card/', SingleCardView.as_view(), name='single_card'), 
    
    path('friends/user_data/', UserData.as_view(), name='user_data'),
    path('friends/friend_posts/', FriendPostsView.as_view(), name='friend_posts'), 
    path('friends/change_status/<str:status>/', ChangeStatusView.as_view(), name='change_status'),
    
    path('friends/<str:section>/', SectionsView.as_view(), name='friends_section'),
]