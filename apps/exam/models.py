# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from .validation import Validation
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    # Validate login credentials and check authentication
    def check_login(self, post_data):
        # create object that will be returned
        input_reqs = [
            ('email', 'email', post_data['email']),
            ('pass_check', 'password', post_data['password'], post_data['password'], 8, 16)
        ]
        # Validate Post_Data using validation class and assign results to Validated
        validated = Validation(input_reqs)
        # Try to get user object with email address
        try:
            user = User.objects.get(email=validated.data['email'])
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
            ('email', 'email', post_data['email']),
            ('birthdate', post_data['birthdate']),
            ('pass_check', 'password', post_data['password'], post_data['confirm_password'], 8, 16)
        ]
        validated = Validation(input_reqs)
        if len(validated.errors) == 0:
            try:
                user_exists = User.objects.get(email=validated.data['email'])
            except:
                user_exists = False
            if user_exists == False:
                new_user = User.objects.create(f_name=validated.data['f_name'], l_name=validated.data['l_name'], email=validated.data['email'], birthdate=validated.data['birthdate'], password=validated.data['password'])
                validated.data['user_id'] = new_user.id
            else:
                validated.errors.append('The Email provided is already registered. Choose a different email or login.')
        return validated

class User(models.Model):
    f_name = models.CharField(max_length=30)
    l_name = models.CharField(max_length=40)
    email = models.CharField(max_length=65)
    birthdate = models.DateField()
    password = models.CharField(max_length=255)
    salt = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
