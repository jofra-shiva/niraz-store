import os
import re
import requests
from django.conf import settings


IMGBB_UPLOAD_URL = "https://api.imgbb.com/1/upload"


def resolve_direct_image_url(url):
    """
    Ensure the image URL is a direct raw image URL (e.g. https://i.ibb.co/...).
    If the user enters an ImgBB page viewer link like https://ibb.co/zTFB9fC7,
    fetch the page and extract the true direct image URL.
    """
    if not url:
        return url

    url = url.strip()

    # If already a direct i.ibb.co URL with an image extension
    if "i.ibb.co" in url and any(url.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp", ".gif"]):
        return url

    # If it is an ibb.co viewer/page link (e.g. https://ibb.co/zTFB9fC7)
    if "ibb.co/" in url:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            res = requests.get(url, headers=headers, timeout=8)
            if res.status_code == 200:
                # Find direct image link ending in image extensions
                matches = re.findall(r'https://i\.ibb\.co/[a-zA-Z0-9/_.-]+(?:\.jpg|\.jpeg|\.png|\.webp)', res.text, re.IGNORECASE)
                if matches:
                    return matches[0]
                # Fallback to any i.ibb.co URL
                any_match = re.search(r'https://i\.ibb\.co/[a-zA-Z0-9/_.-]+', res.text)
                if any_match:
                    return any_match.group(0)
        except Exception:
            pass

    return url


def upload_to_imgbb(image_file):

    api_key = getattr(settings, "IMGBB_API_KEY", None) or os.getenv("IMGBB_API_KEY")

    if not api_key:
        raise ValueError(
            "IMGBB_API_KEY is not configured. Please add IMGBB_API_KEY to your .env file."
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