from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer

# 물놀이지수와 기온
class WaterPlayScoreView(APIView):
    def get(self, request):
        service_key = "iQ5bkE39dMSPGAw%2Bh0KADor%2BExmLclc%2BUbLhi0FSLYJmnlSLh1pfjiYcb3IwKV6469VVj4Vd4WtUBNV9bQjiOg%3D%3D"
        search_query = request.GET.get('search_query', '')
        # 나머지 로직 생략

# 수온
class WaterTemperatureView(APIView):
    def get(self, request):
        search_query = request.GET.get('search_query', '')
        beach_num = ''
    for key, value in beach_num_mapping.items():
        if search_query in value:
            beach_num = key
            break
    if not beach_num:
        return Response({"error": "검색어에 해당하는 값이 없습니다."}, status=400)
    
    #beach_num = beach_num_mapping.get(search_query, '')  # 검색어에 해당하는 매핑값을 가져옴
    current_time = datetime.datetime.now()#.strftime("%Y%m%d")
    target_time = current_time.replace(minute=45)
    search_time = target_time.strftime("%Y%m%d%H%M")
    params = {
    "serviceKey": service_key,
    "beach_num": beach_num,
    "searchTime": search_time
    }
    url = "http://apis.data.go.kr/1360000/BeachInfoservice/getTwBuoyBeach?serviceKey={}&numOfRows=100&beach_num={}&dataType=JSON&searchTime={}".format(service_key, beach_num, search_time)
    response = requests.get(url, params=params)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'body' in data['response']:
                water_temperature = data['response']['body']['items']['item']
                '''filtered_water_temperature = []
                for item in water_temperature:
                    # if items['item'] in ['tm', 'tw']:
                        filtered_water_temperature.append({
                        #'item' : items['item'],
                        'tm' : item['tm'],
                        'tw' : item['tw']
                    })
                return Response({"water_temperature": filtered_water_temperature}, status=200).data'''
                return Response(water_temperature, status=200)
                
                #return Response({"water_temperature": water_temperature}, status=200)
            else:
                return Response({"error": "API 응답에 'body' 키가 없습니다."}, status=response.status_code)
        else:
            return Response({"error": "API 요청 실패"}, status=response.status_code)
    except requests.exceptions.RequestException as e:
        return Response({"error": "API 요청 중 오류 발생: " + str(e)}, status=500)

        # 나머지 로직 생략

# process_search_query 함수
def process_search_query(request):
    search_query = request.GET.get('search_query', '')
    result1 = WaterPlayScoreView().get(request).rendered_content
    result2 = WaterTemperatureView().get(request).rendered_content

    result = {
        'result1': result1,
        'result2': result2,
    }
    return Response(result, status=status.HTTP_200_OK, content_type='application/json')