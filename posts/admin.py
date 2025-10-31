from django.contrib import admin
from posts.models import Post
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','author','is_draft','created_at')
    list_filter = ('is_draft','created_at')
    search_fields = ('title','description')

admin.site.register(Post,PostAdmin)