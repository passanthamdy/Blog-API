from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.shortcuts import reverse

User = get_user_model()


class Post(models.Model):
    """Model For Blog Posts"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', related_query_name='post')
    title = models.CharField(max_length=100)
    body = models.TextField()
    short_description = models.TextField(max_length=255)
    slug = models.SlugField(blank=True, null=True)
    image = models.ImageField(upload_to='media', blank=True, null=True)
    is_published = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    published_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title


    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter(parent=instance)
        return qs
        
class Meta:
        indexes = [models.Index(fields=['slug'])]
        ordering = ['-published_on']



@receiver(pre_save, sender=Post)
def update_published_on(sender, instance, **kwargs):
    """Update The Date Of 'Published On' When The Post Gets Published"""

    if instance.id:
        old_value = Post.objects.get(pk=instance.id).published_on
        if not old_value:
            instance.published_on = timezone.now()



class Comment(models.Model):
    """Model For The Comments In Posts"""

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    is_displayed = models.BooleanField(default=True)
    published_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Post - "{self.post.title}", Body - "{self.body}"'