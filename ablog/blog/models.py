from django.db import models
from django.db.models import Model
from django.db.models import Manager
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.urls import reverse


class PostListManager(Manager):
    def get_queryset(self):
        return super().get_queryset().all()


class CommentListManager(Manager):
    def get_queryset(self):
        return super().get_queryset().all()


# class PublishedManager(Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(
#             status=PostModel.StatusModel.PUBLISHED
#         )


class PostModel(Model):
    class StatusModel(models.TextChoices):
        DRAFT = ('DF', 'Draft')
        PUBLISHED = ('PB', 'Published')
    
    # relationship
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    
    # fields
    title = models.CharField(max_length=255)
    body = models.TextField()
    
    slug = models.SlugField(max_length=255)
    
    publish = models.DateTimeField(
        default=now,
        unique_for_date='publish'
    )
    
    status = models.CharField(
        max_length=2,
        choices=StatusModel.choices,
        default=StatusModel.DRAFT
    )
    
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    # manager
    # objects = Manager()
    list = PostListManager()
    # published = PublishedManager()
    
    class Meta:
        ordering = [
            'publish'
        ]
    
    def __str__(self):
        return f'{self.title}'
    
    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ]
        )


class CommentModel(Model):
    # relationship
    # user = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     related_name='blog_comments'
    # )
    post = models.ForeignKey(
        PostModel,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    # fields
    name = models.CharField(max_length=255)
    
    email = models.EmailField()
    
    body = models.TextField()
    
    active = models.BooleanField(default=True)
    
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = [
            'created_on'
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
    
    # def get_absolute_url(self):
    #     return reverse(
    #         'blog:post_detail',
    #         args=[
    #             self.publish.year,
    #             self.publish.month,
    #             self.publish.day,
    #             self.slug
    #         ]
    #     )