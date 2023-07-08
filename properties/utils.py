from payments.utils import EmailThread
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string, get_template
from django.contrib.sites.shortcuts import get_current_site
from django.utils.html import strip_tags


from lodges.models import About

from core import settings


#if a request is an ajax request it will return true
def is_ajax(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        is_ajax = True
    else:
        is_ajax = False
    return is_ajax


"""
Function sends users emails upon successful upload of property.
It is used to notify users that their property is being verified, has been verified,
or has been declined.
The following are its parameters:
to_email - recepient mail
p_name - property name
p_status - property status (pending, complete)
v_status - verification status (success, fail, None)
"""
def verification_status(to_email=None, p_name=None, p_status=None, client=None, v_status=None, obj=None, issues=None, request=None):
    print(to_email)
    
    # Get company object
    company = About.objects.first()
    
    # Result
    if p_status == 'pending':
        mail_template = 'properties/verification/pending-email.html'
        
        # Create emails subject
        subject = company.company_name + " Property Verification Request"

    else:
        mail_template = 'properties/verification/complete-email.html'
        
        # Create emails subject
        subject = company.company_name + " Property Verification"

    # Get current site
    current_site = get_current_site(request)

    # Create context variables
    context = {
         'company_name': company.company_name, 'company_addr': company.address,
         'company_tel': company.phone_number, 'user': client, 'property': p_name,
         'current_site': current_site, 'status': p_status, 'support': '#support', 'issues': issues
    }

    # Create email body
    email_body = render_to_string(mail_template, context)
    plain_text = strip_tags(email_body)

    # Create email sender
    from_email = settings.EMAIL_HOST_USER
    print(from_email)

    # Create email object
    email = EmailMultiAlternatives(subject, plain_text, from_email, [to_email])

    # Attach email html image to email
    email.attach_alternative(email_body, 'text/html')
    email.send()
    # Send email via thread
    # EmailThread(email).start()
