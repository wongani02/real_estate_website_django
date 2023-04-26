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
        context = {
            'bnbs': qs, 'bnb_count': qs.count(),
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
    template_name = 'properties/bnb-listing-v2.html'
    paginate_by = 12
    context_object_name = 'properties'

    def post(self, request):
        qs = Property.objects.filter(
            Q(property_type__icontains=request.POST.get('property_type')) | Q(district__id__iexact=request.POST.get('district'))
        ).filter(is_active=True).order_by('created_at').distinct()

        # Set up a 12 object pagination with all properties
        p = Paginator(qs, 12)

        # Get current page numbe
        page = self.request.GET.get('page')

        # Save data to property variable
        results = p.get_page(page)

        context = ({
            'results': results,
        })

        return render(request, self.template_name, context)

