from django.urls import path

from . import views

app_name = 'tour'

urlpatterns = [
    path('', views.tours, name='tours'),
    path('new/', views.NewTourView.as_view(), name='new'),
    path('<pk>/', views.detail, name='detail'),
    path('<pk>/delete/', views.delete, name='delete'),
    path('<pk>/edit/', views.edit, name='edit'),
]
 
 