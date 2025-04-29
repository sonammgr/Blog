from django.db import models
from django.contrib.auth.models import User


# Create your models here.
#represnting author with linked to one django user 
class Author(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)


#post category 
class Category(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=200,blank=True)
   
#representing a post in blog,each post written by author(user) which links to category including tags.
class Post(models.Model):
    title=models.CharField(max_length=100)
    slug=models.SlugField(unique=True)
    content=models.TextField(max_length=500)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    author=models.ForeignKey('Author',on_delete=models.SET_NULL,null=True)
    category=models.ForeignKey('Category',on_delete=models.SET_NULL,null=True)
    tags = models.ManyToManyField('Tag', blank=True)

#categorzing blog posts.
class Tag(models.Model):
    name=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)

#comment made by any user (including memebers or authors)
class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.SET_NULL,null=True)
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    author=models.ForeignKey('Author',on_delete=models.SET_NULL,null=True)
    content=models.TextField(max_length=300)
    created_at=models.DateTimeField(auto_now_add=True)

#allows to like/dislike on a  given post by user(members)
class Feedback(models.Model):
    post=models.ForeignKey(Post,on_delete=models.SET_NULL,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    like=models.BooleanField()
    created_at=models.DateTimeField(auto_now_add=True)



    

