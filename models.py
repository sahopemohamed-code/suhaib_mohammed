from django.db import models
from django.contrib.auth.models import User


class Station(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.city})"

    class Meta:
        ordering = ['city', 'name']


class Route(models.Model):
    origin = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name='departing_trips'
    )
    destination = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name='arriving_trips'
    )
    duration = models.IntegerField(help_text="Duration in minutes")
    passengers = models.ManyToManyField(User, blank=True, related_name='booked_trips')

    def __str__(self):
        return f"{self.origin} → {self.destination} ({self.duration} min)"

    class Meta:
        ordering = ['origin__city', 'destination__city']
