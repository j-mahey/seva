from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from persons.models import Person
from movement.models import Movement
from departments.models import Department
from centres.models import Centre
from vehicles.models import Vehicle

from persons.admin import StaffCreationForm, VisitorCreationForm, GuestCreationForm
from vehicles.admin import VehicleCreationForm
from movement.admin import MovementFilterForm


@login_required
def home(request):
    persons = []
    vehicles = []
    mov_in = []
    mov_all = []
    results = "Welcome to Seva"
    results_code = 1

    all_centres = [ x[0] for x in Centre.objects.all().values_list("code") ]
    all_departments = [ x[0] for x in Department.objects.all().values_list("name")]
    datetime = timezone.now()

    if request.method == "GET":
        if "query" in request.GET:
            query = request.GET.get("query")
            centre = Centre.objects.get(code=request.GET.get("centre-search"))
            if query.strip() != "":
                vehicles = Vehicle.objects.filter(vehicle_no=query.upper())
                if len(vehicles) > 0:
                    for vehicle in vehicles:
                        persons.append(vehicle.person)
                else:
                    persons = Person.objects.filter(badge=query.lower(), centre=centre)
                    for person in persons:
                        vehicles = Vehicle.objects.filter(person=person)
                if len(persons) == 0:
                    results = "{0} not found".format(query)
                    results_code = 0
        
    if request.method == "POST":
        if request.POST.get("action") == "clock-in":
                p = request.POST.get("person")
                v = request.POST.get("vehicle")

                if p != None and v != None:
                    po = Person.objects.get(centre_badge=request.POST.get("person"))
                    vo = Vehicle.objects.get(vehicle_no=request.POST.get("vehicle"))
                    if len(Movement.objects.filter(person=po, vehicle=vo, out_time=None)) == 0:
                        mov = Movement(person=po, vehicle=vo)
                        mov.save()
                        results = "{0} with {1} clocked in".format(po.badge, vo.vehicle_no)
                        results_code = 1
                    else:
                        results = "{0} with {1} already clocked in".format(po.badge, vo.vehicle_no)
                        results_code = 0
                elif p != None:
                    po = Person.objects.get(centre_badge=request.POST.get("person"))
                    if len(Movement.objects.filter(person=po, out_time=None)) == 0:
                        mov = Movement(person=po)
                        mov.save()
                        results = "{0} clocked in".format(po.badge)
                        results_code = 1
                    else:
                        results = "{0} already clocked in".format(po.badge)
                        results_code = 0
                elif v != None:
                    vo = Vehicle.objects.get(vehicle_no=request.POST.get("vehicle"))
                    if len(Movement.objects.filter(vehicle=vo, out_time=None)) == 0:
                        mov = Movement(vehicle=vo)
                        mov.save()
                        results = "{0} clocked in".format(vo.vehicle_no)
                        results_code = 1
                    else:
                        results = "{0} already clocked in".format(vo.vehicle_no)
                        results_code = 0


        if request.POST.get("action") == "clock-out":
            Movement.objects.filter(id=request.POST.get("clock-out")).update(out_time=timezone.now())
            results = "{0} clocked out".format(Movement.objects.get(id=request.POST.get("clock-out")).person.badge)
            results_code = 1

        if request.POST.get("action") == "create-staff":
            staff_create_form = StaffCreationForm(request.POST)    
            if staff_create_form.is_valid():
                po = staff_create_form.save(commit=False)
                po.type = "S"
                po.save()
                results = "{0} successfully created".format(po.badge)
                results_code = 1
                if request.POST.get("clock-in") is not None:
                    mov = Movement(person=po)
                    mov.save()
                    results = "{0} successfully created and clocked".format(po.badge)
                    results_code = 1
            else:
                results = "Staff creation Failed"
                results_code = 0

        if request.POST.get("action") == "create-visitor":
            visitor_create_form = VisitorCreationForm(request.POST)    
            if visitor_create_form.is_valid():
                po = visitor_create_form.save(commit=False)
                po.type = "V"
                po.save()
                results = "{0} successfully created".format(po.badge)
                results_code = 1
                if request.POST.get("clock-in") is not None:
                    mov = Movement(person=po)
                    mov.save()
                    results = "{0} successfully created and clocked".format(po.badge)
                    results_code = 1
            else:
                results = "Visitor creation Failed"
                results_code = 0
            
        if request.POST.get("action") == "create-guest":
            guest_create_form = GuestCreationForm(request.POST)    
            if guest_create_form.is_valid():
                po = guest_create_form.save(commit=False)
                po.type = "G"
                po.save()
                results = "{0} successfully created".format(po.badge)
                results_code = 1
                if request.POST.get("clock-in") is not None:
                    mov = Movement(person=po)
                    mov.save()
                    results = "{0} successfully created and clocked".format(po.badge)
                    results_code = 1
            else:
                results = "Guest creation Failed"
                results_code = 0

        if request.POST.get("action") == "create-vehicle":
            vh_create_form = VehicleCreationForm(request.POST)
            if vh_create_form.is_valid():
                vo = vh_create_form.save(commit=False)
                po = Person.objects.get(badge=request.POST.get("badge"),
                                        centre=Centre.objects.get(code=request.POST.get("centre")))
                if po:
                    vo.person = po
                    vo.save()
                    results = "{0} successfully created".format(vo.vehicle_no)
                    results_code = 1
                    if request.POST.get("clock-in") is not None:
                        mov = Movement(vehicle=vo, person=po)
                        mov.save()
                        results = "{0} successfully created and clocked".format(vo.vehicle_no)
                        results_code = 1
            else:
                results = "Vehicle creation Failed"
                results_code = 0
    
    mov_in = Movement.objects.filter(out_time=None)
    mov_all = Movement.objects.filter(date=timezone.now()).exclude(out_time=None)

    all_male = 0
    all_female = 0
    dept_summary = {"depts": [], "total": {}}
    for x in all_departments:
        dept = x
        male = len(Movement.objects.filter(date=timezone.now(), person__department__name = x, person__gender="M"))
        female = len(Movement.objects.filter(date=timezone.now(), person__department__name = x, person__gender="F"))
        dept_summary["depts"].append({"department": dept,
                             "male": male,
                             "female": female,
                             "total": male + female})
        all_male += male
        all_female += female

    dept_summary["total"]["male"] = all_male
    dept_summary["total"]["female"] = all_female
    dept_summary["total"]["total"] = all_male + all_female

    context = {"persons": persons,
               "vehicles": vehicles,
               "departments": all_departments,
               "centres": all_centres,
               "movement_in": mov_in,
               "movement_all": mov_all,
               "date": datetime,
               "results": results,
               "results_code": results_code,
               "staff_form": StaffCreationForm,
               "visitor_form": VisitorCreationForm,
               "guest_form": GuestCreationForm,
               "vh_form": VehicleCreationForm,
               "mov_filter_form": MovementFilterForm,
               "dept_summary": dept_summary}

    return render(request, "home.html", context=context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is None:
            context = {"error": "Invalid username or password"}
            return render(request, "login.html", context=context)
        login(request, user)
        return redirect('/')
    return render(request, "login.html")


def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect('/login/')
    return render(request, "login.html")
