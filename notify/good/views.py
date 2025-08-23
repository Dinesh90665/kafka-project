from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import NotificationPreference
from kafka import KafkaProducer
import json

# Kafka producer
ACTION_TOPICS = {
    "like_photo": "first",
    "transaction":"first",
    "login":"first",
    "logout":"first",
    "post_photo": "second",
    "added_item": "third",
    "login_system": "fourth",
}




producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)


def first(request):
    return render(request,'first.html')

# ---------- AUTH ----------
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created! You can now login.")
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("first")  # redirect to preferences or home
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "login.html")


# ---------- KAFKA ----------
def send_notification(request):
    if request.method == "POST":
        action = request.POST.get("action")
        topic = ACTION_TOPICS.get(action, "default-topic")
        if(action=="transaction"):
            producer.send(topic,{"action":action},partition=0)
        elif(action=="login"):
            producer.send(topic,{"action":action},partition=1)
        elif(action=="logout"):
            producer.send(topic,{"action":action},partition=2)
        else:
            producer.send(topic,{"action":action},partition=3)
        producer.flush()
        return JsonResponse({"status": "success", "action": action})
    return JsonResponse({"status": "error"})


# ---------- PREFERENCES ----------
@login_required
def preferences_page(request):
    topics = [
        ("first", "first"),
        ("second", "second"),
        ("third", "third"),
        ("fourth", "fourth"),
    ]
    return render(request, "preferences.html", {"topics": topics})


@login_required
def save_preference(request):
    if request.method == "POST":
        topic = request.POST.get("topic")   # FIXED (was "action")
        method = request.POST.get("method")
        user = request.user

        # Update or create preference
        NotificationPreference.objects.update_or_create(
            user=user,
            topic=topic,
            defaults={"method": method}
        )

        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)
