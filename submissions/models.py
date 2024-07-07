from django.db import models
from django.contrib.auth.models import User
from problems.models import Language,Problem

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    code = models.TextField()
    input_data = models.TextField(blank=True, null=True)
    output_data = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.language.name} - {self.created_at}'

class TestCase(models.Model):
    problem = models.ForeignKey(Problem, related_name='submmision_test_cases', on_delete=models.CASCADE)
    input_data = models.TextField()

    def __str__(self):
        return f"TestCase {self.id} for {self.problem.title}"

class ExpectedOutput(models.Model):
    test_case = models.ForeignKey(TestCase, related_name='submission_expected_outputs', on_delete=models.CASCADE)
    output = models.TextField()

    def __str__(self):
        return f"ExpectedOutput {self.id} for TestCase {self.test_case.id}"