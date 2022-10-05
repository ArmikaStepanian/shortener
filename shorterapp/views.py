import random
import string

from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader

from shorterapp.models import Link


def index(request):
    return render(request, 'index.html')


def shortened_url(request):
    n = 7
    random_string = ''.join(random.choices(string.ascii_letters, k=n))
    while not is_unique_combination(str(random_string)):
        random_string = ''.join(random.choices(string.ascii_letters, k=n))
    else:
        x = str(random_string)
        y = request.POST['long_url_input']
        link = Link(shortlink=x, longlink=y)
        link.save()
        context = {
            'link': link,
        }

    template = loader.get_template('shortened_url.html')
    return HttpResponse(template.render(context, request))


def redirect_url_view(request, shortened_part):
    try:
        link = Link.objects.get(shortlink=shortened_part)
        return HttpResponseRedirect(link.longlink)
    except:
        raise Http404('<h2>Sorry page not found</h2>')


def show_help(request):
    return render(request, 'help.html')


def is_unique_combination(combination):
    if Link.objects.filter(shortlink=combination).exists():
        return False
    else:
        return True
