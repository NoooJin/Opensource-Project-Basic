import datetime

import django.conf
from django.shortcuts import render

from djongo import models
from ..models import Restaurant, Review, LatestReviews, ReviewForm


def detail(request, category: str):
    tag_names = {'korean': '한식',
                 'chinese': '중식',
                 'japanese': '돈까스/일식',
                 'dessert': '카페/디저트',
                 'asian': '아시안/양식',
                 'fastfood': '패스트푸트',
                 'bunsik': '분식',
                 'meat': '고기요리',
                 'etc': '기타'
                 }
    tag_names_to_title = {'korean': '한식',
                          'chinese': '중식',
                          'japanese': '돈까스·일식',
                          'dessert': '카페·디저트',
                          'asian': '아시안·양식',
                          'fastfood': '패스트푸드',
                          'bunsik': '분식',
                          'meat': '고기 요리',
                          'etc': '기타'
                 }
    restaurant_list = list(Restaurant.objects.filter(category=tag_names[category]))
    print(type(restaurant_list))
    context = {'restaurant_list': restaurant_list,
               'category': tag_names_to_title[category]
               }
    return render(request, 'foodoctor/detail.html', context)


def add_review(request, restaurant_name: str):
    import datetime
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review_data = form.cleaned_data
            restaurant = Restaurant.objects.get(name=restaurant_name)
            review = {
                'content': review_data['content'],
                'author_name': review_data['author_name'],
                'rating': review_data['rating'],
                'last_updated': datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=9)))
            }
            if restaurant.review is not None:
                restaurant.review.append(review)
                restaurant.rating = restaurant.rating.to_decimal()
                restaurant.save()
            else:
                arr = list()
                arr.append(review)
                restaurant.review = arr
                restaurant.rating = restaurant.rating.to_decimal()
                restaurant.save()

            if len(LatestReviews.objects.all()) > 0:
                latest_reviews = (LatestReviews.objects.all())[0]
                if len(latest_reviews.review) >= 5:
                    latest_reviews.review.pop(0)
                latest_reviews.review.append(review)
            else:
                latest_reviews = LatestReviews()
                arr = list()
                arr.append(review)
                latest_reviews.review = arr
                latest_reviews.save()
            category_to_title = {'한식': '한식',
                                 '중식': '중식',
                                 '돈까스/일식': '돈까스·일식',
                                 '카페/디저트': '카페·디저트',
                                 '아시안/양식': '아시안·양식',
                                 '패스트푸트': '패스트푸드',
                                 '분식': '분식',
                                 '고기요리': '고기 요리',
                                 '기타': '기타'
                                 }
            restaurant_list = list(Restaurant.objects.filter(category=restaurant.category))
            context = {'restaurant_list': restaurant_list,
                       'category': category_to_title[restaurant.category]
                       }
            return render(request, 'foodoctor/detail.html', context)
    else:
        form = ReviewForm()
    context = {'form': form}
    return render(request, 'foodoctor/review.html', context)


def show_review_list(request, restaurant_name: str):
    review_list = (Restaurant.objects.get(name=restaurant_name)).review
    context = {'review_list': review_list}
    return render(request, 'foodoctor/list.html', context)
