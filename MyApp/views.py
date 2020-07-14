from django.shortcuts import render
import requests
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from . import models

BASE_CRAIGSLIST_URL = 'https://delhi.craigslist.org/search/bbb?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_600x450.jpg'

# Create your views here.
def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    postListings = soup.find_all('li', {'class': 'result-row'})

    finalPostings = []

    for post in postListings:
        postTitle = post.find(class_='result-title').text
        postUrl = post.find('a').get('href')

        if post.find(class_='result-price'):
            postPrice = post.find(class_='result-price').text
        else:
            postPrice = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        finalPostings.append((postTitle, postUrl, postPrice, post_image_url))

    context = {
        'search': search,
        'final_postings': finalPostings,
    }
    return render(request, 'MyApp/new_search.html', context)