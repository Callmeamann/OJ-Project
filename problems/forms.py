from django import forms
from .models import Language, TemporaryProblem
from submissions.models import Submission
from .models import TemporaryExpectedOutput, TemporaryTestCase

class CodeSubmissionForm(forms.ModelForm):
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        empty_label="Select Language",
        widget=forms.Select(attrs={
            'id': 'language-select',  # Ensure it has an id for JavaScript
            'class': 'form-control'   # Maintain the form-control class
        })
    )

    code = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'id': 'code-textarea',  # Ensure it has an id for JavaScript
            'class': 'hidden-textarea',  # Add a class to hide it
            'style': 'display:none;',  # Hide the original textarea
            # 'placeholder': 'Write your code here...',
        })
    )

    input_data = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'id': 'input-data',  # Ensure it has an id for JavaScript
            'class': 'hidden-textarea',  # Add a class to hide it
            'style': 'display:none;',  # Hide the original textarea
        })
    )
    
    class Meta:
        model = Submission
        fields = ['language', 'code', 'input_data']


# class AddProblemForm(forms.ModelForm):
#     class Meta:
#         model = TemporaryProblem
#         fields = [
#             'title', 'description', 'input_description', 'output_description', 
#             'example_input', 'example_output', 'difficulty'
#         ]

# class TemporaryTestCaseForm(forms.ModelForm):
#     class Meta:
#         model = TemporaryTestCase
#         fields = [
#              'input_data'
#         ]

# class TemporaryExpectedOutputForm(forms.ModelForm):
#     class Meta:
#         model = TemporaryExpectedOutput
#         fields = [
#             'output'
#         ]