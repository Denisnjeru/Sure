import logging
from .models import Notifications

logger = logging.getLogger(__name__)

def initialize_notification(*args, **kwargs):
    try :
        obj = Notifications.objects.create(
            level = kwargs['level'],
            recipient = kwargs['recipient'],
            unread = kwargs['unread'],
            actor_content_type = kwargs['actor_content_type'],
            actor_object_id = kwargs['actor_object_id'],
            actor = kwargs['actor'],
            verb = kwargs['verb'],
            description = kwargs['description'],
            target_content_type = kwargs['target_content_type'],
            target_object_id = kwargs['target_object_id'],
            target = kwargs['target'],
            action_object_content_type = kwargs['action_object_content_type'],
            action_object_object_id =  kwargs['action_object_object_id'],
            action_object = kwargs['action_object'],
            public = kwargs['public'],
            deleted = kwargs['deleted'],
            data = kwargs['data'],
            type_class = kwargs['type_class']
        )
        logging.info('Notification created !')
    except Exception as e:
        logging.exception(e)