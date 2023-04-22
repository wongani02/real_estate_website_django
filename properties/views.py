from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q 

from properties.models import Property, Districts, PropertyCategory
from properties.forms import *
from properties.filters import AdvancedSearchFilter



class SimpleSearch(generic.ListView):
    template_name = 'properties/page-listing-v2.html'
    paginate_by = 12
    context_object_name = 'properties'

    def get_context_data(self, **kwargs):
        context = super(SimpleSearch, self).get_context_data(**kwargs)
        qs = Property.objects.filter(
            Q(property_type__icontains=kwargs.get('property_type')) | Q(district__iexact=kwargs.get('district'))
        ).filter(active=True).order_by('date').distinct()
        
        context = {
            'results': qs,
        }

        return context

class AdvancedSearch(generic.ListView):
    template_name = 'properties/page-listing-v2.html'

    def post(self, request, *args, **kwargs):
        filter = AdvancedSearchFilter(request.POST)

        return render(request, self.template_name, {'results': filter})

class PropertiesHome(generic.ListView):
    
    def get(self, request):
        property = Property.objects.filter(is_active=True).filter(is_featured=True)
        recents = Property.objects.order_by('-created_at')[:5]

        # forms 
        search_form = SearchForm()
        # print(search_form)

        context = {
            'property': property, 'search': search_form,
            'recents': recents,
        }
        return render(request, 'properties/home.html', context)


class Contact(generic.DetailView):
    def get(self, request):
        return render(request, 'properties/page-contact.html')


class AboutUs(generic.DetailView):
    def get(self, request):
        return render(request, 'properties/page-about.html')


class PropertyListingList(generic.ListView):
    model = Property
    paginate_by = 5
    template_name = 'properties/page-listing-v3.html'

    def get_context_data(self, **kwargs):
        context = super(PropertyListingList, self).get_context_data(**kwargs)
        qs = Property.objects.all()
        print("Property: ", qs)
        context = {
            'all_property': qs,
        }

        return context


class PropertyListingGrid(generic.ListView):
    def get(self, request):
        return render(request, 'properties/page-listing-v4.html')
    

class PropertyPricing(generic.ListView):
    def get(self, request):
        return render(request, 'properties/page-pricing.html')


class PropertyListingMap(generic.ListView):
    def get(self, request):

        return render(request, 'properties/page-listing-v7.html')


class PropertyDetail(generic.DetailView):
    model = Property
    template_name = 'properties/page-listing-single-v4.html'

    def get(self, request, **kwargs):
        qs = Property.objects.get(id=kwargs.get('pk'))
        context = {
            'property': qs,
        }

        return render(request, self.template_name, context)

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
    template_name = 'properties/page-dashboard-new-property.html'

    def get(self, request):
        form=PropertyCreationForm(request.GET)
        cat_form = PropertyCategoryCreationForm(request.GET)
        dis_form = DistrictCreationForm(request.GET)
        # images_form = ImagesCreationForm(request.GET, request.FILES)
        videos_form = VideosCreationForm(request.GET, request.FILES)
        amenity_form = AmenitiesCreationForm(request.GET)

        return render(request, self.template_name, {
            'form': form, 'cat_form': cat_form, 'dis_form': dis_form, 
            # 'img_form': images_form,
            'am_form': amenity_form, 'videos_form': videos_form
        })
    
    def post(self, request, **kwargs):
        property_form = PropertyCreationForm(request.POST)

        if property_form.is_valid():
            property_form.save(commit=False)
            result = self.save_db(request, **kwargs)

            if result:
                property_form.save(commit=True)
            
            return redirect('properties:home')
        
        message = messages.add_message(request, messages.ERROR, 'Failed to create Listing.')

        form=PropertyCreationForm(request.POST)
        cat_form = PropertyCategoryCreationForm(request.POST)
        dis_form = DistrictCreationForm(request.POST)
        # images_form = ImagesCreationForm(request.POST, request.FILES)
        videos_form = VideosCreationForm(request.POST, request.FILES)
        amenity_form = AmenitiesCreationForm(request.POST)

        return render(request, self.template_name, {
            'form': form, 'cat_form': cat_form, 'dis_form': dis_form, 
            # 'img_form': images_form,
            'am_form': amenity_form, 'videos_form': videos_form
        })
    
    def save_db(self, request, **kwargs):
        try:
            video = Videos.objects.create(
                property=kwargs.get('pk'),
                video=request.FILES.get('video'),
                link=request.POST.get('link')
            )
            video.save()
            for item in request.FILES.get('image'):
                image = Images.objects.create(
                    property=kwargs.get('pk'),
                    image=item
                )
                image.save()
            
            return True
        except:
            return False


class EditPropertyListing(generic.UpdateView):
    model = Property
    fields = [
            'no_rooms', 'no_baths', 'no_garages', 'status',
            'property_type', 'district', 'price', 'compound_area',
            'amenities',
        ] 
    success_url = '/'
    template_name = 'properties/page-dashboard-edit-property.html'

    def get(self, request, **kwargs):
        model = Property.objects.get(id=kwargs.get('pk'))
        form = PropertyEditForm(instance=model)

        return render(request, self.template_name, {'form': form})

    def post(self, request, **kwargs):
        model = Property.objects.get(id=kwargs.get('pk'))
        form = PropertyEditForm(request.POST, instance=model)

        if form.is_valid():
            form.save(commit=True)

            return redirect(self.success_url)


class DeletePropertyListing(generic.DeleteView):
    model = Property
    success_url = '/'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()

        return redirect(self.get_success_url())
    

def contextQ(request):

    return {
        'categories': Districts.objects.filter(is_active=True), 
        'districts': PropertyCategory.objects.all(),
    }

def fileUploadView(request):
    session = request.session
    
    if request.method == 'POST':
        image = request.FILES.get('file')
        print(str(image))
    return HttpResponse('upload')


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
