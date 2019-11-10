from django.db import models

class GenderManager(models.Manager):

    def choicefield_choices(self, *args, **kwargs):

        choices = [('---', '---')]

        for gender in self.all():
            choices.append((gender.gender, gender.gender))

        return choices

class Gender(models.Model):

    gender = models.CharField(max_length=30, unique=True)
    
    objects = GenderManager()

    def __str__(self):
        return self.gender
