""" 
"""

from django.db import models

class Address(models.Model):
	
    ''' An abstract object which can be inherited to add an address to another object 
    i.e. UserAddress, HubAddress. '''

    line1 = models.CharField(verbose_name='Address Line 1', max_length=50)
    line2 = models.CharField(verbose_name='Address Line 2',max_length=50, blank=True)
    line3 = models.CharField(verbose_name='Address Line 3',max_length=50, blank=True)
    town_city = models.CharField(verbose_name='Town/City',max_length=50)
    postcode = models.CharField(verbose_name='Postcode',max_length=50, blank=True)
    country = models.CharField(verbose_name='Country',max_length=50, blank=True)

    class Meta:

        abstract = True

    def __str__(self):
        address = '%s\n' % self.line1
        for l in [self.line2, self.line3, self.town_city, self.postcode, self.country]:
            if l != '':
                address += '%s\n' % l
        return address.rstrip()

