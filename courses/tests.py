from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Course, CourseSubscription, Lesson
from users.models import User


class CourseLessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="drf_p1@mail.ru")
        self.course = Course.objects.create(
            name="Python Developer", description="Хороший курс", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title="Начало", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        """Тестирование просмотра курса."""
        url = reverse("courses:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.course.name)

    def test_course_create(self):
        """Тестирование создания курса."""
        url = reverse("courses:course-list")
        data = {
            "name": "Python Developer",
            "description": "Хороший курс",
            "owner": self.user.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_update(self):
        """Тестирование обновления курса."""
        url = reverse("courses:course-detail", args=(self.course.pk,))
        data = {
            "name": "Python Developer",
            "description": "Отличный курс",
            "owner": self.user.pk,
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            data.get(
                "description",
            ),
            "Отличный курс",
        )

    def test_course_delete(self):
        """Тестирование удаления курса."""
        url = reverse("courses:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_list(self):
        """Тестирование вывода списка курсов."""
        url = reverse("courses:course-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "name": self.course.name,
                    "image": None,
                    "description": self.course.description,
                    "owner": self.user.pk,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_lesson_create(self):
        """Тестирование создания урока."""
        url = reverse("courses:lesson-create")
        data = {
            "title": "Начало",
            "video_url": "https://www.youtube.com",
            "course": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_retrieve(self):
        """Тестирование просмотра урока."""
        url = reverse("courses:lesson-retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_update(self):
        """Тестирование обновления урока."""
        url = reverse("courses:lesson-update", args=(self.lesson.pk,))
        data = {
            "title": "Введение",
            "video_url": "https://www.youtube.com",
            "course": self.course.pk,
            "owner": self.user.pk,
        }

        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            data.get(
                "title",
            ),
            "Введение",
        )

    def test_lesson_delete(self):
        """Тестирование удаления урока."""
        url = reverse("courses:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        """Тестирование вывода списка уроков."""
        url = reverse("courses:lesson-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "title": "Начало",
                    "image": None,
                    "description": None,
                    "video_url": None,
                    "course": self.course.pk,
                    "owner": self.user.pk,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class CourseSubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="drf_p1@mail.ru")
        self.course = Course.objects.create(
            name="Python Developer", description="Хороший курс", owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_subscribe_course(self):
        """Тестирование подписки на курс."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("courses:course-subscription"), data={"course_id": self.course.id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            CourseSubscription.objects.filter(
                user=self.user, course=self.course
            ).exists()
        )

    def test_unsubscribe_course(self):
        """Тестирование отписки от курса."""
        CourseSubscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("courses:course-subscription"), data={"course_id": self.course.id}
        )
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            CourseSubscription.objects.filter(
                user=self.user, course=self.course
            ).exists()
        )
