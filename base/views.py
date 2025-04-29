from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from .serializers import PostSerializer,AuthorSerializer,CategorySerializer,CommentSerializer,TagSerializer,FeedbackSerializer,UserSerializer
from base.models import Tag,Category,Feedback,Comment,Author,Post
from rest_framework.response import Response 
from rest_framework import status,viewsets,filters
from django.contrib.auth.models import User,Group
from rest_framework.permissions import IsAuthenticated,DjangoModelPermissions,BasePermission,AllowAny
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth.hashers import make_password
from django.contrib.auth import  authenticate
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.core.mail import send_mail
from django.shortcuts import render,get_object_or_404
#defining and improting the modules used on the base views
# Create your views here.

class IsAuthorGroup(BasePermission):#allowing only author group to do perticular tasks(personal prefrence)
    def has_permission(self,request,view):
        return request.user.is_authenticated and request.user.groups.filter(name='Author').exists()#permission for only authors role or author group based.
    
class IsMemberGroup(BasePermission):##allowing only members group to do perticular tasks(personal prefrence)
    def has_permission(seld,request,view):
        return request.user.is_authenticated and request.user.groups.filter(name='Member').exists()#permission for only member role or memeber group based.    

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
    permission_classes=[DjangoModelPermissions,IsAuthorGroup]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields=['category','created_at']
    search_fields=['title','category__name','author__user__username']

    def list(self,request):#returns list of all the blog posts.
        post_objs=self.filter_queryset(self.get_queryset())
        page=self.paginate_queryset(post_objs)#handles the pagination.
        if page is not None:
            serializer=PostSerializer(page,many=True)
            return self.get_paginated_response(serializer.data)#for returning pagination,filterting,serarching as response.
        serializer=PostSerializer(post_objs,many=True)
        return Response(serializer.data)    
    def create(self,request):#to create a new poset on a blog.
        serializer=PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)   

    def update(self, request, pk=None):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
    def destroy(self, request, pk=None):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    def retrieve(self, request, pk=None):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    
        serializer = PostSerializer(post)
        return Response(serializer.data)

#viewsets to handle comments (autheticated users only)   
class CommentApiView(viewsets.ModelViewSet):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    permission_classes=[IsAuthenticated]

#viewsets to handle like/dislike on posts.
class FeedbackApiView(viewsets.ModelViewSet):
    queryset=Feedback.objects.all()
    serializer_class=FeedbackSerializer
    permission_classes=[IsAuthenticated,IsMemberGroup]

#viewsets to handle author accounts.
class AuthorApiView(viewsets.ModelViewSet):
    queryset=Author.objects.all()
    serializer_class=AuthorSerializer 
    permission_classes=[]
     
from django.contrib.auth.models import Group

@api_view(['POST'])
@permission_classes([AllowAny])
def register_api_view(request):
    role = request.data.get('role', '').capitalize()
    if role not in ['Author', 'Member']:
        return Response({'error': 'Invalid role.'}, status=status.HTTP_400_BAD_REQUEST)

    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()
    
    group, _ = Group.objects.get_or_create(name=role)
    user.groups.add(group)

    # Welcome email
    send_mail(subject='WELCOME TO BLOG PLATFORM',message=f'Successfully registered as a {role}.',from_email='sonammagar017@gmail.com',recipient_list=[email],fail_silently=True)

    return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

    
@api_view(['POST'])
@permission_classes([AllowAny])
def login_api_view(request):
    #handling user login and authetication token in return.
    username=request.data.get('username')    
    password=request.data.get('password') 

    if not username or not password:
        return Response({'error':'ENTER VALID USERNAME AND PASSWORD.'},status=status.HTTP_400_BAD_REQUEST)

    user=authenticate(username=username,password=password)   

    if user is None:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    token,_=Token.objects.get_or_create(user=user)
    return Response({'token':token.key})
  
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
    permission_classes=[AllowAny]#allows any unauthorised user 

def blog_list(request):
    posts = Post.objects.all()
    return render(request, 'base/blog_list.html', {'posts': posts})

def blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'base/blog_details.html', {'post': post})

def category_posts(request, category_slug):
    posts = Post.objects.filter(category__slug=category_slug)
    return render(request, 'base/blog_category.html', {'posts': posts})




