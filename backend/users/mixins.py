from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType

class LogActivityMixin:
    def _log_activity(self, action_flag, instance):
        LogEntry.objects.log_action(
            user_id=self.request.user.id,
            content_type_id=ContentType.objects.get_for_model(instance.__class__).pk,
            object_id=instance.id,
            object_repr=str(instance),
            action_flag=action_flag
        )
    
    def perform_create(self, serializer):
        instance = serializer.save()
        self._log_activity(ADDITION, instance)
        return instance
    
    def perform_update(self, serializer):
        instance = serializer.save()
        self._log_activity(CHANGE, instance)
        return instance
    
    def perform_destroy(self, instance):
        self._log_activity(DELETION, instance)
        instance.delete() 
