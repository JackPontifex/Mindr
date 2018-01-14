"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.views import generic
from rest_framework import views, serializers, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.response import Response
import api.views as api_views
import api.serializers as UserSerializer


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()


class EchoView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED)


class UserView(views.APIView):
    @permission_classes((AllowAny, ))
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED)


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', generic.RedirectView.as_view(
         url='/api/', permanent=False)),
    url(r'^api/$', get_schema_view()),
    url(r'^api/auth/', include(
        'rest_framework.urls', namespace='rest_framework')),
    url(r'^api/auth/token/obtain/$', TokenObtainPairView.as_view()),
    url(r'^api/auth/token/refresh/$', TokenRefreshView.as_view()),
    url(r'^api/echo/$', EchoView.as_view()),
    path(r'api/users/', api_views.users),
    path(r'api/users/<int:userid>/', api_views.get_user),
    path(r'api/users/<int:userid>/cameras/', api_views.cameras),
    path(r'api/users/<int:userid>/cameras/<int:cameraid>', api_views.get_camera),
    path(r'api/users/<int:userid>/children/', api_views.children),
    path(r'api/users/<int:userid>/children/<int:childid>', api_views.get_child),
    path(r'api/users/<int:userid>/children/<int:childid>/events', api_views.events),
    path(r'api/users/<int:userid>/children/<int:childid>/events/<int:eventid>', api_views.get_event),
]
