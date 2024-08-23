from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ResultOfQuiz, Question
from .serializers import ResultSerializer

class ResultsView(APIView):

    def post(self, request, *args, **kwargs):
        user = request.user
        student_responses = request.data.get('studentResponses', [])

        correct_count = 0
        wrong_count = 0
        empty_count = 10 - len(student_responses)
        wrong_questions = []  # To store the IDs of wrong questions

        for response in student_responses:
            try:
                question = Question.objects.get(id=response['id'])
                
                if response['selectedOption'] == question.correct:
                    correct_count += 1
                else:
                    wrong_count += 1
                    wrong_questions.append({
                        "id": question.id,
                        "subject_name": question.subject.name  # Assuming Question model has subject with a 'name' field
                    })
            except Question.DoesNotExist:
                return Response({"error": "Invalid question ID"}, status=status.HTTP_400_BAD_REQUEST)

        score = correct_count * 10

        if score <= 40:
            status_result = 'poor'
        elif score <= 50:
            status_result = 'medium'
        elif score <= 70:
            status_result = 'normal'
        elif score <= 90:
            status_result = 'good'
        else:
            status_result = 'perfect'

        # Save the result with wrong_questions field
        result = ResultOfQuiz.objects.create(
            name=user,
            correct=str(correct_count),
            wrong=str(wrong_count),
            emty=str(empty_count),
            score=str(score),
            status=status_result,
            wrong_questions=wrong_questions  # Saving wrong question details
        )

        serializer = ResultSerializer(result)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
