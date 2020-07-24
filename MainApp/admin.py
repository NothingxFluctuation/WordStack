from django.contrib import admin
from .models import WordData, SubjectData, EnterpriseData
# Register your models here.


class WordAdmin(admin.ModelAdmin):
    list_display = ('word','weight_kpi','variability_kpi','n_of_occurences','n_of_spread','mux','Max')

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('first_name','middle_name','last_name')

class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ('enterprise_name','enterprise_type','country','city')






admin.site.register(WordData, WordAdmin)
admin.site.register(SubjectData, SubjectAdmin)
admin.site.register(EnterpriseData, EnterpriseAdmin)

