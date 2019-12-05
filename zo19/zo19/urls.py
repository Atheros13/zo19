from django.urls import include, path
from django.contrib import admin
from django.contrib.auth.views import LogoutView as PublicLogoutView

from zo.views import PublicHomeView, PublicAboutView
from zo.views import PublicContactView, PublicSignUpView
from zo.views import PublicLoginView, PublicRedirectLoginView
from zo.views import PasswordRequestView, PasswordResetView

from zo import urls as zo_urls
from hub import urls as hub_urls
#from tournament import urls as tournament_urls

urlpatterns = [

    path('', PublicHomeView.as_view(), name='home'),
    path('about/', PublicAboutView.as_view(), name='about'),
    #path('faq/', PublicFAQView.as_view(), name='faq'),
    path('contact/', PublicContactView.as_view(), name='contact'),

    path('signup/', PublicSignUpView.as_view(), name='public_signup'),
    path('confirm_signup/', include(zo_urls.confirm_signup)),

    path('login/', PublicLoginView.as_view(), name='login'),
    path('logout/', PublicLogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/login/', PublicRedirectLoginView.as_view()),
    path('password/request/', PasswordRequestView.as_view(), name='password_request'),
    path('password/reset/<int:id>/<str:random>/', PasswordResetView.as_view(), name='password_reset'),

    path('admin/', admin.site.urls),

    path('user/', include(zo_urls.user)),
    path('hub/', include(hub_urls)),
    #path('tournament', include(tournament_urls)),

]
