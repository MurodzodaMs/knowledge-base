from django.db import models





class Category(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self) -> str:
        return self.title

class Course(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.title

class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order = models.SmallIntegerField()
    title = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.title


class Lesson(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    order = models.SmallIntegerField()
    title = models.CharField(max_length=150)


class Page(models.Model):
    # type = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)



class Block(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    order = models.SmallIntegerField()
    type = models.CharField(max_length=50)
    comment = models.TextField(null=True, blank=True)
    media = models.ImageField(null=True, blank=True)

