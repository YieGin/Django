from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .form import EmailPostForm
from django.core.mail import send_mail


# def post_list(request):
#     post_list = Post.objects.all()
#     paginator = Paginator(post_list, 3)
#     page_number = request.GET.get('page', 1)
#     try:
#         posts = paginator.page(page_number)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     return render(request, 'blog/post/list.html', {'posts': posts})


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
    
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             )
    return render(request, 'blog/post/detail.html', {'post': post})


def post_share(request, post_id):
    # Retrieve the post by ID or return 404 if not found
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)

    # Initialize 'sent' flag
    sent = False

    # Create a new form instance for GET requests
    if request.method == 'GET':
        form = EmailPostForm()

    # Process form data if request method is POST
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n{cd['name']}'s comments: {cd['comments']}"
            send_mail(subject, message, 'pumasami7@gmail.com', [cd['to']])
            sent = True

    # Render response with form and post data
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})
