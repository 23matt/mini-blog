from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


# Create your models here.

class Author(models.Model):
    """ 
    Model representing a blogger
    """
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    bio = models.TextField(max_length=500, help_text="Please enter your bio.")

    class Meta:
        ordering = ['user', 'bio']

    def get_absolute_url(self):
        """
        Returns the url to access a particular blog-author instance.
        """
        return reverse('author_list', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the model object
        """
        return self.user.username


class Post(models.Model):
    """
    Model for representing a blog post.
    """
    title = models.CharField(
        max_length=200, help_text="Please enter your post title.")
    content = models.TextField(
        max_length=2000, help_text="Enter your blog post.")
    author = models.ForeignKey(
        Author, on_delete=models.SET_NULL, null=True)
    post_date = models.DateTimeField(default=timezone.now)

    class Meta:
        """ 
        Ordering to display newest post on top. 
        """
        ordering = ['-post_date']
        permissions = (("can_write_post", "Can write posts"),)

    def __str__(self):
        return f'{self.title} by {self.author}'

    def get_absolute_url(self):
        """ NOT SURE IF THIS WORKS """
        return reverse('post_detail', args=[str(self.id)])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.TextField(
        max_length=2000, help_text="Please enter your comment.")
    comment_date = models.DateTimeField(default=timezone.now)

    class Meta:
        """ Ordering to display newest comment on top. """
        ordering = ['-comment_date']
        permissions = (("can_write_comment", "Can comment"),)

    def __str__(self):
        """ String for representing the model object. """
        return f'{self.author}, {self.comment}'
