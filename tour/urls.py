from django.urls import path

from . import views

app_name = 'tour'

urlpatterns = [
    path('', views.tours, name='tours'),
    path('new/', views.NewTourView.as_view(), name='new'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/edit/', views.edit, name='edit'),

]
 
 