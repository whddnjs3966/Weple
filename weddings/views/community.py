from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.core.paginator import Paginator
from weddings.models import Post, PostComment, NoticeComment, Notice, WeddingProfile
from weddings.forms import PostForm, PostCommentForm, NoticeCommentForm

@login_required
def community_main(request):
    try:
        profile = request.user.wedding_profile
        group = profile.group
        # if not group: pass
    except WeddingProfile.DoesNotExist:
        pass

    # Community Search & Sort
    search_query = request.GET.get('q', '')
    sort_option = request.GET.get('sort', 'date')
    category_filter = request.GET.get('category', '') # Added

    posts_qs = Post.objects.annotate(
        comment_count=Count('comments', distinct=True),
        recommendation_count=Count('recommendations', distinct=True)
    )

    # Filter by category
    if category_filter:
        posts_qs = posts_qs.filter(category=category_filter)

    # Filter by search query
    if search_query:
        posts_qs = posts_qs.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(author__first_name__icontains=search_query) |
            Q(author__username__icontains=search_query)
        )

    # Top recommended posts (only if no search query for cleaner results)
    top_posts = []
    if not search_query and not category_filter:
        top_posts = posts_qs.order_by('-recommendation_count', '-view_count')[:3]

    # Sort posts
    if sort_option == 'likes':
        posts_qs = posts_qs.order_by('-recommendation_count', '-created_at')
    elif sort_option == 'views': # Added sort by views
        posts_qs = posts_qs.order_by('-view_count', '-created_at')
    else:  # default 'date'
        posts_qs = posts_qs.order_by('-created_at')

    notices = Notice.objects.annotate(comment_count=Count('comments'))

    # Pagination
    paginator = Paginator(posts_qs, 10)  # 10 posts per page
    page_number = request.GET.get('page', 1)
    posts_page = paginator.get_page(page_number)
    
    context = {
        'posts': posts_page,
        'notices': notices,
        'top_posts': top_posts, # Added top recommended posts
        'search_query': search_query,
        'sort_option': sort_option,
        'category_filter': category_filter, # Added to context
        'CATEGORIES': Post.CATEGORY_CHOICES, # Pass choices to template
    }
    return render(request, 'weddings/community_main.html', context)

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('community_main')
    else:
        form = PostForm()
    return render(request, 'weddings/post_form.html', {'form': form})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Increment view count
    from django.db.models import F
    Post.objects.filter(id=post_id).update(view_count=F('view_count') + 1)
    post.refresh_from_db()

    comments = post.comments.all()
    form = PostCommentForm()
    return render(request, 'weddings/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })

@login_required
def comment_create(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        notice_id = request.POST.get('notice_id')
        
        if post_id:
            form = PostCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                post = get_object_or_404(Post, id=post_id)
                comment.post = post
                comment.save()
                return redirect('post_detail', post_id=post.id)
                
        elif notice_id:
            form = NoticeCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                notice = get_object_or_404(Notice, id=notice_id)
                comment.notice = notice
                comment.save()
                return redirect('community_main')
    
    return redirect('community_main')

@login_required
def post_recommend(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.recommendations.filter(id=request.user.id).exists():
        post.recommendations.remove(request.user)
    else:
        post.recommendations.add(request.user)
    
    next_url = request.META.get('HTTP_REFERER')
    if next_url:
        return redirect(next_url)
    return redirect('community_main')

@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        post.delete()
    return redirect('community_main')

@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('post_detail', post_id=post.id)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'weddings/post_form.html', {'form': form})
