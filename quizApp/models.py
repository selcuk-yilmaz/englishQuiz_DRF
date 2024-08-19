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
    
class Grade(CreateUpdateTimeField):
    level = models.IntegerField(default=1)


    def __str__(self):
        return str(self.level) 
    
    @property
    def question_count(self):
        return self.question_set.count()     
class Subject(CreateUpdateTimeField):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE,related_name='Lesson')
    grade = models.ForeignKey(Grade, default=1,on_delete=models.CASCADE,related_name='Grade')
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title 

    @property
    def question_count(self):
        return self.question_set.count()
    


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
    difficulty = models.CharField(max_length=255,default="Easy",choices=[("Easy","Easy"),("Medium","Medium"),("Hard","Hard")])
    correct= models.CharField(max_length=1, choices=SCALE)
    number_of_options = models.CharField(max_length=255)


    def __str__(self):
        return self.url   
       