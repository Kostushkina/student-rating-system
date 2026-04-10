from ..models import Request


class ScoringService:
    """Сервис для расчета баллов"""

    POINTS_RULES = {
        'university': {'participant': 5, 'winner': 15, 'organizer': 10},
        'regional': {'participant': 10, 'winner': 25, 'organizer': 15},
        'national': {'participant': 20, 'winner': 40, 'organizer': 25},
    }

    @staticmethod
    def calculate_points(event_level: str, role: str) -> int:
        """Рассчитывает баллы на основе уровня мероприятия и роли"""
        try:
            return ScoringService.POINTS_RULES[event_level][role]
        except KeyError:
            print(f"ERROR: No points rule for level={event_level}, role={role}")
            return 0

    @staticmethod
    def award_points(request_obj: Request) -> int:
        """Начисляет баллы студенту и возвращает количество начисленных баллов"""
        points = ScoringService.calculate_points(
            request_obj.event.level,
            request_obj.role
        )
        request_obj.points_awarded = points
        request_obj.status = 'approved'
        request_obj.save()

        student = request_obj.student
        student.total_points += points
        student.save()

        return points