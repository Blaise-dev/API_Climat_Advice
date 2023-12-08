from django.urls import path, include
from rest_framework import routers
from apichatgpt.views import *

router = routers.DefaultRouter()
router.register(r'request',ChatGPTRequest ,basename='')

urlpatterns = [
    path('', include(router.urls)),
]
