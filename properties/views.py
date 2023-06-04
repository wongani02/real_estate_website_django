from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q 
from django.core.paginator import Paginator

from lodges.models import Lodge, About, BlogPost, BlogCategory

from properties.models import *
from properties.forms import *
from properties.filters import AdvancedSearchFilter
from properties.charts import *



class SimpleSearch(generic.ListView):
    template_name = 'properties/page-listing-v2.html'
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

class AdvancedSearch(generic.ListView):
    template_name = 'properties/page-listing-v2.html'

    def post(self, request, *args, **kwargs):
        filter = AdvancedSearchFilter(request.POST, queryset=Property.objects.all())
        result = ({
            'result': filter,
            'results': Property.objects.all()
        })

        return render(request, self.template_name, result)

class PropertiesHome(generic.ListView):
    
    def get(self, request):
        property = Property.objects.filter(is_active=True).filter(is_featured=True)
        recents = Property.objects.order_by('-created_at')[:5]
        lodges = Lodge.objects.prefetch_related("pictures").filter(is_active=True)
        blogs = BlogPost.objects.filter(is_active=True).order_by('-created')[:4]
        # forms 
        search_form = SearchForm()
        # print(search_form)

        context = {
            'property': property, 'search': search_form,
            'recents': recents, 'lodges': lodges,
            'blogs': blogs
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

        print("TEST: ", PropetyViews.objects.filter(property__id=_property.id))

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
        chart = create_properties_views_chart(kwargs.get('pk'), qs.name)
        # chart_likes = create_properties_likes_chart(request)
        
        context = {
            'property': qs,
            'property_views': chart,
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


class CreatePropertyListing(generic.CreateView):
    model = Property
    template_name = 'properties/page-dashboard-new-property.html'

    def get(self, request):
        # form=PropertyCreationForm(request.GET)
        # cat_form = PropertyCategoryCreationForm(request.GET)
        # dis_form = DistrictCreationForm(request.GET)
        images_form = ImagesCreationForm(request.GET, request.FILES)
        videos_form = VideosCreationForm(request.GET, request.FILES)
        # amenity_form = AmenitiesCreationForm(request.GET)

        return render(request, self.template_name, {
            # 'form': form, 'cat_form': cat_form, 'dis_form': dis_form, 
            'img_form': images_form, 'videos_form': videos_form
            # 'am_form': amenity_form,
        })
    
    def post(self, request, **kwargs):
        property_form = PropertyCreationForm(request.POST)
        print("REQUEST: ", request.POST)
        result = self.save_db(request, **kwargs)
        print("RESULT: ", result)

        if property_form.is_valid():
            property_form.save(commit=False)
            

            if result:
                property_form.save(commit=False)
            
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
            # video = Videos.objects.create(
            #     property=kwargs.get('pk'),
            #     video=request.FILES.get('video'),
            #     link=request.POST.get('link')
            # )
            # video.save()
            print("before: ", request.POST.get('file'))
            print("before 2: ", request.POST.dict())
            for item in request.POST.get('file'):
                print("for 1")
                image = Images.objects.create(
                    property=kwargs.get('pk'),
                    image=item
                )
                print("save 1")
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
        'districts': Districts.objects.filter(is_active=True), 
        'categories': PropertyCategory.objects.all(),
        'about': About.objects.first(),
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
