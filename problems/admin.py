from django.contrib import admin
from .models import Problem,Language, TemporaryProblem, TemporaryExpectedOutput, TemporaryTestCase

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')
    search_fields = ('title', 'description')
  
# Register the Language model
@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(TemporaryProblem)
class TemporaryProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'author', 'created_at')
    search_fields = ('title', 'description', 'author__username')
    

class TestCaseExpectedOutputInline(admin.TabularInline):
    model = TemporaryExpectedOutput
    extra = 1  # How many empty forms to display

@admin.register(TemporaryTestCase)
class TemporaryTestCaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'temporary_problem', 'input_data')
    search_fields = ('problem__title', 'temporary_problem__title', 'input_data')
    list_filter = ('temporary_problem', )
    inlines = [TestCaseExpectedOutputInline]

@admin.register(TemporaryExpectedOutput)
class TemporaryExpectedOutputAdmin(admin.ModelAdmin):
    list_display = ('id', 'test_case', 'output')
    search_fields = ('test_case__input_data', 'output')
    list_filter = ('test_case',)
