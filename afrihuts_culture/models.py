from django.db import models
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField

# Create your models here.


#blog tables
class BlogCategory(models.Model):
    name = models.CharField(max_length=300, null=True)
    slug = models.SlugField(unique=True, null=True)
    is_active = models.BooleanField(default=True, null=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        pass
        # return reverse('', args=[self.slug])


class BlogPost(models.Model):
    title = models.CharField(max_length=500, null=True)
    sub_title = models.CharField(max_length=10000, null=True, blank=True)
    category = models.ManyToManyField(BlogCategory, related_name='blog_cats')
    content = RichTextField(null=True)
    cover_img = models.ImageField(upload_to='blog_cover_img/', null=True)
    author = models.CharField(max_length=200, null=True)
    is_active = models.BooleanField(
        verbose_name=_("blog visibility"),
        help_text=_("Change blog visibility"),
        default=True,
    )
    slug = models.SlugField(unique=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    

class BlogImage(models.Model):
    """
    blog Image table.
    """

    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="blog_images")
    image = models.ImageField(
        verbose_name=_("image"),
        help_text=_("Upload a blog image"),
        upload_to="blog_images/",
        default="images/default.png",
    )
    alt_text = models.CharField(
        verbose_name=_("Alturnative text"),
        help_text=_("Please add alturnative text"),
        max_length=255,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")


#contact table
class About(models.Model):
    company_name = models.CharField(max_length=600, null=True, help_text="Name of your company")
    logo = models.ImageField(null=True, blank=True, upload_to='logo/')
    instagram_link = models.URLField(null=True, blank=True, help_text="link to your instagram")
    twitter_link = models.URLField(null=True, blank=True, help_text="link to your twitter")
    facebook_link = models.URLField(null=True, blank=True, help_text="link to your facebook")
    whatsapp_link = models.URLField(null=True, blank=True, help_text="link to your what's app")
    about_text = RichTextField(null=True, help_text="what is your company like? mission, values etc..")
    phone_number = models.CharField(max_length=10, null=True, blank=True, help_text="your phone number")
    other_number = models.CharField(max_length=10, null=True, blank=True, help_text="other phone number")
    email = models.EmailField(null=True, blank=True, help_text="your email")
    address = models.CharField(max_length=300, blank=True, null=True)
    district = models.CharField(null=True, max_length=300, help_text="where are you based?")
    location = models.CharField(max_length=300, null=True, help_text="eg area 18")

    class Meta:
        verbose_name = _("About  Us")
        verbose_name_plural = _("About Us")

    def __str__(self):
        return 'do not add, just edit this one'
    

class TermsAndCondiotions(models.Model):
    terms = RichTextField(null=True)

    class Meta:
        verbose_name = _("Terms and Conditions")
        verbose_name_plural = _("Terms and Conditions")

    def __str__(self):
        return 'do not add, just edit this one'

