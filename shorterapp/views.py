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
    y = request.POST['long_url_input']
    if long_url_exist_in_db(y):
        return response_with_existed_link(request, y)
    random_string = create_combination()
    while duplicated_combination(str(random_string)):
        random_string = create_combination()
    else:
        return response_with_new_link(request, random_string, y)


def redirect_url_view(request, shortened_part):
    try:
        link = Link.objects.get(shortlink=shortened_part)
        return HttpResponseRedirect(link.longlink)
    except:
        raise Http404('<h2>Sorry page not found</h2>')


def show_help(request):
    return render(request, 'help.html')


def create_combination():
    n = 7
    random_string = ''.join(random.choices(string.ascii_letters, k=n))
    return str(random_string)


def duplicated_combination(combination):
    if Link.objects.filter(shortlink=combination).exists():
        return True
    else:
        return False


def long_url_exist_in_db(long_url):
    if Link.objects.filter(longlink=long_url).exists():
        return True
    else:
        return False


def response_with_existed_link(request, long_url):
    link = Link.objects.get(longlink=long_url)
    context = {
        'link': link,
    }
    template = loader.get_template('shortened_url.html')
    return HttpResponse(template.render(context, request))


def response_with_new_link(request, random_string, long_url):
    x = str(random_string)
    link = Link(shortlink=x, longlink=long_url)
    link.save()
    context = {
        'link': link,
    }
    template = loader.get_template('shortened_url.html')
    return HttpResponse(template.render(context, request))
