from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db import models
from django.db.models import Count
from django.core.paginator import Paginator

from .models import User, Profile, Hobby
from .forms import (
    LoginForm, SignUpForm, UserUpdateForm, 
    HobbyForm, PasswordChangeCustomForm
)

def main_spa(request: HttpRequest) -> HttpResponse:
    """Vue SPA entry point - only accessible after authentication"""
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'api/spa/index.html', {})

def signup_view(request):
    """Handle user registration"""
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create associated profile
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    
    return render(request, 'api/auth/signup.html', {'form': form})

def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        if settings.DEBUG:  # Development mode
            return redirect('http://localhost:5173')  # Frontend dev server
        return redirect('home')
        
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if settings.DEBUG:  # Development mode
                    return redirect('http://localhost:5173')  # Frontend dev server
                return redirect('home')
            form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    
    return render(request, 'api/auth/login.html', {'form': form})

@login_required
def logout_view(request):
    """Handle user logout"""
    logout(request)
    return redirect('login')

@login_required
@require_http_methods(['GET', 'PUT'])
def profile_api(request):
    """API endpoint for profile operations"""
    if request.method == 'GET':
        return JsonResponse(request.user.to_dict())
        
    # Handle PUT request
    data = request.POST if request.POST else request.GET
    form = UserUpdateForm(data, instance=request.user)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'errors': form.errors})

@login_required
def password_change(request):
    """Handle password change"""
    if request.method == 'POST':
        form = PasswordChangeCustomForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
@require_http_methods(['GET', 'POST'])
def hobby_api(request):
    """API endpoint for hobby operations"""
    if request.method == 'GET':
        hobbies = Hobby.objects.all()
        return JsonResponse({
            'hobbies': [hobby.to_dict() for hobby in hobbies]
        })
    
    # Handle POST request to create new hobby
    form = HobbyForm(request.POST)
    if form.is_valid():
        hobby = form.save(commit=False)
        hobby.created_by = request.user
        hobby.save()
        return JsonResponse({'status': 'success', 'hobby': hobby.to_dict()})
    return JsonResponse({'status': 'error', 'errors': form.errors})

@login_required
def similar_users_view(request):
    """
    API view to find users with the most similar hobbies with pagination.
    """
    current_user = request.user

    # Exclude the current user and annotate with the number of common hobbies
    similar_users = (
        User.objects.exclude(id=current_user.id)
        .annotate(common_hobbies=Count('hobbies', filter=models.Q(hobbies__in=current_user.hobbies.all())))
        .order_by('-common_hobbies')
    )

    # Paginate the results
    paginator = Paginator(similar_users, 10)
    page_number = request.GET.get('page', 1)  
    page_obj = paginator.get_page(page_number)

    # Convert the results into a dictionary for JSON response
    similar_users_data = [
        {
            "username": user.username,
            "common_hobbies": user.common_hobbies,
            "hobbies": [hobby.name for hobby in user.hobbies.all()]
        }
        for user in page_obj.object_list
    ]

    return JsonResponse({
        "page": page_obj.number,
        "total_pages": paginator.num_pages,
        "total_users": paginator.count,
        "users_per_page": paginator.per_page,
        "similar_users": similar_users_data,
    })

from datetime import date, timedelta
from django.core.paginator import Paginator
from django.http import JsonResponse

def filtered_users_view(request):
    """
    API view to filter users by age with pagination.
    """
    min_age = int(request.GET.get("min_age", 0))
    max_age = int(request.GET.get("max_age", 100))
    page_number = int(request.GET.get("page", 1))

    # Calculate date range based on age
    today = date.today()
    min_birthdate = date(today.year - max_age - 1, today.month, today.day) + timedelta(days=1)
    max_birthdate = date(today.year - min_age, today.month, today.day)

    # Filter users by date_of_birth
    filtered_users = User.objects.filter(
        date_of_birth__range=(min_birthdate, max_birthdate)
    ).order_by('username') 

    # Paginate results
    paginator = Paginator(filtered_users, 10) 
    page_obj = paginator.get_page(page_number)

    # Prepare JSON  data
    filtered_users_data = [
        {
            "username": user.username,
            "email": user.email,
            "date_of_birth": user.date_of_birth.strftime("%Y-%m-%d"),
            "age": user.age,
            "hobbies": [hobby.name for hobby in user.hobbies.all()],
        }
        for user in page_obj.object_list
    ]

    return JsonResponse({
        "page": page_obj.number,
        "total_pages": paginator.num_pages,
        "total_users": paginator.count,
        "users_per_page": paginator.per_page,
        "filtered_users": filtered_users_data,
    })

