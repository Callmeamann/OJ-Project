from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Role
from django.views.decorators.http import require_GET, require_POST
from django.http import JsonResponse
from contests.decorators import role_required


@require_GET
@login_required
@role_required(['moderator', 'admin'])
def user_search_api(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(username__icontains=query)[:10]  # Limit results for performance
    results = []
    for user in users:
        results.append({
            'id': user.id,
            'username': user.username,
            'role': user.profile.role.name,  # Adjust based on your user model
        })
    return JsonResponse(results, safe=False)

@require_POST
@login_required
@role_required(['moderator', 'admin'])
def update_user_role(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        role_id = request.POST.get('role_id')
        user = User.objects.get(id=user_id)
        role = Role.objects.get(id=role_id)

        user.profile.role = role
        user.profile.save()

        messages.success(request, f'Role for user {user.username} successfully updated to {role.name}!')
        return redirect('update_user_role_view')
    else:
        return render(request, 'admin/update_user_role.html')

@login_required
@role_required(['moderator', 'admin'])
def update_user_role_view(request):
    roles = Role.objects.all()
    return render(request, 'admin/update_user_role.html', {'roles': roles})