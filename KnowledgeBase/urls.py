from django.urls import path
from .views import *

urlpatterns = [


    # ---- CREATE -----
    path("create_lesson/", LessonCreateView.as_view(), name="create_lesson"),
    path("create_chapter/", ChapterCreateView.as_view(), name="create_chapter"),
    path("create_course/", CourseCreateView.as_view(), name="create_course"),
    path("create_cat/", CategoryCreateView.as_view(), name="create_cat"),
    path(
        "<slug:category_slug>/<slug:course_slug>/<int:chapter>.<int:lesson>/create_block",
        BlockCreateView.as_view(),
        name="create_block",
    ),
    # ---- CREATE -----


    # ----  UPDATE ----
    path("block/<int:pk>/update/", BlockUpdateView.as_view(), name="update_block"),
    path("category/<int:pk>/update/", CategoryUpdateView.as_view(),  name="update_category"),
    path("course/<int:pk>/update/", CourseUpdateView.as_view(), name="update_course"),
    path("chapter/<int:pk>/update/", ChapterUpdateView.as_view(), name="update_chapter"),
    path("lesson/<int:pk>/update/", LessonUpdateView.as_view(), name="update_lesson"),
    # ---- UPDATE -----
    

    # ---- READ -----
    path("", CategoryListView.as_view(), name="home"),
    path(
        "<slug:category_slug>/<slug:course_slug>/<int:chapter>.<int:lesson>/",
        LessonDetailView.as_view(),
        name="lesson",
    ),
    path(
        "<slug:category_slug>/<slug:course_slug>/",
        CourseDetailView.as_view(),
        name="course",
    ),
    path("<slug:slug>/", CategoryDetailView.as_view(), name="category"),
    # ---- READ ----
    

    # ---- DELETE ----
    path("block/<int:pk>/delete/", BlockDeleteView.as_view(), name="delete_block"),
    path("category/<int:pk>/delete/", CategoryDeleteView.as_view(),  name="delete_category"),
    path("course/<int:pk>/delete/", CourseDeleteView.as_view(), name="delete_course"),
    path("chapter/<int:pk>/delete/", ChapterDeleteView.as_view(), name="delete_chapter"),
    path("lesson/<int:pk>/delete/", LessonDeleteView.as_view(), name="delete_lesson"),
    # ---- DELETE ----
]
