from django.contrib import admin
from blog.models import Post, Comment, Author

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Author)
