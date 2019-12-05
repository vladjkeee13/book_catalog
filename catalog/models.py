from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Character(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    img = models.ImageField(upload_to='books_images')
    author = models.CharField(max_length=255)
    pages = models.IntegerField()
    published = models.DateField()
    isbn = models.CharField(max_length=255)
    language = models.CharField(max_length=255)

    img_source = models.URLField(max_length=255, null=True)
    book_source = models.URLField(max_length=255, null=True, blank=True)

    parsing_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    cat = models.ManyToManyField(Category)
    char = models.ManyToManyField(Character)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Reviews(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    email = models.EmailField()
    comment = models.TextField()
    rating = models.IntegerField()
    website = models.URLField()
    published = models.DateTimeField(auto_now_add=True)
    moderated = models.BooleanField(default=False)

    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
