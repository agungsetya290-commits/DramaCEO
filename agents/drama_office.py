#!/usr/bin/env python3
"""Kantor AI Drama - Spesialis Naskah & Alur Video 'Orang Diremehkan Jadi Kaya' / 'Undercover Boss'"""
import json, os, sys, time, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
KEY = os.environ.get("GEMINI_API_KEY", "").strip()
BASE = "https://generativelanguage.googleapis.com/v1beta"
WIB = timezone(timedelta(hours=7))
UA = "Mozilla/5.0 (compatible; KantorAIDrama/1.0)"

# Prioritas model Gemini
MODEL_PREF = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash", "flash"]


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

    models = pick_models()
    print(f"[{jam}] Menjalankan Kantor AI Drama dengan model: {models[0]}")

    # 1. Agent Rendra: Ide & Premis Drama Emosional
    rendra_prompt = """Kamu Rendra, creative director ahli meriset plot drama pendek viral (Reels/TikTok/Shorts).
Buat 1 ide cerita bertema: 'Orang Diremehkan, Ternyata Pemilik Asli / Konglomerat yang Menyamar'.
Karakteristik wajib:
- Setting lokasi Indonesia yang realistis (kantor cabang mewah, dealer mobil sport, reuni SMA hotel bintang lima, restoran elit).
- Antagonis yang sombong, manipulatif, dan menghina status sosial / fisik / pakaian.
- Protagonis yang berpura-pura sederhana (OB, kurir, supir, anak magang) tetapi memiliki kekuasaan mutlak.
- Twist kedatangan pihak berwenang / petinggi yang membungkuk hormat padanya.

Format JSON:
{
  "judul": "Judul bombastis yang memancing emosi",
  "lokasi": "Lobi kantor / Dealer / Reuni",
  "protagonis": {"nama": "Rian", "status_samaran": "OB baru", "identitas_asli": "Pewaris Tunggal Mahardika Group"},
  "antagonis": {"nama": "Danu", "jabatan": "Manajer Cabang Arogan", "tindakan_hina": "Menumpahkan kopi dan menyuruh menjilat sepatu"},
  "plot_twist": "Direktur Utama pusat datang membungkuk hormat dan membongkar korupsi si antagonis"
}"""
    ide, m = ask(models, rendra_prompt)
    print(f"[Rendra] Ide selesai: {ide.get('judul')}")

    # 2. Agent Karin: Penulis Naskah Dialog & Hook (60 Detik)
    karin_prompt = f"""Kamu Karin, scriptwriter drama pendek viral spesialis retensi penonton tinggi.
Berdasarkan ide dari Rendra ini:
{json.dumps(ide, ensure_ascii=False)}

Tulis naskah dialog video 60 detik (vertikal 9:16).
Wajib ada:
1. 00:00-00:03 HOOK EKSTREM: Dialog penghinaan yang bikin penonton naik darah.
2. 00:03-00:20 ESKALASI: Antagonis menindas, protagonis tenang membalas dengan kalimat menusuk.
3. 00:20-00:35 THE SECRET: Petunjuk kecil bahwa si protagonis orang berkuasa (telepon/berkas).
4. 00:35-00:50 THE TWIST: Rombongan pimpinan pusat datang, mengabaikan antagonis, tunduk ke protagonis.
5. 00:50-00:60 CLIFFHANGER: Antagonis panik ketakutan, CTA penonton 'Komen LANJUT PART 2'.

Format JSON:
{{
  "hook_awal": "Teks hook 3 detik pertama",
  "naskah_lengkap_voiceover": "Teks utuh yang tinggal di-copy ke Text-to-Speech",
  "scene": [
    {{"timecode": "00:00-00:06", "karakter": "Danu", "dialog": "...", "aksi_visual": "..."}},
    {{"timecode": "00:06-00:15", "karakter": "Danu & Rian", "dialog": "...", "aksi_visual": "..."}},
    {{"timecode": "00:15-00:25", "karakter": "Rian", "dialog": "...", "aksi_visual": "..."}},
    {{"timecode": "00:25-00:35", "karakter": "Narator", "dialog": "...", "aksi_visual": "..."}},
    {{"timecode": "00:35-00:45", "karakter": "Petinggi Pusat", "dialog": "...", "aksi_visual": "..."}},
    {{"timecode": "00:45-00:60", "karakter": "Narator", "dialog": "...", "aksi_visual": "..."}}
  ]
}}"""
    naskah, m = ask(models, karin_prompt)
    print("[Karin] Naskah selesai")

    # 3. Agent Gilang: Prompt Visual & Video Motion (Kling / Runway / Midjourney)
    gilang_prompt = f"""Kamu Gilang, visual director ahli AI image & video prompts (Midjourney, Flux, Kling AI, Runway Gen-3).
Berdasarkan naskah Karin:
{json.dumps(naskah.get('scene', []), ensure_ascii=False)}

Buat 6 prompt video AI dalam BAHASA INGGRIS dengan kualitas sinematik 9:16 vertikal, deskripsi konsistensi karakter, gerakan kamera, dan arahan SFX audio.

Format JSON:
{{
  "character_dna": "Deskripsi wajah & baju karakter utama agar konsisten di setiap scene",
  "shots": [
    {{
      "shot": 1,
      "timecode": "00:00-00:06",
      "prompt_en": "Cinematic vertical 9:16 ...",
      "camera_movement": "Crash zoom / Slow pan",
      "sfx": "Glass breaking, dramatic whoosh"
    }}
  ]
}}"""
    visual, m = ask(models, gilang_prompt)
    print("[Gilang] Prompt visual & SFX selesai")

    # 4. Agent Vina: Distribusi, Judul Clickbait & Caption Sosmed
    vina_prompt = f"""Kamu Vina, social media manager spesialis FYP TikTok & Reels Instagram.
Berdasarkan drama ini:
Judul: {ide.get('judul')}
Hook: {naskah.get('hook_awal')}

Buat 1 paket postingan viral:
- Judul thumbnail (maksimal 5 kata, huruf kapital, bikin penasaran).
- Caption TikTok & Instagram Reels (bahasa Indonesia gaul, memancing perdebatan di kolom komentar).
- 10 Hashtag trending drama.

Format JSON:
{{
  "teks_thumbnail": "...",
  "caption_reels_tiktok": "...",
  "hashtags": ["#dramakantor", "..."]
}}"""
    distribusi, m = ask(models, vina_prompt)
    print("[Vina] Caption & distribusi selesai")

    # Simpan hasil lengkap
    hasil_akhir = {
        "tanggal": tanggal,
        "jam": jam,
        "ide": ide,
        "naskah": naskah,
        "visual_prompts": visual,
        "distribusi": distribusi
    }

    os.makedirs(DATA, exist_ok=True)
    out_file = os.path.join(DATA, f"drama_{tanggal}.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(hasil_akhir, f, ensure_ascii=False, indent=2)

    # Simpan juga ke naskah_terbaru.json agar mudah diakses
    with open(os.path.join(DATA, "naskah_terbaru.json"), "w", encoding="utf-8") as f:
        json.dump(hasil_akhir, f, ensure_ascii=False, indent=2)

    print(f"Sukses! Seluruh naskah, prompt visual, dan caption tersimpan di {out_file}")


if __name__ == "__main__":
    main()
