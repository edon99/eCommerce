import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['categorie'].field.choices = self.get_category_choices()

    def get_category_choices(self):
        queryset = Product.objects.values_list('categorie', flat=True).distinct()
        choices = []
        for categorie in queryset:
            choices.append((categorie, categorie.capitalize()))
        return choices

    categorie = django_filters.ChoiceFilter(empty_label='All')

    date_created = django_filters.ChoiceFilter(
        choices=(
            ('', 'Any'),
            ('recent', 'Most Recent'),
            ('oldest', 'Oldest'),
        ),
        method='filter_by_date_created',
        empty_label=None
    )

    price = django_filters.ChoiceFilter(
        choices=(
            ('', 'Any'),
            ('highest', 'Highest Price'),
            ('lowest', 'Lowest Price'),
        ),
        method='filter_by_price',
        empty_label=None
    )

    def filter_by_date_created(self, queryset, name, value):
        if value == 'recent':
            return queryset.order_by('-date_created')
        elif value == 'oldest':
            return queryset.order_by('date_created')
        else:
            return queryset

    def filter_by_price(self, queryset, name, value):
        if value == 'highest':
            return queryset.order_by('-price')
        elif value == 'lowest':
            return queryset.order_by('price')
        else:
            return queryset

    class Meta:
        model = Product
        fields = ['price', 'date_created', 'categorie']
