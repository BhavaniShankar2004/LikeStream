from django.urls import path
from .views import ( PostListView, PostDetailView , PostCreateView ,PostUpdateView, PostDeleteView, UserPostListView,AddCommentView )
from . import views


urlpatterns = [
    path('',PostListView.as_view(), name='blog-home'),
    path('user/<str:username>',UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/',PostDetailView.as_view(), name='post-detail'),
    path('post/new/',PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/',PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(), name='post-delete'),
    path('about/',views.about, name='blog-about'),
     
    path('search_user/',views.search_user, name='search_user'),
    path('post_likes/<int:pk>',views.post_likes,name='post_likes'),


]


