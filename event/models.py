from django.db import models


class Event(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    type = models.ForeignKey("EventType", null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']


class EventType(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    key = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200)

    class Meta:
        ordering = ['created']
