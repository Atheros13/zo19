from django.contrib import admin
from zo.models import AgeGrade

class AgeGradeAdmin(admin.ModelAdmin):
    fields = ['open', 'under', 'age', 'date']

admin.site.register(AgeGrade, AgeGradeAdmin)