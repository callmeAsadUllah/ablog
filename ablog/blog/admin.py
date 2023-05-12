from django.contrib import admin
from django.contrib.admin import ModelAdmin


from .models import (
    PostModel,
    CommentModel
)


@admin.register(PostModel)
class PostAdminModel(ModelAdmin):
    list_display = [
        'title',
        'slug',
        'user',
        'publish',
        'status'
    ]
    
    list_filter = [
        'status',
        'created_on',
        'publish',
        'user'
    ]
    
    search_fields = [
        'title',
        'body'
    ]
    
    prepopulated_fields = {
        'slug': (
            'title',
        )
    }
    
    raw_id_fields = [
        'user'
    ]
    
    date_hierarchy = 'publish'
    
    ordering = [
        'status',
        'publish'
    ]


@admin.register(CommentModel)
class CommentAdminModel(ModelAdmin):
    pass