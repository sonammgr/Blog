from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.viewsets import GenericViewSet
from .serializers import PostSerializer,AuthorSerializer,CategorySerializer,CommentSerializer,TagSerializer,FeedbackSerializer,UserSerializer
from base.models import Tag,Category,Feedback,Comment,Author,Post
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,DjangoModelPermissions,BasePermission
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import  authenticate
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.filters import SearchFilter
from django.core.mail import send_mail
from rest_framework.permissions import AllowAny
#defining and improting the modules used on the base views
# Create your views here.

class IsAuthorGroup(BasePermission):#allowing only author group to do perticular tasks(personal prefrence)
    def has_permission(self,request,view):
        return request.user.is_authenticated and request.user.groups.filter(name='Authors').exists()#permission for only authors role or author group based.
    
class IsMemberGroup(BasePermission):##allowing only members group to do perticular tasks(personal prefrence)
    def has_permission(seld,request,view):
        return request.user.is_authenticated and request.user.groups.filter(name='Members').exists()#permission for only member role or memeber group based.    

#to manage blog tags and seraching name by filters)
class TagApiView(viewsets.ModelViewSet):
    queryset=Tag.objects.all()
    serializer_class=TagSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['tag'] 
    
#viewsets to manage or handle the categories of the post.
class CategoryApiView(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    
#viewsets to manage the categories of the blog post including the serach,filter and pagnination)
class PostApiView(GenericViewSet):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    permission_classes=[IsAuthenticated,IsAuthorGroup]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields=['category','created_at']
    search_fields=['title','category__name','author__user__username']
    def list(self,request):#returns list of all the blog posts.
        post_objs=self.filter_queryset(self.get_queryset())
        page=self.paginate_queryset(post_objs)#handles the pagination.
        if page==None:
            serializer=PostSerializer(post_objs,many=True)
            return self.get_paginated_response(serializer.data)#for returning pagination,filterting,serarching as response.

    def create(self,request):#to create a new poset on a blog.
        serializer=PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)   

    def update(self,request,pk=None):#to update relevent information and details on a blog post.
        try:
            post_objs=Post.objects.get(id=pk)
        except:
            return Response({'detail': 'no data found'},status=status.HTTP_404_NOT_FOUND)    
        serializer=PostSerializer(post_objs,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self,request,pk=None):#to simply delete a post of the blog.
        try:
            post_objs=Post.objects.get(id=pk)
        except:
            return Response ({'details':'no data found'},status=status.HTTP_404_NOT_FOUND)
        post_objs.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def  retrieve(self,request,pk=None):#to retrieve a single post of a blog by id.
        try:
            post_objs=Post.objects.get(id=pk) 
        except:
            return Response({'details':'no data found'})
        serializer=PostSerializer(post_objs)
        return Response(serializer.data)  

#viewsets to handle comments (autheticated users only)   
class CommentApiView(viewsets.ModelViewSet):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    permission_classes=[IsAuthenticated,IsAuthorGroup]

#viewsets to handle like/dislike on posts.
class FeedbackApiView(viewsets.ModelViewSet):
    queryset=Feedback.objects.all()
    serializer_class=FeedbackSerializer
    permission_classes=[IsAuthenticated,IsMemberGroup]

#viewsets to handle author accounts.
class AuthorApiView(viewsets.ModelViewSet):
    queryset=Author.objects.all()
    serializer_class=AuthorSerializer 
    permission_classes=[IsAuthenticated]
     
@api_view(['POST'])
def register_api_view(request):
    #handling user registration with password hasing and a welcome email.
    password=request.data.get('password')
    hash_password=make_password(password)
    data=request.data.copy()
    data['password']=hash_password

    serializer=UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        email=request.data.get('email')
        send_mail(subject='WELCOME TO BLOG PLATFORM',message='sucessfully registered to the blog platform.',from_email='sonammagar017@gmail.com',recipient_list=[email])
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def login_api_view(request):
    #handling user login and authetication token in return.
    username=request.data.get('username')    
    password=request.data.get('password') 

    user=authenticate(username=username,password=password)   

    if user==None:
        return Response({'details':'INVALID CREDENTIALS'},status=status.HTTP_400_BAD_REQUEST)
    else:
        token,_=Token.objects.get_or_create(user=user)
        return Response(token.key)
  
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout_api_view(request):
    #handling user account logout by emitting the auth token generated.
    user=request.user
    token=Token.objects.get(user=user)
    token.delete()
    return Response({'details':'sucessfully logged out of the system.'},status=status.HTTP_200_OK)

class PublicPostView(viewsets.ReadOnlyModelViewSet):#allows the public user to just read or view the post without any authentications.(added extra for better feature)
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    permission_classes=[AllowAny]#allows anu unauthorised user 




