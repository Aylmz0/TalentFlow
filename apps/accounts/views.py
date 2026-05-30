from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from core.services.resume_parser import ResumeParser
from apps.talent_models.models import Skill, UserSkill


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
    User = get_user_model()
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        target_role = request.POST.get('target_role', '')

        if password != password_confirm:
            messages.error(request, 'Şifreler eşleşmiyor.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Bu kullanıcı adı zaten alınmış.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Bu e-posta adresi zaten kayıtlı.')
        else:
            user = User.objects.create_user(
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


def cv_upload(request):
    user_model = get_user_model()
    user = request.user
    if not user.is_authenticated:
        user = user_model.objects.first() or user_model.objects.create_user(username="konuk_kullanici", email="guest@talentflow.com")

    if request.method == 'POST':
        cv_file = request.FILES.get('cv_file')
        if not cv_file:
            messages.error(request, 'Lütfen bir PDF dosyası seçin.')
            return redirect('dashboard:skill_tree')

        try:
            # 1. Dosyayı kullanıcı profiline kaydet
            user.cv_file = cv_file
            user.save()

            # 2. PDF'ten metin çıkar ve yetenekleri parse et
            parser = ResumeParser(pdf_path=user.cv_file.path)
            parsed = parser.parse()
            found_skills = parsed['skills']

            # Eski yetenekleri temizle (yeni CV'ye göre temiz başlangıç)
            UserSkill.objects.filter(user=user).delete()

            # 3. Yetenekleri DB'ye kaydet ve kullanıcıyla ilişkilendir
            created_count = 0
            for skill_name in found_skills:
                # Skill ismini baş harfleri büyük olacak şekilde temizle (c++ ve c# hariç)
                if skill_name.lower() in ["c++", "c#"]:
                    clean_name = skill_name.upper()
                elif skill_name.lower() == ".net":
                    clean_name = ".NET"
                else:
                    clean_name = " ".join([w.capitalize() for w in skill_name.split()])

                skill_obj, _ = Skill.objects.get_or_create(
                    name=clean_name,
                    defaults={'category': 'Genel'}
                )
                UserSkill.objects.get_or_create(
                    user=user,
                    skill=skill_obj,
                    defaults={'level': 3}  # Başlangıç seviyesi 3 (orta)
                )
                created_count += 1

            if created_count > 0:
                messages.success(request, f'CV başarıyla analiz edildi! {created_count} yetenek çıkarıldı ve profilinize eklendi.')
            else:
                messages.warning(request, 'CV başarıyla yüklendi ancak içerisinde tanımlı bir yetenek bulunamadı.')

        except Exception as e:
            messages.error(request, f'CV analizi sırasında bir hata oluştu: {str(e)}')

    return redirect('dashboard:skill_tree')

