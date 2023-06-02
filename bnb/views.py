from django.shortcuts import render
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q 

from bnb.models import *


class BnbList(generic.ListView):
    model = Property
    paginate_by = 9
    template_name = 'bnb/bnb-listing.html'

    def get_context_data(self, **kwargs):
        context = super(BnbList, self).get_context_data(**kwargs)
        qs = Property.objects.all()

        # Set up a 8 object pagination with all properties
        p = Paginator(Property.objects.order_by('created_at'), 5)

        # Get current page number
        page = self.request.GET.get('page')

        # Save data to property variable
        pg = p.get_page(page)

        context = {
            'bnbs': qs, 'bnb_count': qs.count(),
            'all_property': pg
        }

        return context
    

class BnbDetail(generic.DetailView):
    model = Property
    template_name = 'bnb/bnb-detail.html'

    def get(self, request, **kwargs):
        qs = Property.objects.get(id=kwargs.get('pk'))
        imgs = PropertyImage.objects.filter(property=kwargs.get('pk'))
        context = {
            'property': qs, 'images': imgs
        }

        return render(request, self.template_name, context)


class SimpleSearch(generic.ListView):
    template_name = 'bnb/bnb-listing-v2.html'
    paginate_by = 12

    def post(self, request):
        qs = Property.objects.filter(
            Q(property_type__id__iexact=request.POST.get('bnb_type')) | 
            Q(city__id__iexact=request.POST.get('district'))
        ).order_by('created_at').distinct()

        # Set up a 12 object pagination with all properties
        p = Paginator(qs, 12)

        # Get current page number
        page = self.request.GET.get('page')

        # Save data to property variable
        results = p.get_page(page)

        context = ({
            'results': results, 'count': qs.count()
        })

        return render(request, self.template_name, context)

