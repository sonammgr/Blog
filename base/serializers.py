from rest_framework import serializers
from .models import Author,Post,Comment,Feedback,Tag,Category
from django.contrib.auth.models import User


#for user registeration and for basic access of the data.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['email','username','password']

#serializer for author model
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Author
        fields='__all__'        

#serializer for category model(includes blog categories)
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','created_at','name','description']

#serializer for blogpost model(using related tags)
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields=['id', 'title', 'content', 'created_at', 'updated_at', 'author', 'category'] 

#serializer for tag model
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tag
        fields=['name','created_at'] 

#serializer for comment model(comment on post)
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=['post','author','content','created_at']

#serializer for feedback model (like/dislike)
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model=Feedback
        fields=['post','user','like','created_at']

