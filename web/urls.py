from django.urls import path
from web import views


app_name = 'web'

urlpatterns = [
    
    path('', views.index, name='index'),
    path('home/', views.index, name='home'),
    path('post/<slug:slug>/',views.post_detail,name = 'post_detail'),
    path('test-404/', views.test_404, name='test_404'),
]