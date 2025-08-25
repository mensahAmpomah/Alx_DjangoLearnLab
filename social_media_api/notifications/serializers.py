from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.SerializerMethodField()
    target_repr = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ('id', 'actor', 'verb', 'target_repr', 'unread', 'timestamp', 'target_object_id', 'target_content_type')
        read_only_fields = ('id', 'actor', 'verb', 'target_repr', 'timestamp')

    def get_actor(self, obj):
        return {'id': obj.actor.id, 'username': getattr(obj.actor, 'username', None)}

    def get_target_repr(self, obj):
        try:
            return str(obj.target) if obj.target is not None else None
        except Exception:
            return None