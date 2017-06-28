# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Travel

# Create your views here.

##############################
## Authentication Functions ##
##############################

# Index Get Route
def index(request):
    # If user status not set in Session redirect to login.
    if 'user_status' not in request.session or request.session['user_status'] != 'Authenticated':
        return redirect('/login')
    # Render index.html
    return redirect('/travels')
# Login Get Route
def login(request):
    return render(request, 'exam/login.html')
# Process Login Post Authentication
def authenticate(request):
    # Verify Request is of type POST
    if request.method == 'POST':
        # Copy Post Data
        post_data = request.POST.copy()
        # Pass Post Data copy int UserManager check_login
        validated = User.objects.check_login(post_data)
        # Check if any errors during Validation
        if len(validated.errors) > 0:
            # If Errors - loop through error messages and populate to messages
            for err in validated.errors:
                messages.error(request, err)
            # Redirect to Index route
            return redirect('/')
        else:
        # If Validation had 0 errors
            # Set Session with user info
            request.session['user_id'] = validated.data['id']
            request.session['user_status'] = validated.data['status']
            # populate success message
            messages.success(request, "Welcome Back!")
    # redirect to index route
    return redirect('/')
# Register Get Route
def register(request):
    return render(request, 'exam/register.html')
# Process Post Request from Register
def process(request):
    if request.method == 'POST':
        validated = User.objects.check_register(request.POST)
        if len(validated.errors) > 0:
            validated.data['password'] = ''
            request.session['data'] = validated.data
            for err in validated.errors:
                messages.error(request, err)
            return redirect('/register')
        else:
            request.session['user_id'] = validated.data['user_id']
            request.session['user_status'] = 'Authenticated'
            messages.success(request, 'Thank You for registering! Your user_id is ' + str(validated.data['user_id']))
            if 'data' in request.session:
                del request.session['data']
            return redirect('/')
    return redirect('/register')
# Logout Flushes Session data
def logout(request):
    request.session.flush()
    return redirect('/')


def travels(request):
    if 'user_status' not in request.session or request.session['user_status'] != 'Authenticated':
        return redirect('/login')
    # Else get User for user_id in session
    else:
        data = {
        'user': User.objects.get(id=request.session['user_id']),
        'travel_list' : Travel.objects.filter(user__id=request.session['user_id']),
        'other_travels' : Travel.objects.all().exclude(planner__id=request.session['user_id'])
        }
    return render(request, 'exam/travels/index.html', data)

def add_travels(request):
    if 'user_status' not in request.session or request.session['user_status'] != 'Authenticated':
        return redirect('/login')
    # Else get User for user_id in session

    return render(request, 'exam/travels/add_travel.html')

def create_travels(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        validated = Travel.objects.validate_travel_info(post_data)

        if len(validated.errors) > 0:
            for err in validated.errors:
                messages.error(request, err)
            return redirect('/travels/add')
        else:
            created_travel = Travel.objects.create_travel(validated.data, request.session['user_id'])
            if created_travel != False:
                messages.success(request, 'You have successfully added your travel plans. Your Travel ID is: ' + str(created_travel.id))
            else:
                messages.error(request, 'There was an error with adding your travel info to the DB')
        return redirect('/travels')
    # messages.error(request, 'Please fillout the form completely')
    return redirect('/travels/add')

def show_travels(request,travel_id):
    if 'user_status' not in request.session or request.session['user_status'] != 'Authenticated':
        return redirect('/login')
    # Else get User for user_id in session
    else:
        data = {
        'user': User.objects.get(id=request.session['user_id']),
        'travel' : Travel.objects.get(id=travel_id)
        }

        return render(request, 'exam/travels/show.html', data)

def join_travels(request,travel_id):
    if 'user_status' not in request.session or request.session['user_status'] != 'Authenticated':
        return redirect('/login')
    # Else get User for user_id in session
    else:
        data = {
        'user': User.objects.get(id=request.session['user_id']),
        'travel' : Travel.objects.get(id=travel_id)
        }

        return render(request, 'exam/travels/join.html', data)

def create_join(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        validated = Travel.objects.validate_join(post_data)

        if len(validated['errors']) > 0:
            for err in validated.errors:
                messages.error(request, err)
    else:
        messages.error(request, 'There was an error with the method of your request')
    return redirect('/travels')
