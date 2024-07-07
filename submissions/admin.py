from django.contrib import admin
from .models import Submission, TestCase, ExpectedOutput

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'language', 'created_at', 'updated_at')
    list_filter = ('user', 'language', 'created_at')
    search_fields = ('user__username', 'language__name', 'code')
    readonly_fields = ('created_at', 'updated_at')

class ExpectedOutputInline(admin.TabularInline):
    model = ExpectedOutput
    extra = 1

@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'problem', 'input_data')
    inlines = [ExpectedOutputInline]

@admin.register(ExpectedOutput)
class ExpectedOutputAdmin(admin.ModelAdmin):
    list_display = ('id', 'test_case', 'output')