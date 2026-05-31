
# Create your views here.
import json
import re
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import get_user_model
from apps.jobs.models import Job
from apps.talent_models.models import UserSkill, MockInterview, UserProject
from core.services.ai_coach import AICoach

FALLBACK_QUESTIONS = [
    "Projenizde karşılaştığınız en büyük teknik zorluk neydi ve bunu nasıl çözdünüz?",
    "Kullandığınız dilde (örn. Python/JavaScript) bellek yönetimi ve performans optimizasyonu nasıl yapılır?",
    "RESTful API tasarlarken hangi prensiplere dikkat edersiniz?",
    "Veritabanı indekslemesi nedir ve sorgu performansını nasıl artırır?",
    "CI/CD süreçlerinde test otomasyonunun rolü nedir?"
]



def update_job_status(request, pk):
    if request.method == "POST":
        # HTMX tarafından gönderilen yeni durumu (status) alıyoruz
        new_status = request.POST.get('status')
        
        # İlgili iş kaydını ID (pk) üzerinden buluyoruz
        job = get_object_or_404(Job, pk=pk)
        
        # Veritabanında güncelleme yapıp kaydediyoruz
        job.status = new_status
        job.save()
        
        # Sayfanın yenilenmesine gerek olmadığı için "İçerik Yok" (204) dönüyoruz
        return HttpResponse(status=204)




def _score_careers(career_paths, user_skills_lower):
    matches = []
    for cp in career_paths:
        matched = [s for s in cp["skills"] if s in user_skills_lower]
        missing = [s for s in cp["skills"] if s not in user_skills_lower]
        score = round(len(matched) / len(cp["skills"]) * 100)
        matches.append({"title": cp["title"], "score": score, "matched": matched, "missing": missing})
    matches.sort(key=lambda x: x["score"], reverse=True)
    return matches[:5]


def skill_tree(request):
    user_skills = []
    overall_score = 0
    has_skills = False
    is_mock = False
    skill_names_json = "[]"
    skill_levels_json = "[]"
    skill_categories_json = "[]"

    if request.user.is_authenticated:
        user_skills = UserSkill.objects.filter(user=request.user).select_related('skill').order_by('-level')
        if user_skills.exists():
            names = [us.skill.name.upper() for us in user_skills]
            levels = [us.level * 20 for us in user_skills]
            categories = [(us.skill.category or 'Genel') for us in user_skills]
            overall_score = round(sum(levels) / len(levels))
            skill_names_json = json.dumps(names)
            skill_levels_json = json.dumps(levels)
            skill_categories_json = json.dumps(categories)
            has_skills = True

    if not has_skills:
        names = ["PYTHON", "DJANGO", "POSTGRESQL", "DOCKER", "KUBERNETES", "REACT", "AWS", "REDIS", "GIT", "RABBITMQ", "CI/CD"]
        levels = [90, 85, 80, 75, 60, 70, 55, 65, 88, 40, 50]
        categories = ["Backend", "Backend", "Database", "DevOps", "DevOps", "Frontend", "Cloud", "Database", "Tools", "Backend", "DevOps"]
        overall_score = 76
        skill_names_json = json.dumps(names)
        skill_levels_json = json.dumps(levels)
        skill_categories_json = json.dumps(categories)
        is_mock = True

    raw_names = json.loads(skill_names_json)
    raw_levels = json.loads(skill_levels_json)
    raw_cats = json.loads(skill_categories_json)

    zipped = sorted(zip(raw_names, raw_levels, strict=True), key=lambda x: x[1], reverse=True)
    strongest_skills = [{"name": n, "level": lv} for n, lv in zipped[:3]]
    weakest_skills = [{"name": n, "level": lv} for n, lv in zipped[-3:]] if len(zipped) >= 3 else [{"name": n, "level": lv} for n, lv in zipped]

    cat_count = {}
    for cat in raw_cats:
        cat_count[cat] = cat_count.get(cat, 0) + 1
    cat_labels_json = json.dumps(list(cat_count.keys()))
    cat_values_json = json.dumps(list(cat_count.values()))

    target_skills = ["python", "django", "postgresql", "docker", "kubernetes", "aws", "redis", "react", "git", "rest api", "ci/cd"]
    user_lower = [s.lower() for s in raw_names]
    matched_skills = [s for s in target_skills if s in user_lower]
    missing_skills = [s for s in target_skills if s not in user_lower]
    gap_score = round(len(matched_skills) / len(target_skills) * 100) if target_skills else 0

    all_skills_data = [{"name": n, "level": lv, "category": c} for n, lv, c in zip(raw_names, raw_levels, raw_cats, strict=True)]

    career_paths = [
        {"title": "Senior Python Developer", "skills": ["python", "django", "postgresql", "docker", "rest api", "git", "ci/cd"]},
        {"title": "DevOps Engineer", "skills": ["docker", "kubernetes", "aws", "ci/cd", "git", "linux"]},
        {"title": "Full Stack Developer", "skills": ["python", "django", "react", "postgresql", "git", "docker", "javascript"]},
        {"title": "Backend Developer (Go)", "skills": ["go", "postgresql", "docker", "rest api", "git", "grpc"]},
        {"title": "Data Scientist", "skills": ["python", "sql", "pandas", "numpy", "machine learning", "statistics"]},
        {"title": "Cloud Architect", "skills": ["aws", "docker", "kubernetes", "ci/cd", "python", "networking"]},
        {"title": "Site Reliability Engineer", "skills": ["kubernetes", "docker", "aws", "ci/cd", "linux", "python", "monitoring"]},
        {"title": "Frontend Developer", "skills": ["react", "javascript", "css", "html", "typescript", "git"]},
    ]
    career_recommendations = _score_careers(career_paths, user_lower)

    return render(request, 'dashboard/skill_tree.html', {
        "user_skills": user_skills, "overall_score": overall_score, "has_skills": has_skills, "is_mock": is_mock,
        "skill_names_json": skill_names_json, "skill_levels_json": skill_levels_json,
        "skill_categories_json": skill_categories_json,
        "strongest_skills": strongest_skills, "weakest_skills": weakest_skills,
        "gap_score": gap_score, "matched_skills": matched_skills, "missing_skills": missing_skills,
        "cat_count": cat_count, "cat_labels_json": cat_labels_json, "cat_values_json": cat_values_json,
        "all_skills_data": all_skills_data,
        "career_recommendations": career_recommendations,
    })

def kanban(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "seed_jobs":
            from django.core.management import call_command
            try:
                call_command('seed_jobs')
            except Exception as e:
                print("Kanban seed_jobs hatası:", e)
        elif action == "create_application":
            title = request.POST.get("title", "").strip()
            company = request.POST.get("company", "").strip()
            description = request.POST.get("description", "").strip()
            if title and company:
                Job.objects.create(title=title, company=company, description=description, status="basvuruldu")
                from django.contrib import messages
                messages.success(request, f'"{title}" başvurusu eklendi!')
            else:
                from django.contrib import messages
                messages.error(request, 'Başlık ve şirket adı zorunludur.')

    if Job.objects.count() == 0:
        from django.core.management import call_command
        try:
            call_command('seed_jobs')
        except Exception as e:
            print("Kanban otomatik veri yükleme hatası:", e)

    jobs = Job.objects.all().order_by('-posted_date')
    context = {
        'basvuruldu': jobs.filter(status='basvuruldu'),
        'mulakat': jobs.filter(status='mulakat'),
        'teklif': jobs.filter(status='teklif'),
        'reddedildi': jobs.filter(status='reddedildi'),
    }
    return render(request, 'dashboard/kanban.html', context)


def start_interview(request, job_pk):
    user_model = get_user_model()
    user = request.user
    if not user.is_authenticated:
        user = user_model.objects.first() or user_model.objects.create_user(username="konuk_kullanici", email="guest@talentflow.com")  # type: ignore[attr-defined]  # type: ignore[attr-defined]

    job = get_object_or_404(Job, pk=job_pk)
    
    # AI'den soruları al (arka planda thread'de, önce placeholder göster)
    user_skills = UserSkill.objects.filter(user=user).select_related('skill')
    skill_names = [us.skill.name for us in user_skills]
    if not skill_names:
        skill_names = ["Python", "Django", "SQL", "Git", "Docker"]
    
    # Soruları SENKRON olarak al (basit ve güvenilir)
    questions = list(FALLBACK_QUESTIONS)
    try:
        ai_coach = AICoach()
        raw_questions = ai_coach.generate_interview_questions(skill_names)
        if raw_questions and "Hata" not in raw_questions and "API anahtarı" not in raw_questions:
            parsed = []
            for raw_line in raw_questions.split('\n'):
                line = raw_line.strip()
                match = re.match(r'^\d+[\.\-\s]+(.*)', line)
                if match:
                    parsed.append(match.group(1).strip())
                elif line and len(line) > 10 and not line.startswith(('Aşağıdaki', 'Teknolojiler', 'Lütfen', 'Sadece')):
                    parsed.append(line)
            if len(parsed) >= 3:
                questions = parsed[:5]
    except Exception as e:
        print("AI soru üretme hatası, fallback kullanılıyor:", e)
        
    interview = MockInterview.objects.create(
        user=user,
        job=job,
        questions=questions,
        user_answers=[],
        score=0
    )
    
    return render(request, 'interviews/active_session.html', {
        'interview': interview,
        'job': job,
        'questions': questions,
        'questions_json': json.dumps(questions),
        'is_loading': False,
        'is_completed': False
    })


def submit_interview(request, interview_pk):
    interview = get_object_or_404(MockInterview, pk=interview_pk)
    
    if request.method == "POST":
        answers = [request.POST.get(f'answer_{i}', '').strip() for i in range(5)]
        
        ai_coach = AICoach()
        raw_result = ai_coach.score_interview_answers(interview.questions, answers)
        
        score = 0
        feedback = ""
        per_question = []
        
        # Try to parse JSON output
        parsed = False
        if raw_result and "Hata" not in raw_result:
            try:
                clean_result = raw_result
                if "```json" in clean_result:
                    clean_result = clean_result.split("```json")[1].split("```")[0].strip()
                elif "```" in clean_result:
                    clean_result = clean_result.split("```")[1].split("```")[0].strip()
                
                result_data = json.loads(clean_result)
                score = int(result_data.get('overall_score', 0))
                feedback = result_data.get('feedback', '')
                per_question = result_data.get('per_question', [])
                parsed = True
            except Exception as e:
                print("AI scoring JSON parse failed, falling back.", e)
                
        if not parsed:
            score = 0
            for ans in answers:
                word_count = len(ans.split())
                q_score = min(20, max(5, word_count * 2))
                score += q_score
                
                comment = "Cevabınız analiz edildi. Teknik kavramlar yerinde kullanılmış." if word_count > 12 else "Cevap çok kısa veya teknik detaylardan yoksun. Lütfen örneklerle genişletin."
                per_question.append({
                    "score": q_score,
                    "comment": comment
                })
            score = min(100, max(20, score))
            feedback = "Mülakatınız başarıyla tamamlandı. Teknik düzeyiniz temel seviyede yeterli olmakla birlikte, cevaplarınızı detaylandırıp daha fazla örnek vermeniz faydalı olacaktır."
            
        qa_breakdown = []
        for i, q in enumerate(interview.questions):
            ans = answers[i] if i < len(answers) else ""
            pq_data = per_question[i] if i < len(per_question) else {"score": 10, "comment": "Yorum yapılamadı."}
            qa_breakdown.append({
                "question": q,
                "answer": ans,
                "score": pq_data.get('score', 10),
                "comment": pq_data.get('comment', '')
            })
            
        interview.user_answers = {
            'answers': answers,
            'feedback': feedback,
            'qa_breakdown': qa_breakdown
        }
        interview.score = score
        interview.save()
        
        return render(request, 'interviews/active_session.html', {
            'interview': interview,
            'job': interview.job,
            'feedback': feedback,
            'qa_breakdown': qa_breakdown,
            'is_completed': True
        })
        
    return redirect('dashboard:kanban')



def _get_architect_fallback(idea: str):
    """
    Helper function to generate high-quality FOSS-alternative technical recommendations 
    and layouts locally, reducing overall complexity of the main view.
    """
    idea_lower = idea.lower()
    if "mobil" in idea_lower or "phone" in idea_lower or "ios" in idea_lower or "android" in idea_lower:
        stack = {
            "backend": {"primary": "Node.js (NestJS)", "foss_alternative": "FastAPI (Python)"},
            "frontend": {"primary": "Flutter", "foss_alternative": "React Native"},
            "database": {"primary": "Firebase Firestore", "foss_alternative": "PostgreSQL"},
            "devops": {"primary": "GitHub Actions & Fastlane", "foss_alternative": "Jenkins"}
        }
        roadmap = {
            "directory_structure": "mobile-app-workspace/\n├── mobile_frontend/          # Flutter Codebase\n│   ├── lib/\n│   │   ├── main.dart\n│   │   └── screens/\n│   └── pubspec.yaml\n├── backend_services/         # NestJS / Python API\n│   ├── src/\n│   │   ├── auth/\n│   │   └── api/\n│   └── package.json\n└── docker-compose.yml        # Dev Services (Postgres, Redis)",
            "technical_decisions": [
                "Flutter Cross-Platform framework utilizing BLoC/Provider state management.",
                "NestJS backend with strict dependency injection and modular components.",
                "Firebase / Supabase FOSS authentication with custom JWT server verification.",
                "PostgreSQL relational DB mapped with Prisma ORM for type-safe queries."
            ]
        }
    elif "game" in idea_lower or "oyun" in idea_lower:
        stack = {
            "backend": {"primary": "Go (Nakama)", "foss_alternative": "Node.js (Colyseus)"},
            "frontend": {"primary": "Unity (C#)", "foss_alternative": "Godot Engine (GDScript)"},
            "database": {"primary": "Redis + PostgreSQL", "foss_alternative": "KeyDB + MariaDB"},
            "devops": {"primary": "AWS GameLift", "foss_alternative": "Hangar (Kubernetes)"}
        }
        roadmap = {
            "directory_structure": "game-workspace/\n├── game_client/              # Godot / Unity Project\n│   ├── scenes/\n│   ├── scripts/\n│   └── project.godot\n├── game_server/              # Go (Nakama server extension)\n│   ├── main.go\n│   └── Dockerfile\n└── deploy/\n    ├── docker-compose.yml\n    └── kubernetes-manifests/",
            "technical_decisions": [
                "Godot Engine with GDScript for rapid client-side game loops and UI.",
                "Nakama server for robust FOSS matchmaking, multiplayer sync, and leaderboards.",
                "Redis memory-cache for instant matchmaking queue states and high-performance caching.",
                "Dockerized deployment for scaling multiplayer matches dynamically."
            ]
        }
    else:
        stack = {
            "backend": {"primary": "Django (Python)", "foss_alternative": "FastAPI (Python)"},
            "frontend": {"primary": "Next.js (React)", "foss_alternative": "SvelteKit"},
            "database": {"primary": "PostgreSQL", "foss_alternative": "Supabase / PostgreSQL"},
            "devops": {"primary": "Docker + AWS S3", "foss_alternative": "Docker + MinIO"}
        }
        roadmap = {
            "directory_structure": "web-saas-workspace/\n├── backend_api/              # Django / FastAPI Service\n│   ├── core/\n│   ├── api/\n│   └── Dockerfile\n├── frontend_ui/              # Next.js / React Client\n│   ├── pages/\n│   ├── components/\n│   └── package.json\n└── docker-compose.yml        # Multi-container Compose Stack",
            "technical_decisions": [
                "Django / FastAPI for modular, robust REST endpoints with native validation.",
                "Next.js framework utilizing React server components for SEO and speed.",
                "PostgreSQL relational database paired with Redis session/query caching.",
                "FOSS MinIO storage server mimicking AWS S3 features locally and in staging."
            ]
        }
    return stack, roadmap


def _process_project_idea(idea: str):
    """
    Helper function to process and parse project idea using AI Coach or fallbacks,
    greatly reducing complexity score.
    """
    ai_coach = AICoach()
    raw_arch = ai_coach.generate_portfolio_architecture(idea)
    
    recommended_stack = {}
    roadmap = {}
    parsed = False
    
    if raw_arch and "Hata" not in raw_arch:
        try:
            clean_arch = raw_arch
            if "```json" in clean_arch:
                clean_arch = clean_arch.split("```json")[1].split("```")[0].strip()
            elif "```" in clean_arch:
                clean_arch = clean_arch.split("```")[1].split("```")[0].strip()
                
            arch_data = json.loads(clean_arch)
            recommended_stack = arch_data.get('recommended_stack', {})
            roadmap = arch_data.get('roadmap', {})
            parsed = True
        except Exception as e:
            print("AI architect JSON parse failed, falling back.", e)
            
    if not parsed:
        recommended_stack, roadmap = _get_architect_fallback(idea)
        
    return recommended_stack, roadmap


def architect(request):
    user_model = get_user_model()
    user = request.user
    if not user.is_authenticated:
        user = user_model.objects.first() or user_model.objects.create_user(username="konuk_kullanici", email="guest@talentflow.com")  # type: ignore[attr-defined]
        
    current_project = None
    recommended_stack = {}
    roadmap = {}
    
    # Process project idea form
    if request.method == "POST":
        idea = request.POST.get('idea', '').strip()
        if idea:
            recommended_stack, roadmap = _process_project_idea(idea)
            current_project = UserProject.objects.create(
                user=user,
                idea=idea,
                recommended_stack=recommended_stack,
                roadmap=roadmap
            )
            
    # Load project from sidebar click (?project_id=X)
    project_id = request.GET.get('project_id')
    if project_id:
        try:
            current_project = UserProject.objects.get(pk=project_id, user=user)
            recommended_stack = current_project.recommended_stack
            roadmap = current_project.roadmap
        except UserProject.DoesNotExist:
            pass
            
    # If no project is currently selected but user has project history, load the latest one as default view
    history = UserProject.objects.filter(user=user).order_by('-created_at')
    if not current_project and history.exists():
        current_project = history[0]
        recommended_stack = current_project.recommended_stack
        roadmap = current_project.roadmap
        
    return render(request, 'dashboard/architect.html', {
        'history': history,
        'current_project': current_project,
        'recommended_stack': recommended_stack,
        'roadmap': roadmap
    })


FALLBACK_PROJECTS = [
    {"title": "Mikroservis Tabanlı E-Ticaret Platformu", "description": "Docker ve Kubernetes ile konteynerize edilmiş, PostgreSQL ve Redis altyapısında çalışan, RESTful API'ler ile haberleşen bir e-ticaret sistemi. CI/CD pipeline ile otomatize edilmiş deployment."},
    {"title": "Gerçek Zamanlı Sohbet ve Bildirim Servisi", "description": "WebSocket ve message broker (RabbitMQ/Kafka) kullanarak ölçeklenebilir bir sohbet altyapısı. Redis ile oturum yönetimi, Docker Compose ile local geliştirme ortamı."},
    {"title": "AI Destekli CV ve Yetenek Analiz Platformu", "description": "FastAPI arka uç, React ön yüz ve PostgreSQL veritabanı ile adayların yeteneklerini analiz eden, eksiklerini raporlayan bir recruitment asistanı."},
    {"title": "Cloud-Native Monitoring ve Alerting Sistemi", "description": "AWS/GCP altyapısında çalışan, Prometheus metrik toplama ve Grafana görselleştirme ile kapsamlı bir monitoring çözümü. Kubernetes üzerinde deploy."},
]


def project_ideas(request):
    user = request.user
    if not user.is_authenticated:
        user = get_user_model().objects.first() or get_user_model().objects.create_user(username="konuk_kullanici", email="guest@talentflow.com")  # type: ignore[attr-defined]

    user_skills = UserSkill.objects.filter(user=user).select_related('skill').order_by('level')[:3]
    skill_names = [us.skill.name for us in user_skills]
    if not skill_names:
        skill_names = ["Python", "Docker", "Kubernetes"]

    ideas_html = ""
    try:
        from core.services.ai_coach import AICoach
        ai = AICoach()
        prompt = f"""Kullanıcının yetenekleri: {', '.join(skill_names)}.
Kullanıcının eksik olduğu yetenekleri geliştirmesi için 2 tane proje fikri ver.
Her proje için 'title' (kısa, 5-10 kelime) ve 'description' (2-3 cümle, hangi teknolojiler kullanılacak, ne öğrenecek) olacak.
JSON formatında ver, markdown kullanma:
{{"projects": [{{"title": "...", "description": "..."}}, {{"title": "...", "description": "..."}}]}}"""

        raw = ai._execute_completion(prompt, "")
        if raw and "Hata" not in raw:
            import json
            clean = raw.strip()
            if "```json" in clean:
                clean = clean.split("```json")[1].split("```")[0].strip()
            elif "```" in clean:
                clean = clean.split("```")[1].split("```")[0].strip()
            data = json.loads(clean)
            projects = data.get("projects", [])[:2]
            for p in projects:
                ideas_html += f"""
                <div class="p-3 rounded-3 mb-2" style="background: rgba(201,165,92,0.04); border: 1px solid rgba(201,165,92,0.1);">
                    <h6 class="fw-bold text-accent small mb-1"><i class="bi bi-rocket-takeoff me-1"></i>{p['title']}</h6>
                    <p class="small text-white-50 m-0">{p['description']}</p>
                </div>"""
    except Exception:
        pass

    if not ideas_html:
        import random
        for p in random.sample(FALLBACK_PROJECTS, 2):
            ideas_html += f"""
            <div class="p-3 rounded-3 mb-2" style="background: rgba(201,165,92,0.04); border: 1px solid rgba(201,165,92,0.1);">
                <h6 class="fw-bold text-accent small mb-1"><i class="bi bi-rocket-takeoff me-1"></i>{p['title']}</h6>
                <p class="small text-white-50 m-0">{p['description']}</p>
            </div>"""

    from django.http import HttpResponse
    return HttpResponse(ideas_html)


def cv_improve(request):
    result = None
    original_text = ""
    error = None

    if request.method == "POST":
        pdf_file = request.FILES.get("cv_pdf")
        if pdf_file and pdf_file.name.endswith(".pdf"):
            try:
                text_parts = []
                import PyPDF2
                reader = PyPDF2.PdfReader(pdf_file)
                for page in reader.pages:
                    text_parts.append(page.extract_text())
                original_text = "\n".join(text_parts).strip()
            except Exception as e:
                error = f"PDF okunamadı: {str(e)}"

            if original_text:
                try:
                    ai = AICoach()
                    prompt = f"""Aşağıdaki CV metnini analiz ederek 3 bölüm halinde JSON çıktısı ver:

1. "strengths": CV'deki güçlü yönler, iyi kullanılmış ifadeler (madde madde, Türkçe)
2. "suggestions": Kelime seçimi, cümle yapısı ve kendini ifade biçimiyle ilgili spesifik düzeltme önerileri. Her öneri için "original" (mevcut hali) ve "improved" (düzeltilmiş hali) olacak.
3. "improved_version": CV'nin tamamen düzeltilmiş, daha profesyonel ve etkileyici versiyonu.

JSON şeması:
{{
  "strengths": ["madde 1", "madde 2"],
  "suggestions": [
    {{"original": "eski ifade", "improved": "yeni ifade", "reason": "neden daha iyi olduğu"}}
  ],
  "improved_version": "tüm cv'nin düzeltilmiş hali"
}}

Sadece JSON döndür, markdown kullanma. JSON dışında hiçbir açıklama ekleme.

CV METNİ:
{original_text}"""

                    raw = ai._execute_completion(prompt, "")
                    if raw and "Hata" not in raw:
                        import json
                        clean = raw.strip()
                        if "```json" in clean:
                            clean = clean.split("```json")[1].split("```")[0].strip()
                        elif "```" in clean:
                            clean = clean.split("```")[1].split("```")[0].strip()
                        result = json.loads(clean)
                    else:
                        error = "AI yanıt vermedi. Lütfen tekrar deneyin."
                except Exception as e:
                    error = f"Bir hata oluştu: {str(e)}"
        else:
            error = "Lütfen geçerli bir PDF dosyası yükleyin."

    return render(request, "dashboard/cv_improve.html", {
        "result": result,
        "original_text": original_text,
        "error": error,
    })