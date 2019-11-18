from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import datetime as dt
import bcrypt
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile('^[A-z]+$')
DEST_REGEX = re.compile('^[a-zA-Z0-9_]+( [a-zA-Z0-9_]+)*$')

class UsersManager(models.Manager):
    def validate_reg(self, postData):
        errors = {}
        email_duplicate = Users.objects.filter(email = postData['email'])
        
        if 'first_name'not in postData or 'last_name' not in postData or 'email' not in postData or 'password' not in postData or 'confirm_password' not in postData:
            errors['forms'] = "Stop"
            return errors
        
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be more than 2 characters!"
        elif not NAME_REGEX.match(postData['first_name']):
            errors['first_name'] = 'First name must only contain alphabet'
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be more than 2 characters!"
        elif not NAME_REGEX.match(postData['last_name']):
            errors['last_name'] = 'Last name must only contain alphabet'
        if len(postData['email']) < 10:
            errors['email'] = "Email must be more than 7 characters!"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invalid email format'
        if len(email_duplicate) > 0:
            errors['email'] = "Oops! Seems you have already registered with that email!"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be greater than 8 characters!"
        if postData['confirm_password'] != postData['password']:
            errors['password'] = "Passwords don't match!"
        return errors
    
    def validate_log(self, postData):
        errors = {}
        
        if 'email' not in postData or 'password' not in postData:
            errors['forms'] = "Stop"
            return errors
        if len(Users.objects.filter(email=postData['email'])):
            user = Users.objects.get(email=postData['email'])
            if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                return errors
            else:
                errors['login'] = "Invalid email/password"
                return errors
        else:
            errors['login'] = "Invalid email/password"
            return errors
        
        if not EMAIL_REGEX.match(postData['email']) or len(postData['email']) < 10:            
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors["password"] = "Invalid password/email"
        return errors
    
    def validate_destination(self, postData):
        errors={}
        if postData['start_date'] == '' or postData['end_date'] == '':
            errors['dates'] = "Dates can't be blank"
        else:
            start_date = datetime.strptime(postData['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(postData['end_date'], '%Y-%m-%d')
            if start_date.date() < dt.date.today():
                errors['start_date'] = "Start date must be future date"
            if postData['end_date'] < postData['start_date']:
                errors['end_date'] = "Travel end date must be after start date"
        if 'start_date' not in postData or 'end_date' not in postData or 'destination' not in postData or 'description' not in postData:
            errors['forms'] = "Stop"

        if len(postData['destination']) < 3:
            errors['destination'] = "Destination can't be blank"
        elif not DEST_REGEX.match(postData['destination']):
            errors['destination'] = 'Destination must only contain alphabet'
        if len(postData['description']) < 3:
            errors['description'] = "Description can't be blank"
        return errors
    
    def get_dates(self, postData):
        start_date = datetime.strptime(postData['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(postData['end_date'], '%Y-%m-%d')
        return start_date.date(), end_date.date()
    
class Users(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsersManager()
    
class Destination(models.Model):
    destination = models.CharField(max_length=150)
    description = models.CharField(max_length=150)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    planner = models.ForeignKey(Users, related_name = 'trips', on_delete=models.CASCADE)
    others = models.ManyToManyField(Users, related_name='joins')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsersManager()