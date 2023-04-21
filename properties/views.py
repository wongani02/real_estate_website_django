from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages
from django.http import HttpResponse

from properties.models import Property, Districts, PropertyCategory
from properties.forms import *


class PropertiesHome(generic.ListView):
    def get(self, request):
        property = Property.objects.filter(is_active=True).filter(is_featured=True)
        recents = Property.objects.order_by('-created_at')[:5]
        context = {
            # 'property': property,
            # 'recents': recents,
        }
        return render(request, 'properties/home.html', context)


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
    

class PropertyPricing(generic.ListView):
    def get(self, request):
        return render(request, 'properties/page-pricing.html')


class PropertyListingMap(generic.ListView):
    def get(self, request):

        return render(request, 'properties/page-listing-v7.html')


class PropertyDetail(generic.ListView):
    def get(self, request):
        return render(request, 'properties/page-listing-single-v7.html')


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
        amenity_form = AmenitiesCreationForm()

        return render(request, self.template_name, {
            'form': form, 'cat_form': cat_form, 'dis_form': dis_form, 'img_form': images_form,
            'am_form': amenity_form,
        })
    
    def post(self, request, **kwargs):
        property_form = PropertyCreationForm(request.POST)
        print(request.POST)

        if property_form.is_valid():
            property_form.save(commit=True)
            print('\nsaved\n')

            return redirect('properties:home')
        
        message = messages.add_message(request, messages.ERROR, 'Failed to create Listing.')
        print("error: ", property_form.errors)
        
        return render(request, self.template_name, {
            'message': message, 'form': property_form, 'cat_form': PropertyCategoryCreationForm(),
            'dis_form': DistrictCreationForm(), 'img_form': ImagesCreationForm(),
            'am_form': AmenitiesCreationForm()
        })
    

def contextQ(request):

    return {
        'categories': Districts.objects.filter(is_active=True), 
        'districts': PropertyCategory.objects.all(),
    }


def create_property_category(request):
    db = PropertyCategory.objects.create(name=request.POST.get('name'))
    db.refresh_from_db()


def create_district(request):
    print('request: ', request.POST.get('district_name'))
    db = Districts.objects.create(
        district_name=request.POST.get('district_name'),
        is_active=True
    )
    db.refresh_from_db()

def create_amenities(request):
    db = Amenities.objects.create(
        name=request.POST.get('amenity_name'),
        desc=request.POST.get('amenity_desc'),
    )
    db.refresh_from_db()

    return HttpResponse({'success': 200})
