import asyncio
import json

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from channels.layers import get_channel_layer
from appschedule.models import Event, EventDraft, EventNote, EventChatMessage
from appschedule.serializers import EventSerializer, EventDraftSerializer, EventNoteSerializer, EventChatMessageSerializer


@receiver(post_save, sender=Event)
def event_saved(sender, instance, **kwargs):
    if getattr(settings, 'ENABLE_WEBSOCKET_NOTIFICATIONS', False):
        channel_layer = get_channel_layer()
        serializer = EventSerializer(instance)

        event_data = serializer.data
        asyncio.run(channel_layer.group_send(
            "calendar_updates",
            {
                'type': 'event.updated',
                'event_data': event_data,
            }
        ))


@receiver(post_delete, sender=Event)
def event_deleted(sender, instance, **kwargs):
    if getattr(settings, 'ENABLE_WEBSOCKET_NOTIFICATIONS', False):
        channel_layer = get_channel_layer()
        event_data = {
            'id': instance.id,
        }
        asyncio.run(channel_layer.group_send(
            "calendar_updates",
            {
                'type': 'event.updated',
                'event_data': event_data,
            }
        ))


@receiver(post_save, sender=EventDraft)
def event_draft_saved(sender, instance, **kwargs):
    if getattr(settings, 'ENABLE_WEBSOCKET_NOTIFICATIONS', False):
        channel_layer = get_channel_layer()
        serializer = EventDraftSerializer(instance)

        event_data = serializer.data
        asyncio.run(channel_layer.group_send(
            "calendar_updates",
            {
                'type': 'event_draft.updated',
                'event_data': event_data,
            }
        ))


@receiver(post_delete, sender=EventDraft)
def event_draft_deleted(sender, instance, **kwargs):
    if getattr(settings, 'ENABLE_WEBSOCKET_NOTIFICATIONS', False):
        channel_layer = get_channel_layer()
        event_data = {
            'id': instance.id,
        }
        asyncio.run(channel_layer.group_send(
            "calendar_updates",
            {
                'type': 'event_draft.updated',
                'event_data': event_data,
            }
        ))

@receiver(post_save, sender=EventNote)
def event_note_saved(sender, instance, **kwargs):
    if getattr(settings, 'ENABLE_WEBSOCKET_NOTIFICATIONS', False):
        channel_layer = get_channel_layer()
        serializer = EventNoteSerializer(instance)

        event_data = serializer.data
        asyncio.run(channel_layer.group_send(
            f"event_{instance.event_id}_notes",
            {
                'type': 'note.updated',
                'event_data': event_data,
            }
        ))


@receiver(post_save, sender=EventChatMessage)
def event_chatmessage_saved(sender, instance, **kwargs):
    if getattr(settings, 'ENABLE_WEBSOCKET_NOTIFICATIONS', False):
        channel_layer = get_channel_layer()
        serializer = EventChatMessageSerializer(instance)

        event_data = serializer.data
        asyncio.run(channel_layer.group_send(
            f"schedule_{instance.event_id}_chat",
            {
                'type': 'chat.updated',
                'data': event_data,
            }
        ))
