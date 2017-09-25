from django.contrib import admin
from BLOG.models import BlogPost,Category,Tag

# Register your models here.
admin.site.register(BlogPost)
admin.site.register(Category)
admin.site.register(Tag)