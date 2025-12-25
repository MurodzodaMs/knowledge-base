from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('<slug:slug>/', CategoryPageView.as_view(), name='category'),
    path('<slug:category_slug>/<slug:course_slug>/', CoursePageView.as_view(), name='course')
    path('<slug:category_slug>/<slug:course_slug>/<int:chapter>.<int:chapter>', CoursePageView.as_view(), name='lesson')
]