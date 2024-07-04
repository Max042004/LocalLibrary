from django.db import models
from django.urls import reverse # Used in get_absolute_url() to get URL for specified ID

from django.db.models import UniqueConstraint # Constrains fields to unique values
from django.db.models.functions import Lower # Returns lower cased value of field

import uuid

class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)"
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular genre instance.
          url mapper是先定義URL, 而reverse則會創造URL, 
          for this to work, we will have to define a URL mapping that has the name genre-detail, 
          and define an associated view and template"""
        return reverse('genre-detail', args=[str(self.id)])

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='genre_name_case_insensitive_unique',
                violation_error_message = "Genre already exists (case insensitive match)"
            ),
        ]

class Book(models.Model):
    title = models.CharField(
        max_length=200,
        help_text="Enter the full book name",
        )
    
    author = models.ForeignKey(
        'Author',
        on_delete=models.RESTRICT,
        null=True)
    """on_delete=models.RESTRICT, 
    which will prevent the book's associated author being deleted if it is referenced by any book."""

    language = models.ForeignKey(
        'Language',
        on_delete=models.SET_NULL,
        null=True,
    )

    summary = models.TextField(
        max_length=2000,
        help_text="Enter the summary",

    )

    isbn = models.CharField(
        "ISBN",
        max_length=50,
        unique=True,
        help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>',)

    genre = models.ManyToManyField(
        Genre, help_text="Select a genre for this book")
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.id)])

class BookInstance(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="Unique ID for this particular book across whole library",
    )

    book = models.ForeignKey("Book", on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text="book availablilty")
    
    class Meta:
        ordering = ['due_back']
    
    def __str__(self):
        return f'{self.id} ({self.book.title})'
    
class Author(models.Model):
    first_name = models.CharField(
        max_length=200,
        help_text="Enter Author's name",
    )
    last_name = models.CharField(
        max_length=200,
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )
    date_of_death = models.DateField(
        "Died",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["last_name", "first_name"]

    def get_absolute_url(self):
        return reverse("author-detail", args=[str(self.id)])
    
    def __str__(self):
        return f"{self.last_name}, {self.last_name}"

class Language(models.Model):
    lan = models.CharField(
        max_length=100,
    )

    def __str__(self):
        return self.lan
    
    def get_absolute_url(self):
        return reverse("lan-name", args=[str(self.id)])

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower("lan"),
                name='language_name_case_insensitive_unique',
                violation_error_message = "Language already exists (case insensitive match)"
            ),
        ]
