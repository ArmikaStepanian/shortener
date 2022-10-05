import random
import string

from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader

from shorterapp.models import Link


def index(request):
    links = Link.objects.all().values()
    template = loader.get_template('index.html')
    context = {
        'links': links,
    }
    return HttpResponse(template.render(context, request))


def shortened_url(request):
    N = 7
    random_string = ''.join(random.choices(string.ascii_letters, k=N))
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
