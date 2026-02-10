import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def search_naver_local(query, display=5):
    """
    네이버 지역 검색 API 호출
    """
    client_id = settings.NAVER_CLIENT_ID
    client_secret = settings.NAVER_CLIENT_SECRET
    
    if not client_id or not client_secret or client_id == 'YOUR_NAVER_CLIENT_ID':
        logger.warning("Naver API keys are not configured.")
        return []

    url = "https://openapi.naver.com/v1/search/local.json"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    params = {
        "query": query,
        "display": display,
        "sort": "random" 
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('items', [])
    except requests.exceptions.RequestException as e:
        logger.error(f"Naver Local Search API failed: {e}")
        return []

def search_google_places(query):
    """
    Google Places API (Text Search) 호출
    """
    api_key = settings.GOOGLE_MAPS_API_KEY
    
    if not api_key or api_key == 'YOUR_GOOGLE_MAPS_API_KEY':
        logger.warning("Google Maps API key is not configured.")
        return []

    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": query,
        "key": api_key,
        "language": "ko"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('results', [])
    except requests.exceptions.RequestException as e:
        logger.error(f"Google Places API failed: {e}")
        return []

def fetch_google_place_details(place_id):
    """
    Google Places API (Place Details) 호출 - 필요시 추가 정보 획득
    """
    api_key = settings.GOOGLE_MAPS_API_KEY
    
    if not api_key or api_key == 'YOUR_GOOGLE_MAPS_API_KEY':
        return None

    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "key": api_key,
        "language": "ko",
        "fields": "name,formatted_address,rating,user_ratings_total,reviews"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('result')
    except requests.exceptions.RequestException as e:
        logger.error(f"Google Place Details API failed: {e}")
        return None
