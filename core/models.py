from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import uuid

class University(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=50)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    course = models.CharField(max_length=50)
    members = models.ManyToManyField(User, related_name="groups_joined")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="groups_created")
    created_at = models.DateTimeField(auto_now_add=True)
    invite_code = models.UUIDField(default=uuid.uuid4, unique=True)

    def get_absolute_url(self):
        return reverse("Core:group_view", kwargs={"id": self.id})

    def get_note_create_url(self):
        return reverse("Core:note_create", kwargs={'id': self.id})

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    universities = models.ManyToManyField(University, blank=False)
    groups = models.ManyToManyField(Group, blank=True)

    def __str__(self):
        return self.user.username


class Note(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    context = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    is_personal = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("Core:note_view", kwargs={"id": self.id})

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE, null=True, blank=True)
    context = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
