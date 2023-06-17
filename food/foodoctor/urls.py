from django.urls import path

from .views import base_views, db_control, detail_views
from .api import queryHandler

app_name = 'foodoctor'

urlpatterns = [
    path('', base_views.index, name='index'),

    # json 으로 된 식당 정보를 DB에 추가하는 db_control.temp() 실행
    path('db/import/', db_control.insert_restaurant_data, name='import'),
    path('db/addNaverplace/', db_control.add_naverplace_url, name='naverplace_insert'),

    path('<str:category>/', detail_views.detail, name='detail'),
    path('<str:restaurant_name>/reviews/write', detail_views.add_review, name='add_review'),
    # 내부 api ( roulette.js 에서 랜덤으로 뽑은 카테고리를 인자로 리퀘스트 -> 카테고리에 맞는 식당중 하나의 정보 반환 )
    path('roulette/roulette_query', queryHandler.roulette_query, name='roulette_query')
]
