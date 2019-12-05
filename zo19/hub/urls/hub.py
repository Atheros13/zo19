from django.urls import include, path

from hub.views.hub import HubView

urlpatterns = [

    path('<int:pk>/<str:hub_name>/' , HubView.as_view(), name='hub_hub'),

]
