from .models import *
from django.views import generic
from django.contrib.auth.decorators import login_required

class CategoryListView(generic.ListView):
    model = Category
    template_name = 'homepage.html'
    context_object_name = 'categories'


 
# ------------ DETAIL -------------
class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'data'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['courses'] = Course.objects.all()

        return context
 

class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'course.html'
    context_object_name = 'data'


    def get_object(self, *args, **kwargs):
        return Course.objects.filter(
            slug=self.kwargs['course_slug'],
            category__slug=self.kwargs['category_slug'],
        ).first()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        context['chapters'] = Chapter.objects.filter(course=course)
        context['lessons'] = Lesson.objects.filter(chapter__in=context['chapters'])
        context['categories'] = Category.objects.all()
        return context




class LessonDetailView(generic.DetailView):
    template_name = 'lesson.html'
    model = Lesson
    context_object_name = 'data'

    def get_object(self, *args, **kwargs):
        return Lesson.objects.get(
            chapter__course__category__slug=self.kwargs['category_slug'],
            chapter__course__slug=self.kwargs['course_slug'],
            chapter__order=self.kwargs['chapter'],
            order=self.kwargs['lesson'],
        )
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = self.get_object()
        chapter = lesson.chapter
        course = chapter.course

        context['categories'] = Category.objects.all()
        context['chapters'] = Chapter.objects.filter(course=course)
        context['lessons'] = Lesson.objects.filter(chapter=chapter)
        context['page'] = Page.objects.get(lesson=lesson)
        context['blocks'] = Block.objects.filter(page=context['page'])

        return context
# ---------- DETAIL ------------



# --------- CREATE --------------
class BlockCreateView(generic.CreateView):
    model = Block
    template_name = 'lesson_edit.html'
    success_url = '/'
    


class CategoryCreateView(generic.CreateView):
    queryset = Category.objects.all()
    template_name = 'create.html'
    fields = '__all__' 
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Category'
        return context



class CourseCreateView(generic.CreateView):
    model = Course
    template_name = 'create.html'
    fields = '__all__'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Course'
        return context



class ChapterCreateView(generic.CreateView):
    model = Chapter
    template_name = 'create.html'
    fields = '__all__'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Chapter'
        return context



class LessonCreateView(generic.CreateView):
    model = Lesson
    template_name = 'create.html'
    fields = '__all__'
    success_url = '/'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Lesson'
        return context
# --------------- CREATE ----------------


