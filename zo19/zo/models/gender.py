from django.db import models

class Gender(models.Model):

    gender = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.gender
