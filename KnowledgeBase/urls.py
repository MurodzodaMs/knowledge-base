from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('create_lesson/', LessonCreateView.as_view(), name='create_lesson'),
    path('create_chapter/', ChapterCreateView.as_view(), name='create_chapter'),
    path('create_course/', CourseCreateView.as_view(), name='create_course'),
    path('create_cat/', CategoryCreateView.as_view(), name='create_cat'),
    path('<slug:category_slug>/<slug:course_slug>/<int:chapter>.<int:lesson>/', LessonView.as_view(), name='lesson'),
    path('<slug:category_slug>/<slug:course_slug>/', CoursePageView.as_view(), name='course'),
    path('<slug:slug>/', CategoryPageView.as_view(), name='category'),
]