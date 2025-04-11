from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import MovieInformationData
from django.core.files.storage import FileSystemStorage

def list(request):
    movies = MovieInformationData.objects.all()
    return render(request, 'list.html', {'movies': movies})

def create(request):
    if request.method == 'POST':
        try:
 
            title = request.POST.get('title')
            year = request.POST.get('year')
            director = request.POST.get('director')
            rating = request.POST.get('rating')
            description = request.POST.get('description')
            
 
            if request.FILES.get('poster'):
                poster = request.FILES['poster']
                fs = FileSystemStorage(location='djangotest/static/images/movies')
                filename = fs.save(poster.name, poster)
                poster_url = f'images/{filename}'
            else:
                poster_url = 'images/default.jpg' 


            movie = MovieInformationData(
                title=title,
                year=year,
                director=director,
                rating=rating,
                description=description,
                poster=poster_url
            )
            movie.save()
            
            return redirect('list')
        except Exception as e:

            return render(request, 'create.html', {'error': str(e)})
    
    return render(request, 'create.html')


