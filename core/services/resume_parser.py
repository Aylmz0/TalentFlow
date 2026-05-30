import re

from PyPDF2 import PdfReader  # PDF okuma için


class ResumeParser:

    def __init__(self, text=None, pdf_path=None):
        if pdf_path:
            extracted_text = self.extract_text_from_pdf(pdf_path)
            self.text = extracted_text.lower() if extracted_text else ""
        else:
            self.text = text.lower() if text else ""

    def extract_text_from_pdf(self, pdf_path):
        try:
            reader = PdfReader(pdf_path)
            text = ""

            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + " "

            return text

        except Exception as e:
            print("PDF okuma hatası:", e)
            return ""

    def extract_skills(self):
        skills_db = [
            # Diller (Languages)
            "python", "java", "javascript", "typescript", "c++", "c#", "php", "ruby", "go", "rust",
            "swift", "kotlin", "scala", "dart", "r", "julia", "perl", "cobol", "fortran", "haskell",
            "shell", "bash", "powershell", "c", "objective-c", "assembly", "sql", "html", "css",
            "sass", "scss", "less", "lisp", "clojure", "elixir", "erlang", "f#", "groovy", "lua",
            "matlab", "pascal", "prolog", "solidity", "vb.net", "yaml", "json", "xml",
            
            # Backend Frameworks & Runtimes
            "django", "flask", "fastapi", "spring", "spring boot", "node.js", "express", "nestjs",
            "rails", "ruby on rails", "laravel", "symfony", "codeigniter", "asp.net", ".net",
            ".net core", "gin", "fiber", "echo", "actix", "axum", "koa", "hapi", "phoenix",
            "play framework", "struts", "celery", "gunicorn", "uwsgi",
            
            # Frontend Frameworks & Libraries
            "react", "angular", "vue.js", "next.js", "nuxt.js", "svelte", "sveltekit", "ember.js",
            "backbone.js", "jquery", "alpine.js", "bootstrap", "tailwind css", "tailwindcss",
            "material-ui", "mui", "chakra ui", "shadcn/ui", "bulma", "semantic ui", "webpack",
            "vite", "gulp", "grunt", "redux", "mobx", "pinia", "rxjs", "htmx",
            
            # Mobil Geliştirme (Mobile Development)
            "flutter", "react native", "swiftui", "xamarin", "ionic", "cordova", "nativescript",
            
            # Veritabanları (Databases)
            "postgresql", "mysql", "sqlite", "oracle", "mssql", "sql server", "mongodb", "redis",
            "cassandra", "elasticsearch", "mariadb", "dynamodb", "couchdb", "neo4j", "firestore",
            "firebase", "supabase", "clickhouse", "influxdb", "timescaledb", "memcached",
            
            # DevOps, Bulut & Altyapı (DevOps, Cloud & Infrastructure)
            "docker", "kubernetes", "aws", "amazon web services", "azure", "gcp", "google cloud",
            "google cloud platform", "heroku", "vercel", "netlify", "digitalocean", "cloudflare",
            "terraform", "ansible", "jenkins", "github actions", "gitlab ci", "circleci", "argocd",
            "helm", "nginx", "apache", "traefik", "prometheus", "grafana", "elk stack", "datadog",
            "splunk", "linux", "unix", "windows server", "centos", "ubuntu", "debian", "redhat",
            "alpine linux", "ssh", "bash scripting", "openshift",
            
            # Veri Bilimi, Yapay Zeka & ML (Data Science, AI & ML)
            "tensorflow", "pytorch", "keras", "scikit-learn", "sklearn", "pandas", "numpy", "scipy",
            "matplotlib", "seaborn", "plotly", "opencv", "nltk", "spacy", "huggingface", "llm",
            "langchain", "llama-index", "openrouter", "weaviate", "pinecone", "qdrant", "milvus",
            "deep learning", "machine learning", "computer vision", "nlp", "artificial intelligence",
            
            # Big Data & Pipelines
            "hadoop", "spark", "apache spark", "kafka", "rabbitmq", "activemq", "airflow",
            "apache airflow", "nifi", "beam", "dbt", "snowflake", "databricks", "hive", "pig",
            
            # API & İletişim (APIs & Communication)
            "rest", "restful", "graphql", "grpc", "soap", "web sockets", "websockets", "trpc",
            "postman", "swagger", "openapi", "amqp",
            
            # Test & Kalite (Testing & Quality)
            "pytest", "unittest", "junit", "mocha", "jest", "cypress", "selenium", "playwright",
            "puppeteer", "rspec", "cucumber", "sonarqube", "testing library",
            
            # Araçlar & Platformlar (Tools & Platforms)
            "git", "github", "gitlab", "bitbucket", "jira", "confluence", "figma", "adobe xd",
            "photoshop", "illustrator", "unity", "unreal engine", "blender", "docker compose",
            "slack", "trello", "asana", "notion",
            
            # Metodolojiler & Mimari (Methodologies & Architecture)
            "agile", "scrum", "kanban", "devops", "mvc", "microservices", "serverless",
            "clean architecture", "hexagonal architecture", "ddd", "tdd", "bdd", "oop",
            "functional programming", "ci/cd", "rest api", "soap api", "spa", "pwa", "jamstack"
        ]

        found_skills = []

        for skill in skills_db:
            # Kelimenin başlangıç ve bitiş karakterlerine göre regex sınırı belirliyoruz.
            # Böylece c++, c# ve c kelimeleri yanlış eşleşmez (örn: certificate veya architecture içinde c bulunmaz).
            prefix = r'\b' if skill[0].isalnum() else r'(?<!\w)'
            suffix = r'\b' if skill[-1].isalnum() else r'(?!\w)'
            pattern = re.compile(prefix + re.escape(skill) + suffix, re.IGNORECASE)
            
            if pattern.search(self.text):
                found_skills.append(skill)

        return found_skills

    def extract_experience_years(self):
        # Hem Türkçe hem İngilizce deneyim kalıplarını destekleyen arama
        match = re.search(r"(\d+)\s*(yıl|year|yr|sene)", self.text, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return 0

    def parse(self):
        return {
            "skills": self.extract_skills(),
            "experience_years": self.extract_experience_years()
        }