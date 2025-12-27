from typing import Iterable
from django.db import models
from django.utils.text import slugify



class Category(models.Model):
    title = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)
        # Ensure a Page exists for this category, but avoid duplicates
        if not Page.objects.filter(category=self).exists():
            Page.objects.create(category=self)
    
    
    def __str__(self) -> str:
        return self.title



class Course(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['category', 'slug'],
                name='unique_course_slug_per_category'
            )
        ]

    def __str__(self) -> str:
        return self.title



class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order = models.SmallIntegerField()
    title = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title



class Page(models.Model):
    # type = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self) -> str:
        if self.lesson:
            return self.lesson.title
        if self.category:
            return self.category.title
        return 'Page'


class Lesson(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    order = models.SmallIntegerField()
    title = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Ensure a Page exists for this lesson, but avoid duplicates
        if not Page.objects.filter(lesson=self).exists():
            Page.objects.create(lesson=self)
    

    def __str__(self) -> str:
        return self.title





class Block(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    order = models.SmallIntegerField()
    type = models.CharField(max_length=50)
    comment = models.TextField(null=True, blank=True)
    media = models.ImageField(null=True, blank=True)



