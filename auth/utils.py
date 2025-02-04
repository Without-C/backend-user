import os
import uuid
import requests
from urllib.parse import urlparse

def get_image_file(image_url):
    """
    주어진 image_url으로부터 사진 다운로드
    """
    response = requests.get(image_url)
    if response.status_code != 200:
        return None
    return response.content

def get_random_filename(image_url):
    """
    주어진 image_url으로부터 얻은 이미지 확장자를 유지하며, 무작위 파일 이름 생성
    """
    original_filename = os.path.basename(urlparse(image_url).path)
    _, ext = os.path.splitext(original_filename)
    random_filename = uuid.uuid4().hex
    return f"{random_filename}{ext}"
