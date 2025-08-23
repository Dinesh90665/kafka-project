from django.db import models
from django.contrib.auth.models import User

class NotificationPreference(models.Model):
    TOPIC_CHOICES = [
        ("first", "first"),
        ("second", "second"),
        ("third", "third"),
        ("fourth", "fourth"),
    ]

    METHOD_CHOICES = [
        ("email", "Email"),
        ("sms", "SMS"),
        ("whatsapp", "WhatsApp"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=50, choices=TOPIC_CHOICES)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)

    class Meta:
        unique_together = ("user", "topic")  # only one method per topic per user

    def __str__(self):
        return f"{self.user.username} - {self.topic} ({self.method})"

from django.contrib.auth.models import User
  # Or your profile model

# Example profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    
