from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Submission, TestCase
from problems.models import Problem, Language

from django.contrib.auth.decorators import login_required
import subprocess
import uuid
from pathlib import Path
from django.conf import settings

@login_required
@csrf_exempt
def run_code(request, pk):
    if request.method == 'POST':
        # print("CSRF token from request:", request.META.get('HTTP_X_CSRFTOKEN'))  # Debug statement
        user = request.user
        language_id = request.POST.get('language')
        code = request.POST.get('code')
        input_data = request.POST.get('custom_input', '')  # Get custom input from the request

        # # Debugging prints
        # print('input_data:', input_data)
        # print('request.POST:', request.POST)
        # print('language_id:', language_id)
        # print('code:', code)

        if not language_id or not code:
            return HttpResponseBadRequest("Missing required parameters.")

        try:
            language = Language.objects.get(id=language_id)
        except Language.DoesNotExist:
            return HttpResponseBadRequest("Invalid language.")
        
        # Execute the code
        result = execute_code(language.id, code, input_data)
        result = result.strip()                                             # Remove leading/trailing whitespaces
        # print(result)                                                     # Debug print
        # Create a submission record
        
        submission = Submission.objects.create(
            user=user,
            language=language,
            code=code,
            input_data=input_data,
            output_data=result
        )
        # print(result) # debug print
        return JsonResponse({'result': result, 'submission_id': submission.id})

    else:
        return HttpResponse("This endpoint only supports POST requests.", status=405)


# API for Submit Code

@login_required
@csrf_exempt
def submit_code(request, pk):
    if request.method == 'POST':
        user = request.user
        language_id = request.POST.get('language')
        code = request.POST.get('code')

        if not language_id or not code:
            return HttpResponseBadRequest("Missing required parameters.")

        try:
            language = Language.objects.get(id=language_id)
        except Language.DoesNotExist:
            return HttpResponseBadRequest("Invalid language.")

        try:
            problem = Problem.objects.get(pk=pk)
            test_cases = TestCase.objects.filter(problem=problem)
        except Problem.DoesNotExist:
            return HttpResponseBadRequest('Problem not found')
        
        # Compare the output of the code with the expected output of each test case
        results = []
        for test_case in test_cases:
            actual_output = execute_code(language.id, code, test_case.input_data).strip()
            
            # Retrieve all expected outputs for the test case
            expected_outputs = test_case.submission_expected_outputs.all()
            
            # Check if actual_output matches any of the expected outputs
            is_success = any(expected_output.output.strip() == actual_output for expected_output in expected_outputs)
            status = 'Success' if is_success else 'Fail'
            
            result = {
                'test_case_id': test_case.id,
                'input': test_case.input_data,
                'expected_outputs': [eo.output for eo in expected_outputs],
                'actual_output': actual_output,
                'status': status,
            }
            results.append(result)
            
            if status == 'Fail':
                # Save the code and return a success message
                submission = Submission.objects.create(
                    user=user,
                    problem=problem,
                    language=language,
                    code=code,
                    status=status,
                )
                return JsonResponse({
                    'status': status,
                    'test_id': test_case.id,
                    'submission_id': submission.id,
                    'expected_output': [eo.output for eo in expected_outputs],
                    'actual_output': actual_output
                })
        
        # Save the code and return a success message
        submission = Submission.objects.create(
            user=user,
            problem=problem,
            language=language,
            code=code,
            status='Success',
        )
        
        return JsonResponse({'status': 'Success', 'submission_id': submission.id})
    else:
        return HttpResponse("This endpoint only supports POST requests.", status=405)



# Execute code function (Do not Perform Updations)

def execute_code(language, code, input_data):
    project_path = Path(settings.RESOURCES_DIR)
    directories = ["codes", "inputs", "outputs"]

    for directory in directories:
        dir_path = project_path / directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)

    codes_dir = project_path / "codes"
    inputs_dir = project_path / "inputs"
    outputs_dir = project_path / "outputs"

    unique = str(uuid.uuid4())

    # Determine file extensions based on language
    if language == 1:
        code_file_extension = "cpp"
    elif language == 3:
        code_file_extension = "py"
    elif language == 2:
        code_file_extension = "java"
    else:
        return "Unsupported language"

    code_file_name = f"{unique}.{code_file_extension}"
    input_file_name = f"{unique}.txt"
    output_file_name = f"{unique}.txt"

    code_file_path = codes_dir / code_file_name
    input_file_path = inputs_dir / input_file_name
    output_file_path = outputs_dir / output_file_name

    with open(code_file_path, "w") as code_file:
        code_file.write(code)

    with open(input_file_path, "w") as input_file:
        input_file.write(input_data)

    with open(output_file_path, "w") as output_file:
        pass  # This will create an empty file

    try:
        if language == 1:
            executable_path = codes_dir / unique
            compile_result = subprocess.run(
                ["g++", str(code_file_path), "-o", str(executable_path)],
                capture_output=True,
                text=True
            )
            if compile_result.returncode != 0:
                return filter_error_message(compile_result.stderr)

            with open(input_file_path, "r") as input_file, open(output_file_path, "w") as output_file:
                subprocess.run(
                    [str(executable_path)],
                    stdin=input_file,
                    stdout=output_file,
                    stderr=subprocess.STDOUT
                )
        
        elif language == 3:
            with open(input_file_path, "r") as input_file, open(output_file_path, "w") as output_file:
                run_result = subprocess.run(
                    ["python", str(code_file_path)],
                    stdin=input_file,
                    stdout=output_file,
                    stderr=subprocess.PIPE,
                    text=True
                )
                if run_result.returncode != 0:
                    return filter_error_message(run_result.stderr)
        
        elif language == 2:
            compile_result = subprocess.run(
                ["javac", str(code_file_path)],
                capture_output=True,
                text=True
            )
            if compile_result.returncode != 0:
                return filter_error_message(compile_result.stderr)

            class_file = code_file_path.stem  # Get the filename without extension
            with open(input_file_path, "r") as input_file, open(output_file_path, "w") as output_file:
                subprocess.run(
                    ["java", "-cp", str(codes_dir), class_file],
                    stdin=input_file,
                    stdout=output_file,
                    stderr=subprocess.STDOUT
                )

        with open(output_file_path, "r") as output_file:
            output_data = output_file.read()

    finally:
        # pass
        # Clean up files
        code_file_path.unlink(missing_ok=True)
        input_file_path.unlink(missing_ok=True)
        output_file_path.unlink(missing_ok=True)
        if language == 1 and executable_path.exists():
            executable_path.unlink(missing_ok=True)
        elif language == 2:
            class_file_path = codes_dir / f"{class_file}.class"
            if class_file_path.exists():
                class_file_path.unlink(missing_ok=True)

    return output_data

# Error Filter Function

def filter_error_message(error):
    """
    This function takes an exception object and returns a filtered error message.
    """
    import traceback
    tb = traceback.format_exception(None, error, error.__traceback__)
    filtered_message = ""
    for line in tb:
        if "File" in line and ", line" in line:
            filtered_message += line
        elif "Error" in line or "Exception" in line:
            filtered_message += line
    return filtered_message.strip()
