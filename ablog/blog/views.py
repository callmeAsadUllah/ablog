from django.http import Http404
from django.shortcuts import (
    render,
    get_object_or_404
)
from django.core.mail import send_mail
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger
)
from django.views.decorators.http import (
    require_POST
)
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank
)
from django.db.models import Count



from taggit.models import Tag


from blog.models import (
    PostModel
)
from blog.forms import (
    EmailPostForm,
    CommentForm,
    SearchForm
)



def post_list(request, tag_slug=None):
    tag = None
    
    post_model = PostModel.objects.all()

    if tag_slug:
        try: tag = Tag.objects.get(slug=tag_slug)
        except Tag.DoesNotExist: raise Http404("No Tag found.")
        
        post_model = post_model.filter(tags__in=[tag])
        
    post_paginator = Paginator(post_model, 3)
    page_number = request.GET.get('page', 1)
    
    try: posts = post_paginator.page(page_number)
    except PageNotAnInteger: posts = post_paginator.page(1)
    except EmptyPage: posts = post_paginator.page(post_paginator.num_pages)
    
    context = {
        'posts': posts,
        'tag': tag
    }
    
    return render(
        request,
        'blog/post/list.html',
        context
    )
    
    
def post_detail(request, year, month, day, post):
    try:
        post_model = PostModel.objects.get(
            status=PostModel.StatusModel.PUBLISHED,
            slug=post,
            publish__year=year,
            publish__month=month,
            publish__day=day
        )
    except PostModel.DoesNotExist:
        raise Http404("No Post found.")
    
    comments = post_model.comments.filter(active=True)
    
    form = CommentForm()
    
    # List of similar posts
    post_tags_ids = post_model.tags.values_list('id', flat=True)
    similar_posts = PostModel.objects.filter(
        tags__in=post_tags_ids
    ).exclude(
        id=post_model.id
    )
    similar_posts = similar_posts.annotate(
        same_tags=Count(
            'tags'
        )
    )
    # .order_by(
    #     '-same_tags','-publish')[:4]
    
    context = {
        'post': post_model,
        'comments': comments,
        'form': form,
        'similar_posts': similar_posts
    }

    return render(
        request,
        'blog/post/detail.html',
        context
    )



def post_share(request, id):
    sent = False
    
    try:
        post_model = PostModel.objects.get(id=id)
    except PostModel.DoesNotExist:
        raise Http404("No Post found.")
    
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post_model.get_absolute_url()
            )
            subject = f"{cd['name']} recommends you read {post_model.title}"
            message = f"Read {post_model.title} at {post_url}\n\n{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'your_account@gmail.com',
            [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    
    context = {
        'post': post_model,
        'form': form,
        'sent': sent
    }
    
    return render(
        request,
        'blog/post/share.html',
        context
    )


@require_POST
def post_comment(request, id):
    comment = None
    
    try:
        post_model = PostModel.objects.get(id=id)
    except PostModel.DoesNotExist:
        raise Http404("No Post found.")
    
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post_model
        comment.save()
    
    context = {
        'post': post_model,
        'form': form,
        'comment': comment
    }
    
    return render(
        request,
        'blog/post/comment.html',
        context
    )


def post_search(request):
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            results = PostModel.objects.annotate(
                search=search_vector,
                rank=SearchRank(
                    search_vector,
                    search_query
                )).filter(rank__gte=0.3).order_by('-rank')
    form = SearchForm()
    
    context = {
        'form': form,
        'query': query,
        'results': results
    }
    
    return render(
        request,
        'blog/post/search.html',
        context
    )