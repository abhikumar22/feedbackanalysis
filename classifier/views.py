from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from classifier.models import Classifier
import json
import re   
import os
import pickle
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings
from rest_framework import status
from nltk.stem import PorterStemmer
from django.views.decorators.csrf import csrf_exempt 

porter = PorterStemmer()

def tokenizer(text):
    return text.split()

def tokenizer_porter(text):
    return [porter.stem(word) for word in text.split()]
    
def preprocessor(text):
    """ Return a cleaned version of text
    """
    text = re.sub('<[^>]*>', '', text)
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', text)
    text = (re.sub('[\W]+', ' ', text.lower()) + ' ' + ' '.join(emoticons).replace('-', ''))
    return text


# Create your views here.
# @api_view(["GET"])
def baseurl(request):
    # return JsonResponse("API Running Successfully",safe=False)
    # return HtmlR('index.html')
    return render_to_response('classifier/index.html')

def formValidation(request):
    feedback = request.GET['feedback']

    ss = preprocessor(feedback)
    text = tokenizer(ss)
    k = tokenizer_porter(ss)
    ff= []
    ff = ' '.join(k)
    list =[]
    list.append(ff)
    file_path = os.path.join(settings.STATIC_ROOT, 'data/clf.pkl')
    with open(file_path, 'rb') as f:
        clf=pickle.load(f)
    preds = clf.predict(list)
    
    prob_neg, prob_pos = clf.predict_proba(list)[0]
    s = 'Positive Feedback' if prob_pos >= prob_neg else 'Negative Feedback'
    p = prob_pos if prob_pos >= prob_neg else prob_neg
    res = '<h1>'+s+' with probability '+str(p)+'</h1>'
    return HttpResponse(res)

@csrf_exempt
def getPrediction(request):
    json_data = json.loads(request.body)
    feedback = json_data.get("feedback")
    print("pppppp",feedback)
    
    ss = preprocessor(feedback)
    text = tokenizer(ss)
    k = tokenizer_porter(ss)
    ff= []
    ff = ' '.join(k)
    list =[]
    list.append(ff)
    file_path = os.path.join(settings.STATIC_ROOT, 'data/clf.pkl')
    with open(file_path, 'rb') as f:
        clf=pickle.load(f)
    prob_neg, prob_pos = clf.predict_proba(list)[0]
    pred = 1 if prob_pos >= prob_neg else 0
    rate = prob_pos if prob_pos >= prob_neg else prob_neg

    data = {
            "prediction": pred,
            "rate": rate
        }

    return JsonResponse(data, status=status.HTTP_200_OK)
   

    
