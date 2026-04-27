from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('routes/<int:route_id>/', views.route_detail, name='route_detail'),
    path('routes/<int:route_id>/book/', views.book_route, name='book_route'),
    path('routes/<int:route_id>/unbook/', views.unbook_route, name='unbook_route'),
    path('my-routes/', views.my_routes, name='my_routes'),
    path('stations/<int:station_id>/', views.station_detail, name='station_detail'),
    path('register/', views.register_view, name='register'),
]
