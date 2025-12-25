from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.views import generic


class HomePageView(generic.ListView):
    model = Category
    template_name = 'homepage.html'
    context_object_name = 'categories'


class CategoryPageView(generic.DetailView):
    model = Category
    # slug_field = 'slug'
    # slug_url_kwarg = 'category_slug '
    template_name = 'category.html'
    context_object_name = 'data'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['courses'] = Course.objects.all()
 
        return context
 

class CoursePageView(generic.DetailView):
    model = Course
    # slug_url_kwarg = 'c'
    template_name = 'course.html'
    context_object_name = 'data'


    def get_object(self, queryset: QuerySet[Any] | None = ...):
        return Course.objects.get(
            slug=self.kwargs['course_slug'],
            category__slug=self.kwargs['category_slug'],
        )


    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['lessons'] = Lesson.objects.all()
        context['chapters'] = Chapter.objects.all()
        context['categories'] = Category.objects.all()
        return context




class CategoryCreateView(generic.CreateView):
    queryset = Category.objects.all()
    template_name = 'create.html'
    fields = '__all__' 
    success_url = '/'

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return redirect('home')


# class UserCreateView(generic.CreateView):
    