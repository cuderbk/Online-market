from django.urls import path

from . import views

app_name = 'tour'

urlpatterns = [
    path('', views.tours, name='tours'),
    path('create_tour/', views.create_tour, name='create_tour'),
    path('add_diadiem_thamquan/<tour>/<int:day_number>/', views.add_diadiem_thamquan, name='add_diadiem_thamquan'),
    path('add_ngaykhoihanh_tour/<tour>/', views.add_ngaykhoihanh_tour, name='add_ngaykhoihanh_tour'),
    path('add_hanhdong_lichtrinh_tour/<tour>/<int:day_number>/', views.add_hanhdong_lichtrinh_tour, name ='add_hanhdong_lichtrinh_tour'),

    # path('ngaykhoihanh_tour/', views.ngaykhoihanh_tour_view),
    # path('diadiem_thamquan/', views.diadiem_thamquan_view),
    # path('lichtrinh_tour/', views.lichtrinh_tour_view),
    # path('new/diadiem', views.Diadiemthamquan_view, name='diadiemthamquan_view'),
    path('<pk>/', views.detail, name='detail'),
    path('<pk>/delete/', views.delete, name='delete'),
    path('<pk>/edit/', views.edit, name='edit'),
    path('<pk>/buy/', views.buy, name='buy'),
]
 