# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from .validation import Validation
from datetime import datetime
from dateutil import relativedelta
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    # Validate login credentials and check authentication
    def check_login(self, post_data):
        # create object that will be returned
        input_reqs = [
            ('user_check', 'username', post_data['username']),
            ('pass_check', 'password', post_data['password'], post_data['password'], 8, 16)
        ]
        # Validate Post_Data using validation class and assign results to Validated
        validated = Validation(input_reqs)
        # Try to get user object with email address
        try:
            user = User.objects.get(username=validated.data['username'])
        except:
            # If user does not exist set user to false and return validated with validation resuls
            user = False
            validated.errors.append('User Does not exist')
            return validated
        if user:
            validated.data['id'] = user.id
            validated.data['hash'] = user.password.encode()
            if bcrypt.hashpw(post_data['password'].encode(), validated.data['hash']) == validated.data['hash']:
                validated.data['status'] = 'Authenticated'
            else:
                validated.data['status'] = 'Failed'
        return validated

    def check_register(self, post_data):
        input_reqs = [
            ('alpha', 'f_name', post_data['f_name']),
            ('alpha', 'l_name', post_data['l_name']),
            ('user_check', 'username', post_data['username']),
            ('pass_check', 'password', post_data['password'], post_data['confirm_password'], 8, 16)
        ]
        validated = Validation(input_reqs)
        if len(validated.errors) == 0:
            try:
                user_exists = User.objects.get(email=validated.data['email'])
            except:
                user_exists = False
            if user_exists == False:
                new_user = User.objects.create(f_name=validated.data['f_name'], l_name=validated.data['l_name'], username=validated.data['username'], password=validated.data['password'])
                validated.data['user_id'] = new_user.id
            else:
                validated.errors.append('The Email provided is already registered. Choose a different email or login.')
        return validated

class User(models.Model):
    f_name = models.CharField(max_length=30)
    l_name = models.CharField(max_length=40)
    username = models.CharField(max_length=65)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class TravelManager(models.Manager):
    def validate_travel_info(self,post_data):
        input_reqs = [
            ('text_check', 'destination', post_data['destination']),
            ('text_check', 'description', post_data['description']),
        ]

        validated = Validation(input_reqs)
        try:
            validated.data['date_from'] = datetime.strptime(post_data['date_from'], '%Y-%m-%d')
            validated.data['date_to'] = datetime.strptime(post_data['date_to'], '%Y-%m-%d')
        except:
            validated.errors.append('Please Verify the format of the date and time selected')
        if len(validated.errors) == 0:
            if validated.data['date_from'] < datetime.now():
                validated.errors.append('Travel From Date must be a date in the future')
            if validated.data['date_to'] < datetime.now() or validated.data['date_to'] < validated.data['date_from']:
                validated.errors.append('Travel To Date must be a date in the future and must be after Travel From Date')
        return validated

    def create_travel(self, post_data, user_id):
        user = User.objects.get(id=user_id)
        try:
            travel_log_id = Travel.objects.create(destination=post_data['destination'], description=post_data['description'], planner=user, date_from=post_data['date_from'], date_to=post_data['date_to'])
        except:
            travel_log_id = False
        if travel_log_id != False:
            travel_log = Travel.objects.get(id=travel_log_id.id)
            travel_log.user.add(user)
        return travel_log_id

    def validate_join(self, post_data):
        data = {
        'errors' : []
        }
        try:
            user = User.objects.get(id=post_data['user_id'])
        except:
            user = False
        try:
            valid_travel = Travel.objects.get(id=post_data['travel_id'])
        except:
            valid_travel = False
        if user == False or valid_travel == False:
            data['errors'].append('Make sure you are logged into your account and trying to add a valid Travel plan.')
        else:
            valid_travel.user.add(user)
        return data




class Travel(models.Model):
    destination = models.CharField(max_length=65)
    description = models.CharField(max_length=140)
    date_from = models.DateField()
    date_to = models.DateField()
    planner = models.ForeignKey(User, related_name='planned_by_user')
    user = models.ManyToManyField(User, related_name='users_travels')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TravelManager()
