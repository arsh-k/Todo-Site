"""to_do URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from mainpage import views

urlpatterns = [
    path('admin/', admin.site.urls),

    #Auth
    path('login/', views.loginuser, name ="loginuser"),
    path('signup/', views.signupuser, name = "signupuser"),
    path('logout/', views.logoutuser, name = "logoutuser"),
    path('accounts/', include('allauth.urls')),

    #Site Layout
    path('createtodo/', views.createtodo, name = "createtodo"),
    path('currenttodos/', views.currenttodos, name= "currenttodos"),
    path('', views.home, name = "home"),
    path('mytodo/<int:mytodo_pk>', views.viewtodo, name = "viewtodo"),
    path('mytodo/<int:mytodo_pk>/completed', views.completedtodo, name = "completedtodo"),
    path('mytodo/<int:mytodo_pk>/deleted', views.deletetodo, name = "deletetodo"),
    path('completedtodos/', views.completedtodos, name= "completedtodos"),
    path('completedtodos/cleared', views.clearcompleted, name= "clearcompleted"),

]
