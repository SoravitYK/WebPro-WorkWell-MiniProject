from fnmatch import filter

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
import math

from co_working_space.models import Member, SeatBooking, TopupLog, Zone


# Create your views here.
def index(request):
    context = {}
    context["zone"] = Zone.zone
    check_in = None
    check_out = None
    if request.method == "GET":
        member_id = request.GET.get("member_id")

    if request.method == "POST":
        member_id = request.POST.get("member_id")
        zone = request.POST.get("zone")
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")

    context["member_id"] = member_id
    if member_id:
        try:
            member = Member.objects.get(pk=member_id)
            context["member"] = member
            seat = SeatBooking.objects.filter(member=member)
            context["seat"] = seat
            if check_in:
                zone_type = Zone.objects.get(title=zone)
                if member.money >= zone_type.price:
                    seat_booking = SeatBooking.objects.create(member=member, zone=zone_type, create_by=request.user)
                    seat_booking.save()
                else:
                    context["error"] = "You Don't Have Enough Money"
            if check_out:
                try:
                    seat_booking = SeatBooking.objects.get(member=member, time_out__isnull=True, total_price__isnull=True)
                    seat_booking.time_out = timezone.now()
                    result_price = (seat_booking.time_out - seat_booking.time_in)
                    t_price = (math.ceil(result_price.seconds/3600)*seat_booking.zone.price)
                    seat_booking.total_price = t_price
                    member.money -= t_price
                    member.save()
                    seat_booking.save()
                except SeatBooking.DoesNotExist:
                    context["error"] = "You Did't Check In"
        except Member.DoesNotExist:
            context["error"] = "Member ID doesn't exist"
    return render(request, template_name='co_working_space/index.html', context=context)

def register(request):
    context={}
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        if firstname and lastname:
            try:
                member = Member.objects.get(first_name=firstname, last_name=lastname)
                context["error"] = "Member Already Exist"
            except Member.DoesNotExist:
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
    btn=None
    if request.method == "GET":
        member_id = request.GET.get("member_id")

    if request.method == "POST":
        btn = int(request.POST.get("btn"))
        member_id = request.POST.get("member_id")

    context["member_id"] = member_id
    if member_id:
            try:
                member = Member.objects.get(pk=member_id)
                context["member"] = member
                log = TopupLog.objects.filter(member=member)
                context["log"] =log
                if btn:
                    if member.money < -40:
                        btn -= 20
                    member.money += btn
                    member.save()
                    topup = TopupLog.objects.create(member=member, amount=btn, topup_by=request.user)
                    topup.save()
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
