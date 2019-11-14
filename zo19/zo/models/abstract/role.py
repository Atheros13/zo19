from django.db import models


class Role(models.Model):

    ''' '''

    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)

    class Meta:

        abstract = True

    def __str__(self):

        return self.name
