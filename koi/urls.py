from django.urls import path
from . import views


app_name = 'koi'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:koinoxrista_id>/', views.DapanesViewDet, name='dapanes'),
    path('<int:koin_id>/dist', views.distribution, name='katanomi'),
    path('xiliosta/', views.xiliosta_view, name='xiliosta'),
    path('<int:apod_id>/apodeijeis/', views.apodeijeis, name='apodeijeis'),
]
