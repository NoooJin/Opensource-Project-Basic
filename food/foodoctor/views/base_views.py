import django.conf
from django.shortcuts import render

from ..models import LatestReviews


def index(request):
    latest_reviews = LatestReviews.objects.first()
    if latest_reviews is not None:
        review_list = latest_reviews.review
        for i in range(len(review_list)):
            review_list[i]['rating_range'] = range(review_list[i]['rating'])
        context = {
            'review_list': review_list
        }
    else:
        review_list = None
        context = {
            'review_list': review_list,
        }
    return render(request, 'foodoctor/index.html', context)
