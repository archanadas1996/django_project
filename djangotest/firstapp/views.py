from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import MovieInformationData, CensorInfo, Director, Actor
from .forms import MovieForm, CensorInfoForm, DirectorForm, ActorForm
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.db.models import Q
from .utils import get_recently_viewed, set_recently_viewed_cookie

def list(request):
    # Track visit count in session
    if 'visit_count' not in request.session:
        request.session['visit_count'] = 1
    else:
        request.session['visit_count'] += 1
    
    # Get filter parameters from request
    search_query = request.GET.get('search', '')
    year_filter = request.GET.get('year', '')
    director_filter = request.GET.get('director', '')
    actor_filter = request.GET.get('actor', '')
    censor_filter = request.GET.get('censor', '')
    sort_by = request.GET.get('sort', '-year')  # Default sort by year descending
    
    # Start with all movies
    movies = MovieInformationData.objects.all()
    
    # Apply search filter if provided
    if search_query:
        movies = movies.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Apply year filter if provided
    if year_filter:
        movies = movies.filter(year=year_filter)
    
    # Apply director filter if provided
    if director_filter:
        movies = movies.filter(directed_by__id=director_filter)
    
    # Apply actor filter if provided
    if actor_filter:
        movies = movies.filter(actors__id=actor_filter)
    
    # Apply censor filter if provided
    if censor_filter:
        movies = movies.filter(censor_details__rating=censor_filter)
    
    # Apply sorting
    if sort_by == 'title':
        movies = movies.order_by('title')
    elif sort_by == '-title':
        movies = movies.order_by('-title')
    elif sort_by == 'year':
        movies = movies.order_by('year')
    elif sort_by == '-year':
        movies = movies.order_by('-year')
    elif sort_by == 'rating':
        movies = movies.order_by('rating')
    elif sort_by == '-rating':
        movies = movies.order_by('-rating')
    
    # Get all directors, actors, and censor ratings for filter dropdowns
    directors = Director.objects.all()
    actors = Actor.objects.all()
    censor_ratings = CensorInfo.RATING_CHOICES
    
    # Get unique years for year filter
    years = MovieInformationData.objects.values_list('year', flat=True).distinct().order_by('year')
    
    # Get recently viewed movies
    recently_viewed_ids = [m['id'] for m in get_recently_viewed(request)]
    recently_viewed = MovieInformationData.objects.filter(id__in=recently_viewed_ids)
    
    context = {
        'movies': movies,
        'directors': directors,
        'actors': actors,
        'censor_ratings': censor_ratings,
        'years': years,
        'search_query': search_query,
        'year_filter': year_filter,
        'director_filter': director_filter,
        'actor_filter': actor_filter,
        'censor_filter': censor_filter,
        'sort_by': sort_by,
        'recently_viewed': recently_viewed,
        'visit_count': request.session['visit_count'],  # Add visit count to context
    }
    
    response = render(request, 'firstapp/list.html', context)
    return response

def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form but don't commit to database yet
            movie = form.save(commit=False)
            
            # Handle the poster file
            if request.FILES.get('poster'):
                poster = request.FILES['poster']
                fs = FileSystemStorage(location='djangotest/static/images')
                filename = fs.save(poster.name, poster)
                movie.poster = f'images/{filename}'
            else:
                movie.poster = 'images/default.jpg'
            
            # Save the movie first
            movie.save()
            
            # Now save the many-to-many relationships
            form.save_m2m()
            
            # Explicitly set the actors
            if 'actors' in request.POST:
                movie.actors.set(request.POST.getlist('actors'))
            
            messages.success(request, 'Movie added successfully!')
            return redirect('movie_list')
    else:
        form = MovieForm()
    
    return render(request, 'firstapp/add_movie.html', {'form': form})

def edit_movie(request, movie_id):
    movie = get_object_or_404(MovieInformationData, pk=movie_id)
    
    # Update recently viewed
    viewed_movies = get_recently_viewed(request, movie_id)
    
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            movie = form.save(commit=False)
            if request.FILES.get('poster'):
                poster = request.FILES['poster']
                fs = FileSystemStorage(location='djangotest/static/images')
                filename = fs.save(poster.name, poster)
                movie.poster = f'images/{filename}'
            
            # Save the movie first
            movie.save()
            
            # Now save the many-to-many relationships
            form.save_m2m()
            
            # Explicitly set the actors
            if 'actors' in request.POST:
                movie.actors.set(request.POST.getlist('actors'))
            
            messages.success(request, 'Movie updated successfully!')
            return redirect('movie_list')
    else:
        form = MovieForm(instance=movie)
    
    response = render(request, 'firstapp/edit_movie.html', {'form': form, 'movie': movie})
    return set_recently_viewed_cookie(response, viewed_movies)

def delete_movie(request, movie_id):
    movie = get_object_or_404(MovieInformationData, pk=movie_id)
    if request.method == 'POST':
        movie.delete()
        messages.success(request, 'Movie deleted successfully!')
        return redirect('movie_list')
    return render(request, 'firstapp/delete_movie.html', {'movie': movie})

def add_censor_info(request):
    if request.method == 'POST':
        form = CensorInfoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Censor information added successfully!')
            return redirect('movie_list')
    else:
        form = CensorInfoForm()
    return render(request, 'firstapp/add_censor_info.html', {'form': form})

def add_director(request):
    if request.method == 'POST':
        form = DirectorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Director added successfully!')
            return redirect('movie_list')
    else:
        form = DirectorForm()
    return render(request, 'firstapp/add_director.html', {'form': form})

def add_actor(request):
    if request.method == 'POST':
        form = ActorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Actor added successfully!')
            return redirect('movie_list')
    else:
        form = ActorForm()
    return render(request, 'firstapp/add_actor.html', {'form': form})


