from django.db.models import Q
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from django.db.models import Avg
from .models import Movie, Category, Actor, Genre, Raiting
from .forms import ReviewForm, RaitingForm

class GenreYear:
    """Жанры и года выхода фильмов"""
    def get_genres(self):
        return Genre.objects.all()
    def get_years(self):
        return Movie.objects.filter(draft=False).values("year")

class MoviesView(GenreYear, ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft= False)
    paginate_by = 3
    # template_name = 'movies/movies.html'
    """Navbar Category"""
    # def get_context_data(self, *args,**kwargs):
    #     context = super().get_context_data(*args ,**kwargs)
    #     context["categories"] = Category.objects.all()
    #     return context

class MovieDetailView(GenreYear, DetailView):
    """Полное описание фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    slug_field = "url"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RaitingForm()
        context["form"] = ReviewForm()
        return context



class AddReview(View):
    """Отзывы"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())

class ActorView(GenreYear, DetailView):
    '''Вывод инофрмации о актере'''
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = 'name'

class FilterMoviesView(GenreYear, ListView):
    """Фильтр фильмов"""
    paginate_by = 2
    
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct()
        return queryset
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['year'] = ''.join([f"year={x}&" for x in self.request.GET.getlist('year')])
        context['genre'] = ''.join([f"genre={x}&" for x in self.request.GET.getlist('genre')])
        return context
    
class JsonFilterMoviesView(ListView):
    """Фильтр фильмов в json"""
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct().values("title", "tagline", "url", "poster")
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"movies": queryset}, safe=False)

class AddStarRating(View):
    """Добавление рейтинга фильму"""
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    def post(self, request):
        form = RaitingForm(request.POST)
        if form.is_valid():
            Raiting.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id':int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)

class Seacrh(ListView):
    """Поиск фильмов"""
    paginate_by = 3

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get("q"))
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context

class CategoryView(View):
    def get(self, request, slug):
        category = Category.objects.get(slug=slug)
        product = Movie.objects.filter(category=category)
        return render(request, 'movies/category.html', {'product': product})