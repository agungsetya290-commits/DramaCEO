#!/usr/bin/env python3
"""Kantor Konten Universal - Multi-Agent Factory untuk Semua Niche:
1. Drama Kehidupan / Undercover Boss / Karma
2. Horor & Misteri Nusantara / Urban Legend (Jeda Horor)
3. Dark History / Misteri Sejarah / Konspirasi
4. Fakta Unik & Sains Mengejutkan
5. Finansial / Cerita Sukses & Bisnis
"""
import json, os, sys, time, random, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
KEY = os.environ.get("GEMINI_API_KEY", "").strip()
BASE = "https://generativelanguage.googleapis.com/v1beta"
WIB = timezone(timedelta(hours=7))
UA = "Mozilla/5.0 (compatible; KantorKontenAI/2.0)"

MODEL_PREF = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash", "flash"]

# Database konfigurasi niche
NICHE_PROFILES = {
    "drama": {
        "nama": "Drama & Balas Dendam",
        "tema": "Orang diremehkan, pura-pura miskin, ternyata konglomerat/pemilik asli yang menyamar.",
        "gaya_hook": "Penghinaan status sosial atau pakaian di 3 detik pertama.",
        "visual_style": "Cinematic Korean/Indonesian corporate drama, high contrast, warm and cold rim lighting.",
        "sound_style": "Dramatic orchestral strings, loud glass breaking, tense bass drops."
    },
    "horor": {
        "nama": "Horor & Misteri",
        "tema": "Kisah mistis nyata, urban legend nusantara, pantangan ritual yang dilanggar, teror malam.",
        "gaya_hook": "Pertanyaan mencekam atau bisikan larangan kematian di 3 detik pertama.",
        "visual_style": "Dark atmospheric, 35mm grainy vintage footage, foggy midnight, flickering dim lights.",
        "sound_style": "Eerie binaural whisper, ticking grandfather clock, creeping heartbeat, sudden jump-scare bass."
    },
    "sejarah_gelap": {
        "nama": "Sejarah Gelap & Konspirasi",
        "tema": "Peristiwa mengerikan masa lalu yang dirahasiakan, eksperimen terlarang, tokoh misterius.",
        "gaya_hook": "Fakta terlarang yang disembunyikan pemerintah/sejarah resmi.",
        "visual_style": "Retro archive documentary, faded sepia photos, newspaper clippings, forensic evidence aesthetic.",
        "sound_style": "Typewriter sound, static radio frequency, deep documentary cinematic brass."
    },
    "sukses_bisnis": {
        "nama": "Kisah Sukses & Bisnis Gila",
        "tema": "Strategi licik miliarder, jatuh bangun bangkrut hingga punya ribuan cabang, perang brand dunia.",
        "gaya_hook": "Pemberitahuan nominal uang fantastis atau cara gila brand mengalahkan lawannya.",
        "visual_style": "High-end luxury corporate, sleek graphics, dynamic chart overlays, modern neon accents.",
        "sound_style": "Energetic modern beat, subtle cash register chime, inspiring build-up."
    }
}


def http(url, data=None, timeout=50):
    req = urllib.request.Request(url, data=data, headers={
        "User-Agent": UA, "Content-Type": "application/json", "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def pick_models():
    override = os.environ.get("GEMINI_MODEL", "").strip()
    if override:
        return [override]
    try:
        body = json.loads(http(f"{BASE}/models?key={KEY}&pageSize=100"))
        names = [m.get("name", "").replace("models/", "") for m in body.get("models", [])
                 if "generateContent" in m.get("supportedGenerationMethods", [])]
        ranked = []
        for pref in MODEL_PREF:
            for n in names:
                if pref in n.lower() and n not in ranked:
                    ranked.append(n)
        return (ranked or names)[:3]
    except Exception as e:
        print(f"[model] gagal list model: {e}", file=sys.stderr)
        return ["gemini-1.5-flash"]


def ask(models, prompt, retries=2):
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.85,
            "maxOutputTokens": 8192,
            "responseMimeType": "application/json"
        },
    }).encode()
    last = None
    for model in models:
        for i in range(retries):
            try:
                body = json.loads(http(f"{BASE}/models/{model}:generateContent?key={KEY}", payload))
                txt = body["candidates"][0]["content"]["parts"][0]["text"].strip()
                if txt.startswith("```json"):
                    txt = txt[7:]
                if txt.startswith("```"):
                    txt = txt[3:]
                if txt.endswith("```"):
                    txt = txt[:-3]
                return json.loads(txt.strip()), model
            except urllib.error.HTTPError as e:
                last = f"HTTP {e.code} ({model})"
                print(f"[gemini] {last}: {e.read().decode()[:200]}", file=sys.stderr)
                if e.code in (429, 500, 502, 503) and i < retries - 1:
                    time.sleep(8 * (i + 1))
                    continue
                break
            except Exception as e:
                last = f"{type(e).__name__} ({model}): {e}"
                print(f"[gemini] {last}", file=sys.stderr)
                if i < retries - 1:
                    time.sleep(6)
                    continue
                break
    raise RuntimeError(f"Semua model gagal; terakhir: {last}")


def main():
    now = datetime.now(WIB)
    tanggal = now.strftime("%Y-%m-%d")
    jam = now.strftime("%H:%M WIB")

    if not KEY:
        print("GEMINI_API_KEY belum disetel!", file=sys.stderr)
        sys.exit(1)

    # Pilih Niche: Bisa dari environment variable NICHE, atau diacak otomatis tiap shift
    target_niche = os.environ.get("NICHE", "").strip().lower()
    if target_niche not in NICHE_PROFILES:
        target_niche = random.choice(list(NICHE_PROFILES.keys()))

    niche = NICHE_PROFILES[target_niche]
    models = pick_models()
    print(f"[{jam}] Kantor Konten AI memproduksi niche: {niche['nama']} (Model: {models[0]})")

    # 1. Agent Rendra: Konseptor Ide Berdasarkan Niche Terpilih
    rendra_prompt = f"""Kamu Rendra, creative researcher ahli merancang konten viral untuk YouTube Shorts, Reels, dan TikTok.
Niche yang diproduksi saat ini: {niche['nama']}
Tema: {niche['tema']}
Gaya Hook: {niche['gaya_hook']}

Buat 1 ide cerita/topik paling adiktif dengan retensi penonton tinggi.
Format JSON:
{{
  "niche": "{target_niche}",
  "judul": "Judul bombastis yang memancing klik dan rasa penasaran",
  "latar": "Setting lokasi / era kejadian",
  "karakter_atau_tokoh": "Nama dan peran karakter utama",
  "inti_konflik": "Pemicu utama ketegangan",
  "plot_twist": "Pembalikan cerita yang tidak terduga di akhir"
}}"""
    ide, m = ask(models, rendra_prompt)
    print(f"[Rendra] Ide selesai: {ide.get('judul')}")

    # 2. Agent Karin: Penulis Naskah Audio & Timecode 60 Detik
    karin_prompt = f"""Kamu Karin, scriptwriter spesialis retensi penonton tinggi di YouTube Shorts/Reels.
Berdasarkan ide dari Rendra ini:
{json.dumps(ide, ensure_ascii=False)}

Gaya hook wajib: {niche['gaya_hook']}

Tulis naskah video 60 detik vertikal (9:16) yang membagi tensi secara proporsional:
- 00:00-00:03 Hook tajam pemancing emosi
- 00:03-00:20 Eksplorasi masalah / eskalasi ketegangan
- 00:20-00:40 Petunjuk misterius / titik balik
- 00:40-00:52 Klimaks pembalasan / pengungkapan fakta
- 00:52-00:60 Call-To-Action (ajak komen / follow untuk part 2)

Format JSON:
{{
  "hook_3_detik": "Kalimat pembuka 3 detik pertama",
  "teks_voiceover_lengkap": "Teks narasi utuh tinggal dicopy ke ElevenLabs atau TTS",
  "scenes": [
    {{"timecode": "00:00-00:06", "narasi": "...", "teks_di_layar": "..."}},
    {{"timecode": "00:06-00:15", "narasi": "...", "teks_di_layar": "..."}},
    {{"timecode": "00:15-00:28", "narasi": "...", "teks_di_layar": "..."}},
    {{"timecode": "00:28-00:42", "narasi": "...", "teks_di_layar": "..."}},
    {{"timecode": "00:42-00:52", "narasi": "...", "teks_di_layar": "..."}},
    {{"timecode": "00:52-00:60", "narasi": "...", "teks_di_layar": "..."}}
  ]
}}"""
    naskah, m = ask(models, karin_prompt)
    print("[Karin] Naskah selesai")

    # 3. Agent Gilang: Creative Director (Visual Prompts & SFX)
    gilang_prompt = f"""Kamu Gilang, visual & sound director untuk video faceless/motion.
Naskah:
{json.dumps(naskah.get('scenes', []), ensure_ascii=False)}

Pedoman Visual Niche: {niche['visual_style']}
Pedoman Audio/SFX Niche: {niche['sound_style']}

Buat 6 prompt video AI (Bahasa Inggris) untuk Kling AI, Runway Gen-3, atau Midjourney, lengkap dengan pergerakan kamera dan rancangan sound effect per adegan.

Format JSON:
{{
  "style_preset": "{niche['visual_style']}",
  "audio_ambience": "{niche['sound_style']}",
  "shots": [
    {{
      "shot": 1,
      "timecode": "00:00-00:06",
      "prompt_en": "Vertical 9:16, cinematic ...",
      "camera_motion": "Slow zoom in / Pan / Tracking",
      "sfx": "Nama suara efek (misal: whoosh, slap, whisper)"
    }}
  ]
}}"""
    visual, m = ask(models, gilang_prompt)
    print("[Gilang] Prompt visual & SFX selesai")

    # 4. Agent Vina: Distribusi, Thumbnail Clickbait & Tagar
    vina_prompt = f"""Kamu Vina, social media manager spesialis FYP & algoritma rekomendasi YouTube/IG.
Judul Cerita: {ide.get('judul')}
Niche: {niche['nama']}

Buat paket postingan:
- Teks thumbnail (maksimal 4 kata, huruf kapital, bikin shock/penasaran).
- Caption menarik (bahasa Indonesia, memicu debat di kolom komentar).
- 10 Hashtag paling relevan.

Format JSON:
{{
  "teks_thumbnail": "...",
  "caption_postingan": "...",
  "hashtags": ["#...", "#..."]
}}"""
    distribusi, m = ask(models, vina_prompt)
    print("[Vina] Caption & hashtag selesai")

    # Kompilasi hasil
    hasil = {
        "tanggal": tanggal,
        "jam": jam,
        "niche_terpilih": target_niche,
        "ide": ide,
        "naskah": naskah,
        "visual_dan_sfx": visual,
        "distribusi": distribusi
    }

    os.makedirs(DATA, exist_ok=True)
    nama_file = f"konten_{target_niche}_{tanggal}.json"
    path_file = os.path.join(DATA, nama_file)
    with open(path_file, "w", encoding="utf-8") as f:
        json.dump(hasil, f, ensure_ascii=False, indent=2)

    with open(os.path.join(DATA, "naskah_terbaru.json"), "w", encoding="utf-8") as f:
        json.dump(hasil, f, ensure_ascii=False, indent=2)

    print(f"Selesai! Konten niche '{target_niche}' berhasil diproduksi di {path_file}")


if __name__ == "__main__":
    main()
