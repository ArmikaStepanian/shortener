import random
import string

from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader

from shorterapp.models import Link


# Function loads initial application page index.html
def index(request):
    return render(request, 'index.html')


# Function creates short URL for requested long URL
def shortened_url(request):
    # extract long URL from http request
    y = request.POST['long_url_input']
    # check if requested long URL has been shortened already
    if long_url_exist_in_db(y):
        # return existed short URL from database
        return response_with_existed_link(request, y)
    # create short URL combination
    random_string = create_combination()
    # while combination is not unique
    while duplicated_combination(str(random_string)):
        # create short URL combination
        random_string = create_combination()
    else:
        # return new short URL
        return response_with_new_link(request, random_string, y)


# Function redirects from short URL to corresponding long URL
def redirect_url_view(request, shortened_part):
    try:
        # retrieve short URL from database
        link = Link.objects.get(shortlink=shortened_part)
        # count redirections
        count_redirections(link)
        # redirect to corresponding long URL
        return HttpResponseRedirect(link.longlink)
    except Exception:
        # or return 404
        raise Http404('<h2>Sorry page not found</h2>')


# Function loads Help page with instructions how to use service
def show_help(request):
    return render(request, 'help.html')


# Function generates random short URL combination
def create_combination():
    n = 7
    random_string = ''.join(random.choices(string.ascii_letters, k=n))
    return str(random_string)


# Function checks if random short URL combination already exists in database
def duplicated_combination(combination):
    if Link.objects.filter(shortlink=combination).exists():
        return True
    else:
        return False


# Function checks if requested long URL already exists in database
def long_url_exist_in_db(long_url):
    if Link.objects.filter(longlink=long_url).exists():
        return True
    else:
        return False


# Function returns http response with existed short URL from database
def response_with_existed_link(request, long_url):
    link = Link.objects.get(longlink=long_url)
    context = {
        'link': link,
    }
    template = loader.get_template('shortened_url.html')
    return HttpResponse(template.render(context, request))


# Function returns http response with newly created short URL
def response_with_new_link(request, random_string, long_url):
    short_url = str(random_string)
    link = Link(shortlink=short_url, longlink=long_url)
    link.save()
    context = {
        'link': link,
    }
    template = loader.get_template('shortened_url.html')
    return HttpResponse(template.render(context, request))


# Function increments counter and saves result in database
def count_redirections(link):
    link.count = link.count + 1
    link.save()
