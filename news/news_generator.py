import os
import requests
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import News
from .serializers import NewsSerializer
from accounts.models import User


class GenerateNews(APIView):
    def get(self, request):
        if request.data.get("type") == "gn+":
            all_news = News.objects.filter(type == "gn+")
        else:
            all_news = News.objects.all()

        serialzier = NewsSerializer(
            all_news,
            many=True,
            context={"request": request},
        )
        return Response(serialzier.data)

    def post(self, request):
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
        response = requests.post(openai_url, json=data, headers=headers)

        if response.status_code == 200:
            generated_data = response.json()
            news_data = json.loads(generated_data["choices"][0]["message"]["content"])
            admin_user = User.objects.get(username="admin")

            serializer = NewsSerializer(
                data={
                    "type": "gn+",
                    "title": news_data["title"],
                    "content": news_data["content"],
                    "url": news_data["url"],
                },
                context={"request": request},
            )
            if serializer.is_valid():
                serializer.save(author_id=admin_user.pk)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"error": "Failed to generate story from AI"},
                status=response.status_code,
            )
