from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    profile_name = models.CharField(max_length=264,)

    profile_last_name = models.CharField(max_length=264,)

    profile_department = models.CharField(max_length=264,)

    profile_age = models.PositiveIntegerField()

    profile_pic = models.ImageField(upload_to="profile_pictures", blank=True)

    def __str__(self):
        return self.user.username

class GroupChat(models.Model):
    name = models.CharField(max_length=264)
    members = models.ManyToManyField(User)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("project:detail", kwargs={"pk":self.pk})

class Message(models.Model):
    group = models.ForeignKey(GroupChat, on_delete=models.CASCADE, related_name="Group")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.content
    def get_absolute_url(self):
        return reverse("project:detail")

class JoinRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=(("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected")), default="pending")
    admin_approved = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.username} - {self.group.name}"

        







