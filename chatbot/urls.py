from django.urls import path, include
from rest_framework import routers
from chatbot.views import *

router = routers.DefaultRouter()
router.register(r'request',ChatBotRequest ,basename='')

urlpatterns = [
    path('', include(router.urls)),
]
