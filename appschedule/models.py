from django.db import models
from django.contrib.auth.models import User
from crewsapp.models import Crew
from ctrctsapp.models import Builder, HouseModel, Job

    
class AbsenceReason(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Absence Reasons"
        verbose_name_plural = "Absence Reasons"
        # ordering = ['-date', 'title']


class Event(models.Model):
    """
    A model representing an event with details related to a construction job.
    """
    date = models.DateField()
    end_dt = models.DateField()
    crew = models.ForeignKey(Crew, on_delete=models.CASCADE, verbose_name='Crew')
    builder = models.ForeignKey(Builder, on_delete=models.CASCADE, related_query_name='events', blank=True, null=True)
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, related_query_name='events', blank=True, null=True)
    house_model = models.ForeignKey(HouseModel, on_delete=models.SET_NULL, related_query_name='events', blank=True, null=True)
    lot = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    extended_service = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_absence = models.BooleanField(default=False)
    absence_reason = models.ForeignKey(AbsenceReason, null=True, blank=True, on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = self.title.upper()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        # ordering = ['-date', 'title']


class EventDraft(models.Model):
    """
    A model representing an event draft with details related to a construction job.
    """
    event = models.OneToOneField(Event, on_delete=models.CASCADE, verbose_name='events_draft', null=True, blank=True)
    date = models.DateField()
    end_dt = models.DateField()
    crew = models.ForeignKey(Crew, on_delete=models.CASCADE, related_query_name='drafts')
    builder = models.ForeignKey(Builder, on_delete=models.CASCADE, related_query_name='drafts', blank=True, null=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_query_name='drafts', blank=True, null=True)
    house_model = models.ForeignKey(HouseModel, on_delete=models.CASCADE, related_query_name='drafts', blank=True, null=True)
    lot = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    extended_service = models.BooleanField(default=False)
    is_absence = models.BooleanField(default=False)
    absence_reason = models.ForeignKey(AbsenceReason, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Event Draft"
        verbose_name_plural = "Events Draft"
        # ordering = ['-date', 'title']


class EventNote(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE, verbose_name='event_note')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.notes


class EventChatMessage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='chat_messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message[:50]}"
    

class EventChatReadStatus(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='read_statuses')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_read = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('event', 'user')
        verbose_name = "Event Chat Read Status"
        verbose_name_plural = "Event Chat Read Statuses"

    def __str__(self):
        return f"{self.user.username} read {self.event.id} at {self.last_read}"
