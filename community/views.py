from django.db.models import Q
from django.http import JsonResponse
from .models import Community
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Community, Post, Comment
from .forms import CommunityForm, PostForm
from django.http import JsonResponse, HttpResponseForbidden


def community_list(request):
    query = request.GET.get('q')
    if query:
        communities = Community.objects.filter(name__icontains=query)
    else:
        communities = Community.objects.all()
    
    followed_communities = []
    if request.user.is_authenticated:
        followed_communities = request.user.profile.followed_communities.all()
    
    context = {
        'communities': communities,
        'followed_communities': followed_communities,
        'query': query,
    }
    return render(request, 'community/community_list.html', context)


def community_detail(request, pk):
    community = get_object_or_404(Community, pk=pk)
    posts = Post.objects.filter(community=community)
    is_following = False

    if request.user.is_authenticated:
        is_following = request.user.profile.followed_communities.filter(pk=pk).exists()

    context = {
        'community': community,
        'posts': posts,
        'is_following': is_following,
    }
    return render(request, 'community/community_detail.html', context)

@login_required
def follow_community(request, pk):
    community = get_object_or_404(Community, pk=pk)
    request.user.profile.followed_communities.add(community)
    return JsonResponse({'success': True})

@login_required
def unfollow_community(request, pk):
    community = get_object_or_404(Community, pk=pk)
    request.user.profile.followed_communities.remove(community)
    return JsonResponse({'success': True})

# Need work
@login_required
def create_community(request):
    if request.method == 'POST':
        form = CommunityForm(request.POST)
        if form.is_valid():
            community = form.save(commit=False)
            community.created_by = request.user
            community.save()
            return redirect('community_detail', pk=community.pk)
    else:
        form = CommunityForm()
    return render(request, 'community/community_form.html', {'form': form})

@login_required
def create_post(request, pk):
    community = get_object_or_404(Community, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.community = community
            post.created_by = request.user
            post.save()
            return redirect('community_detail', pk=community.pk)
        else:
            return render(request, 'community/community_detail.html', {
                'community': community,
                'form': form
            })
    else:
        return redirect('community_detail', pk=community.pk)

@login_required
def delete_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)

        if post.created_by == request.user:
            post.delete()
            return JsonResponse({'success': True})
        else:
            return HttpResponseForbidden("You don't have permission to delete this post.")
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post).order_by('-created_at')

    context = {
        'post': post,
        'comments': comments
    }
    return render(request, 'community/post_detail.html', context)

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment = Comment.objects.create(
                post=post,
                content=content,
                created_by=request.user
            )
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'Content is required'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@login_required
def delete_comment(request):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        comment = get_object_or_404(Comment, id=comment_id, created_by=request.user)
        if comment:
            comment.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'Comment not found or you do not have permission to delete this comment'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})