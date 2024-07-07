from django.db import models
from django.contrib.auth.models import User

class Language(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Problem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    input_description = models.TextField()
    output_description = models.TextField()
    example_input = models.TextField()
    example_output = models.TextField()
    difficulty = models.CharField(max_length=50, default='Medium')  # Default value for difficulty
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Default to the first user (adjust as needed)

    def __str__(self):
        return self.title

class TemporaryProblem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    input_description = models.TextField()
    output_description = models.TextField()
    example_input = models.TextField()
    example_output = models.TextField()
    difficulty = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class TemporaryTestCase(models.Model):
    # problem = models.ForeignKey(Problem, related_name='problem_test_cases', on_delete=models.CASCADE, null=True, blank=True)
    temporary_problem = models.ForeignKey(TemporaryProblem, related_name='temporary_test_cases', on_delete=models.CASCADE, null=True, blank=True)
    input_data = models.TextField()

    def __str__(self):
        return f"TestCase {self.id} for Problem {self.temporary_problem.title}"

class TemporaryExpectedOutput(models.Model):
    test_case = models.ForeignKey(TemporaryTestCase, related_name='temporary_expected_outputs', on_delete=models.CASCADE)
    output = models.TextField()

    def __str__(self):
        return f"ExpectedOutput {self.id} for TestCase {self.test_case.id}"