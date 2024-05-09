import os, requests, json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import News
from .serializers import NewsSerializer
from accounts.models import User


def GenerateNews():

        prompt = 'Please recommend one of the IT related news. Please let me know the title, content and url as well. Provide your response as a Json object with the following schema: {"title" : "", "content":"", "url":""}.'

        openai_url = "https://api.openai.com/v1/chat/completions"
        openai_api_key = os.environ.get("OPENAI_KEY")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai_api_key}",
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        }
        return requests.post(openai_url, json=data, headers=headers)
