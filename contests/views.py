from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Contest
from django.contrib.auth.decorators import login_required
from contests.decorators import role_required

@login_required
def contests_list(request):
    contests = Contest.objects.all()
    return render(request, 'contests/contests_list.html', {'contests': contests})

@login_required
@role_required(['moderator','admin'])
def host_contest(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        # Create and save the new contest
        contest = Contest(
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            host=request.user
        )
        contest.save()
        messages.success(request, 'Contest created successfully!')
        return redirect('home')
    
    return render(request, 'contests/host_contest.html')