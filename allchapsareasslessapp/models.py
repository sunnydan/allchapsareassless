from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from django.conf import settings
from allchapsareasslessapp.storage import OverwriteStorage


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)
    displayName = models.CharField(max_length=30)
    avatar = models.ImageField(
        upload_to='avatars/', default='/avatars/default.png', storage=OverwriteStorage())
    memberSince = models.DateTimeField(default=datetime.now, blank=True)
    gamesPlayed = models.IntegerField(default=0)
    gamesWon = models.IntegerField(default=0)
    roundsWon = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'

    # does not contain email because it automatically contains the USERNAME_FIELD, which is set to email.
    REQUIRED_FIELDS = []

    objects = UserManager()


class Card(models.Model):
    image = models.ImageField(upload_to='cards/')
    bonusCard = models.BooleanField(default=False)
    private = models.BooleanField(default=False)
    dateCreated = models.DateTimeField(default=datetime.now, blank=True)

    author = models.ForeignKey(
        User, related_name="cards", null=True, on_delete=models.SET_NULL)
    likingUsers = models.ManyToManyField(User, related_name="likedCards")


class Deck(models.Model):
    name = models.TextField(max_length=30, blank=False)
    description = models.TextField(max_length=255, blank=False)
    private = models.BooleanField(default=False)
    dateCreated = models.DateTimeField(default=datetime.now, blank=True)

    author = models.ForeignKey(
        User, related_name="decks", null=True, on_delete=models.SET_NULL)
    likingUsers = models.ManyToManyField(User, related_name="likedDecks")
    cards = models.ManyToManyField(Card, related_name="decks")


class Tag(models.Model):
    name = models.TextField(max_length=30, blank=False)

    cards = models.ManyToManyField(Card, related_name="tags")
    decks = models.ManyToManyField(Deck, related_name="tags")
