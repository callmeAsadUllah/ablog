from django.urls import path


from blog.feeds import (
    PostFeed
)


from blog.views import (
    post_detail,
    post_list,
    post_share,
    post_comment,
    post_search
)


app_name = 'blog'


urlpatterns = [
    # post views
    path('', post_list, name='post_list'),
    #
    path('tag/<slug:tag_slug>/', post_list, name='post_list_by_tag'),
    # path('<id>/', post_detail, name='post_detail'),
    path(
        '<int:year>/<int:month>/<int:day>/<slug:post>/',
        post_detail,
        name='post_detail'
    ),
    #
    path(
        '<int:id>/share/',
        post_share,
        name='post_share'
    ),
    path(
        '<int:id>/comment/',
        post_comment,
        name='post_comment'
    ),
    path('feed/', PostFeed(), name='post_feed'),
    path('search/', post_search, name='post_search'),
]