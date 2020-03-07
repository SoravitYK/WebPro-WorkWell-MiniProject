from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone

from co_working_space.models import Member, SeatBooking, TopupLog, Zone



# Create your views here.
def index(request):
    context = {}
    context["zone"] = Zone.zone
    check_in = None
    if request.method == "GET":
        member_id = request.GET.get("member_id")

    if request.method == "POST":
        member_id = request.POST.get("member_id")
        check_in = request.POST.get("check_in")
        zone = request.POST.get("zone")

    context["member_id"] = member_id
    if member_id:
        try:
            member = Member.objects.get(pk=member_id)
            context["member"] = member
            seat = SeatBooking.objects.filter(member=member)
            context["seat"] = seat
            if check_in:
                zone_type = Zone.objects.get(title="GREEN")
                if member.money >= zone_type.price:
                    seat_booking = SeatBooking.objects.create(member=member, zone=zone_type, create_by=request.user)
                    seat_booking.save()
        except Member.DoesNotExist:
            context["error"] = "Member ID doesn't exist"
    return render(request, template_name='co_working_space/index.html', context=context)

def register(request):
    context={}
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        if firstname and lastname:
            member = Member.objects.create(first_name=firstname, last_name=lastname, money=100)
            member.save()
            context["success"] = "Member Is Registered"
        else:
            context["firstname"] = firstname
            context["lastname"] = lastname
            context["error"] = "Firstname Or Lastname Is Blank"
    return render(request, template_name='co_working_space/register.html', context=context)

def topup(request):
    context={}
    if request.method == "GET":
        member_id = request.GET.get("member_id")
        context["member_id"] = member_id
        if member_id:
            try:
                member = Member.objects.get(pk=member_id)
                context["member"] = member
            except Member.DoesNotExist:
                context["error"] = "Member ID doesn't exist"
    return render(request, template_name='co_working_space/topup.html', context=context)

def my_login(request):
    context={}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("index")
        else:
            context["username"] = username
            context["password"] = password
            context["error"] = "Wrong Username Or Password"
    return render(request, template_name='co_working_space/login.html', context=context)

def my_logout(request):
    logout(request)
    return redirect("login")
