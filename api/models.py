from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from typing import Dict, Any

#Create your models here.
class User(AbstractUser):
    '''
    Custom User model inheriting from Django's AbstractUser
    to make use of Django's authentication system while adding
    hobby and friend-related functionality
    '''
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True)
    profile = models.OneToOneField(
        to='Profile',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    hobbies = models.ManyToManyField(
        to='Hobby',
        blank=True,
        related_name='users'
    )
    friends = models.ManyToManyField(
        to='self',
        blank=True,
        symmetrical=False,
        through='FriendRequest',
        related_name='related_to'
    )

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self) -> str:
        return self.username

    def to_dict(self) -> Dict[str, Any]:
        return {
            'username': self.username,
            'email': self.email,
            'date_of_birth': self.date_of_birth.strftime("%Y-%m-%d") if self.date_of_birth else None,
            'profile': self.profile.to_dict() if self.profile else None,
            'hobbies': [hobby.to_dict() for hobby in self.hobbies.all()],
            'age': self.age,
        }

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def update_password(self, new_password: str) -> None:
        self.set_password(new_password)
        self.save()
    
    def update_profile(self, data: Dict[str, Any]) -> None:
        for field, value in data.items():
            if hasattr(self, field):
                setattr(self, field, value)
        self.save()

    @property
    def age(self) -> int:
        if self.date_of_birth:
            today = timezone.now().date()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < 
                (self.date_of_birth.month, self.date_of_birth.day)
            )
        return 0

    @property
    def friend_count(self) -> int:
        '''Count of confirmed friends'''
        return FriendRequest.objects.filter(
            (models.Q(from_user=self) | models.Q(to_user=self)) &
            models.Q(status='accepted')
        ).count()

    def get_common_hobbies(self, other_user: 'User') -> int:
        '''Count number of hobbies in common with another user'''
        return self.hobbies.filter(id__in=other_user.hobbies.all()).count()


class Profile(models.Model):
    '''
    Profile model for additional user information
    '''
    bio = models.CharField(max_length=4096, blank=True)
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)

    def __str__(self) -> str:
        return f"Profile for {self.user_check}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            'bio': self.bio,
            'avatar': self.avatar.url if self.avatar else None,
        }

    @property
    def has_user(self) -> bool:
        '''Check if profile is associated with a user'''
        return hasattr(self, 'user') and self.user is not None

    @property
    def user_check(self) -> str:
        '''Return username of associated user or NONE'''
        return str(self.user) if self.has_user else 'NONE'


class Hobby(models.Model):
    '''
    Hobby model to store available hobbies
    '''
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_hobbies'
    )

    class Meta:
        verbose_name_plural = "hobbies"

    def __str__(self) -> str:
        return self.name

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M"),
            'created_by': self.created_by.username if self.created_by else None,
        }


class FriendRequest(models.Model):
    '''
    Through model for managing friend relationships between users
    '''
    from_user = models.ForeignKey(
        User,
        related_name='sent_requests',
        on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        User,
        related_name='received_requests',
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected')
        ],
        default='pending'
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self) -> str:
        return f"Friend request from {self.from_user} to {self.to_user}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'from_user': self.from_user.username,
            'to_user': self.to_user.username,
            'status': self.status,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M"),
        }
    
