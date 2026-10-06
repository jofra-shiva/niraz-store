import requests
from django.conf import settings


IMGBB_UPLOAD_URL = "https://api.imgbb.com/1/upload"


def upload_to_imgbb(image_file):

    api_key = settings.IMGBB_API_KEY

    if not api_key:
        raise ValueError(
            "IMGBB_API_KEY is not configured."
        )

    try:
        response = requests.post(
            IMGBB_UPLOAD_URL,
            params={
                "key": api_key
            },
            files={
                "image": image_file
            },
            timeout=30
        )

    except requests.RequestException as e:
        raise ValueError(
            f"ImgBB connection failed: {e}"
        )

    if response.status_code != 200:
        raise ValueError(
            f"ImgBB upload failed: {response.text}"
        )

    data = response.json()

    if not data.get("success"):
        raise ValueError(
            data.get("error", {}).get(
                "message",
                "ImgBB upload failed."
            )
        )

    image_url = data["data"]["url"]

    return image_url