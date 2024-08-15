from django.urls import path, include
from .views import (
    LessonList,
    SubjectList,
    GradeList,
    QestionViewSet,
)
from rest_framework import routers
router=routers.DefaultRouter()

# router.register('results',ResultsGetPost)
router.register(r'questions', QestionViewSet)


urlpatterns = [
    path('lesson/', LessonList.as_view()),
    path('subject/', SubjectList.as_view()),
    path('grade/', GradeList.as_view()),
    path('',include(router.urls)),
]