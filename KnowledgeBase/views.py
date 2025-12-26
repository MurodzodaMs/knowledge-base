from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
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
    template_name = 'course.html'
    context_object_name = 'data'


    def get_object(self, queryset: QuerySet[Any] | None = ...):
        return Course.objects.get(
            slug=self.kwargs['course_slug'],
            category__slug=self.kwargs['category_slug'],
        )


    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        course = self.object
        context['chapters'] = Chapter.objects.filter(course=course)
        context['lessons'] = Lesson.objects.filter(chapter__in=context['chapters'])
        context['categories'] = Category.objects.all()
        return context


class LessonView(generic.DetailView):
    template_name = 'lesson.html'
    model = Lesson
    context_object_name = 'data'

    def get_object(self, queryset: QuerySet[Any] | None = ...):
        return Lesson.objects.get(
            chapter__course__slug=self.kwargs['course_slug'],
            chapter__course__category__slug=self.kwargs['category_slug'],
            chapter__order=self.kwargs['chapter'],
            order=self.kwargs['lesson'],
        )
    

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        lesson = self.object
        chapter = lesson.chapter
        course = chapter.course

        context['categories'] = Category.objects.all()
        context['chapters'] = Chapter.objects.filter(course=course)
        context['lessons'] = Lesson.objects.filter(chapter=chapter)
        context['page'] = Page.objects.get(lesson=lesson)
        context['blocks'] = Block.objects.filter(page=context['page'])

        return context




class CategoryCreateView(generic.CreateView):
    queryset = Category.objects.all()
    template_name = 'create.html'
    fields = '__all__' 
    success_url = '/'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Category'
        return context

class CourseCreateView(generic.CreateView):
    model = Course
    template_name = 'create.html'
    fields = '__all__'
    success_url = '/'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Course'
        return context

class ChapterCreateView(generic.CreateView):
    model = Chapter
    template_name = 'create.html'
    fields = '__all__'
    success_url = '/'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Chapter'
        return context

class LessonCreateView(generic.CreateView):
    model = Lesson
    template_name = 'create.html'
    fields = '__all__'
    success_url = '/'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        print('---yes---')
        response = super().form_valid(form)
        Page.objects.create(lesson=self.object)
        return response
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Lesson'
        return context
    
class UserCreateView(generic.CreateView):
    model = User
    template_name = 'create.html'
    success_url = '/login'
    fields = []