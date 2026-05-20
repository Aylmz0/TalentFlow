from django.http import JsonResponse
from core.services.ai_coach import AICoach


def ai_coach_view(request):
    coach = AICoach()

    skills = ["python", "django", "docker"]

    questions = coach.generate_mock_interview(skills)
    stack = coach.suggest_portfolio_stack(skills)

    return JsonResponse({
        "questions": questions,
        "tech_stack": stack
    })