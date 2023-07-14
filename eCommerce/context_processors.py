
from eCommerce.models import Notification


def notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(receiver=request.user).order_by('-time')
        unread = Notification.objects.filter(receiver=request.user, read_state=False).count()
        return {
            'notifications': notifications,
            'unread': unread
        }
    else:
        # Handle the case where the user is not authenticated
        return {
            'notifications': None,
            'unread': None
        }
