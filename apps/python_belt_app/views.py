from django.shortcuts import render, redirect

from .models import Users, Destination

from django.contrib import messages

import bcrypt


def index(request):
    print("Login/Registration Page")
    print(80 * "*")

    return render(request, "python_belt_app/index.html")

def register(request):
    errors = Users.objects.validate_reg(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = Users.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        )
        request.session['id'] = user.id
        messages.success(request, "New User Created")
        return redirect('/dashboard')

def login(request):
    errors = Users.objects.validate_log(request.POST)
    
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = Users.objects.get(email=request.POST['email'])
        request.session['id'] = user.id
        return redirect('/success')

def success(request):
    user = Users.objects.get(id=request.session['id'])
    return render (request, 'python_belt_app/success.html', {'first_name' : user.first_name, 'user_id':user.id})

def dashboard(request):    
    user = Users.objects.get(id=request.session['id'])
    context = {
        'user': user,
        'user_trips': Destination.objects.filter(planner=user),
    }
    return render(request, 'python_belt_app/dashboard.html', context)

def add(request):
    user = Users.objects.get(id=request.session['id'])
    context = {
        'user': user,
    }
    return render(request, 'python_belt_app/new_trip.html', context)

def add_trip(request):    
    errors = Destination.objects.validate_destination(request.POST)
    
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/add')
    else:
        start_date, end_date = Destination.objects.get_dates(request.POST)
        Destination.objects.create(
            destination = request.POST['destination'],
            description = request.POST['description'],
            start_date = start_date,
            end_date = end_date,
            planner = Users.objects.get(id=request.session['id'])
        )
        messages.success(request, "New Trip Created")
        return redirect('/dashboard')

def trip_info(request, id):
    context = {
        'trip': Destination.objects.get(id=id)
    }
    return render(request, 'python_belt_app/trip_info.html', context)

def edit_info(request, id):
    if request.method == 'GET':
        user = Users.objects.get(id=request.session['id'])
        context = {
            'user': user,
            'trip': Destination.objects.get(id=id)
        }
        return render(request, 'python_belt_app/edit.html', context)
    
    if request.method == 'POST':
        errors = Destination.objects.validate_destination(request.POST)
        
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/trips/edit/' + str(id))
        else:
            trip = Destination.objects.get(id = id)
            trip.destination = request.POST['destination']
            trip.description = request.POST['description']
            trip.start_date = request.POST['start_date']
            trip.end_date = request.POST['end_date']
            trip.save()
            return redirect('/dashboard')

def delete(request, id):
    user = Users.objects.get(id=request.session['id'])
    trip = Destination.objects.get(id=id)
    if trip.planner == user:
        trip.delete()
    return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/')
