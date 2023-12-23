from django.shortcuts import render, redirect
from .forms import UserLoginForm, AdminLoginForm, RegisterDatasetForm
from django.contrib import messages
from django.contrib.auth import logout
from .models import CustomUser, Dataset, UserDataset
import os

def home_page_view(request):
    user_form = UserLoginForm(request.POST or None)
    admin_form = AdminLoginForm(request.POST or None)

    if request.method == "POST":
        if 'user_login' in request.POST and user_form.is_valid():
            email = user_form.cleaned_data.get('email')
            user = CustomUser.objects.filter(EMAIL=email).first()
            if not user:
                user = CustomUser.objects.create(EMAIL=email)
            request.session['user_id'] = user.USERID
            return redirect('personal_page_view')
        
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


def personal_page_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('home_page_view')  

    user = CustomUser.objects.get(USERID=user_id)

    if 'remove_dataset_id' in request.POST:
        dataset_id = request.POST['remove_dataset_id']
        try:
            user_dataset = UserDataset.objects.get(pk=dataset_id, customuser=user)
            user_dataset.delete()
        except UserDataset.DoesNotExist:
            pass  

    if request.method == "POST":
        form = RegisterDatasetForm(request.POST)
        if form.is_valid():
            selected_dataset = form.cleaned_data.get('dataset')
            description = form.cleaned_data.get('description')
            UserDataset.objects.create(customuser=user, dataset=selected_dataset, description=description)
            return redirect('personal_page_view')
    else:
        registered_dataset_ids = UserDataset.objects.filter(customuser=user).values_list('dataset_id', flat=True)
        form = RegisterDatasetForm(exclude_datasets=registered_dataset_ids)

    user_datasets = UserDataset.objects.filter(customuser=user).order_by('dataset__TITEL')
    context = {'user': user,'form': form,'user_datasets': user_datasets,}
    return render(request, 'personal_page.html', context)


def admin_page_view(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    return render(request, 'admin_page.html')


def logout_admin(request):
    logout(request)
    if 'admin_logged_in' in request.session:
        del request.session['admin_logged_in']
    return redirect('home_page_view')


def logout_view(request):
    request.session.flush()
    return redirect('home_page_view')


def dataset_users_view(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    datasets_with_users = Dataset.objects.filter(userdataset__isnull=False).order_by('TITEL').distinct()

    dataset_user_info = {}
    for dataset in datasets_with_users:
        user_datasets = UserDataset.objects.filter(dataset=dataset).select_related('customuser')
        dataset_user_info[dataset] = user_datasets

    return render(request, 'dataset_users.html', {'dataset_user_info': dataset_user_info})


def users_view(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    
    users = CustomUser.objects.order_by('EMAIL').all()
    user_dataset_info = {}
    for user in users:
        user_datasets = UserDataset.objects.filter(customuser=user).order_by('dataset__TITEL').select_related('dataset')
        user_dataset_info[user] = user_datasets

    return render(request, 'users.html', {'user_dataset_info': user_dataset_info})

def delete_user(request, user_id):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    user = CustomUser.objects.get(USERID=user_id)
    user.delete()
    return redirect('users_view')


def datasets_view(request):
    datasets = Dataset.objects.all()
    return render(request, 'datasets.html', {'datasets': datasets})

