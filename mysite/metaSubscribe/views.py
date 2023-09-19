from django.shortcuts import render
from django.http import HttpResponse

def new_page(request):
    return HttpResponse("Hello, this is the new page!")

# Create your views here.
