from django.urls import path, include
from .views import (
    LessonList,
    SubjectList,
    GradeList,
    QuestionViewSet,
)
from rest_framework import routers
router=routers.DefaultRouter()

# router.register('results',ResultsGetPost)
router.register(r'questions', QuestionViewSet)


urlpatterns = [
    path('lesson/', LessonList.as_view()),
    path('subject/', SubjectList.as_view()),
    path('grade/', GradeList.as_view()),
    path('',include(router.urls)),
]