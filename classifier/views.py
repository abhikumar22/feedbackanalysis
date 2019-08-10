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


# Create your views here.
# @api_view(["GET"])
def baseurl(request):
    # return JsonResponse("API Running Successfully",safe=False)
    # return HtmlR('index.html')
    return render_to_response('classifier/index.html')

def formValidation(request):
    feedback = request.GET['feedback']

#     classifier_object = Classifier()
#     classifier_object.feedback=feedback
#     Classifier.set_val(classifier_object)

    # text = tokenizer("hello")
    # text = preprocessor("hello")

    # modulePath = os.path.dirname(__file__)
    # filePath = os.path.join(modulePath, 'clf.pkl')
    # url = static('data\clf.pkl')
    # with open(filePath, 'rb') as f:
    #     clf=pickle.load(f)

    # list = []
    # list.append(feedback)
    # preds = clf.predict(list)

    # if(preds[0]==1):
    #     return render(request,'classifier/index.html',{'phn':'Positive Feedback'})
    # else:
    #     return render(request,'classifier/index.html',{'phn':'Negative FeedBack'})

    # path = 'data\clf.pkl'

    # k = staticfiles_storage.url(path, force=True)

    file_path = os.path.join(settings.STATIC_ROOT, 'data\clf.pkl')
    with open(file_path, 'rb') as f:
        clf=pickle.load(f)

    list = []
    list.append(feedback)
    preds = clf.predict(list)

    if(preds[0]==1):
        return render(request,'classifier/index.html',{'phn':'Positive Feedback'})
    else:
        return render(request,'classifier/index.html',{'phn':'Negative FeedBack'})
   

    
