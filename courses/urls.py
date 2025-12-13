from django.urls import path
from rest_framework.routers import SimpleRouter

from courses.apps import CoursesConfig
from courses.views import (CourseViewSet, LessonCreateApiView,
                           LessonDestroyApiView, LessonListApiView,
                           LessonUpdateApiView, LessonRetrieveApiView, CourseSubscriptionView)

app_name = CoursesConfig.name

router = SimpleRouter()
router.register("", CourseViewSet)

urlpatterns = [
    path("lesson/", LessonListApiView.as_view(), name="lesson-list"),
    path("lesson/<int:pk>/", LessonRetrieveApiView.as_view(), name="lesson-retrieve"),
    path("lesson/create/", LessonCreateApiView.as_view(), name="lesson-create"),
    path(
        "lesson/<int:pk>/update/", LessonUpdateApiView.as_view(), name="lesson-update"
    ),
    path(
        "lesson/<int:pk>/delete/", LessonDestroyApiView.as_view(), name="lesson-delete"
    ),
    path("subscribe/", CourseSubscriptionView.as_view(), name="course-subscription"),
]

urlpatterns += router.urls
