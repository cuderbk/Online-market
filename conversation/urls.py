from django.urls import path

from . import views

app_name = 'conversation'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('<pk>/', views.detail, name='detail'),
    path('new/<tour_pk>/', views.new_conversation, name='new'),
]
