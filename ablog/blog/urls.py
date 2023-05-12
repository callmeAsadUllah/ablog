from django.urls import path


from .views import (
    post_detail,
    post_list,
    post_share,
    post_comment
)

app_name = 'blog'

urlpatterns = [
    # post views
    path('', post_list, name='post_list'),
    # path('<id>/', post_detail, name='post_detail'),
    path(
        '<int:year>/<int:month>/<int:day>/<slug:post>/',
        post_detail,
        name='post_detail'
    ),
    #
    path(
        '<id>/share/',
        post_share,
        name='post_share'
    ),
    path(
        '<int:id>/comment/',
        post_comment,
        name='post_comment'
    )
]