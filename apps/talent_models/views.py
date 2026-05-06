from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "status": "TalentFlow çalışıyor 🚀",
        "version": "v1"
    })