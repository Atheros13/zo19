from django.urls import include, path

from zo.views.zo_admin import ZoAdminConfirmSignUpView

urlpatterns = [

    path('confirm_signup/', ZoAdminConfirmSignUpView.as_view(), name='zo_admin_confirm_signup'),
    path('confirm_signup/<str:type>/<int:id>/', ZoAdminConfirmSignUpView.as_view(), name='zo_admin_confirm_signup_id'),

]
