from django.db import models

class CreateUpdateTimeField(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Lesson(models.Model):
    name = models.CharField(max_length=25)

    class Meta:
        verbose_name_plural = "Lesson"

    def __str__(self):
        return self.name
    
    # @property
    # def lesson_count(self):
    #     return self.Lesson.count() 
    
class Subject(CreateUpdateTimeField):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE,related_name='Lesson')
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title 

    @property
    def question_count(self):
        return self.question_set.count()
    
class Grade(CreateUpdateTimeField):
    # lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE,related_name='Lesson')
    level = models.CharField(max_length=255)

    def __str__(self):
        return self.level  

class Question(CreateUpdateTimeField):
    SCALE = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,related_name='subject')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE,related_name='grade')
    url = models.URLField(max_length=200)
    difficulty = models.IntegerField(default=1,choices=[(1,"Easy"),(2,"Medium"),(3,"Hard")])
    correct= models.CharField(max_length=1, choices=SCALE)
    number_of_options = models.CharField(max_length=255)


    def __str__(self):
        return self.url      