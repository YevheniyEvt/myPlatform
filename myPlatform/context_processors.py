from django.utils import timezone


def set_search(request):
    """ Search value to set in templates in search field"""
    
    search = request.GET.get('search', '')
    return {
        "search": search,
    }   


def can_add(request):
    """Check user`s permissions"""

    can_add_topic = request.user.has_perm('notebook.add_topic')

    can_add_section =  request.user.has_perm('notebook.add_section')

    can_add_articke = request.user.has_perm('comunication.add_articke')
    
    context = {
        'can_add_topic': can_add_topic,
        'can_add_section': can_add_section,
        'can_add_articke': can_add_articke
    }
    return context

def localdate(request):
    date = timezone.localdate()
    return {"date": date}