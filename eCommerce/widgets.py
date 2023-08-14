# widgets.py
from django.forms import widgets

class ImagePreviewWidget(widgets.ClearableFileInput):
    template_name = 'eCommerce/image_preview_widget.html'
