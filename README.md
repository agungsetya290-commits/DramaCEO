# 🎬 Kantor Drama AI

Otomatisasi pembuatan naskah, alur video, dan prompt visual bertema **"Orang Diremehkan / Undercover Boss Jadi Kaya"** untuk YouTube Shorts, Instagram Reels, dan TikTok.

---

## 👥 Tim Agent Virtual

1. **Rendra (Konseptor Cerita)**: Meriset premis drama balas dendam & orang diremehkan dengan setting realistis (lobi kantor elit, dealer mobil, reuni hotel).
2. **Karin (Penulis Naskah & Hook)**: Menulis naskah dialog 60 detik dengan hook penghinaan 3 detik pertama, eskalasi konflik, petunjuk rahasia, plot twist, dan cliffhanger.
3. **Gilang (Visual Director)**: Membuat prompt visual sinematik (Bahasa Inggris) untuk Kling AI, Runway Gen-3, atau Midjourney lengkap dengan efek pergerakan kamera dan SFX audio.
4. **Vina (Sosmed & Distribusi)**: Membuat judul clickbait, caption Reels/TikTok pemancing debat di komentar, dan hashtag trending.

---

## 🚀 Cara Menjalankan

### 1. Jalankan Manual di Lokal:
```bash
# Pastikan sudah mengisi API Key Gemini
$env:GEMINI_API_KEY="AIzaSy..."
python agents/drama_office.py
```
Hasil naskah, prompt visual, dan caption akan otomatis tersimpan rapi di folder `data/`.

### 2. Jalankan Otomatis di GitHub Actions:
- Masukkan Secret `GEMINI_API_KEY` di repo GitHub (**Settings -> Secrets and variables -> Actions**).
- Workflow `.github/workflows/drama_shift.yml` akan berjalan otomatis setiap hari atau bisa dijalankan manual lewat tombol **Run workflow**.
