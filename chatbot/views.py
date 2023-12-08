from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
import json
import string
import random 
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer 
import tensorflow as tf
from chatbot.utils import *

model = load_model('chatbot_model.h5')

class ChatBotRequest(viewsets.ViewSet):
	def list(self, request):
		# Chemin vers le fichier JSON externe
		file_path = 'intentions.json'

		# Chargement du fichier JSON comme dictionnaire
		with open(file_path, 'r') as json_file:
			data = json.load(json_file)

		# initialisation de lemmatizer pour obtenir la racine des mots
		lemmatizer = WordNetLemmatizer()
		# création des listes
		words = []
		classes = []
		doc_X = []
		doc_y = []
		# parcourir avec une boucle For toutes les intentions
		# tokéniser chaque pattern et ajouter les tokens à la liste words, les patterns et
		# le tag associé à l'intention sont ajoutés aux listes correspondantes
		for intent in data["intents"]:
			for pattern in intent["patterns"]:
				tokens = nltk.word_tokenize(pattern)
				words.extend(tokens)
				doc_X.append(pattern)
				doc_y.append(intent["tag"])
			
			# ajouter le tag aux classes s'il n'est pas déjà là 
			if intent["tag"] not in classes:
				classes.append(intent["tag"])
		# lemmatiser tous les mots du vocabulaire et les convertir en minuscule
		# si les mots n'apparaissent pas dans la ponctuation
		words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in string.punctuation]
		# trier le vocabulaire et les classes par ordre alphabétique et prendre le
		# set pour s'assurer qu'il n'y a pas de doublons
		words = sorted(set(words))
		classes = sorted(set(classes))

		# Chargement du modèle

		intents = pred_class(request.GET.get('message'), words, classes)
		result = get_response(intents, data)
		return Response(
			{
				"request": request.GET.get('message'),
				"response": result,
			},
		)

