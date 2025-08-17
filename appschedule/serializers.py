from datetime import timedelta
from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import (
    Event, EventDraft, EventNote, EventChatMessage, 
    AbsenceReason,EventImage 
)

class EventSerializer(serializers.ModelSerializer):
    """Serializer for events objects"""
    crew_title = serializers.SerializerMethodField()
    crew_category = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    def get_crew_title(self, obj):
        return obj.crew.name
    
    def get_crew_category(self, obj):
        if obj.crew and obj.crew.category:
            return obj.crew.category.name
        return None 

    def get_images(self, obj):
        images = obj.images.all()
        return EventImageSerializer(images, many=True, context=self.context).data

    class Meta:
        model = Event
        fields = '__all__'
        extra_fields = ['crew_title', 'crew_category', 'images']


class EventDraftSerializer(serializers.ModelSerializer):
    """Serializer for events draft objects"""

    crew_title = serializers.SerializerMethodField()

    def get_crew_title(self, obj):
        return obj.crew.name

    class Meta:
        model = EventDraft
        fields = '__all__'
        extra_kwargs = {
            'end_dt': {'required': False, 'allow_null': True},
            'title': {'required': True, 'allow_null': False, 'allow_blank': False},
        }

    def create(self, validated_data):
        date = validated_data.get('date')
        end_dt = validated_data.get('end_dt')
        if date:
            if not end_dt or end_dt <= date:
                validated_data['end_dt'] = date + timedelta(days=1)

        return super().create(validated_data)


    def validate(self, data):
        is_absence = data.get('is_absence', getattr(self.instance, 'is_absence', False))
        if is_absence:
            return data
        # Tomar valores del instance si no están en data (caso PATCH parcial)
        lot = data.get('lot', getattr(self.instance, 'lot', None))
        address = data.get('address', getattr(self.instance, 'address', None))
        job = data.get('job', getattr(self.instance, 'job', None))
        crew = data.get('crew', getattr(self.instance, 'crew', None))
        event = data.get('event', getattr(self.instance, 'event', None))
        event_id = event.pk if event else None
        start_at = data.get('date', getattr(self.instance, 'date', None))
        end_at = data.get('end_dt', getattr(self.instance, 'end_dt', None))

        if not crew:
            raise ValidationError("Crew is required")

        category = crew.category

        if start_at and (not end_at or end_at <= start_at):
            end_at = start_at + timedelta(days=1)
            data['end_dt'] = end_at

        if not (lot or address or job):
            raise ValidationError("Address or lot/job must be provided")

        qs_ed = EventDraft.objects.filter(crew__category=category)
        qs_e = Event.objects.filter(crew__category=category, deleted=False)

        if lot:
            qs_ed = qs_ed.filter(job=job, lot=lot)
            qs_e = qs_e.filter(job=job, lot=lot)
        elif address:
            qs_ed = qs_ed.filter(address=address)
            qs_e = qs_e.filter(address=address)

        if self.instance:
            qs_ed = qs_ed.exclude(pk=self.instance.pk)
        if event_id:
            qs_ed = qs_ed.exclude(event_id=event_id)
            qs_e = qs_e.exclude(pk=event_id)

        if qs_ed.exists() or qs_e.exists():
            raise ValidationError("Duplicate Event Detected")

        return data


class EventNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventNote
        fields = ['notes', 'updated_at', 'updated_by', 'event']
        read_only_fields = ['updated_at', 'updated_by']

    def create(self, validated_data):
        print('create validated_data', validated_data)
        event = validated_data['event']
        validated_data['updated_by'] = self.context['request'].user
        print('create validated_data', validated_data)
        try:
            event_note, created = EventNote.objects.update_or_create(
                event=event,
                defaults=validated_data
            )
            return event_note
        except Exception as e:
            raise serializers.ValidationError(f"Error creating EventNote: {e}")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class EventChatMessageSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = EventChatMessage
        fields = ['id', 'event', 'author', 'message', 'timestamp']
        read_only_fields = ['id', 'timestamp', 'author']
        extra_kwargs = {'event': {'write_only': True}}

    def create(self, validated_data):
        event = validated_data.pop('event')
        author = self.context['request'].user
        return EventChatMessage.objects.create(event=event, author=author, **validated_data)
    
class AbsenceReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbsenceReason
        fields = ['id', 'name', 'description']


class EventImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = EventImage
        fields = ['id', 'event', 'image', 'image_url', 'uploaded_at', 'uploaded_by']
        read_only_fields = ['id', 'uploaded_at', 'uploaded_by', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        elif obj.image:
            return obj.image.url
        return None
