from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Restaurant


# todo csrf 처리해야 함
'''
룰렛에서 category 를 인자로 가지는 request 를 보낸다
category에 맞는 식당중 무작위로 골라 고른 식당의 도로명 주소를 response 로 돌려줌
이때 response는 Json 형식
'''
@csrf_exempt
def roulette_query(request):
    if request.method == 'POST':
        import random
        category_name = request.POST.get('category')
        category_mapping = {
            "한식": "한식",
            "중식": "중식",
            "돈까스 일식": "돈까스/일식",
            "카페 디저트": "카페/디저트",
            "아시안 양식": "아시안/양식",
            "패스트푸드": "패스트푸트",
            "분식": "분식",
            "고기 요리": "고기요리",
            "기타": "기타"
        }
        category_name = category_mapping[category_name]

        rest_list = Restaurant.objects.filter(category=category_name)
        rest = random.choice(rest_list)
        print(f"선택된 식당은 {rest.name} 입니다")
        import re
        si_re = re.compile(r"[가-힣]+시 ")
        gu_re = re.compile(r"[0-9가-힣]+구 ")
        road_re = re.compile(r"[0-9가-힣]+로([0-9]+번가*길)* [0-9]+(-[0-9]+)*")
        address = rest.address
        if road_re.search(address) is None:
            print(f'{address} 는 지번 주소입니다')
            return JsonResponse({'error': 'Invalid Address : lot number address'})
        else:
            print(f'{address} 는 도로명 주소입니다')

        road_address = '충북 '
        match = si_re.search(address)
        if match is not None:
            road_address = road_address + match.group(1)
        match = gu_re.search(address)
        if match is not None:
            road_address = road_address + match.group(1)
        match = road_re.search(address)
        if match is not None:
            road_address = road_address + match.group(1)

        urlstring = rest.naverplaceURL
        response = {'address': road_address,
                    'name': rest.name,
                    'url': urlstring}

        # Return the JSON response
        return JsonResponse(response)

    return JsonResponse({'error': 'Invalid request method.'})
