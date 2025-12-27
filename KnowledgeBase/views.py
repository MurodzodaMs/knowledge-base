from .models import *
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse


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
        context['categories'] = Category.objects.all()
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

        context['categories'] = Category.objects.all()
        context['chapters'] = Chapter.objects.filter(course=course)
        context['lessons'] = Lesson.objects.filter(chapter=chapter)
        context['page'] = Page.objects.get(lesson=lesson)
        context['blocks'] = Block.objects.filter(page=context['page'])
        try:
            context['group'] = self.request.user.groups.first().name
        except:
            pass
        return context
# ---------- DETAIL ------------


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
        context['categories'] = Category.objects.all()
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
    queryset = Category.objects.all()
    template_name = 'create.html'
    fields = '__all__'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Category'
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
        return context
# --------------- CREATE ----------------


# --------------- UPDATE ----------------

class BlockUpdateView(LoginRequiredMixin, generic.UpdateView):
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
        context['title'] = 'Update Block'
        context['page'] = self.object.page
        return context


class BlockDeleteView(LoginRequiredMixin, generic.TemplateView):
    login_url = 'home'
    template_name = 'lesson.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Delete Block'
#         context['categories'] = Category.objects.all()
#         context['course'] = Course.objects.filter(
#             slug=self.kwargs['course_slug']).first()
#         context['chapters'] = Chapter.objects.filter(course=context['course'])
#         context['lessons'] = Lesson.objects.filter(
#             chapter__in=context['chapters'])
#         context['page'] = Page.objects.get(
#             lesson__chapter__course__category__slug=self.kwargs['category_slug'],
#             lesson__chapter__course__slug=self.kwargs['course_slug'],
#             lesson__chapter__order=self.kwargs['chapter'],
#             lesson__order=self.kwargs['lesson'],
#         )
#         context['blocks'] = Block.objects.filter(page=context['page'])
#         context['group'] = self.request.user.groups.first().name
#         return context

#     def get_success_url(self):
#         return reverse('lesson', kwargs={
#             'category_slug': self.kwargs['category_slug'],
#             'course_slug': self.kwargs['course_slug'],
#             'chapter': self.kwargs['chapter'],
#             'lesson': self.kwargs['lesson'],
#         })


class BlockDeleteActionView(LoginRequiredMixin, generic.DeleteView):
    login_url = 'home'
    model = Block
    template_name = 'lesson.html'

#     def get_success_url(self):
#         page = self.object.page
#         return reverse('lesson', kwargs={
#             'category_slug': page.lesson.chapter.course.category.slug,
#             'course_slug': page.lesson.chapter.course.slug,
#             'chapter': page.lesson.chapter.order,
#             'lesson': page.lesson.order,
#         })
