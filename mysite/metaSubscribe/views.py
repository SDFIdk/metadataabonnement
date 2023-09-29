from django.shortcuts import render
from django.http import HttpResponse
from .models import Dataset

def datasets_view(request):
    datasets = Dataset.objects.all()
    return render(request, 'datasets.html', {'datasets': datasets})

def new_page(request):
    return HttpResponse("Hello human, I am the messenger and this is the new page! Mark my words!")

# Create your views here.
