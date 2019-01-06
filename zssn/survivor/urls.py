from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from survivor import views

urlpatterns = format_suffix_patterns([
    path('', views.api_root),
    path('survivor/', views.survivor_list, name='survivor-list'),
    path('survivor/<int:pk>/', views.survivor_detail, name='survivor-detail'),
    path('reports/', views.survivor_reports, name='reports-list'),
    path('updatelocation/<int:pk>/', views.survivor_update_location, name='update-location'),
    path('infected/<int:pk>/', views.survivor_flag_as_infected, name='infected'),
    path('trade/', views.survivor_trade, name='trade')
])
