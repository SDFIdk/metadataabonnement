from django.shortcuts import render
from django.http import HttpResponse
from .models import Dataset
from .models import CustomUser

def user_datasets_view(request):
    users = CustomUser.objects.prefetch_related('datasets').all()
    return render(request, 'user_datasets.html', {'users': users})

def users_view(request):
    users = CustomUser.objects.all()
    return render(request, 'users.html', {'users': users})


def datasets_view(request):
    datasets = Dataset.objects.all()
    return render(request, 'datasets.html', {'datasets': datasets})

def home_page(request):
    return render(request, 'homepage.html')
    # return HttpResponse("Hello human, I am the messenger and this is the homepage!")

# Create your views here.
