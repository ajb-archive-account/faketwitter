import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .forms import TweetForm
from .models import Tweet

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_view(request, *args, **kwargs):
    """Set the homepage view"""
    # return HttpResponse("<h1>Hello World</h1>")
    return render(request, "pages/home.html", context={}, status=200)


def tweet_create_view(request, *args, **kwargs):
    """ Renders the tweet input form and allows manipulation by the user. """
    form = TweetForm(request.POST or None)
    # print('post data is', request.POST)
    next_url = request.POST.get('next') or None

    if form.is_valid():
        obj = form.save(commit=False)
        # Do other form related logic here.
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)

        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()

    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)

    return render(request, 'components/form.html', context={"form": form})


def tweet_list_view(request, *args, **kwargs):
    """View a list of posted tweets

    REST API VIEW
    Consume by JavaScript or Swift/Java/iOS/Android
    Return Json data.
    """
    qs = Tweet.objects.all()
    tweets_list = [x.serialize() for x in qs]
    data = {
        "isUser": False,
        "response": tweets_list
    }
    return JsonResponse(data)


def tweet_detail_view(request, tweet_id, *args, **kwargs):
    """View the requested tweet by id

    REST API VIEW
    Consume by JavaScript or Swift/Java/iOS/Android
    Return Json data.
    """
    data = {
        "isUser": False,
        "id": tweet_id,
    }

    status = 200

    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not Found"
        status = 404

    return JsonResponse(data, status=status)
