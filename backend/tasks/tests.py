from django.test import TestCase
from .scoring import detect_cycle, calculate_priority_for_task
from datetime import date, timedelta

class ScoringUnitTests(TestCase):

    def test_detect_cycle_true(self):
        tasks = [
            {"id": "1", "dependencies": ["2"]},
            {"id": "2", "dependencies": ["1"]},
        ]
        self.assertTrue(detect_cycle(tasks))

    def test_detect_cycle_false(self):
        tasks = [
            {"id": "1", "dependencies": ["2"]},
            {"id": "2", "dependencies": []},
        ]
        self.assertFalse(detect_cycle(tasks))

    def test_priority_overdue_and_defaults(self):
        # overdue task
        t = {
            "id": "a",
            "title": "overdue",
            "due_date": (date.today() - timedelta(days=2)).isoformat(),
            "estimated_hours": 2,
            "importance": 9,
            "dependencies": []
        }
        score, explanation = calculate_priority_for_task(t)
        self.assertIsInstance(score, float)
