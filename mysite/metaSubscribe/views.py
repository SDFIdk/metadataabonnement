from django.shortcuts import render, redirect
from .forms import UserLoginForm
from django.http import HttpResponse
from .models import Dataset
from .models import CustomUser

def logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('login_view')

def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = CustomUser.objects.filter(EMAIL=email).first()

            # If the user doesn't exist, create them
            if not user:
                user = CustomUser.objects.create(EMAIL=email)

            # Set user id in session to indicate they're logged in
            request.session['user_id'] = user.USERID
            return redirect('personal_page_view') # Redirect to personal page
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})


def personal_page_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login_view') # Redirect to login if not logged in

    user = CustomUser.objects.get(USERID=user_id)
    return render(request, 'personal_page.html', {'user': user})


def dataset_users_view(request):
    datasets = Dataset.objects.all().prefetch_related('users')
    return render(request, 'dataset_users.html', {'datasets': datasets})

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
