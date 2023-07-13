
from eCommerce.models import Notification


def notifications(request):
    # Retrieve the notifications object or perform any necessary logic
    notifications = Notification.objects.filter(receiver = request.user)  # Customize the filter as per your requirements

    # Return the context variables as a dictionary
    return {
        'notifications': notifications,
        'notifications_count': notifications.count(),
    }