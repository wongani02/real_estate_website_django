
#if a request is an ajax request it will return true
def is_ajax(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        is_ajax = True
    else:
        is_ajax = False
    return is_ajax