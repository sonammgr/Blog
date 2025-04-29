"""
URL configuration for Blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from base.views import TagApiView,CategoryApiView,PostApiView,AuthorApiView,CommentApiView,FeedbackApiView,register_api_view,login_api_view,logout_api_view,PublicPostView,blog_detail,blog_list,category_posts
from base.models import Tag,Category,Post,Feedback,Comment,Author
from base import views
from django.http import HttpResponse


def favicon_view(request):
    return HttpResponse(status=204)


urlpatterns = [
    #blog features 
    path('admin/', admin.site.urls),
    path('tag/', TagApiView.as_view({'get': 'list', 'post': 'create'})), 
    path('tag/<int:pk>/', TagApiView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('category/', CategoryApiView.as_view({'get': 'list', 'post': 'create'})), 
    path('category/<int:pk>/', CategoryApiView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('post/',PostApiView.as_view({'get':'list','post':'create'}),name='post-list-create'),
    path('post/<int:pk>/',PostApiView.as_view({'put':'update','delete':'destroy','get':'retrieve'})),
    path('comments/', CommentApiView.as_view({'get': 'list', 'post': 'create'}), name='comment-list-create'),
    path('comments/<int:pk>/', CommentApiView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='comment-detail'),
    path('feedback/', FeedbackApiView.as_view({'get': 'list', 'post': 'create'}), name='feedback-list-create'),
    path('feedback/<int:pk>/', FeedbackApiView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='feedback-detail'),
    path('authors/', AuthorApiView.as_view({'get': 'list', 'post': 'create'}), name='author-list-create'),
    path('authors/<int:pk>/', AuthorApiView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='author-detail'),
    #authteication declartion of url.
    path('register/',register_api_view),
    path('login/',login_api_view),
    path('logout/',logout_api_view),
    #for the public viewing (extra)
    path('public-posts/',PublicPostView.as_view({'get':'list'})),
    path('', views.blog_list, name='blog_list'),  # Homepage → all posts
    path('post/<slug:slug>/', views.blog_detail, name='blog_detail'),  # Single post page
    path('category/<slug:category_slug>/', views.category_posts, name='category_posts') # Category page
    
]
