from django.contrib import admin
from .models import BlogPost
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'keyword', 'slug', 'readcount', 'pub_date')

admin.site.register(BlogPost, PostAdmin)