import markdown


from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe


from blog.models import (
    PostModel
)


register = template.Library()


@register.simple_tag(name='post_model_list')
def total_posts():
    return PostModel.objects.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=3):
    latest_posts = PostModel.objects.order_by('-publish')[:count]
    return {
        'latest_posts': latest_posts
    }


@register.simple_tag
def get_most_commented_posts(count=2): # default value for count is 5.
    return PostModel.objects.annotate(
        total_comments=Count(
            'comments'
        )
    ).order_by(
        '-total_comments'
    )[
        :count
    ]
    
    

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
