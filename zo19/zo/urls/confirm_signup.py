from django.urls import include, path

from zo.views.public import ConfirmUserSignUpView, ConfirmUserHubSignUpView, ConfirmHubSignUpView

urlpatterns = [

    path('user/<int:pk>/', ConfirmUserSignUpView.as_view(), name='confirm_signup_user'),
    path('user-hub/<int:pk>/', ConfirmUserHubSignUpView.as_view(), name='confirm_signup_user-hub'),
    path('hub/<int:pk>/', ConfirmHubSignUpView.as_view(), name='confirm_signup_hub'),
]
