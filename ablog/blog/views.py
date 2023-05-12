from django.http import Http404
from django.shortcuts import (
    render
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


from .models import (
    PostModel
)
from .forms import (
    EmailPostForm,
    CommentForm
)


def post_list(request):
    post_model = PostModel.list.all()
    
    post_paginator = Paginator(post_model, 3)
    page_number = request.GET.get('page', 1)
    try: posts = post_paginator.page(page_number)
    except PageNotAnInteger: posts = post_paginator.page(1)
    except EmptyPage: posts = post_paginator.page(post_paginator.num_pages)
    
    context = {
        'posts': posts
    }
    
    return render(
        request,
        'blog/post/list.html',
        context
    )
    
    
def post_detail(request, year, month, day, post):
    try:
        post_model = PostModel.list.get(
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
    
    context = {
        'post': post_model,
        'comments': comments,
        'form': form
    }

    return render(
        request,
        'blog/post/detail.html',
        context
    )



def post_share(request, id):
    sent = False
    
    try:
        post_model = PostModel.list.get(id=id)
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
        post_model = PostModel.list.get(id=id)
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