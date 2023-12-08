from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from openai import OpenAI

import openai

class ChatGPTRequest(viewsets.ViewSet):
	def list(self, request):
		client = OpenAI()

		completion = client.chat.completions.create(
		model="gpt-3.5-turbo",
		messages=[
			{"role": "system", "content": "You are a poetic assistant."},
			{"role": "user", "content": request.GET.get('prompt')}
		]
		)

		return Response(
			{
				"request": request.GET.get('prompt'),
				"response": completion.choices[0].message.content,
			},
		)

