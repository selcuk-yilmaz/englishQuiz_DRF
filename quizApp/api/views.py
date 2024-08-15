from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from quizApp.models import (
    Lesson,
    Subject,
    Grade,
    Question,
    
)
from .serializers import (
    LessonSerializer,
    SubjectSerializer,
    GradeSerializer,
    QuestionSerializer

)


class LessonList(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class SubjectList(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class GradeList(generics.ListAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import cloudinary.uploader


class QestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Cloudinary'ye yükle
        upload_result = cloudinary.uploader.upload(
            serializer.validated_data['image'],
            folder="english_quiz",
            use_filename=True
        )

        # print("yüklenen resim",upload_result)
        # Modeli kaydet
        question = Question.objects.create(
            subject=serializer.validated_data['subject'],
            grade=serializer.validated_data['grade'],
            url=upload_result['secure_url'],
            # image_id=upload_result['public_id']
            difficulty=serializer.validated_data['difficulty'],
            correct=serializer.validated_data['correct'],
            number_of_options=serializer.validated_data['number_of_options'],

        )
        
        return Response(QuestionSerializer(question).data, status=status.HTTP_201_CREATED)
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()        