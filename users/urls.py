"""
URL configuration for ScheduleManager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from django.urls import path
from .views import UserSignupView, UserLoginView, UserProfileView, UserScheduleView, UserProjectsView
from django.contrib.auth.views import LogoutView

app_name = 'users'



urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('projects/', UserProjectsView.as_view(), name='projects'),
    path('projects/<int:id>/tasks', UserScheduleView.as_view(), name='tasks'),
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout')

]