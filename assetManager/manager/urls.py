from django.urls import path
from django.conf.urls import include, url

from . import views

app_name = 'manager'

urlpatterns = [
    path('',views.index, name='index'),
    path('add/', views.add, name='add'),
    path('deploy/',views.deploy, name='deploy'),
    path('receive/',views.receive, name='receive'),
    path('addgrp/',views.addgrp, name='addgrp'),
    path('<int:asset_tag>/',views.asset, name='asset'),
    path('select/',views.selectAsset, name='selectAsset'),
    path('deployed/',views.deployed, name='deployed'),
    path('undeployed/',views.undeployed, name='undeployed'),
    path('bygroup/',views.bygroup, name='bygroup'),
]
