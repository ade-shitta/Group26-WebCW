from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db import models
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from datetime import date, timedelta

from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
import json

from .models import User, Profile, Hobby, Friends
from .forms import (
    LoginForm, SignUpForm, UserUpdateForm, 
    HobbyForm, PasswordChangeCustomForm
)

@ensure_csrf_cookie
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
            user.save()
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
        return redirect('home')
        
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
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
        
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)

        form = UserUpdateForm(data, instance=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'}, status=200)
        else:
            # Log form errors for debugging
            print(form.errors)
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

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
    data = json.loads(request.body)
    form = HobbyForm(data)
    if form.is_valid():
        hobby = form.save(commit=False)
        hobby.created_by = request.user
        hobby.save()
        # Link the created hobby to the user
        request.user.hobbies.add(hobby)
        return JsonResponse({'status': 'success', 'hobby': hobby.to_dict()})
    return JsonResponse({'status': 'error', 'errors': form.errors})

@login_required
@require_http_methods(['POST'])
def add_hobby_to_profile(request):
    """API endpoint to add an existing hobby to the user's profile"""
    data = json.loads(request.body)
    hobby_id = data.get('hobby_id')
    if not hobby_id:
        return JsonResponse({'status': 'error', 'errors': {'hobby_id': ['This field is required.']}})

    try:
        hobby = Hobby.objects.get(id=hobby_id)
    except Hobby.DoesNotExist:
        return JsonResponse({'status': 'error', 'errors': {'hobby_id': ['Hobby not found.']}})

    request.user.hobbies.add(hobby)
    return JsonResponse({'status': 'success'})

@login_required
@require_http_methods(['POST'])
def delete_hobby_from_profile(request):
    """API endpoint to delete a hobby from the user's profile"""
    data = json.loads(request.body)
    hobby_id = data.get('hobby_id')
    if not hobby_id:
        return JsonResponse({'status': 'error', 'errors': {'hobby_id': ['This field is required.']}})

    try:
        hobby = Hobby.objects.get(id=hobby_id)
    except Hobby.DoesNotExist:
        return JsonResponse({'status': 'error', 'errors': {'hobby_id': ['Hobby not found.']}})

    request.user.hobbies.remove(hobby)
    return JsonResponse({'status': 'success'})

@login_required
def similar_users_with_filters_view(request):
    """
    API view to find users with the most similar hobbies and filter by age, with pagination.
    """
    current_user = request.user
    min_age = int(request.GET.get("min_age", 0))
    max_age = int(request.GET.get("max_age", 100))
    page_number = int(request.GET.get("page", 1))

    # Calculate birthdate range for age filter
    today = date.today()
    min_birthdate = date(today.year - max_age - 1, today.month, today.day) + timedelta(days=1)
    max_birthdate = date(today.year - min_age, today.month, today.day)

    # Query users, excluding the current user, and annotate with the number of common hobbies
    similar_users = (
        User.objects.exclude(id=current_user.id)
        .filter(date_of_birth__range=(min_birthdate, max_birthdate))  # Apply age filter
        .annotate(common_hobbies=Count('hobbies', filter=Q(hobbies__in=current_user.hobbies.all())))
        .order_by('-common_hobbies')  # Sort by most common hobbies first
    )

    # Paginate the results
    paginator = Paginator(similar_users, 10)  # 10 users per page
    page_obj = paginator.get_page(page_number)

    # Convert results into a JSON-serializable format
    similar_users_data = [
        {
            "username": user.username,
            "common_hobbies": user.common_hobbies,
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
        "similar_users": similar_users_data,
    })

@login_required
def friends_view(request):
    if request.method == 'GET':
        friends = Friends.objects.filter(
            (models.Q(from_user=request.user) | models.Q(to_user=request.user)) &
            models.Q(status='accepted')
        )
        friends_data = [friend.to_dict(current_user=request.user) for friend in friends]
        print(friends_data)
        return JsonResponse({'status': 'success', 'friends': friends_data})

@login_required
def get_friend_requests(request):
    if request.method == 'GET':
        friend_requests = Friends.objects.filter(to_user=request.user, status='sent')
        requests_data = [fr.to_dict() for fr in friend_requests]
        print(requests_data)
        return JsonResponse({'status': 'success', 'friend_requests': requests_data})


@login_required
@require_http_methods(['POST'])
def send_request(request):
    """Send a friend request to another user."""
    data = json.loads(request.body)
    username = data.get('username')

    recipient = User.objects.filter(username=username).first()
    if not recipient:
        return JsonResponse({"status": "error", "message": "User not found"}, status=404)

    # Create a friend request
    Friends.objects.create(from_user=request.user, to_user=recipient, status='sent')
    return JsonResponse({"status": "success", "message": f"Friend request sent to {username}"})

@login_required
@require_http_methods(['POST'])
def accept_request(request):
    """Accept a friend request."""
    if request.method == 'POST':
        data = json.loads(request.body)
        request_id = data.get('request_id')
        friend_request = get_object_or_404(Friends, id=request_id, to_user=request.user, status='sent')
        friend_request.status = 'accepted'
        friend_request.save()
        return JsonResponse({'status': 'success', 'message': 'Friend request accepted'})

@login_required
def reject_request(request):
    """Reject a friend request."""
    if request.method == 'POST':
        data = json.loads(request.body)
        request_id = data.get('request_id')
        friend_request = get_object_or_404(Friends, id=request_id, to_user=request.user, status='sent')

        friend_request.status = 'rejected'
        friend_request.save()
        return JsonResponse({'status': 'success', 'message': 'Friend request rejected'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})




