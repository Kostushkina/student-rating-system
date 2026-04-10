from django.test import TestCase
from django.utils import timezone
from .models import Student, Event, Request
from .services.scoring_service import ScoringService


class StudentModelTest(TestCase):
    """Tests for Student model"""

    def test_create_student(self):
        """Test creating a student"""
        student = Student.objects.create(
            full_name="Ivanov Ivan Ivanovich",
            group="PI-23-1",
            email="ivanov@test.ru"
        )
        self.assertEqual(student.full_name, "Ivanov Ivan Ivanovich")
        self.assertEqual(student.group, "PI-23-1")
        self.assertEqual(student.total_points, 0)

    def test_update_total_points(self):
        """Test updating student's total points"""
        student = Student.objects.create(
            full_name="Petrova Anna",
            group="PI-23-1",
            email="petrova@test.ru"
        )
        student.total_points = 25
        student.save()
        self.assertEqual(student.total_points, 25)


class ScoringServiceTest(TestCase):
    """Tests for Scoring service"""

    def setUp(self):
        """Prepare test data"""
        self.student = Student.objects.create(
            full_name="Sidorov Alexey",
            group="IVT-22-2",
            email="sidorov@test.ru"
        )
        self.event = Event.objects.create(
            name="Student Spring",
            level="regional",
            date=timezone.now().date()
        )

    def test_calculate_points_participant_regional(self):
        """Test points calculation for regional participant"""
        points = ScoringService.calculate_points('regional', 'participant')
        self.assertEqual(points, 10)

    def test_calculate_points_winner_national(self):
        """Test points calculation for national winner"""
        points = ScoringService.calculate_points('national', 'winner')
        self.assertEqual(points, 40)

    def test_calculate_points_invalid_role(self):
        """Test points calculation with invalid role"""
        points = ScoringService.calculate_points('regional', 'invalid_role')
        self.assertEqual(points, 0)

    def test_award_points(self):
        """Test awarding points when request is approved"""
        request_obj = Request.objects.create(
            student=self.student,
            event=self.event,
            role='winner'
        )
        points = ScoringService.award_points(request_obj)

        self.assertEqual(points, 25)
        self.assertEqual(request_obj.status, 'approved')
        self.assertEqual(request_obj.points_awarded, 25)

        self.student.refresh_from_db()
        self.assertEqual(self.student.total_points, 25)


class EventFilterTest(TestCase):
    """Tests for Event filtering"""

    def setUp(self):
        """Prepare test data"""
        Event.objects.create(
            name="Freshman Day",
            level="university",
            date=timezone.now().date()
        )
        Event.objects.create(
            name="Student Spring",
            level="regional",
            date=timezone.now().date()
        )
        Event.objects.create(
            name="Russian Olympiad",
            level="national",
            date=timezone.now().date()
        )

    def test_filter_by_level_university(self):
        """Test filtering events by 'university' level"""
        events = Event.objects.filter(level="university")
        self.assertEqual(events.count(), 1)
        self.assertEqual(events.first().name, "Freshman Day")

    def test_filter_by_level_national(self):
        """Test filtering events by 'national' level"""
        events = Event.objects.filter(level="national")
        self.assertEqual(events.count(), 1)
        self.assertEqual(events.first().name, "Russian Olympiad")