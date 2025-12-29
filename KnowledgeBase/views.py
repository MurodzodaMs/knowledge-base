from typing import Any

from django.db.models.query import QuerySet
from .models import *
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse


class CategoryListView(generic.ListView):
    model = Category
    template_name = 'homepage.html'
    context_object_name = 'categories'

    def get_queryset(self) -> QuerySet[Any]:
        return Category.objects.filter(is_active=True)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        return super().get_context_data(**kwargs)


# ------------ READ -------------
class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'data'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        context['courses'] = Course.objects.filter(is_active=True)
        context['page'] = Page.objects.filter(category=self.get_object()).first()
        context['blocks'] = Block.objects.filter(page=context['page'])
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
        context['lessons'] = Lesson.objects.filter(
            chapter__in=context['chapters'])
        context['categories'] = Category.objects.filter(is_active=True)
        return context


class LessonDetailView(generic.DetailView):
    template_name = 'lesson.html'
    model = Lesson
    context_object_name = 'data'

    def get_object(self, *args, **kwargs):
        return Lesson.objects.filter(
            chapter__course__category__slug=self.kwargs['category_slug'],
            chapter__course__slug=self.kwargs['course_slug'],
            chapter__order=self.kwargs['chapter'],
            order=self.kwargs['lesson'],
        ).first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = self.get_object()
        chapter = lesson.chapter
        course = chapter.course

        context['categories'] = Category.objects.filter(is_active=True)
        context['chapters'] = Chapter.objects.filter(course=course)
        context['lessons'] = Lesson.objects.filter(chapter=chapter)
        context['page'] = Page.objects.filter(lesson=lesson).first()
        context['blocks'] = Block.objects.filter(page=context['page'])
        try:
            context['group'] = self.request.user.groups.first().name
        except:
            pass
        return context
# ---------- READ ------------




# --------- CREATE --------------
class BlockCreateView(LoginRequiredMixin, generic.CreateView):
    login_url = 'home'
    model = Block
    template_name = 'lesson.html'
    fields = ['type', 'comment', 'media']

    def get_success_url(self):
        return reverse('lesson', kwargs={
            'category_slug': self.kwargs['category_slug'],
            'course_slug': self.kwargs['course_slug'],
            'chapter': self.kwargs['chapter'],
            'lesson': self.kwargs['lesson'],
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Block'
        context['action'] = 'create'
        context['categories'] = Category.objects.filter(is_active=True)
        context['course'] = Course.objects.filter(
            slug=self.kwargs['course_slug']).first()
        context['chapters'] = Chapter.objects.filter(course=context['course'])
        context['lessons'] = Lesson.objects.filter(
            chapter__in=context['chapters'])
        context['page'] = Page.objects.filter(
            lesson__chapter__course__category__slug=self.kwargs['category_slug'],
            lesson__chapter__course=context['course'],
            lesson__chapter__order=self.kwargs['chapter'],
            lesson__order=self.kwargs['lesson'],
        ).first()
        context['blocks'] = Block.objects.filter(page=context['page'])
        context['group'] = self.request.user.groups.first().name
        return context

    def form_valid(self, form):
        page = Page.objects.filter(
            lesson__chapter__course__category__slug=self.kwargs['category_slug'],
            lesson__chapter__course__slug=self.kwargs['course_slug'],
            lesson__chapter__order=self.kwargs['chapter'],
            lesson__order=self.kwargs['lesson'],
        ).first()
        form.instance.page = page
        last_block = Block.objects.filter(page=page).order_by('-order').first()
        if last_block:
            form.instance.order = last_block.order + 1
        else:
            form.instance.order = 1
        return super().form_valid(form)


class CategoryCreateView(LoginRequiredMixin, generic.CreateView):
    login_url = 'home'
    queryset = Category.objects.filter(is_active=True)
    template_name = 'create.html'
    fields = '__all__'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Category'
        context['action'] = 'add'
        return context


class CourseCreateView(LoginRequiredMixin, generic.CreateView):
    login_url = 'home'
    model = Course
    template_name = 'create.html'
    fields = '__all__'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Course'
        context['action'] = 'add'
        return context


class ChapterCreateView(LoginRequiredMixin, generic.CreateView):
    login_url = 'home'
    model = Chapter
    template_name = 'create.html'
    fields = '__all__'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Chapter'
        context['action'] = 'add'
        return context


class LessonCreateView(LoginRequiredMixin, generic.CreateView):
    login_url = 'home'
    model = Lesson
    template_name = 'create.html'
    fields = '__all__'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Lesson'
        context['action'] = 'add'
        return context
# --------------- CREATE ----------------


# --------------- UPDATE ----------------
class BlockUpdateView(LoginRequiredMixin, generic.UpdateView):
    login_url = 'home'
    model = Block
    template_name = 'lesson.html'
    fields = ['type', 'comment', 'media']
    success_url = '/'
    
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = "Update Block"
        context['block'] = self.get_object()
        context['page'] = context['block'].page
        lesson = context['page'].lesson
        context['lesson'] = lesson.order
        chapter = lesson.chapter
        context['chapter'] = chapter.order
        course = chapter.course
        context['course'] = course.slug
        category = course.category
        context['category'] = category.slug

        return context

    def get_success_url(self) -> str:
        context = self.get_context_data()
        return reverse('lesson', kwargs={
            'category_slug': context['category'],
            'course_slug': context['course'],
            'chapter': context['chapter'],
            'lesson': context['lesson'],
        })


    def form_valid(self, form):
        block = self.get_object()
        page = block.page
        # lesson = page.lesson
        # chapter = lesson.chapter
        # course = chapter.course
        # category = course.category
        # page = Page.objects.filter(
        #     lesson__chapter__course__category__slug=self.kwargs['category_slug'],
        #     lesson__chapter__course__slug=self.kwargs['course_slug'],
        #     lesson__chapter__order=self.kwargs['chapter'],
        #     lesson__order=self.kwargs['lesson'],
        # ).first()
        # form.instance.page = page
        last_block = Block.objects.filter(page=page).order_by('-order').first()
        if last_block:
            form.instance.order = last_block.order + 1
        else:
            form.instance.order = 1
        return super().form_valid(form)
    



class CategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Category
    login_url = 'home'
    template_name = 'create.html'
    success_url = '/'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Category'
        context['action'] = 'Update'
        return context

class CourseUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Course
    login_url = 'home'
    template_name = 'create.html'
    success_url = '/'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Course'
        context['action'] = 'Update'    
        return context


class ChapterUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Chapter
    login_url = 'home'
    template_name = 'create.html'
    success_url = '/'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Chapter'
        context['action'] = 'Update'    
        return context


class LessonUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Lesson
    login_url = 'home'
    template_name = 'create.html'
    success_url = '/'    
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Lesson'
        context['action'] = 'Update'    
        return context
# --------------- UPDATE ----------------




# ----------- DELETE ---------------
class BlockDeleteView(LoginRequiredMixin, generic.DeleteView):
    login_url = 'home'
    model = Block
    template_name = 'lesson.html'
    success_url = '/'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = "Delete Block"
        context['block'] = self.get_object()
        context['page'] = context['block'].page
        lesson = context['page'].lesson
        context['lesson'] = lesson.order
        chapter = lesson.chapter
        context['chapter'] = chapter.order
        course = chapter.course
        context['course'] = course.slug
        category = course.category
        context['category'] = category.slug

        return context

    def get_success_url(self) -> str:
        context = self.get_context_data()
        return reverse('lesson', kwargs={
            'category_slug': context['category'],
            'course_slug': context['course'],
            'chapter': context['chapter'],
            'lesson': context['lesson'],
        })



class CategoryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Category
    login_url = 'home'
    template_name = 'create.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Category'
        context['action'] = 'delete'
        return context

class CourseDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Course
    login_url = 'home'
    template_name = 'create.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Course'
        context['action'] = 'delete'    
        return context


class ChapterDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Chapter
    login_url = 'home'
    template_name = 'create.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Chapter'
        context['action'] = 'delete'    
        return context


class LessonDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Lesson
    login_url = 'home'
    template_name = 'create.html'
    success_url = '/'    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Lesson'
        context['action'] = 'delete'    
        return context
# ----------- DELETE ---------------


