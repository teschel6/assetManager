from django.urls import path

from . import views

app_name = 'manager'

urlpatterns = [
    path('',views.index, name='index'),
    path('add/', views.add, name='add'),
    path('deploy/',views.deploy, name='deploy'),
    path('receive/',views.receive, name='receive'),
    path('addgrp/',views.addgrp, name='addgrp'),
]
