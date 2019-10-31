from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCount,HitCountMixin
# Create your models here.

class Post(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User,related_name='likes',blank=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


    def total_likes(self):
        return self.likes.count()


    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={'pk': self.pk})




class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField(max_length=200)
    timestamp=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return '{}-{}'.format(self.post.title, str(self.user.username))


# class TrackedPosts(models.Model):
#     post = models.ForeignKey(Post,on_delete=models.CASCADE)
#     ip = models.CharField(max_length=16) #only accounting for ipv4
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#
# class Blog(models.Model):
#     #fields you need
#     blog_views=models.IntegerField(default=0)
