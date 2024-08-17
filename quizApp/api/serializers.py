from rest_framework import serializers
from quizApp.models import (
    Lesson,
    Subject,
    Grade,
    Question,
    
)


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            'id',
            'name',
            # 'lesson_count'
        )

class SubjectSerializer(serializers.ModelSerializer):
    question_count=serializers.SerializerMethodField()
    class Meta:
        model = Subject
        fields = (
            'id',
            'lesson',
            'title',
            'question_count',
        )
    def get_question_count(self,obj):
        return Question.objects.filter(subject=obj.id).count()
    
class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = (
            'id',
            'level',
            # 'question_count'
        )

class QuestionSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True,required=False)  # Dosya yüklemeleri için
    subject_title = serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields = ['id', 'subject','subject_title', 'grade', 'url', 'image', 'difficulty', 'correct', 'number_of_options']
        read_only_fields = ['url']

    def get_subject_title(self, obj):
        return obj.subject.title  # subject'in title alanını döndürüyoruz   