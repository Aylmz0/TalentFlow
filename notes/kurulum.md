# 🚀 TalentFlow Intelligence - Kurulum Kılavuzu


**Terminali açın ve proje dizinine gidin, ardından şu komutu çalıştırın:**

```bash
# Linux / macOS / Windows
python -m venv .venv
```

## 2. Sanal Ortamı Aktif Etme

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.\.venv\Scripts\activate.bat
```

**Linux / macOS (Bash/Zsh):**
```bash
source .venv/bin/activate
```

**Linux / macOS (Fish):**
```fish
source .venv/bin/activate.fish
```

> Aktif ettiğinizde terminal satırının başında `(.venv)` ibaresini görmelisiniz.

## 3. Bağımlılıkların Yüklenmesi (requirements.txt)


```bash
pip install -r requirements.txt
```

---

## Önemli Notlar
- Projeyi her açtığınızda sanal ortamı **aktif etmeyi unutmayın**.
- Yeni bir paket yüklediğinizde lütfen `pip freeze > requirements.txt` komutuyla dosyayı güncelleyin (Lead Architect onayı ile).