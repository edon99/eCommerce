
from eCommerce.models import Notification,Product


def notifications(request):
    # search = request.GET.get('search')
    # if search:
    #     data = Product.objects.filter(title__icontains=search)
    # else:
    #     data = Product.objects.all()

        if request.user.is_authenticated:
            notifications = Notification.objects.filter(receiver=request.user).order_by('-time')
            unread = Notification.objects.filter(receiver=request.user, read_state=False).count()
            
            return {
                'notifications': notifications,
                'unread': unread,
                # 'data':data
                
            }
        else:
            # Handle the case where the user is not authenticated
            return {
                'notifications': None,
                'unread': None,
                
                
            }
