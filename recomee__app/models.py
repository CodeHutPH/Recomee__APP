from django.db import models
import uuid

# Create your models here.

class Username(models.Model):
    name = models.CharField(max_length=100, null= True)

    def __str__(self):
        return self.name


class InputResults(models.Model):
    user_name = models.ForeignKey(Username, on_delete=models.CASCADE, null=True)
    user_course = models.CharField(max_length=100, null=True)
    user_industry = models.CharField(max_length=100, null=True)
    user_skills = models.CharField(max_length=100, null=True)
    user_interest = models.CharField(max_length=100, null=True)
    career_one = models.CharField(max_length=100, null=True)
    career_two = models.CharField(max_length=100, null=True)
    career_three = models.CharField(max_length=100, null=True)
    career_one_prob = models.IntegerField(null=True)
    career_two_prob = models.IntegerField(null=True)
    career_three_prob = models.IntegerField(null=True)
