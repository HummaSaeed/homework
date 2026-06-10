from notifications.models import Notification


def create_notification(user, title, message):
    """Helper to create a notification for a given user."""
    Notification.objects.create(user=user, title=title, message=message)
