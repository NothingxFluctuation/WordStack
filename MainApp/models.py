from django.db import models
from django.utils import timezone


# Create your models here.

class WordData(models.Model):
    word = models.CharField(max_length=1000)
    weight_kpi = models.CharField(max_length=1000, null=True, blank=True)
    variability_kpi = models.CharField(max_length=1000, null=True, blank=True)
    n_of_occurences = models.CharField(max_length=1000, null=True, blank=True)
    n_of_spread = models.CharField(max_length=1000, null=True, blank=True)
    mux = models.CharField(max_length=1000, null=True, blank=True)
    Max = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.word




class SubjectData(models.Model):
    first_name = models.CharField(max_length=1000, null=True, blank=True)
    middle_name = models.CharField(max_length=1000, null=True, blank=True)
    last_name = models.CharField(max_length=1000, null=True, blank=True)


    def __str__(self):
        if self.first_name:
            return self.first_name
        elif self.middle_name:
            return self.middle_name
        else:
            return self.last_name



class EnterpriseData(models.Model):
    enterprise_name = models.CharField(max_length=1000, null=True, blank=True)
    enterprise_type = models.CharField(max_length=1000, null=True, blank=True)
    country = models.CharField(max_length=1000, null=True, blank=True)
    city = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        if self.enterprise_name:
            return self.enterprise_name
        elif self.enterprise_type:
            return self.enterprise_type
        elif self.country:
            return self.country
        else:
            return self.city

