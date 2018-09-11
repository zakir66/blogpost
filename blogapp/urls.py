"""blogpost URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from . import views
urlpatterns = [
    path('', views.index, name = "index"),
    path('author/<name>', views.getauthor, name = "author"),
    path('post/<int:id>', views.getsingle, name = "single_post"),
    path('topic/<name>', views.gettopic, name = "topic"),
    path('login/', views.getlogin, name = "login"),
    path('logout/', views.getlogout, name = "logout"),
    path('create/', views.getcreate, name = "create"),
    path('profile/', views.getprofile, name = "profile"),
    path('update/<int:pid>', views.getUpdate, name = "update"),
    path('delete/<int:pid>', views.getdelete, name = "delete"),
    path('register/', views.getregister, name = 'register'),
    path('topics/', views.getcategory, name = 'category'),
    path('create/topic/', views.createTopic, name = 'createTopic'),
    path('cdelete/<int:pid>', views.cdelete, name = "cdelete"),
    path('cupdate/<int:pid>', views.cUpdate, name = 'cupdate'),
]
