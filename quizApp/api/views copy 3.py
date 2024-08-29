
from quizApp.models import (
    Lesson,
    Subject,
    Grade,
    Question,
    ResultOfQuiz,
)
from .serializers import (
    LessonSerializer,
    SubjectSerializer,
    GradeSerializer,
    QuestionSerializer,
    ResultSerializer
)
from .pagination import MyLimitOffsetPagination

#  BELOW İS Lesson Grade Subject listeler
from rest_framework import generics
class LessonList(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
class GradeList(generics.ListCreateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
class SubjectList(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

#  BELOW İS QuestionViewSet
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import cloudinary.uploader


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        print("req data",request.data)

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors) 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.is_valid(raise_exception=True)
        print("serializer url", serializer.validated_data['url'])
        print("serializer image", serializer.validated_data['image'])

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
            # grade=serializer.validated_data['grade'],
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

class SelectedGradeList(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class =  SubjectSerializer 
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
       grade = self.kwargs['grade']
    #    print(subject)
       return Subject.objects.filter(grade=grade)     
# views.py
class SelectedSubjectView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer 
    pagination_class = MyLimitOffsetPagination
  

    def get_queryset(self):
        subject_slug = self.kwargs['slug']
        return Question.objects.filter(subject__title=subject_slug)
    
#  BELOW IS ResultsView without save db
from rest_framework.views import APIView

class ResultsView(APIView):

    def post(self, request, *args, **kwargs):
        user = request.user
        student_responses = request.data.get('studentResponses', [])

        correct_count = 0
        wrong_count = 0
        empty_count = 10- len(student_responses)
        wrong_questions = []
        correct_questions = []

        for response in student_responses:
            try:
                question = Question.objects.get(id=response['id'])
                
                if response['selectedOption'] == question.correct:
                    correct_count += 1
                    correct_questions.append({
                    "id": question.id,
                    "subject_title": question.subject.title,
                    "url": question.url,
                    "correct": question.correct,
                    "difficulty":question.difficulty
                    })
                else:
                    wrong_count += 1
                    wrong_questions.append({
                    "id": question.id,
                    "subject_title": question.subject.title,
                    "url": question.url,
                    "correct": question.correct,
                    "difficulty":question.difficulty
                    })
            except Question.DoesNotExist:
                return Response({"error": "Invalid question ID"}, status=status.HTTP_400_BAD_REQUEST)        

        score = correct_count * 10

        # Determine the status based on the score
        if score <= 40:
            status_result = 'bad'
        elif score <= 50:
            status_result = 'poor'
        elif score <= 70:
            status_result = 'good'
        elif score <= 90:
            status_result = 'better'
        else:
            status_result = 'perfect'

        # Return the response with full question details for wrong and empty questions
        return Response({
            "user": str(user),
            "correct": correct_count,
            "wrong": wrong_count,
            "empty": empty_count,
            "score": score,
            "status": status_result,
            "wrong_questions": wrong_questions,
            "correct_questions": correct_questions 
        }, status=status.HTTP_200_OK)
