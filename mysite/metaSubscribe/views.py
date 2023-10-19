from django.shortcuts import render, redirect
from .forms import UserLoginForm
from django.http import HttpResponse
from .models import Dataset
from .models import CustomUser, Dataset, UserDataset
from .forms import RegisterDatasetForm

def admin_page_view(request):
    return render(request, 'admin_page.html')


def logout_view(request):
    # Clear out the entire session
    request.session.flush()
    return redirect('home_page')


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
        return redirect('login_view')  # Redirect to login if not logged in

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
    # Filter out datasets without users
    datasets_with_users = Dataset.objects.filter(users__isnull=False).distinct().prefetch_related('users')

    return render(request, 'dataset_users.html', {'datasets': datasets_with_users})


def user_datasets_view(request):
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
    users = CustomUser.objects.all()
    return render(request, 'users.html', {'users': users})


def datasets_view(request):
    datasets = Dataset.objects.all()
    return render(request, 'datasets.html', {'datasets': datasets})

def home_page(request):
    if 'user_id' in request.session:
        return redirect('personal_page_view')  # If the user is already logged in, redirect to personal page

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

    return render(request, 'homepage.html', {'form': form})

    # return HttpResponse("Hello human, I am the messenger and this is the homepage!")


