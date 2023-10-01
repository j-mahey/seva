from django.utils import timezone
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from persons.models import Person
from movement.models import Movement
from departments.models import Department
from centres.models import Centre
from vehicles.models import Vehicle

from persons.admin import PersonCreationForm
from vehicles.admin import VehicleCreationForm
from movement.admin import MovementFilterForm


@login_required
def home(request):

    person_search = []
    vehicle_search = []

    person_info = []
    vehicle_info = []
    mov_info = []
    mov_in_info = []

    mov_in = []
    mov_all = []
    results = "Welcome to Seva"
    results_code = 1
    clocked = 0

    all_centres = [ x[0] for x in Centre.objects.all().values_list("code") ]
    all_departments = [ x[0] for x in Department.objects.all().values_list("name")]
    datetime = timezone.now()

    if request.method == "GET":
        if request.GET.get("action") == "clock-search":
            query = request.GET.get("query")
            model = request.GET.get("model-search")
            centre = Centre.objects.get(code=request.GET.get("centre-search"))

            if query.strip() != "":
                if model == "person":
                    person_search = Person.objects.filter(Q(full_name__contains=query.lower()) | Q(badge__contains=query.lower()), centre=centre)
                    if len(person_search) == 0:
                        results = "{0} not found".format(query)
                        results_code = 0
                    elif len(person_search) == 1:
                        person_info = person_search
                        vehicle_info = Vehicle.objects.filter(person__in=person_info)
                        mov_info = Movement.objects.filter(person__in=person_info, date=timezone.now()).exclude(out_time=None)
                        mov_in_info = Movement.objects.filter(person__in=person_info, out_time=None)
                        if len(mov_in_info) > 0:
                            clocked = 1

                if model == "vehicle":
                    vehicle_search = Vehicle.objects.filter(Q(vehicle_no__contains=query.upper()) | Q(custom_id__contains=query))
                    if len(vehicle_search) == 0:
                        results = "{0} not found".format(query)
                        results_code = 0
                    elif len(vehicle_search) == 1:
                        vehicle_info = vehicle_search
                        person_info = [x.person for x in vehicle_search]
                        mov_info = Movement.objects.filter(person__in=person_info, date=timezone.now()).exclude(out_time=None)
                        mov_in_info = Movement.objects.filter(person__in=person_info, out_time=None)
                        if len(mov_in_info) > 0:
                            clocked = 1

        if request.GET.get("action") == "get-info":
            p = request.GET.get("person")
            v = request.GET.get("vehicle")
            if p != None:
                po = Person.objects.get(centre_badge=p)
                if p:
                    person_info = [po]
                    vehicle_info = Vehicle.objects.filter(person=po)
                    mov_info = Movement.objects.filter(person__in=person_info, date=timezone.now()).exclude(out_time=None)
                    mov_in_info = Movement.objects.filter(person__in=person_info, out_time=None)
                    if len(mov_in_info) > 0:
                        clocked = 1

            if v != None:
                vo = Vehicle.objects.get(vehicle_no=v)
                if v:
                    vehicle_info = [vo]
                    person_info = [vo.person]
                    mov_info = Movement.objects.filter(person__in=person_info, date=timezone.now()).exclude(out_time=None)
                    mov_in_info = Movement.objects.filter(person__in=person_info, out_time=None)
                    if len(mov_in_info) > 0:
                        clocked = 1

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
            id=request.POST.get("clock-out")
            Movement.objects.filter(id=id).update(out_time=timezone.now())
            results = "{0} clocked out".format(Movement.objects.get(id=id).person.badge)
            results_code = 1

        if request.POST.get("action") == "create-person":
            person_create_form = PersonCreationForm(request.POST)    
            if person_create_form.is_valid():
                po = person_create_form.save()
                results = "{0} successfully created".format(po.badge)
                results_code = 1
                if request.POST.get("clock-in") is not None:
                    mov = Movement(person=po)
                    mov.save()
                    results = "{0} successfully created and clocked".format(po.badge)
                    results_code = 1
            else:
                results = "Person creation Failed"
                results_code = 0

        if request.POST.get("action") == "create-vehicle":
            vh_create_form = VehicleCreationForm(request.POST)
            print('yay')
            if vh_create_form.is_valid():
                vo = vh_create_form.save(commit=False)
                po = Person.objects.get(badge=request.POST.get("badge"),
                                        centre=Centre.objects.get(code=request.POST.get("centre")))
                if po:
                    vo.person = po
                    vo.save()
                    results = "{0} ({1}) successfully created".format(vo.vehicle_no, vo.custom_id)
                    results_code = 1
                    if request.POST.get("clock-in") is not None:
                        mov = Movement(vehicle=vo, person=po)
                        mov.save()
                        results = "{0} ({1}) successfully created and clocked".format(vo.vehicle_no, vo.custom_id)
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

    context = {"person_search": person_search,
               "vehicle_search": vehicle_search,
               "person_info": person_info,
               "vehicle_info": vehicle_info,
               "movement_info": mov_info,
               "movement_in_info": mov_in_info,
               "in_status": clocked,
               "departments": all_departments,
               "centres": all_centres,
               "movement_in": mov_in,
               "movement_all": mov_all,
               "date": datetime,
               "results": results,
               "results_code": results_code,
               "person_form": PersonCreationForm,
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
