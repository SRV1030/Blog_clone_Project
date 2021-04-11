"""bloggy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import re_path,path,include

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'',include('blog.urls')),
    re_path(r'^accounts/login/$', views.LoginView.as_view(), name='login'),
    re_path(r'^accounts/logout/$', views.LogoutView.as_view(), name='logout', kwargs={'next_page': '/'}),
    #view.login and logout are from django.contrin.auth that manage login of superuser
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
