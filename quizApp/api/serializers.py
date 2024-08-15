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
    class Meta:
        model = Subject
        fields = (
            'id',
            'lesson',
            'title',
            # 'question_count'
        )

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

    class Meta:
        model = Question
        fields = ['id', 'subject', 'grade', 'url', 'image', 'difficulty', 'correct', 'number_of_options']
        read_only_fields = ['url']