#!/usr/bin/env python3
"""Kantor Cerita Viral Indonesia - Multi-Agent untuk Semua Tema 'Diremehkan Ternyata Sultan':
1. POV Makan di Warteg / Angkringan tapi Saldo Puluhan Miliar
2. Tukang Bakso / Pedagang Kaki Lima Ternyata Juragan Tanah & Investor
3. Beli Cash di Showroom / Toko Emas saat Berpakaian Lusuh Dihina Sales
4. Reuni Teman Lama / Warkop: Si Sombong Pamer vs Si Santai Pemilik Bisnis
5. Bos / Pewaris Menyamar Jadi Pelayan, Kuli, atau Kurir
"""
import json, os, sys, time, random, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
KEY = os.environ.get("GEMINI_API_KEY", "").strip()
BASE = "https://generativelanguage.googleapis.com/v1beta"
WIB = timezone(timedelta(hours=7))
UA = "Mozilla/5.0 (compatible; CeritaViralAI/3.0)"

MODEL_PREF = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash", "flash"]

# Bank Tema Kehidupan Nyata & Populer di Indonesia
TEMA_LIST = [
    {
        "kategori": "POV Warteg / Angkringan",
        "deskripsi": "Makan sederhana di warteg pinggir jalan memakai kaos oblong dan sandal jepit. Orang di sebelah pamer gaya hidup dan meremehkan, lalu pas bayar kasir kasbon ditutup atau saldo m-banking/Black Card terlihat tanpa sengaja bernilai puluhan miliar.",
        "hook": "Makan di warteg nasi tempe orek, tapi pas buka m-banking saldonya bikin kasir gemetar.",
        "lokasi": "Warteg pinggir jalan ramai / Angkringan malam hari"
    },
    {
        "kategori": "Tukang Bakso / Kaki Lima Sultan",
        "deskripsi": "Tukang gerobak bakso/cilok yang tampil sederhana dan sering dipalak preman atau dicibir pelanggan sombong, ternyata pemilik belasan ruko di jalan utama dan juragan kontrakan.",
        "hook": "Jangan remehkan bapak tukang bakso kuah ini, ruko tempat kamu nongkrong itu punya dia.",
        "lokasi": "Gerobak bakso pinggir jalan / Pelataran ruko"
    },
    {
        "kategori": "Beli Cash di Showroom / Toko Mewah",
        "deskripsi": "Orang tua atau pemuda berkaos lusuh masuk dealer mobil sport atau toko emas perhiasan. Ditolak dan diusir sales sombong, sampai akhirnya mengeluarkan karung/koper berisi uang tunai cash.",
        "hook": "Sales showroom tertawa sinis saat pria bersandal jepit ini menunjuk mobil termahal.",
        "lokasi": "Showroom mobil mewah / Toko perhiasan emas"
    },
    {
        "kategori": "Reuni Kawan Lama / Warkop",
        "deskripsi": "Nongkrong reuni teman sekolah di kafe atau warkop. Satu orang pamer mobil cicilan dan gaji manajer sambil menyindir temannya yang cuma diam, sampai pemilik gedung kafe datang menyapa teman yang diam itu sebagai bos pemilik kafe.",
        "hook": "Puas pamer kunci mobil di reuni, dia nggak tahu sewa tempat nongkrongnya milik temannya sendiri.",
        "lokasi": "Kafe modern / Warkop tongkrongan"
    },
    {
        "kategori": "Kurir / Ojol Penyelamat",
        "deskripsi": "Driver ojol atau kurir paket yang diinjak-injak arogansi pelanggan kaya baru, ternyata mantan konglomerat dermawan atau pemilik saham utama aplikasi tersebut yang lagi turun ke lapangan.",
        "hook": "Paket dilempar ke tanah karena dianggap kotor, semenit kemudian ada telepon dari kantor pusat.",
        "lokasi": "Depan rumah mewah / Pagar perumahan elit"
    }
]


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

    # Pilih tema acak dari bank tema kehidupan nyata Indonesia
    pilihan_tema = random.choice(TEMA_LIST)
    models = pick_models()
    print(f"[{jam}] Memproduksi Cerita: {pilihan_tema['kategori']} (Model: {models[0]})")

    # 1. Agent Rendra: Plot & Karakter Lokal Realistis
    rendra_prompt = f"""Kamu Rendra, creative researcher ahli merancang drama pendek viral Indonesia.
Kategori Terpilih: {pilihan_tema['kategori']}
Deskripsi: {pilihan_tema['deskripsi']}
Contoh Hook: {pilihan_tema['hook']}
Lokasi: {pilihan_tema['lokasi']}

Buat 1 alur cerita POV / orang diremehkan yang sangat adiktif dengan bumbu lokal Indonesia (warteg, warkop, sandal jepit, m-banking, preman, dll).

Format JSON:
{{
  "kategori": "{pilihan_tema['kategori']}",
  "judul": "Judul heboh yang memancing rasa penasaran penonton",
  "karakter": {{
    "protagonis": "Nama & deskripsi penampilan sederhana",
    "antagonis": "Nama & deskripsi gaya sombong / arogan"
  }},
  "situasi_penghinaan": "Detail adegan saat si protagonis diremehkan di tempat umum",
  "plot_twist": "Momen mengejutkan saat kekayaan atau identitas asli terungkap",
  "ending": "Reaksi syok dan penyesalan si antagonis"
}}"""
    ide, m = ask(models, rendra_prompt)
    print(f"[Rendra] Ide selesai: {ide.get('judul')}")

    # 2. Agent Karin: Naskah Dialog & Hook 60 Detik
    karin_prompt = f"""Kamu Karin, scriptwriter spesialis retensi penonton tinggi.
Ide Cerita dari Rendra:
{json.dumps(ide, ensure_ascii=False)}

Tulis naskah video 60 detik vertikal (9:16) dengan ritme cepat:
- 00:00-00:03 HOOK: Ucapan hinaan pedas atau narasi yang bikin penonton emosi.
- 00:03-00:20 ESKALASI: Antagonis pamer & menghina, protagonis tetap santai dan tenang.
- 00:20-00:40 THE REVEAL: Muncul bukti kekayaan (saldo rekening, sertifikat tanah, kedatangan orang penting).
- 00:40-00:52 KARMA INSTAN: Antagonis langsung pucat dan gemetar.
- 00:52-00:60 CLIFFHANGER / CTA: 'Komen LANJUT PART 2 untuk lihat kelanjutannya!'

Format JSON:
{{
  "hook_awal": "Teks hook 3 detik pertama",
  "naskah_voiceover_lengkap": "Teks lengkap siap dibaca Text-to-Speech",
  "timeline": [
    {{"detik": "00:00-00:06", "dialog_narasi": "...", "visual_aksi": "...", "teks_layar": "..."}},
    {{"detik": "00:06-00:15", "dialog_narasi": "...", "visual_aksi": "...", "teks_layar": "..."}},
    {{"detik": "00:15-00:28", "dialog_narasi": "...", "visual_aksi": "...", "teks_layar": "..."}},
    {{"detik": "00:28-00:42", "dialog_narasi": "...", "visual_aksi": "...", "teks_layar": "..."}},
    {{"detik": "00:42-00:52", "dialog_narasi": "...", "visual_aksi": "...", "teks_layar": "..."}},
    {{"detik": "00:52-00:60", "dialog_narasi": "...", "visual_aksi": "...", "teks_layar": "..."}}
  ]
}}"""
    naskah, m = ask(models, karin_prompt)
    print("[Karin] Naskah dialog selesai")

    # 3. Agent Gilang: Prompt Visual AI (Kling / Runway / Midjourney) & Sound Design
    gilang_prompt = f"""Kamu Gilang, visual director untuk video pendek AI.
Timeline Naskah:
{json.dumps(naskah.get('timeline', []), ensure_ascii=False)}

Buat 6 prompt video AI sinematik dalam BAHASA INGGRIS, rasio vertikal 9:16, pencahayaan realistis, gerakan kamera, dan sound effect per adegan.

Format JSON:
{{
  "character_consistency": "Deskripsi fisik protagonis & antagonis agar sama di tiap adegan",
  "shots": [
    {{
      "shot": 1,
      "timecode": "00:00-00:06",
      "prompt_en": "Cinematic vertical 9:16 ...",
      "camera_motion": "Slow pan / Zoom in",
      "sound_fx": "Nama suara SFX"
    }}
  ]
}}"""
    visual, m = ask(models, gilang_prompt)
    print("[Gilang] Prompt visual AI & SFX selesai")

    # 4. Agent Vina: Distribusi, Judul Thumbnail & Caption
    vina_prompt = f"""Kamu Vina, social media manager spesialis FYP TikTok & Instagram Reels.
Judul: {ide.get('judul')}
Kategori: {ide.get('kategori')}
Hook: {naskah.get('hook_awal')}

Buat 1 paket postingan:
- Judul thumbnail (maksimal 4 kata, huruf besar, bikin kaget).
- Caption TikTok & Instagram Reels (bahasa Indonesia gaul, mengundang netizen berkomentar).
- 10 Hashtag trending drama lokal.

Format JSON:
{{
  "teks_thumbnail": "...",
  "caption_postingan": "...",
  "hashtags": ["#ceritahidup", "#sultanmenyamar", "#drama"]
}}"""
    distribusi, m = ask(models, vina_prompt)
    print("[Vina] Caption & distribusi selesai")

    hasil = {
        "tanggal": tanggal,
        "jam": jam,
        "kategori": pilihan_tema["kategori"],
        "ide": ide,
        "naskah": naskah,
        "visual_prompts": visual,
        "distribusi": distribusi
    }

    os.makedirs(DATA, exist_ok=True)
    slug = pilihan_tema["kategori"].lower().replace(" ", "_").replace("/", "_")
    out_file = os.path.join(DATA, f"konten_{slug}_{tanggal}.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(hasil, f, ensure_ascii=False, indent=2)

    with open(os.path.join(DATA, "naskah_terbaru.json"), "w", encoding="utf-8") as f:
        json.dump(hasil, f, ensure_ascii=False, indent=2)

    print(f"Berhasil! Konten tema '{pilihan_tema['kategori']}' tersimpan di {out_file}")


if __name__ == "__main__":
    main()
