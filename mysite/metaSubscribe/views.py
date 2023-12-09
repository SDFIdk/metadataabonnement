from django.shortcuts import render, redirect
from .forms import UserLoginForm, AdminLoginForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
# from .forms import AdminLoginForm
from django.http import HttpResponse
from .models import Dataset
from .models import CustomUser, Dataset, UserDataset
from .forms import RegisterDatasetForm
import os

def delete_user(request, user_id):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    # Get the user and delete
    user = CustomUser.objects.get(USERID=user_id)
    user.delete()  # This will delete the user and all related data

    return redirect('users_view')  # Redirect back to the users page

def admin_page_view(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    return render(request, 'admin_page.html')

def admin_login(request):
    if request.method == "POST":
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            admin_email = os.environ.get("ADMIN_EMAIL")
            admin_password = os.environ.get("ADMIN_PASSWORD")

            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            if email == admin_email and password == admin_password:
                request.session['admin_logged_in'] = True
                return redirect('admin_page')  # redirect to the admin page view
            else:
                messages.error(request, 'Invalid admin credentials')
    else:
        form = AdminLoginForm()

    return render(request, 'homepage.html', {'form': form})

@login_required
def admin_page(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')  # if not logged in as admin, redirect to admin login

    # ... (code to handle admin page)
    return render(request, 'admin_page.html')

def logout_admin(request):
    logout(request)
    if 'admin_logged_in' in request.session:
        del request.session['admin_logged_in']
    return redirect('home_page')  # redirect to the homepage or wherever appropriate


def logout_view(request):
    # Clear out the entire session
    request.session.flush()
    return redirect('home_page')


def personal_page_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('home_page')  # Redirect to login if not logged in

    user = CustomUser.objects.get(USERID=user_id)

    # Handle the dataset removal
    if 'remove_dataset_id' in request.POST:
        dataset_id = request.POST['remove_dataset_id']
        try:
            # The ID here should refer to the UserDataset object, not the Dataset object.
            user_dataset = UserDataset.objects.get(pk=dataset_id, customuser=user)
            user_dataset.delete()
        except UserDataset.DoesNotExist:
            # Handle the error if no entry matches
            pass  # Or provide a message or logging
        return redirect('personal_page_view')

    # Handle dataset registration
    if request.method == "POST":
        form = RegisterDatasetForm(request.POST)
        if form.is_valid():
            selected_datasets = form.cleaned_data.get('dataset')
            
            # Ensure selected_datasets is iterable
            if isinstance(selected_datasets, Dataset):
                selected_datasets = [selected_datasets]
            
            for dataset in selected_datasets:
                description = form.cleaned_data['description']
                
                # Create a record in metaSubscribe_userdataset
                UserDataset.objects.create(customuser=user, dataset=dataset, description=description)

                # Create a record in UserDataset
                """UserDataset.objects.create(customuser=user, dataset=dataset, description=description)"""

                # Add the dataset to the user's datasets
                user.datasets.add(dataset)
            
            return redirect('personal_page_view')
    else:
        form = RegisterDatasetForm()

    user_datasets = UserDataset.objects.filter(customuser=user)  # Retrieve user's datasets with descriptions

    context = {
        'user': user,
        'form': form,
        'user_datasets': user_datasets,
    }
    return render(request, 'personal_page.html', context)






def dataset_users_view(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    # Fetch all datasets that have at least one user associated via UserDataset
    datasets_with_users = Dataset.objects.filter(userdataset__isnull=False).distinct()

    # Create a data structure to hold users per dataset
    dataset_user_info = {}
    for dataset in datasets_with_users:
        # Get users associated with each dataset
        users_for_dataset = CustomUser.objects.filter(userdataset__dataset=dataset)
        dataset_user_info[dataset] = users_for_dataset

    return render(request, 'dataset_users.html', {'dataset_user_info': dataset_user_info})



def user_datasets_view(request):

    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    
    # This query might be inefficient if the number of users is large.
    # Consider using pagination or filtering.
    users = CustomUser.objects.all()

    # Prepare a structure to hold datasets with descriptions per user
    user_dataset_info = {}
    for user in users:
        user_datasets = UserDataset.objects.filter(customuser=user).select_related('dataset')
        user_dataset_info[user] = user_datasets  # This pairs the user with their respective datasets and descriptions

    return render(request, 'user_datasets.html', {'user_dataset_info': user_dataset_info})

def users_view(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    
    users = CustomUser.objects.all()
    return render(request, 'users.html', {'users': users})


def datasets_view(request):
    datasets = Dataset.objects.all()
    return render(request, 'datasets.html', {'datasets': datasets})

def home_page(request):
    user_form = UserLoginForm(request.POST or None)
    admin_form = AdminLoginForm(request.POST or None)

    if request.method == "POST":
        if 'user_login' in request.POST and user_form.is_valid():
            email = user_form.cleaned_data.get('email')
            user = CustomUser.objects.filter(EMAIL=email).first()

            # If the user doesn't exist, create them
            if not user:
                user = CustomUser.objects.create(EMAIL=email)

            # Set user id in session to indicate they're logged in
            request.session['user_id'] = user.USERID
            return redirect('personal_page_view')  # Redirect to the personal page

        elif 'admin_login' in request.POST and admin_form.is_valid():
            admin_email = os.environ.get("ADMIN_EMAIL")
            admin_password = os.environ.get("ADMIN_PASSWORD")

            email = admin_form.cleaned_data.get("email")
            password = admin_form.cleaned_data.get("password")

            if email == admin_email and password == admin_password:
                request.session['admin_logged_in'] = True
                return redirect('admin_page')
            else:
                messages.error(request, 'Invalid admin credentials')

    context = {'user_form': user_form, 'admin_form': admin_form}
    return render(request, 'homepage.html', context)


