from django.urls import path
from survivor import views

urlpatterns = [
    path('survivor/', views.survivor_list),
    path('survivor/<int:pk>/', views.survivor_detail),
    path('reports/', views.survivor_reports),
    path('updatelocation/<int:pk>/', views.survivor_update_location)
]
