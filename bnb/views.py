from django.shortcuts import render
from django.views import generic
from bnb.models import *


class BnbList(generic.ListView):
    model = Property
    paginate_by = 9
    template_name = 'bnb/bnb-listing.html'

    def get_context_data(self, **kwargs):
        context = super(BnbList, self).get_context_data(**kwargs)
        qs = Property.objects.all()
        context = {
            'bnbs': qs, 'bnb_count': qs.count()
        }

        return context
    

class BnbDetail(generic.DetailView):
    model = Property
    template_name = 'bnb/bnb-detail.html'

    def get(self, request, **kwargs):
        qs = Property.objects.get(id=kwargs.get('pk'))
        context = {
            'property': qs,
        }

        return render(request, self.template_name, context)
