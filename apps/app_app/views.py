from django.shortcuts import render, redirect
from models import *
from django.contrib import messages
from datetime import datetime
import time

def index(request):
    return render(request, 'app_app/index.html')

def register(request):

    name = request.POST['name']
    email = request.POST['email']
    birthday = request.POST['birthday']
    password = request.POST['password']
    re_password = request.POST['re_password']

    validation_errors = User.objects.validate_user(name, email, birthday, password, re_password)

    if len(validation_errors) == 0:
        user_full = User.objects.create(name=name, email=email, birthday=birthday, password=password)
        if 'name' not in request.session:
            request.session['name'] = user_full.name
        if 'email' not in request.session:
            request.session['email'] = user_full.email
        if 'user_id' not in request.session:
            request.session['user_id'] = user_full.id
        return redirect('/appointments')

    else:
        for error in validation_errors:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/main')

def login(request):
    email = request.POST['email']
    password = request.POST['password']

    is_authenticated = User.objects.authenticate_user(email, password)
    if is_authenticated == True:
        user = User.objects.get(email=email)
        request.session['email'] = user.email
        request.session['name'] = user.name
        request.session['user_id'] = user.id


        return redirect('/appointments')
    else:
        return redirect('/main')

def main(request):
    return render(request, 'app_app/main.html')

def appointments(request):
    appointments = []
    user = User.objects.get(id=request.session['user_id'])
    user_id = user.id
    appointments = Appointment.objects.filter(user_id=user_id)
    time_now = time.strftime("%x")

    context = {
    'appointments' : appointments,
    'user' : 'user',
    'time_now' : time_now
    }
    return render(request, 'app_app/appointments.html', context)

def add_appointment(request):


    description = request.POST['description']
    due_date = request.POST['due_date']
    time_due = request.POST['time_due']
    status = request.POST['status']
    user = User.objects.get(id=request.session['user_id'])
    user_id = user.id


    appointment = Appointment.objects.create(description=description, due_date=due_date, time_due=time_due, status=status, user_id=user_id)
    return redirect('/appointments')


def edit_appointment(request, id):

    appointment = Appointment.objects.get(id = id)
    context = {
    'appointment' : appointment
    }
    return render(request, 'app_app/edit_appointment.html', context)

def update_appointment(request, id):


    appointment = Appointment.objects.get(id=id)

    appointment.description = description = request.POST['description']
    appointment.due_date = request.POST['due_date']
    appointment.time_due = request.POST['time_due']
    appointment.status = request.POST['status']
    appointment.save()

    return redirect('/appointments')

def delete(request, id):
    appointment = Appointment.objects.get(id=id)
    appointment.delete()
    return redirect('/appointments')




def logout(request):
    request.session.clear()
    return redirect('/main')
