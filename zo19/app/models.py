from __future__ import unicode_literals

from django.db import models
from django.conf import settings 
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail, BadHeaderError
from django.utils.translation import ugettext_lazy as _


### ABSTRACT BASE MODELS ###

class NamePerson(models.Model):

    ''' An abstract class which can be inherited by other models, 
    to be give a person-based "name" to a model i.e. User, HubMember etc. '''

    firstname = models.CharField(verbose_name='First Name', max_length=50)
    middlenames = models.CharField(verbose_name='Middle Name/s', max_length=50, 
                                   blank=True)
    surname = models.CharField(max_length=30)
    
    preferred_name = models.CharField(verbose_name='Preferred Name', max_length=50, 
                                      blank=True, default='')

    class Meta:

        abstract = True

    def __str__(self):
        firstname = self.firstname
        if self.preferred_name:
            firstname = self.preferred_name
        
        return '%s %s' % (firstname, self.surname)

    def name(self):
        if self.preferred_name:
            return self.preferred_name
        return self.firstname

    def fullname(self, preferred=True):

        firstname = self.firstname
        if preferred == True and self.preferred_firstname != '':
            firstname = self.preferred_firstname

        return '%s %s %s' % (firstname, self.middlenames, self.surname)

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

### BASE MODELS ###

class Gender(models.Model):

    gender = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.gender

### USER ###

class UserManager(BaseUserManager):
    
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):

    ''' '''

    ### IN ATTRIBUTES ###
    # name

    ## OWN ATTRIBUTES
    email = models.EmailField(unique=True)
    dob = models.DateField(null=True)
    phone_number = models.CharField(max_length=30, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # is ZO-SPORTS staff i.e. can access /admin
    is_authorised = models.BooleanField(default=False) # Authorised/Verified User - create Hubs/Tournaments

    ## OUT ATTRIBUTES
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True, related_name='users')

    ### MISC ###
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    ### META DATA ###
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

        
    def __str__(self):
        try:
            return self.name.__str__()
        except:
            return self.email

    ### FUNCTIONS ###
    def email_user(self, subject, message, from_email='no-reply@zo-sports.com', **kwargs):
        
        ''' Sends an email to this User. '''

        send_mail(subject, message, from_email, [self.email])

### USER MODELS ###

class UserName(NamePerson):

    ''' A NamePerson inherited model, for use with a User. '''

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE, related_name='name')

class UserAddress(Address):

    ''' An Address inherited model, for use with a User. '''

    user = models.OneToOneField(settings.AUTH_USER_MODEL, 
                                    on_delete=models.CASCADE, related_name='address')