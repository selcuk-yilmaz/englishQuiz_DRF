from django.urls import path, include
from .views import (
    LessonList,
    GradeList,
    SelectedGradeList,
    SubjectList,
    SelectedSubjectView,
    QuestionViewSet,
    ResultsView,
    LessonDetail,
    GradeDetail,
    SubjectDetail
)
from rest_framework import routers
router=routers.DefaultRouter()

# router.register('results',ResultsGetPost)
router.register(r'questions', QuestionViewSet)



urlpatterns = [
    path('lesson/', LessonList.as_view()),
    path('lesson/<pk>/', LessonDetail.as_view()),
    path('grade/', GradeList.as_view()),
    path('grade/detail/<pk>/', GradeDetail.as_view()),
    path('grade/<str:grade>/', SelectedGradeList.as_view()),
    path('subject/', SubjectList.as_view()),
    path('subject/detail/<pk>/', SubjectDetail.as_view()),
    path("subject/<str:slug>/",SelectedSubjectView.as_view()),
    path('results/', ResultsView.as_view(), name='results'),

    path('',include(router.urls)),
]