from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.


class User(AbstractUser):
    google_id = models.CharField(max_length=255, null=True, blank=True)
    headline = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    reset_expiry = models.DateField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    skills = models.JSONField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    github_url = models.URLField(null=True, blank=True)
    portfolio_url = models.URLField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    date_joined = models.DateField(auto_now_add=True)

class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class Mentee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    cv_url = models.URLField()

class Service(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    type = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    session_time = models.IntegerField()
    deleted_at = models.DateField(null=True, blank=True)

class Availability(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    availability = models.JSONField()

class SessionRequest(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    agenda = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')])
    rejection_reason = models.TextField(null=True, blank=True)  
