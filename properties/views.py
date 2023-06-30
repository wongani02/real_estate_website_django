from django.urls import reverse
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q 
from django.views import View
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder

from datetime import date, datetime, timedelta

from lodges.models import Lodge, About, BlogPost, BlogCategory
from properties.models import *
from properties.forms import *
from properties.filters import AdvancedSearchFilter
from properties.charts import *
from bnb.models import Property as BNB
from users.models import User

import json
import ast
import shutil, os



class SimpleSearch(generic.ListView):
    template_name = 'properties/page-listing-v2.html'
    paginate_by = 12
    context_object_name = 'properties'


    def post(self, request):
        q = request.POST.get('property_search')

        qs = Property.objects.filter(
            Q(property_type__icontains=q) | Q(district__district_name__icontains=q) | Q(property_cat__name__icontains=q) | Q(property_status__icontains=q) | Q(location_area__icontains=q) | Q(name__icontains=q)
        ).filter(is_active=True).order_by('?').distinct()

        # Set up a 12 object pagination with all properties
        p = Paginator(qs, 12)

        # Get current page numbe
        page = self.request.GET.get('page')

        # Save data to property variable
        results = p.get_page(page)

        context = ({
            'results': results,
            'count': qs.count,
            'search_type': 'Simple'
        })

        return render(request, self.template_name, context)

class AdvancedSearch(generic.ListView):
    template_name = 'properties/page-listing-v2.html'

    def post(self, request, *args, **kwargs):
        filter = AdvancedSearchFilter(request.POST, queryset=Property.objects.all())

        result = ({
            'results': filter,
            # 'results': Property.objects.all(),
            'search_type': 'Advanced'
        })

        return render(request, self.template_name, result)

class PropertiesHome(generic.ListView):
    
    def get(self, request):

        #properties pagination for load more functionality
        properties = Property.objects.all()
        property_paginator = Paginator(properties, 4)
        property_page_number = request.GET.get('page', 1)
        property_obj = property_paginator.get_page(property_page_number)

        #blogs
        blogs = BlogPost.objects.filter(is_active=True).order_by('-created')[:4]

        # forms 
        search_form = SearchForm()

        
        context = {
            'properties': property_obj,
            'search': search_form,
            'blogs': blogs
        }
        if request.htmx:
            return render(request, 'properties/partials/properties-partial.html', context)
        
        return render(request, 'properties/home.html', context)
    

class LodgesHTMXView(generic.ListView):

    def get(self, request):

        #lodge pagination for load more functionality
        lodges = Lodge.active_lodges.prefetch_related("pictures").order_by('?')
        lodge_paginator = Paginator(lodges, 3)
        lodge_page_number = request.GET.get('page', 1)
        lodge_obj = lodge_paginator.get_page(lodge_page_number)
        
        context = {
            'lodges': lodge_obj,
        }

        if request.htmx:
            return render(request, 'properties/partials/lodge-partial.html', context)
        return render(request, 'properties/partials/lodge-partial.html', context)
    

class BnbHTMXView(generic.ListView):

    def get(self, request):

        #bnb pagination with load more funtionality
        bnb = BNB.objects.prefetch_related("bnb_image").filter(is_active=True).order_by('-created_at')
        bnb_paginator = Paginator(bnb, 1)
        bnb_page_number = request.GET.get('page', 1)
        bnb_obj = bnb_paginator.get_page(bnb_page_number)
        
        context = {
            'bnb': bnb_obj,
        }

        if request.htmx:
            return render(request, 'properties/partials/bnb-partial.html', context)
        return render(request, 'properties/partials/bnb-partial.html', context)


class Contact(generic.DetailView):
    def get(self, request):
        return render(request, 'properties/page-contact.html')


class AboutUs(generic.DetailView):
    def get(self, request):
        return render(request, 'properties/page-about.html')


class PropertyListingList(generic.ListView):
    model = Property
    template_name = 'properties/page-listing-v3.html'
    context_object_name = 'all_property'

    def get_context_data(self, **kwargs):
        context = super(PropertyListingList, self).get_context_data(**kwargs)
        
        # Set up a 8 object pagination with all properties
        p = Paginator(Property.objects.order_by('created_at'), 5)

        # Get current page number
        page = self.request.GET.get('page')

        # Save data to property variable
        qs = p.get_page(page)

        context = {
            'all_property': qs,
        }

        return context



class PropertyPricing(generic.ListView):
    def get(self, request):
        return render(request, 'properties/page-pricing.html')


class PropertyListingMap(generic.ListView):
    def get(self, request):

        return render(request, 'properties/page-listing-v7.html')


class PropertyDetail(generic.DetailView):
    model = Property
    template_name = 'properties/page-listing-single-v4.html'

    """"
    Function creates or updates the views table based on an existence of 
    a foreign key property object and date.
    If either the foreign key or date dont exist, one is created, else, updated.
    """
    def update_views(self, _property):
        from datetime import datetime

        date = datetime.now().strftime('%Y-%m-%d')
        property_view, created = PropetyViews.objects.get_or_create(property=_property, date=date)

        # Update entry
        property_view.views += 1
        property_view.save()


    def get(self, request, **kwargs):
        qs = Property.objects.get(id=kwargs.get('pk'))

        # Update property views before loading chart
        self.update_views(qs)

        # Get chart objects
        chart = create_properties_views_chart(kwargs.get('pk'))
        chart_likes = create_properties_likes_chart(kwargs.get('pk'))
        
        context = {
            'property': qs,
            'property_charts': [
                chart, chart_likes
            ]
            # 'property_likes': chart_likes,
        }

        return render(request, self.template_name, context)
    

class BlogDetailView(generic.DetailView):
    model = BlogPost
    template_name = 'properties/blog-detail.html'

    def get(self, request, **kwargs):
        qs = self.model.objects.prefetch_related('blog_images').get(slug=kwargs.get('slug'))
        get_current_id = self.model.objects.filter(slug=self.kwargs['slug']).first()
        
        context = {
            'blog': qs,
            'next': self.model.objects.filter(id__gt=get_current_id.pk).first(),
            'previous':  self.model.objects.filter(id__lt=get_current_id.pk).first(),
        }
        return render(request, self.template_name, context)


class BlogList(generic.ListView):
    def get(self, request):
        blogs = BlogPost.objects.filter(is_active=True)
        blog_cat = BlogCategory.objects.filter(is_active=True)
        context = {
            'blogs': blogs,
            'blog_cats': blog_cat,
        }
        return render(request, 'properties/page-blog-list.html', context)


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
    


def editPropertyOptions(request, pk):
    context = {'pk': pk}

    return render(request, 'properties/edit/index.html', context)

class EditPropertyDetails(generic.UpdateView):
    model = Property
    success_url = '/'
    template_name = 'properties/edit/details.html'

    def get(self, request, **kwargs):
        model = Property.objects.get(id=kwargs.get('pk'))
        form = PropertyInfoCreationForm(instance=model)

        return render(request, self.template_name, {'form': form, 'pk': model.id})

    def post(self, request, **kwargs):
        model = Property.objects.get(id=kwargs.get('pk'))
        form = PropertyInfoCreationForm(request.POST, instance=model)

        if form.is_valid():
            form.save(commit=True)

            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form, 'pk': model.id})

class EditPropertyLocationAmenities(generic.UpdateView):
    model = Property
    template_name = 'properties/edit/location.html'

    def get(self, request, **kwargs):
        model = Property.objects.get(id=kwargs.get('pk'))
        form = PropertyLocationCreationForm(instance=model)

        return render(request, self.template_name, {'form': form, 'pk': model.id})

    def post(self, request):
        model = Property.objects.get(id=kwargs.get('pk'))
        form = PropertyLocationCreationForm(request.POST, instance=model)

        if form.is_valid():
            form.save(commit=True)

            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form, 'pk': model.id})

class EditPropertyPolicies(generic.UpdateView):
    model = Property
    template_name = ''

    def get(self, request):
        model = Property.objects.get(id=kwargs.get('pk'))
        form = PropertyLocationCreationForm(instance=model)

        return render(request, self.template_name, {'form': form, 'pk': model.id})

    def post(self, request):
        model = Property.objects.get(id=kwargs.get('pk'))
        form = PropertyLocationCreationForm(request.POST, instance=model)

        if form.is_valid():
            form.save(commit=True)

            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form, 'pk': model.id})


"""
CBV edits property images
image deletion has not yet been included
"""
class EditPropertyMedia(generic.UpdateView):
    model = Images
    template_name = 'properties/edit/images.html'

    def get(self, request, **kwargs):
        images = self.model.objects.filter(property=kwargs.get('pk'))

        return render(request, self.template_name, {'images': images, 'pk': kwargs.get('pk')})

    def post(self, request):
        # Get files from request
        images = request.FILES.get('file')

        # Create property object
        property_ = Property.objects.get(id=kwargs.get('pk'))

        # Create image instances
        instance = Images.objects.create(
            property=property_, image=images
        )

        return render(request, self.template_name, {'images': images, 'pk': kwargs.get('pk')})

class DeletePropertyListing(generic.DeleteView):
    model = Property
    success_url = '/'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()

        return redirect(self.get_success_url())
    

def contextQ(request):

    return {
        'districts': Districts.objects.filter(is_active=True), 
        'categories': PropertyCategory.objects.all(),
        'about': About.objects.first(),
    }


"""
CBV gets and stores property data in session 'step_1'
"""
class CreatePropertyListing(generic.CreateView):
    model = Property
    template_name = 'properties/page-dashboard-new-property-1.html'
    template_next = 'properties/page-dashboard-new-property-2.html'

    def get(self, request):
        # Check for existence of incomplete session and append data
        print("Status: ", 'step_1' in self.request.session)
        if 'step_1' in self.request.session:
            # Add existing session data to form
            # del self.request.session['step_1']
            session_data = json.loads(self.request.session['step_1'])
            session_data['year_built'] = date.fromisoformat(session_data['year_built'])

            property_form = PropertyInfoCreationForm(initial={
                'name': session_data['name'], 'desc': session_data['desc'], 'property_type': session_data['property_type'],
                'property_area': session_data['property_area'], 'compound_area': session_data['property_area'],
                'no_rooms': session_data['no_rooms'], 'no_garages': session_data['no_garages'],
                'no_baths': session_data['no_baths'], 'price': session_data['price'], 'year_built': session_data['year_built'],
                'property_type': session_data['property_type'], 'property_cat': session_data['property_cat']
            })
            
        else:
            # Create a new and empty form
            property_form = PropertyInfoCreationForm()
            
        return render(request, self.template_name, { 
            'form': property_form, 
        })
    
    # POST request handles session data and sends user to next page
    def post(self, request, **kwargs):
        # Get form data
        form = PropertyInfoCreationForm(request.POST)

        if form.is_valid():

            # Check session for 'incomplete listing' data
            if 'step_1' in self.request.session:
                # If session data doesnt match form data, update session
                session_data = self.request.session['step_1']

                if session_data != form.cleaned_data:
                    # Convert form date to string before assignig to session
                    self.request.session['step_1'] = json.dumps(form.cleaned_data, cls=DateEncoder)
            else:
                # Create dictionary if it doesnt exist
                self.request.session['step_1'] = json.dumps(form.cleaned_data, cls=DateEncoder)

            # Save changes to list
            self.request.session.modified = True
            
            return redirect('properties:create-listing-location')
        else:
            print(form.errors)
        
        return render(request, self.template_name, {'form': form})


"""
CBV gets and stores property location and amenity data in session 'step_2'
"""
class CreatePropertyLocationListing(generic.CreateView):
    model = Property
    template_name = 'properties/page-dashboard-new-property-2.html'
    template_next = 'properties/page-dashboard-new-property-3.html'

    def get(self, request):
        # Property Creation form variable
        property_form = None
        amenity = AmenitiesCreationForm()

        # Check for existence of incomplete session and append data
        if 'step_2' in self.request.session:
            
            # Add existing session data to form
            session_data = json.loads(self.request.session['step_2'])

            property_form = PropertyLocationCreationForm(initial={
                'location_area': session_data['location_area'], 'district': session_data['district'], 
                'lat': session_data['lat'], 'lon': session_data['lon']
            })
        else:
            # Create a new and empty form
            property_form = PropertyLocationCreationForm()

        return render(request, self.template_name, { 
            'form': property_form, 'am_form': amenity
        })
    
    # POST request handles session data and sends user to next page
    def post(self, request, **kwargs):
        # Get form data
        form = PropertyLocationCreationForm(request.POST)
        amenity = AmenitiesCreationForm(request.POST)

        if form.is_valid():
            # Check session for 'incomplete listing' data
            # If session data doesnt match form data, update session
            form.cleaned_data['amenities'] = self.get_amenities(form.cleaned_data['amenities'])

            # Convert form date to string before assignig to session
            self.request.session['step_2'] = json.dumps(form.cleaned_data, cls=DateEncoder)

            # Save changes to list 
            self.request.session.modified = True

            return render(request, self.template_next, {}) 
        
        else:
            print(form.errors)
        
        return render(request, self.template_name, {'form': form, 'am_form': amenity})

    # Function converts and Amenity objects as strings
    def get_amenities(self, obj):
        _list = []
        for amenity in obj:
            _list.append(str(amenity))

        return str(_list)


class OfferPackage(generic.View):

    def get(self, request):



        context = {
            
        }
        return render(request, 'properties/payments/offer-package.html', context)


def discover(request):
    citys = Districts.objects.all().order_by("?")[:8]

    context = {'citys': citys}

    return render(request, 'properties/discover.html', context)

class PaymentOptions(generic.View):

    def get(self, request):
        context = {

        }
        return render(request, 'properties/payments/payment-options.html', context)
    

    def post(self, request):
        context = {

        }
        return render(request, 'properties/payments/payment-options.html', context)


def save_data(request):
    # avoid queryset error 
    error = Property.objects.all()
    # Get session data and save to database
    property_info = json.loads(request.session['step_1'])
    location_info = json.loads(request.session['step_2'])

    #  Create property instance
    property_, _amenities = create_property(request, property_info, location_info)
    
    # Create amenity instance
    create_amenity_link(request, property_.id, _amenities)

    # Create property images instance
    create_property_images(request, property_, request.user.username)
    
    # Delete all sessions 
    del request.session['step_1']
    del request.session['step_2']
    
    request.session['property_id'] = str(property_.id)
    
    return redirect('properties:offers')

"""
Function creates property object with the following parameters
object1: property information session object
object2: property location session object
"""
def create_property(request, object1, object2):
    from users.models import User
    
    # Create PropertyCategory object
    cat = PropertyCategory.objects.get(name=object1['property_cat'])
    
    # Create district object
    dis = Districts.objects.get(district_name=object2['district'])

    # Get agent object
    agent = User.objects.get(username=request.user.username)

    _property = Property.objects.create(
    # session: step_1
    name=object1['name'], desc=object1['desc'], property_area=object1['property_area'], 
    compound_area=object1['compound_area'], year_built=object1['year_built'], price=object1['price'],
    property_type=object1['property_type'], property_status=object1['property_status'],
    property_cat=cat, no_garages=object1['no_garages'], no_rooms=object1['no_rooms'],
    no_baths=object1['no_baths'],
    # session: step_2
    location_area=object2['location_area'], district=dis, lat=object2['lat'],
    lon=object2['lon'], agent=agent
    )

    return _property, object2['amenities']
    
"""
Function creates and saves links created between the Property and Amenity classes
"""
def create_amenity_link(request, property_id, objects):
    # List to hold amenity instances
    amenities_ = []

    # Convert str object to dict
    objects = ast.literal_eval(objects)

    # Create Property instance 
    property_ = Property.objects.get(pk=property_id)

    # Loop and create through list of amenities
    for object in objects:
        # Get amenity object
        object = Amenities.objects.get(name=object)
        amenity = PropertyAmenityLink.objects.create(
        _property=property_, amenity=object
        )

        # Add amenity obbjects to list
        amenities_.append(amenity)

    return amenities_

"""
Function saves property images from the temporary table
to a permant images tables. The temporary images and table entries
are deleted once the operation is complete.
The first image saved in the temporary table is selected as the featured 
image for the property
"""
def create_property_images(request, property_, object_):
    # List to hold image instances
    images_ = []

    # Get user instance
    user = User.objects.get(username=object_)

    # Filter all temporary images of the user
    temp = TempImageStore.objects.filter(user=user).order_by('date')

    for temp_obj in temp:
        images = Images.objects.create(property=property_, file=temp_obj.image)
        images.save()
        name = str(temp_obj.image.name).split('/')

        # move file on filesystem
        source_path = temp_obj.image.path
        destination_path = '/property_images/' + name[-1]
        shutil.move(source_path, destination_path)

        # delete temporary image object
        temp_obj.delete()

    # Get all image objects related to the property
    images = Images.objects.filter(property=property_).order_by('date')

    for image in images:
        # make the first image that was uploaded a featured image
        image.is_feature = True
        image.save()

        # break the loop
        break


"""
CBV gets and saves images to a temporary database table.
These images are later on transferred to a permanent table when the user
completes the payments process. At the same time, the temporary files are
deleted from the database
"""
class CreatePropertyMediaListing(generic.CreateView):
    model = Property
    template_name = 'properties/page-dashboard-new-property-3.html'
    template_next = 'users/page-dashboard.html'

    def get(self, request):
        # Property Creation form variable
        property_form = None

        # Check for existence of incomplete session and append data
        if 'step_3' in self.request.session:
            # Add existing session data to form
            session_data = self.request.session['step_3']
            
            property_form = ImagesCreationForm()
        else:
            # Create a new and empty form
            property_form = ImagesCreationForm()

        return render(request, self.template_name, { 
            'form': property_form,
        })
    
    # POST request handles session data and sends user to next page
    def post(self, request, **kwargs):
        # Get form data
        form = ImagesCreationForm(request.POST, request.FILES)

        if form.is_valid():
            # Get user instance
            agent = User.objects.get(username=self.request.user.username)

            # Create a temporary property images instance
            images_ = TempImageStore(user=agent, image=request.FILES['file'])
            images_.save()

            return redirect('accounts:dashboard')
              
    
    
def redirectUser(request):
    return redirect('accounts:dashboard')
      
class DateEncoder(DjangoJSONEncoder): 

    def default(self, obj):
        if isinstance(obj, (date, PropertyCategory, Districts)):
            return str(obj)
        return super().default(obj)


def create_amenities(request):
    db = Amenities.objects.create(
        name=request.POST.get('amenity_name'),
        desc=request.POST.get('amenity_desc'),
    )
    db.refresh_from_db()

    return HttpResponse({'success': 200})


