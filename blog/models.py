from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

class ClientUser(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    author = models.ForeignKey(User, default=None, on_delete= models.CASCADE)
    title = models.CharField(max_length = 200)
    text = models.TextField()
    create_date = models.DateTimeField(default= timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    #def approve_comments(self):
     #   return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('blog.post', on_delete= models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, default=None, on_delete= models.CASCADE)
    text = models.TextField()
    create_date = models.DateTimeField(default= timezone.now)
    #approved_comment = models.BooleanField(default= False)

    def get_absolute_url(self):
        return reverse("post_list")
    

    def __str__(self):
        return self.text
    
