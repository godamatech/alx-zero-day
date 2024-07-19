from . import views
from django.urls import path

app_name, urlpatterns =  "blog",[
    path('', views.index_view, name='index_view'),
    path('<int:pk>/', views.detail_view, name='detail_view'),
]