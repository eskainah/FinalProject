from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .models import Course, Enrollment
from rest_framework.test import APIClient


User = get_user_model()

class CourseViewSetTests(APITestCase):

    def setUp(self):
        # Create users
        self.admin_user = User.objects.create_user(
            username='admin', password='adminpassword', role='admin'
        )
        self.teacher_user = User.objects.create_user(
            username='teacher', password='teacherpassword', role='teacher'
        )
        self.student_user = User.objects.create_user(
            username='student', password='studentpassword', role='student'
        )
        
        # Generate tokens for each user
        self.admin_token = Token.objects.create(user=self.admin_user)
        self.teacher_token = Token.objects.create(user=self.teacher_user)
        self.student_token = Token.objects.create(user=self.student_user)

        # Create a course
        self.course = Course.objects.create(
            course_code='CSC101', 
            course_name='Computer Science 101',
            credit_hours=3,
            class_lab='CL-1',
            day='Monday',
            start_time='09:00:00',
            end_time='12:00:00',
            instructor_id=self.teacher_user
        )

    def test_admin_create_course(self):
        url = '/api/courses/create_course/'
        data = {
            'course_code': 'CSC102',
            'course_name': 'Computer Science 102',
            'credit_hours': 3,
            'class_lab': 'CL-2',
            'day': 'Tuesday',
            'start_time': '10:00:00',
            'end_time': '13:00:00',
            'instructor_id_input': self.teacher_user.custom_id,
            'semester': 'Fall 2024',
        }
        # Use admin token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)  # Verify a new course has been created

    def test_teacher_create_course_forbidden(self):
        url = '/api/courses/create_course/'
        data = {
            'course_code': 'CSC103',
            'course_name': 'Computer Science 103',
            'credit_hours': 3,
            'class_lab': 'CL-3',
            'day': 'Wednesday',
            'start_time': '14:00:00',
            'end_time': '17:00:00',
            'instructor_id_input': self.teacher_user.custom_id,
            'semester': 'Fall 2024',
        }
        # Use teacher token (should be forbidden for teachers to create a course)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.teacher_token.key)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_view_course(self):
        url = f'/api/courses/retrieve_course/{self.course.course_code}/'
        # Use student token (students can only view their enrolled courses, assume student is enrolled)
        Enrollment.objects.create(student_id=self.student_user, course_code=self.course)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.student_token.key)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['course_name'], self.course.course_name)

    def test_teacher_view_assigned_courses(self):
        url = '/api/courses/teacher_courses/'
        # Teacher can view their assigned courses
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.teacher_token.key)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)  # Teacher should have at least one course

    def test_admin_delete_course(self):
        url = f'/api/courses/delete_course/{self.course.course_code}/'
        # Admin can delete courses
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)  # Verify the course was deleted

    def test_teacher_enroll_student_in_course(self):
        url = '/api/courses/enroll-student/'
        data = {
            'student_id': self.student_user.custom_id,
            'course_codes': ['CSC101'],
        }
        # Teacher can enroll a student
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.teacher_token.key)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Enrollment.objects.count(), 1)  # Verify enrollment was created

    def test_admin_delete_enrollment(self):
        # First enroll the student
        enrollment = Enrollment.objects.create(student_id=self.student_user, course_code=self.course)
        url = f'/api/courses/delete-enrollment/{self.course.course_code}/'
        data = {'student_id': self.student_user.custom_id}

        # Admin can delete an enrollment
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.delete(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Enrollment.objects.count(), 0)  # Verify the enrollment was deleted

