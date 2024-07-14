import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse, HttpResponseBadRequest
from django.urls import reverse

# Models
from submissions.models import Submission
from .models import Problem, Language, TemporaryProblem ,TemporaryTestCase, TemporaryExpectedOutput
from submissions.models import TestCase, ExpectedOutput
from contests.decorators import role_required

# CSRF
from django.views.decorators.csrf import csrf_exempt

# Form
from .forms import CodeSubmissionForm



# Problem List

def problems_list(request):
    query = request.GET.get('q')
    if query:
        problems = Problem.objects.filter(Q(id__icontains=query) | Q(title__icontains=query))
    else:
        problems = Problem.objects.all()

    solved_problems = []
    if request.user.is_authenticated:
        solved_problems = Submission.objects.filter(user=request.user, status='Success').values_list('problem_id', flat=True)
        
    return render(request, 'problems/problems_list.html', {
        'problems': problems,
        'query': query,
        'solved_problems': solved_problems
    })
    
    
def problem_detail(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    solved = False

    if request.user.is_authenticated:
        solved = Submission.objects.filter(problem=problem, user=request.user, status='Success').exists()

    # print(solved)
    if request.method == 'POST':
        form = CodeSubmissionForm(request.POST)
    else:
        form = CodeSubmissionForm()

    return render(request, 'problems/problem_detail.html', {'problem': problem, 'form': form, 'solved': solved})

#Problem Submission

@login_required
# @csrf_protect
def run_code_transfer(request, pk):
    if request.method == 'POST':
        # print("CSRF token from request:", request.META.get('HTTP_X_CSRFTOKEN'))  # Debug statement
        form = CodeSubmissionForm(request.POST)
        
        if form.is_valid():
            language = form.cleaned_data['language']
            code = form.cleaned_data['code']
            input_data = form.cleaned_data['input_data']

            # Prepare the data to send
            data = {
                'language': language.id,
                'code': code,
                'custom_input': input_data,
            }
            # print(data) # {correct till now}
            
            # Build the absolute URL for the submissions API
            submissions_url = request.build_absolute_uri(reverse('run_code', kwargs={'pk': pk}))

            try:
                # Send POST request to the submissions API
                response = requests.post(submissions_url, data=data, cookies=request.COOKIES)                
                if response.status_code == 200:
                    return JsonResponse(response.json())
                else:
                    return HttpResponseBadRequest(f"Error: {response.text}")
            except requests.exceptions.RequestException as e:
                return HttpResponseBadRequest(f"RequestException: {str(e)}")

        return HttpResponseBadRequest('Invalid form data')
    else:
        form = CodeSubmissionForm()
    return render(request, 'problems/problem_detail.html', {'form': form})
            

@login_required
@csrf_exempt
def submit_code_transfer(request, pk):
    if request.method == 'POST':
        form = CodeSubmissionForm(request.POST)
        
        if form.is_valid():
            language = form.cleaned_data['language']
            code = form.cleaned_data['code']

            # Prepare the data to send
            data = {
                'language': language.id,
                'code': code,
            }
            # print(data) # {correct till now}
            
            # Build the absolute URL for the submissions API
            submissions_url = request.build_absolute_uri(reverse('submit_code', kwargs={'pk': pk}))

            try:
                # Send POST request to the submissions API
                response = requests.post(submissions_url, data=data, cookies=request.COOKIES)                
                if response.status_code == 200:
                    return JsonResponse(response.json())
                else:
                    return HttpResponseBadRequest(f"Error: {response.text}")
            except requests.exceptions.RequestException as e:
                return HttpResponseBadRequest(f"RequestException: {str(e)}")

        return HttpResponseBadRequest('Invalid form data')
    else:
        form = CodeSubmissionForm()
    return render(request, 'problems/problem_detail.html', {'form': form})


@login_required
@role_required(['moderator', 'admin'])
def review_problems(request):
    temp_problems = TemporaryProblem.objects.all()
    return render(request, 'problems/review_problems.html', {'temp_problems': temp_problems})

# views.py

@login_required
def add_problem_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        input_description = request.POST.get('input_description')
        output_description = request.POST.get('output_description')
        example_input = request.POST.get('example_input')
        example_output = request.POST.get('example_output')
        difficulty = request.POST.get('difficulty')
        author = request.user
        test_case_count = int(request.POST.get('test_case_count'))

        # Create the problem instance
        problem = TemporaryProblem.objects.create(
            title=title,
            description=description,
            input_description=input_description,
            output_description=output_description,
            example_input=example_input,
            example_output=example_output,
            difficulty=difficulty,
            author=author
        )
        # print(test_case_count)
        # Handle test cases
        for i in range(1, test_case_count + 1):
            input_data = request.POST.get(f'test_cases_{i}')
            if input_data:
                test_case = TemporaryTestCase.objects.create(
                    temporary_problem=problem,
                    input_data=input_data
                )
                # Handle expected outputs for each test case
                expected_outputs = request.POST.getlist(f'expected_outputs_{i}[]')
                for output in expected_outputs:
                    TemporaryExpectedOutput.objects.create(
                        test_case=test_case,
                        output=output
                    )
        
        messages.success(request, 'Problem added successfully!')
        return redirect('add_problem')
    
    return render(request, 'problems/add_problem.html')


@login_required
@role_required(['moderator', 'admin'])
def approve_problem_view(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to approve problems.')
        return redirect('home')
    
    temp_problem = get_object_or_404(TemporaryProblem, pk=pk)
    
    if request.method == 'POST':
        # Create the permanent problem instance
        problem = Problem.objects.create(
            title=temp_problem.title,
            description=temp_problem.description,
            input_description=temp_problem.input_description,
            output_description=temp_problem.output_description,
            example_input=temp_problem.example_input,
            example_output=temp_problem.example_output,
            difficulty=temp_problem.difficulty,
            author=temp_problem.author
        )
        
        # Handle test cases
        for temp_test_case in temp_problem.temporary_test_cases.all():
            test_case = TestCase.objects.create(
                problem=problem,
                input_data=temp_test_case.input_data
            )
            # Handle expected outputs for each test case
            for temp_expected_output in temp_test_case.temporary_expected_outputs.all():
                ExpectedOutput.objects.create(
                    test_case=test_case,
                    output=temp_expected_output.output
                )
        
        # Delete the temporary problem and its related data
        temp_problem.delete()
        
        messages.success(request, 'Problem approved successfully!')
        return redirect('review_problems')
    
    return render(request, 'problems/approve_problem.html', {
        'temp_problem': temp_problem,
        'test_cases': temp_problem.temporary_test_cases.all()
    })

@login_required
@role_required(['moderator', 'admin'])
def discard_problem_view(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to discard problems.')
        return redirect('home')
    
    temp_problem = get_object_or_404(TemporaryProblem, pk=pk)
    
    if request.method == 'POST':
        # Delete the temporary problem and its related data
        temp_problem.delete()
        
        messages.success(request, 'Problem discarded successfully!')
        return redirect('review_problems')
    
    return redirect('review_problems')