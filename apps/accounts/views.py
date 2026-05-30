from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.services.resume_parser import ResumeParser
from apps.talent_models.models import Skill, UserSkill

def index(request):
    return redirect('dashboard:skill_tree')

@login_required
def cv_upload(request):
    if request.method == 'POST':
        cv_file = request.FILES.get('cv_file')
        if not cv_file:
            messages.error(request, 'Lütfen bir PDF dosyası seçin.')
            return redirect('dashboard:skill_tree')

        try:
            # 1. Dosyayı kullanıcı profiline kaydet
            request.user.cv_file = cv_file
            request.user.save()

            # 2. PDF'ten metin çıkar ve yetenekleri parse et
            parser = ResumeParser(pdf_path=request.user.cv_file.path)
            parsed = parser.parse()
            found_skills = parsed['skills']

            # Eski yetenekleri temizle (yeni CV'ye göre temiz başlangıç)
            UserSkill.objects.filter(user=request.user).delete()

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
                    user=request.user,
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

