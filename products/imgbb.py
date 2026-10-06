import requests
from django.conf import settings


IMGBB_UPLOAD_URL = "https://api.imgbb.com/1/upload"


def upload_to_imgbb(image_file):
    """
    Upload an image to ImgBB and return the hosted image URL.
    """

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
            f"ImgBB connection failed: {str(e)}"
        )

    if response.status_code != 200:
        raise ValueError(
            f"ImgBB upload failed: {response.text}"
        )

    try:
        data = response.json()
    except ValueError:
        raise ValueError(
            "ImgBB returned an invalid response."
        )

    if not data.get("success"):
        raise ValueError(
            data.get("error", {}).get(
                "message",
                "ImgBB upload failed."
            )
        )

    image_data = data.get("data", {})

    image_url = image_data.get("url")

    if not image_url:
        raise ValueError(
            "ImgBB did not return an image URL."
        )

    return image_url