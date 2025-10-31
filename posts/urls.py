from django.urls import path
from posts import views
app_name = 'posts'

urlpatterns = [
    path('create/',views.create_view,name='create'),
    path('my-posts/',views.my_posts,name='my-posts'),

    path('delete-post/<slug:slug>/', views.delete_post, name='delete_post'),
    path('draft-post/<slug:slug>/', views.draft_post, name='draft_post'),
    path('edit-post/<slug:slug>/', views.edit_post, name='edit_post'),
]