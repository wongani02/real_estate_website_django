from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, Http404
from django.db.models import Q, Sum, Count, ForeignKey, Value, CASCADE, CharField
from django.views import View
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.core.mail import EmailMessage

from datetime import date, datetime, timedelta, timezone

from lodges.models import Lodge, About, BlogPost, BlogCategory, LodgesViews
from properties.models import *
from properties.forms import *
from .email_context import bookmark_email_context
from properties.filters import AdvancedSearchFilter
from properties.charts import *
from bnb.models import Property as BNB, BnbViews
from users.models import User
from payments.models import PropertyPayment, PropertyCharge, PaymentOption
from verifications.views import create_property_listing
from payments.utils import EmailThread


import json
import ast
import shutil, os, random



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
        property_paginator = Paginator(properties, 1)
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

        # get property documents
        docs = Documents.objects.filter(property=qs)
        
        context = {
            'property': qs,
            'property_charts': [
                chart, chart_likes
            ],
            'docs': docs,
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
    model = Policy
    template_name = 'properties/edit/policies.html'

    def get(self, request, **kwargs):
        model = Property.objects.get(id=kwargs.get('pk'))
        form = PropertyLocationCreationForm(instance=model)

        return render(request, self.template_name, {'form': form, 'pk': model.id})

    def post(self, request, **kwargs):
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


class EditPropertyDocuments(generic.UpdateView):
    model = Documents
    template_name = 'properties/edit/documents.html'

    def get(self, request, **kwargs):
        docs = Documents.objects.filter(property=kwargs.get('pk'))

        return render(request, self.template_name, {'docs': docs, 'pk': kwargs.get('pk')})

    def post(self, request):
        pass


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

    def get(self, request, **kwargs):
        # get choice
        request.session['property_choice'] = kwargs.get('choice')

        # Check for existence of incomplete session and append data
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
            'form': property_form, 'choice': kwargs.get('choice')
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
        
        return render(request, self.template_name, {'form': form,'choice': kwargs.get('choice')})


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
            session_data = request.session['step_2']

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

        # get request data
        data = request.POST

        if form.is_valid():
            # Check session for 'incomplete listing' data
            # If session data doesnt match form data, update session
            form.cleaned_data['amenities'] = self.get_amenities(form.cleaned_data['amenities'])

            # Convert form data to string before assignig to session
            self.request.session['step_2'] = {
                'amenities': json.dumps(form.cleaned_data, cls=DateEncoder),
                'location_area': data.get('location_area'), 'lat': data.get('lat'),
                'lon': data.get('lon'), 'district': data.get('district')
            }

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
    

class CreatePropertyDocuments(generic.CreateView):
    model = Documents
    template_name = 'properties/page-dashboard-new-property-4.html'

    def get(self, request):
        # check for existence of incomplete session and append data
        # del request.session['property_documents']
        if 'property_documents' in request.session:
            session = request.session['property_documents']

            form = PropertyDocumentsForm()

        # create and send empty form
        else:
            form = PropertyDocumentsForm(request.GET, request.FILES)

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # get form data
        form = PropertyDocumentsForm(request.POST, request.FILES)

        if form.is_valid():
            # get user object
            user = User.objects.get(username=request.user.username)

            # save document to temporary db table
            temp = TempDocumentStore.objects.create(
                user=user, file=request.FILES['file']
            )

            # redirect user to policy page
            return redirect('accounts:dashboard')

        return render(request, self.template_name, {'form': form})


class CreatePropertyPolicy(generic.CreateView):
    model = Policy
    template_name = 'properties/page-dashboard-new-property-5.html'

    def get(self, request):
        # chech for session data
        if 'policy_data' in request.session:
            session = request.session['policy_data']
            form = PropertyPolicyForm(initial={
                'policy': session['policy']
            })

        else:
            form = PropertyPolicyForm()

        return render(request, self.template_name, {'policy': form})


def select_property_policy(request, **kwargs):
    # get form data
    form = PropertyPolicyForm(request.POST)
    
    if form.is_valid():
        # add data to session
        request.session['policy_data'] = {
            'policy': request.POST.get('policy')
        }

        print(request.POST.get('policy'))

        return redirect('properties:process-details')

    return render(request, 'properties/page-dashboard-new-property-5.html', {'policy': form})


def process_payment_detail(request, *kwargs):
    
    if request.method == 'POST':
        # get form data
        form = PropertyPaymentDetailForm(request.POST)

        if form.is_valid():
            # add form data to session variable
            request.session['property_payment_data'] = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'note': request.POST.get('note') 
            }

            return redirect('properties:process-payment')
    else:
        # get data from session if it exists
        if 'property_payment_data' in request.session:
            # get session variable
            session = request.session['property_payment_data']

            form = PropertyPaymentDetailForm(initial={
                'name': session['name'],
                'email': session['email'],
                'note': session['note']
            })

        else:
            form = PropertyPaymentDetailForm(request.GET)

    return render(request, 'properties/bookings/booking-step-1.html', {'form': form})


def process_payment_view(request, **kwargs):
    # get total charge price
    charge = PropertyCharge.objects.first()

    # get session data
    session = request.session['property_payment_data']
    property_session = json.loads(request.session['step_1'])

    context = {
        'total_price': charge, 'name': session['name'],
        'email': session['email'], 'note': session['note'],
        'property_name': property_session['name']
    }

    return render(request, 'properties/bookings/booking-step-2.html', context)


def payment_approved(request):
    # save all data and get returned property object
    property_ = save_data(request)

    # create a property verification pending object and notify user
    create_property_listing(request, property_) 

    # payment processing
    session = request.session['property_payment_data']

    # get user object
    user = User.objects.get(username=request.user.username)

    # get form body
    body = json.loads(request.body)

    # crete a receipts instance
    receipt = Receipt.objects.create(
        user=user,
        note=session['note'],
        property_id=property_.id,
        is_paid=True,
    )

    # create a property payment instance
    payment = PropertyPayment.objects.create(
        user=user,
        property_id=property_.id,
        full_name=body['fullname'],
        email=body['email'],
        total_paid=body['totalPaid'],
        order_key=body['orderId'],
        payment_option=PaymentOption.objects.first(),
        billing_status=True,
        receipts=receipt
    )

    # Add payment id to session variable "property_payment"
    request.session['property_payment'] = payment.order_key

    # Add email to session
    request.session['payment_email'] = request.session['property_payment_data']['email']

    return JsonResponse('payment complete', safe=False)


"""
Function calls all other methods required to save a property object
(1) create_property()
(2) create_amenity_link
(3) create_property_images
(4) create_property_documents
(5) create_property_policy_link
"""
def save_data(request):
    # avoid queryset error 
    error = Property.objects.all()
    # Get session data and save to database
    print("1: ", request.session['step_2'])
    property_info = json.loads(request.session['step_1'])
    location_info = request.session['step_2']

    #  Create property instance
    property_, _amenities = create_property(request, property_info, location_info)
    
    # Create amenity instance
    create_amenity_link(request, property_.id, _amenities)

    # Create property images instance
    create_property_images(request, property_, request.user.username)

    # create property documents instance
    create_property_documents(request, property_, request.user.username)

    # create property policy
    create_property_policy_link(request, property_)
    
    # Delete all sessions 
    # del request.session['step_1']
    # del request.session['step_2']
    
    request.session['property_id'] = str(property_.id)
    
    return property_


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
    dis = Districts.objects.get(id=object2['district'])

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

    # get Property instance 
    property_ = Property.objects.get(pk=property_id)


    # Loop and create through list of amenities
    for object in objects:
        # Get amenity object
        object = Amenities.objects.get(name=object)
        amenity = PropertyAmenityLink.objects.create(
        _property=property_, amenity=object
        )
        amenity.save()

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
        # get the name of the file
        name = str(temp_obj.image.name).split('/')

        # create property_image folder if it does not exist
        to_directory = settings.MEDIA_ROOT + '\\property_images\\'

        if not os.path.exists(to_directory):
            os.makedirs(to_directory)

        # move file on filesystem
        source_path = temp_obj.image.path
        destination_path = to_directory + name[-1]
        shutil.move(source_path, destination_path)

        # move data from temporary table to permanent
        images = Images.objects.create(property=property_, file=destination_path)
        images.save()

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
Function saves property documents from the temporary table
to a permant documents tables. The temporary documents and table entries
are deleted once the operation is complete.
"""
def create_property_documents(request, property_, object_):
    # List to hold document instances
    images_ = []

    # Get user instance
    user = User.objects.get(username=object_)

    # Filter all temporary document of the user
    temp = TempDocumentStore.objects.filter(user=user).order_by('date')

    for temp_obj in temp:
        # get the name of the file
        name = str(temp_obj.file.name).split('/')

        # create property_image folder if it does not exist
        to_directory = settings.MEDIA_ROOT + '\\property_documents\\'

        if not os.path.exists(to_directory):
            os.makedirs(to_directory)

        # move file on filesystem
        source_path = temp_obj.file.path
        destination_path = to_directory + name[-1]
        shutil.move(source_path, destination_path)

        # move data from temporary table to permanent
        doc = Documents.objects.create(
            property=property_, file=destination_path,
            name=name[-1]
        )
        doc.save()

        # delete temporary image object
        temp_obj.delete()


"""
Function creates a policy object linked to a property object
"""
def create_property_policy_link(request, property_, objects):
    # get session data
    session = request.session['policy_data']

    # get policy object
    obj = Policy.objects.get(pk=session['policy'])

    # create policy object
    policy = PropertyPolicyLink.objects.create(
        property=property_,
        policy=obj
    )
    

"""
Class to be implemented later after additional payment packages have been
added to the system
"""
class OfferPackage(generic.View):

    def get(self, request):



        context = {
            
        }
        return render(request, 'properties/payments/offer-package.html', context)


"""
Function returns data to the discover page. Calls the following additional functions
(1) most_viewed_property
(2) get_featured_listings
"""
def discover(request):
    # get list of most viewed properties
    most_viewed = most_viewed_property()

    # get all featured properties
    featured = get_featured_listings()

    # get featured listings
    context = {'most_viewed': most_viewed, 'featured': featured}

    return render(request, 'properties/discover.html', context)

"""
Function returns the 3 most viewed properties 
"""
def most_viewed_property():
    propety_views = (
        PropetyViews.objects.values('property')
        .annotate(view_count=Sum('views', filter=Q(date__lte=datetime.now())))
        .annotate(view_type=Value('Property', output_field=CharField()))
    )

    lodges_views = (
        LodgesViews.objects.values('property')
        .annotate(view_count=Sum('views', filter=Q(date__lte=datetime.now())))
        .annotate(view_type=Value('Lodge', output_field=CharField()))
    )

    bnb_views = (
        BnbViews.objects.values('property')
        .annotate(view_count=Sum('views', filter=Q(date__lte=datetime.now())))
        .annotate(view_type=Value('BNB', output_field=CharField()))
    )

    views_ = propety_views.union(lodges_views, bnb_views).order_by('-view_count')[:7]

    listings = []

    for listing_id in views_:
        try:
            listings.append(Property.objects.get(pk=listing_id['property']))
        except:
            pass
        try:
            listings.append(BNB.objects.get(pk=listing_id['property']))
        except:
            pass
        try:
            listings.append(Lodge.objects.get(pk=listing_id['property']))
        except:
            pass

    return listings

"""
Function returns all featured listings
"""
def get_featured_listings():
    listings = []

    for model_name in [Property, BNB, Lodge]:
        listings.extend(
            model_name.objects.filter(is_featured=True)[:10]
        )
    
    # randomize contents of list
    random.shuffle(listings)

    return listings


class PaymentOptions(generic.View):

    def get(self, request):
        context = {

        }
        return render(request, 'properties/payments/payment-options.html', context)
    

    def post(self, request):
        context = {

        }
        return render(request, 'properties/payments/payment-options.html', context)


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


def get_onbording(request, **kwargs):
    template_name = 'users/onbording-3.html'

    return render(request, template_name)


def download_doc(request, **kwargs):
    # get doc from db
    doc = Documents.objects.get(pk=kwargs.get('pk'))

    filepath = os.path.join(settings.MEDIA_ROOT, str(doc.file))

    if os.path.exists(filepath):
        with open(filepath, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/file')
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(filepath)

            return response
    raise Http404


def bookmarkProperty(request, pk):

    property = get_object_or_404(Property, pk=pk)

    if request.user.is_authenticated:
        property.user_bookmark.add(request.user)
        subject = 'Your Property Has Been Bookmarked!'
        message = bookmark_email_context.format(
            property.agent.username,
            property.name,
            property.id,
            property.price
        )
        email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [property.agent.email])

        EmailThread(email).start()
        messages.success(request, f'property "{property.name}" has been added bookmarks')
    else:
        messages.error(request, f'Please login to bookmark this property')
        return render(request, 'properties/partials/bookmark-removed.html', {'property':property})

    return render(request, 'properties/partials/properties-bookmarked.html', {'property':property})


def removeBookmark(request, pk):

    property = get_object_or_404(Property, pk=pk)
    if request.user.is_authenticated:
        property.user_bookmark.remove(request.user)
        messages.info(request, f'property "{property.name}" has been removed bookmarks')
    else:
        messages.error(request, f'Please login to bookmark this property')

    return render(request, 'properties/partials/bookmark-removed.html', {'property':property})

