from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages
from django.db.models.signals import pre_save

from properties.models import *
from properties.forms import *
from .signals import create_amenities

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
        form=PropertyCreationForm()
        cat_form = PropertyCategoryCreationForm()
        dis_form = DistrictCreationForm()
        images_form = ImagesCreationForm()

        return render(request, self.template_name, {
            'form': form, 'cat_form': cat_form, 'dis_form': dis_form, 'img_form': images_form,
        })
    
    def post(self, request, **kwargs):
        property_form = PropertyCreationForm(request.POST)
        print(request.POST)

        if property_form.is_valid():
            property_form.save(commit=True)
            print('\nsaved\n')
            # property_form.custom_save(_id)

        
            # Get amenity data from hightlights form
            # amenity_form = AmenitiesCreationForm(request.POST)

            # # Process amenities form before property creation form
            # # Inorder to obtain the amenity id required for properties
            # if amenity_form.is_valid():
            #     print("Valid")
            #     _id = amenity_form.custom_save()

            

            return redirect('properties:home')
        
        message = messages.add_message(request, messages.ERROR, 'Failed to create Listing.')
        # print("form: ", form)
        # print('request: ', request.POST)
        # print("form: ", form.is_valid)
        print("error")
        

        return render(request, self.template_name, {'message': message})


def create_property_category(request):
    print("Category Name: ", request.POST.get('name'))
    db = PropertyCategory.objects.create(name=request.POST.get('name'))
    db.refresh_from_db()


def create_district(request):
    print("District Name: ", request.POST.get('district_name'))
    db = Districts.objects.create(district_name=request.POST.get('district_name'))
    db.refresh_from_db()

    
def dud_func(request):
    print('dud activate')
    


pre_save.connect(create_amenities, sender=Property)