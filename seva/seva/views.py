from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from users.models import User
from vehicles.models import Vehicle
from movement.models import Movement

@login_required
def home(request):
    users = []
    vehicles = []
    mov_in = []
    mov_all = []

    datetime = timezone.now()

    context = {"users": [],
                "vehicles": [],
                "movement_in": [],
                "movement_all": [],
                "date": datetime}
    
    if request.GET:
        query_dict = request.GET
        query = str(query_dict.get("query"))

        vehicles = Vehicle.objects.filter(vehicle_no=query)
        if len(vehicles) > 0:
            for vehicle in vehicles:
                users.append(vehicle.user)
        else:
            users = User.objects.filter(badge=query)
            for user in users:
                vehicles = Vehicle.objects.filter(user=user)
        
        if query_dict.get("clock") is not None:
            clock = int(query_dict.get("clock"))
            if len(users) > 0:
                mov = Movement.objects.filter(user=users[0], out_time=None)
                
                if len(mov) == 1 and clock == 0:
                    Movement.objects.filter(user=users[0], out_time=None).update(out_time=timezone.now())
                elif len(mov) == 0 and clock == 1:
                    if len(users) > 0 and len(vehicles) > 0:
                        mov = Movement(user=users[0], vehicle=vehicles[0])
                        mov.save()
                    elif len(users) > 0:
                        mov = Movement(user=users[0])
                        mov.save()
                    elif len(vehicles) > 0:
                        mov = Movement(vehicle=vehicles[0])
                        mov.save()

        mov_in = Movement.objects.filter(out_time=None)
        mov_all = Movement.objects.filter(date=timezone.now())

        context = {"users": users,
                   "vehicles": vehicles,
                   "movement_in": mov_in,
                   "movement_all": mov_all,
                   "date": datetime}
        
    return render(request, "home.html", context=context)

def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        badge = request.POST.get("badge")
        password = request.POST.get("password")
        user = authenticate(request, badge=badge, password=password)
        if user is None:
            context = {"error": "Invalid badge or password"}
            return render(request, "login.html", context=context)
        login(request, user)
        return redirect('/')
    return render(request, "login.html")

def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect('/login/')
    return render(request, "login.html")
