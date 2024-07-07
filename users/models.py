from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, firstName, lastName, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), firstName=firstName, lastName=lastName)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, firstName, lastName, password):
        user = self.create_user(email, firstName, lastName, password)
        user.is_admin = True
        user.save(using=self._db)
        return user
    
import random
class User(AbstractBaseUser):
    userId = models.AutoField(primary_key=True)
    id = models.IntegerField(default=random.randint(100,45633))
    firstName = models.CharField(max_length=30, null=False)
    lastName = models.CharField(max_length=30, null=False)
    email = models.EmailField(unique=True, null=False)
    phone = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=100, null=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName']

    def __str__(self):
        return self.email

class Organisation(models.Model):
    orgId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(blank=True, null=True)
    users = models.ManyToManyField(User, related_name='organisations')

    def __str__(self):
        return self.name