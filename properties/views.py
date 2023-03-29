from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages

from properties.models import *
from properties.forms import *

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

        print('before: ', PropertyCreationForm.f)

        return render(request, self.template_name, {
            'form': form, 'cat_form': cat_form, 'dis_form': dis_form, 'img_form': images_form,
        })
    
    def post(self, request, **kwargs):
        form = PropertyCreationForm(request.POST, request.FILES)
        
        if form.is_valid():
            print("form: ", form.is_valid())
            form.save(commit=False)

            return redirect('properties:home')
        
        message = messages.add_message(request, messages.ERROR, 'Failed to create Listing.')
        print("form: ", form)
        print('request: ', request.POST)
        print("form: ", form.is_valid)
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

    