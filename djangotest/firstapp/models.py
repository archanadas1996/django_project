from django.db import models

# Create your models here.

class CensorInfo(models.Model):
    RATING_CHOICES = [
        ('G', 'General Audiences'),
        ('PG', 'Parental Guidance'),
        ('PG-13', 'Parents Strongly Cautioned'),
        ('R', 'Restricted'),
        ('NC-17', 'Adults Only'),
    ]
    
    rating = models.CharField(max_length=5, choices=RATING_CHOICES)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_rating_display()} - {self.description[:50]}"

    class Meta:
        verbose_name = "Censor Information"
        verbose_name_plural = "Censor Information"

class Director(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=50)
    awards = models.TextField(blank=True)
    photo = models.ImageField(upload_to='directors/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Actor(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=50)
    awards = models.TextField(blank=True)
    photo = models.ImageField(upload_to='actors/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class MovieInformationData(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    rating = models.CharField(max_length=10)
    description = models.TextField()
    poster = models.ImageField(upload_to='posters/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    censor_details = models.OneToOneField(CensorInfo, null=True, on_delete=models.SET_NULL, related_name='movie')
    directed_by = models.ForeignKey(Director, null=True, on_delete=models.SET_NULL, related_name='directed_movies')
    actors = models.ManyToManyField(Actor, related_name='acted_movies')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
    