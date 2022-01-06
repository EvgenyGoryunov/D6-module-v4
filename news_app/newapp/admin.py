from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'author', 'dateCreation', )

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )


admin.site.register(Author)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)


