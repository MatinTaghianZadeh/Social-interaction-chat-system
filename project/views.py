from django.shortcuts import render
from project.form import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from project.models import GroupChat, Message, JoinRequest, UserProfile
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.models import User
import requests
import datetime

# Create your views here.
def Home(request):
    return render(request, "project/home_page.html")

    

def fetch_weather_and_forecast(city, api_key, current_wether_url):
    response = requests.get(current_wether_url.format(city, api_key)).json()
    print(response)

    #lat, lon = response["coord"]["lat"], response["coord"]["lon"]
    #forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()
    #print("yes", forecast_response)

    weather_data = {
        "city":city,
        "temprature":round(response["main"]["temp"] - 273.15, 2),
        "description": response["weather"][0]["description"],
        "icon": response["weather"][0]["icon"]
    }

    #daily_forecast = []
    #for daily_data in forecast_response["daily"][:5]:
      #  daily_forecast.append({
      #      "day":datetime.datetime.fromtimestamp(daily_data["dt"]).strftime("A"),
      #      "min_temp":round(daily_data["temp"]["min"] - 273.15, 2),
      #      "max_temp": round(daily_data["temp"]["max"] - 273.15, 2),
      #      "description": daily_data["weather"][0]["description"],
       #     "icon": daily_data["weather"][0]["icon"],
       # })

    return weather_data#, daily_forecast
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("home_page"))
def Register(request):
    register = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user # here we are doing one to one field

            if "profile_pic" in request.FILES:
                profile.profile_pic = request.FILES["profile_pic"]

            profile.save()

            register = True
        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, "project/registration.html", context={"register":register, "user_form":user_form, "profile_form":profile_form})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request ,username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("home_page"))

            else:
                return HttpResponse("ACCOUNT IS NOT ACTIVE")

        else:
            return HttpResponse("ACCOUNT DOES'NT EXIST")

    else:
        return render(request, "project/login.html", {})


    

class groupList(ListView):
    context_object_name = "groups"
    model = GroupChat
    template_name = "project/groups_list.html"


def send(request, pk):
    group = get_object_or_404(GroupChat, pk=pk)
    msg = Message.objects.filter(group=group)

    if request.method == "POST":
        pm = request.POST.get("message")

        #if pm.is_valid():
        content = pm
        author = request.user
        message = Message(author=author, content=content, group=group)
        message.save()
        return HttpResponseRedirect("/project/{}/".format(pk))
            #return HttpResponse("Message sent successfully")

        #else:
            #print(pm.errors)

    return render(request, "project/messages.html", context={"group":group, "messages":msg})
    
def getMessage(request, pk):
    group = get_object_or_404(GroupChat, pk=pk)
    messages = Message.objects.filter(group=group).order_by("timestamp")
    messages_data = [{'author': msg.author.username, 'content': msg.content, 'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')} for msg in messages]
    return JsonResponse({"messages": messages_data})

@staff_member_required
def admin_dashboard(request):
    pending_requests = JoinRequest.objects.filter(status="pending")
    return render(request, 'project/admin_manage_requests.html', {'pending_requests': pending_requests})

@staff_member_required
def approved_request(request, pk):
    join_request = get_object_or_404(JoinRequest, pk=pk)
    join_request.status="approved"
    join_request.admin_approved=True
    join_request.save()
    messages.success(request, 'Join request approved successfully!')

    join_request.group.members.add(join_request.user)

    return redirect("project:admin_dashboard")

@staff_member_required
def rejected_request(request, pk):
    join_request = get_object_or_404(JoinRequest, pk=pk)
    join_request.status = "rejected"
    join_request.save()
    messages.info(request, 'Join request rejected.')
 
    return redirect("project:admin_dashboard")

@login_required
def SendRequest(request, pk):
    group = get_object_or_404(GroupChat, pk=pk)
    user = request.user
    join_request, created = JoinRequest.objects.get_or_create(user=user, group=group)

    if user.is_staff:
        join_request.status = "approved"
        join_request.save()

    if created:
        return render(request, "project/request_sent.html", {"group":group})

    elif join_request.status == "pending":
        return render(request, "project/request_pending.html", {"group":group})

    elif join_request.status == "approved":
        return redirect("project:detail", pk=pk)

    elif join_request.status == "rejected":
        join_request.status = "pending"
        join_request.save()
        return render(request, "project/request_pending.html", {"group":group})

    return HttpResponse("Something went wrong.")


def request_sent(request):
    return render(request, 'request_sent.html')

def request_pending(request):
    return render(request, 'request_pending.html')
    


def weather(request):
    API_KEY = "f33c83b0a846ef9f0f649056c37c5da3"
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    #forecast_url = "https://api.openweathermap.org/data/3.0/onecall?lat={}&lon={}&exclude=hourly,daily&appid={}"
    if request.method == "POST":
        city = request.POST["city"]
        weather_data = fetch_weather_and_forecast(city, API_KEY, current_weather_url)


        context={
            "weather_data":weather_data, 
            #"daily_forecast": daily_forecast,
        }
        return render(request, "project/city_weather.html", context)

    else:
        return render(request, "project/city_weather.html", context=None)

class Group_Detail(DetailView):
    context_object_name = "Group"
    model = GroupChat
    template_name = "project/Group_detail.html"

class Delete_Group(DeleteView):
    contaxt_object_name = "Group"
    model = GroupChat
    success_url = reverse_lazy("project:group")

class Create_Group(CreateView):
    fields = ["name"]
    model = GroupChat
    template_name = "project/Group_creation.html"

    def form_valid(self, form):
        group = form.save(commit=False)
        group.save()
        
        # Add the current user as a member and admin of the group
        group.members.add(self.request.user)
        
        # Automatically approve the group creator as an admin member
        JoinRequest.objects.create(
            user=self.request.user,
            group=group,
            status="approved",
            admin_approved=True
        )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("project:group")

class Group_Update(UpdateView):
    fields = {"name"}
    model = GroupChat
    template_name="project/Update_group.html"

@staff_member_required
def remove_member(request, group_pk, user_pk):
    group = get_object_or_404(GroupChat, pk=group_pk)
    user = get_object_or_404(User, pk=user_pk)
    
    if user in group.members.all():
        group.members.remove(user)
        join_request = JoinRequest.objects.filter(
            user=user,
            group=group
        ).first()
        if join_request:
            join_request.status = "pending"
            join_request.admin_approved = False
            join_request.save()
            messages.success(request, f'{user.username} has been removed from the group.')
        else:
            messages.warning(request, f'{user.username} is not a member of the group.')

    return redirect(reverse('project:group_detail', kwargs={'pk': group_pk}))



class User_list(ListView):
    context_object_name = "Users"
    model = User
    template_name = "project/user_list.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group_pk = self.kwargs['group_pk']
        group = GroupChat.objects.get(pk=group_pk)
        context['Group'] = group
        context['group_pk'] = group_pk
        return context

@staff_member_required
def add(request, group_pk, user_pk):
    group = get_object_or_404(GroupChat, pk=group_pk)
    user = get_object_or_404(User, pk=user_pk)

    if not user in group.members.all():
        group.members.add(user)
        join_request = JoinRequest.objects.filter(
            user=user,
            group=group
        ).first()
        if join_request:
            join_request.status = "approved"
            join_request.admin_approved = False
            join_request.save()
            print("yes")
            messages.success(request, f'{user.username} has been removed from the group.')
        else:
            JoinRequest.objects.create(
            user=user,
            group=group,
            status="approved",
            admin_approved=True
        )
    return redirect(reverse('project:group_detail', kwargs={'pk': group_pk}))