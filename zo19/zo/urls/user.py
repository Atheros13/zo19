from django.urls import include, path

from zo.views.user import *

urlpatterns = [

    path('', UserProfileView.as_view(), name='user_profile'),
    path('hubs/', UserHubsView.as_view(), name='user_hubs'),
    path('tournaments/', UserTournamentsView.as_view(), name='user_tournaments'),
    path('contact/', UserContactView.as_view(), name='user_contact'),
    path('settings/', UserSettingsView.as_view(), name='user_settings'),


]
