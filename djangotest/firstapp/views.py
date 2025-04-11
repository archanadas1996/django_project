from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import MovieInformationData
from .forms import MovieForm
from django.core.files.storage import FileSystemStorage

def list(request):
    movies = MovieInformationData.objects.all()
    return render(request, 'list.html', {'movies': movies})

def create(request):
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
            
            # Save the movie with the updated poster path
            movie.save()
            return redirect('list')
    else:
        form = MovieForm()
    
    return render(request, 'create.html', {'form': form})

def edit(request, pk):
    movie = get_object_or_404(MovieInformationData, pk=pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            movie = form.save(commit=False)
            if request.FILES.get('poster'):
                poster = request.FILES['poster']
                fs = FileSystemStorage(location='djangotest/static/images')
                filename = fs.save(poster.name, poster)
                movie.poster = f'images/{filename}'
            movie.save()
            return redirect('list')
    else:
        form = MovieForm(instance=movie)
    return render(request, 'edit.html', {'form': form, 'movie': movie})

def delete(request, pk):
    movie = get_object_or_404(MovieInformationData, pk=pk)
    if request.method == 'POST':
        movie.delete()
        return redirect('list')
    return render(request, 'delete.html', {'movie': movie})


