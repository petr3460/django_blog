"""project URL Configuration

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
from django.urls import path, include
from django.contrib.auth import views as auth_views

from app import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/profile/', core_views.settings, name='settings'),
    path('', core_views.home, name='home'),
    path('articles/<slug:tag>/', core_views.home, name='articles_by_tag'),
    path('articles/<slug:tag>/<int:page_number>/', core_views.home, name='tag-pagination' ),
    path('page/<int:page_number>/', core_views.home, name='pagination' ),
    path('article/<slug:article_id>/', core_views.article, name='post'),
    path('accounts/login/', auth_views.login, name='login'),
    path('accounts/logout/', auth_views.logout, name='logout'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('settings/', core_views.settings, name='settings'),
    path('settings/password/', core_views.password, name='password'),
    
    path('like/', core_views.like, name='like'),
    
]


LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'home'