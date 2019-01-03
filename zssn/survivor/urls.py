from django.urls import path
from snippets import views

urlpatterns = [
    path('survivor/', views.survivor_list),
    path('survivor/<int:pk>/', views.survivor_detail),
    path('reports', views.survivor_reports)
]
