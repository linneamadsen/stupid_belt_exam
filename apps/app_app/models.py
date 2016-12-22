from __future__ import unicode_literals
from django.db import models
import re

REGEX_EMAIL = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate_user(self, name, email, birthday, password, re_password):
        validation_errors = []

        if REGEX_EMAIL.search(email) is None:
            validation_errors.append("Email is not valid")
        if len(name) == 0:
            validation_errors.append("Name cannot be empty")
        if len(email) == 0:
            validation_errors.append("Email cannot be empty")
        # if len(birthday) == 0:
        #     validation_errors.append("Birthday cannot be empty")
        if len(password) == 0:
            validation_errors.append("Password cannot be empty")
        if password != re_password:
            validation_errors.append("Passwords must match")
        return validation_errors

    def validate_login(self, email, password):
        return len(email) != 0 and len(password) != 0

    def authenticate_user(self, email, password):
        if self.validate_login(email, password):
            try:
                user = User.objects.get(email=email)
                return user.password == password
            except:
                return False
        else:
            return False


class User(models.Model):
    name = models.CharField(max_length=64, blank=False)
    email = models.EmailField(unique=True, blank=False)
    password = models.CharField(max_length=64, blank=False)
    birthday = models.DateField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Appointment(models.Model):
    description = models.CharField(max_length=2048, blank=False)
    due_date = models.CharField(max_length=64, blank=False)
    time_due = models.CharField(max_length=64, blank=False)
    status = models.CharField(max_length=16, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('User')
