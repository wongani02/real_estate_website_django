from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages

from properties.models import Property
from properties.forms import PropertyCreationForm

class PropertiesHome(generic.ListView):
    def get(self, request):
        return render(request, 'properties/home.html')


class Contact(generic.DetailView):
    def get(self, request):
        return render(request, 'properties/page-contact.html')


class AboutUs(generic.DetailView):
    def get(self, request):
        return render(request, 'properties/page-about.html')


class PropertyListingList(generic.ListView):
    def get(self, request):
        return render(request, 'properties/page-listing-v3.html')


class PropertyListingGrid(generic.ListView):
    def get(self, request):
        return render(request, 'properties/page-listing-v4.html')


class PropertyListingMap(generic.ListView):
    def get(self, request):
        return render(request, 'properties/page-listing-v7.html')


class PropertyDetail(generic.DetailView):
    def get(self, request):
        return render(request, 'properties/page-listing-all.html')


class BlogList(generic.ListView):
    def get(self, request):
        return render(request, 'properties/page-blog-list.html')


class BlogGrid(generic.ListView):
    def get(self, request):
        return render(request, 'properties/page-blog-grid.html')
    

class AgencyList(generic.ListView):
    def get(self, request):
        return render(request, 'properties/page-agency-list.html')
    

class AgencyDetails(generic.DetailView):
    def get(self, request):
        return render(request, 'properties/page-agency-single.html')


class AgentList(generic.ListView):
    def get(self, request):
        return render(request, 'properties/page-agent-list.html')


class AgentDetails(generic.DetailView):
    def get(self, request):
        return render(request, 'properties/page-agent-single.html')


class CreatePropertyListing(generic.CreateView):
    model = Property
    fields = '__all__'
    template_name = 'properties/page-dashboard-new-property.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request, **kwargs):
        form = PropertyCreationForm(request.POST, request.FILES)
        print("form: ", form)
        
        if form.is_valid():
            form.save(commit=False)

            return redirect('properties:home')
        
        message = messages.add_message(request, messages.ERROR, 'Failed to create Listing.')
        print("error")
        
        return render(request, self.template_name, {'message': message})
    