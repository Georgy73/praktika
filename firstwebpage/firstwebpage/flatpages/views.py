from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse('1238569', content_type="text/plain")

# Create your views here.
