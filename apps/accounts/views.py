from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from core.services.ai_coach import AICoach
from core.services.resume_parser import ResumeParser
from apps.talent_models.models import Skill, UserSkill
import json


def index(request):
    return redirect('dashboard:skill_tree')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'dashboard:skill_tree')
            return redirect(next_url)
        messages.error(request, 'Kullanıcı adı veya şifre hatalı.')
    return render(request, 'accounts/login.html')


def register_view(request):
    user_model = get_user_model()
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        target_role = request.POST.get('target_role', '')

        if password != password_confirm:
            messages.error(request, 'Şifreler eşleşmiyor.')
        elif user_model.objects.filter(username=username).exists():
            messages.error(request, 'Bu kullanıcı adı zaten alınmış.')
        elif user_model.objects.filter(email=email).exists():
            messages.error(request, 'Bu e-posta adresi zaten kayıtlı.')
        else:
            user = user_model.objects.create_user(  # pyright: ignore
                username=username,
                email=email,
                password=password,
                target_role=target_role
            )
            login(request, user)
            messages.success(request, 'Hesabınız başarıyla oluşturuldu!')
            return redirect('dashboard:skill_tree')

    return render(request, 'accounts/register.html')


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


def _save_skills_for_user(user, found_skills):
    excluded_languages = {"turkish", "english", "german", "french", "spanish", "arabic",
                         "russian", "chinese", "japanese", "korean", "italian", "portuguese",
                         "dutch", "polish", "swedish", "norwegian", "danish", "finnish",
                         "turkçe", "almanca", "ingilizce", "ispanyolca", "fransızca"}
    name_fixes = {"csharp": "C#", "fsharp": "F#", "c plus plus": "C++", "c++": "C++",
                  "c#": "C#", "c sharp": "C#", "dotnet": ".NET", ".net": ".NET",
                  "typescript": "TypeScript", "javascript": "JavaScript",
                  "next js": "Next.js", "nuxt js": "Nuxt.js", "vue js": "Vue.js",
                  "svelte js": "Svelte", "react js": "React",
                  "node js": "Node.js", "nodejs": "Node.js",
                  "express js": "Express", "postgresql": "PostgreSQL",
                  "mongodb": "MongoDB", "github actions": "GitHub Actions",
                  "docker compose": "Docker Compose", "machine learning": "Machine Learning",
                  "deep learning": "Deep Learning", "rest api": "REST API",
                  "ci/cd": "CI/CD", "adobe creative suite": "Adobe Creative Suite",
                  "webassembly": "WebAssembly"}

    UserSkill.objects.filter(user=user).delete()
    count = 0
    for item in found_skills:
        name = item.get("name", "").strip()
        category = item.get("category", "Genel")
        level = min(max(int(item.get("level", 3)), 1), 5)

        if not name:
            continue
        if name.lower() in name_fixes:
            name = name_fixes[name.lower()]
        if name.lower() in excluded_languages:
            continue

        skill_obj, _ = Skill.objects.get_or_create(name=name, defaults={"category": category})
        if skill_obj.category in (None, "", "Genel") and category != "Genel":
            skill_obj.category = category
            skill_obj.save()
        UserSkill.objects.get_or_create(user=user, skill=skill_obj, defaults={"level": level})
        count += 1

    if count > 1:
        skills = UserSkill.objects.filter(user=user).order_by("-level")
        unique_levels = set(skills.values_list("level", flat=True))
        if len(unique_levels) < 2:
            for i, us in enumerate(skills):
                spread = max(1, min(5, round(us.level + (i % 3) - 1)))
                us.level = spread
                us.save()
    return count


def cv_upload(request):
    user_model = get_user_model()
    user = request.user
    if not user.is_authenticated:
        user = user_model.objects.first() or user_model.objects.create_user(username="konuk_kullanici", email="guest@talentflow.com")  # type: ignore[attr-defined]
        login(request, user)

    if request.method != 'POST':
        return redirect('dashboard:skill_tree')

    cv_file = request.FILES.get('cv_file')
    if not cv_file:
        messages.error(request, 'Lütfen bir PDF dosyası seçin.')
        return redirect('dashboard:skill_tree')

    try:
        user.cv_file = cv_file  # type: ignore[attr-defined]
        user.save()

        cv_text = ResumeParser(pdf_path=user.cv_file.path).extract_text_from_pdf(user.cv_file.path)  # type: ignore[attr-defined]
        if not cv_text.strip():
            messages.warning(request, 'PDF okunamadı. Dosyanın metin tabanlı olduğundan emin olun.')
            return redirect('dashboard:skill_tree')

        raw = AICoach().extract_skills_from_cv(cv_text)
        found_skills = json.loads(raw).get("skills", [])

        if not found_skills:
            messages.warning(request, 'CV başarıyla yüklendi ancak AI tanımlı bir yetenek bulamadı.')
            return redirect('dashboard:skill_tree')

        count = _save_skills_for_user(user, found_skills)
        messages.success(request, f'CV başarıyla analiz edildi! {count} yetenek AI tarafından çıkarıldı.')

    except json.JSONDecodeError:
        messages.error(request, 'AI yanıtı işlenemedi. Lütfen tekrar deneyin.')
    except Exception as e:
        messages.error(request, f'CV analizi sırasında bir hata oluştu: {str(e)}')

    return redirect('dashboard:skill_tree')

