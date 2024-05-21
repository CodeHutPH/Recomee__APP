from django.contrib import admin
from .models import InputResults

class InputResultsAdmin(admin.ModelAdmin):
    list_display = (
        'user_name', 'user_course', 'user_industry', 'user_skills',
        'user_interest', 'career_one', 'career_two', 'career_three',
        'career_one_prob', 'career_two_prob', 'career_three_prob'
    )

admin.site.register(InputResults, InputResultsAdmin)
