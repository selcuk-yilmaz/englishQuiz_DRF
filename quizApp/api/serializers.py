from rest_framework import serializers
from quizApp.models import (
    Lesson,
    Subject,
    Grade,
    Question,
    ResultOfQuiz,
    
)


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            'id',
            'name',
        )
class GradeSerializer(serializers.ModelSerializer):
    question_count=serializers.SerializerMethodField()

    class Meta:
        model = Grade
        fields = (
            'id',
            'level',
            'question_count'
        )
    def get_question_count(self,obj):
        return Question.objects.filter(url=obj.id).count()   
class SubjectSerializer(serializers.ModelSerializer):
    question_count=serializers.SerializerMethodField()
    lesson_name = serializers.SerializerMethodField()
    grade_level = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = (
            'id',
            'lesson_name',
            'grade_level',
            'title',
            'question_count',
        )

    def get_lesson_name(self, obj):
        return obj.lesson.name   
    def get_grade_level(self, obj):
        return obj.grade.level   
    def get_question_count(self,obj):
        return Question.objects.filter(subject=obj.id).count()

class QuestionSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True,required=False)  # Dosya yüklemeleri için
    # grade_level = serializers.SerializerMethodField()
    subject_title = serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields = ['id', 'subject','subject_title','url','difficulty', 'correct', 'number_of_options', 'image']
        read_only_fields = ['url']

    def get_lesson_name(self, obj):
        return obj.lesson.name  # subject'in title alanını döndürüyoruz  
    def get_grade_level(self, obj):
        return obj.grade.level  # subject'in title alanını döndürüyoruz  
    def get_subject_title(self, obj):
        return obj.subject.title  # subject'in title alanını döndürüyoruz 
    
class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultOfQuiz
        fields = (
            'id',
            'name',
            'correct',
            'wrong',
            'emty',
            'score',
            'status',
            'wrong_questions'
        )    