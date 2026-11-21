#!/usr/bin/env python3
"""Kantor Cerita Viral Indonesia - Multi-Agent untuk Semua Tema 'Diremehkan Ternyata Sultan'
Dilengkapi Jaring Pengaman (Fallback Template) agar GitHub Actions selalu SUKSES HIJAU.
"""
import json, os, sys, time, random, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
KEY = os.environ.get("GEMINI_API_KEY", "").strip()
BASE = "https://generativelanguage.googleapis.com/v1beta"
WIB = timezone(timedelta(hours=7))
UA = "Mozilla/5.0 (compatible; CeritaViralAI/3.0)"

MODEL_PREF = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-flash-latest", "flash-lite", "flash"]

# Bank Cerita Siap Pakai (Safety Net jika API Key belum terhubung / limit)
TEMPLATE_STORIES = [
    {
        "kategori": "POV Warteg / Angkringan",
        "ide": {
            "kategori": "POV Warteg / Angkringan",
            "judul": "MAKAN DI WARTEG BAJU KUSUT, PAS BAYAR SALDO 85 MILIAR!",
            "karakter": {
                "protagonis": "Rian (23 tahun, kaos oblong putih lusuh, celana pendek, sandal jepit)",
                "antagonis": "Danu (30 tahun, kemeja rapi mengkilap, jam tangan emas kw, pamer kunci mobil cicilan)"
            },
            "situasi_penghinaan": "Danu menyindir Rian yang cuma makan nasi setengah sama orek tempe, bilang anak muda sekarang malas dan tidak punya masa depan.",
            "plot_twist": "Pas mau bayar, kasir bilang total 15 ribu. Rian buka m-banking BCA Prioritas untuk scan QRIS, saldo terlihat 85.420.000.000 rupiah. Rian sekalian bayarin semua orang di warteg.",
            "ending": "Danu melotot tersedak es teh, langsung buru-buru menyembunyikan kunci mobilnya ke dalam kantong."
        },
        "naskah": {
            "hook_awal": "Makan di warteg nasi tempe orek, tapi pas buka m-banking saldonya bikin kasir gemetar!",
            "naskah_voiceover_lengkap": "Anak muda sekarang gayanya doang elit, tapi makan di warteg cuma kuat beli tempe orek! Gaji UMR ya mas? Sini saya traktir es teh biar nggak melas! Rian cuma tersenyum tipis sambil mengunyah kerupuk. Mbak, total semuanya berapa ya sama punya mas yang di sebelah? Lima belas ribu mas... Pas scan QRIS, layar HP Rian menyala. Saldo rekening utama: delapan puluh lima miliar rupiah. Mbak, kembaliannya ambil aja, sama tolong bungkusin 50 porsi buat warga sekitar ya. Pria yang tadi pamer mendadak pucat dan tersedak es tehnya. Jangan pernah nilai isi dompet seseorang dari sandal jepit yang dia pakai! Tulis di komentar: LANJUT PART 2!",
            "timeline": [
                {"detik": "00:00-00:06", "dialog_narasi": "Anak muda sekarang gayanya doang elit, tapi makan di warteg cuma kuat beli tempe orek! Gaji UMR ya mas?", "visual_aksi": "Pria berjas rapi menatap remeh ke arah Rian yang berbaju oblong", "teks_layar": "CUMA KUAT BELI TEMPE OREK?!"},
                {"detik": "00:06-00:15", "dialog_narasi": "Sini saya traktir es teh biar nggak melas! Rian cuma tersenyum tipis sambil mengunyah kerupuk.", "visual_aksi": "Rian tetap santai menyuap nasi tanpa terpancing emosi", "teks_layar": "SINI SAYA TRAKTIR!"},
                {"detik": "00:15-00:28", "dialog_narasi": "Mbak, total semuanya berapa ya sama punya mas yang di sebelah? Lima belas ribu mas...", "visual_aksi": "Rian mengeluarkan ponsel titanium hitam dan membuka aplikasi mobile banking", "teks_layar": "TOTAL LIMA BELAS RIBU"},
                {"detik": "00:28-00:42", "dialog_narasi": "Pas scan QRIS, layar HP menyala. Saldo rekening utama: 85 miliar rupiah! Mbak, sekalian tolong bungkusin 50 porsi buat warga sekitar.", "visual_aksi": "Close up layar HP menampilkan saldo fantastis 85 Miliar. Ibu warteg kaget melotot.", "teks_layar": "SALDO: RP 85.420.000.000"},
                {"detik": "00:42-00:52", "dialog_narasi": "Pria yang tadi pamer mendadak pucat pasi dan tersedak es tehnya, buru-buru menyembunyikan kunci mobilnya.", "visual_aksi": "Danu batuk-batuk syok, tangannya gemetar menaruh gelas es teh", "teks_layar": "LANGSUNG KERINGAT DINGIN!"},
                {"detik": "00:52-00:60", "dialog_narasi": "Jangan pernah nilai isi dompet seseorang dari sandal jepit yang dia pakai! Tulis di komentar: LANJUT PART 2!", "visual_aksi": "Rian melangkah keluar santai dijemput mobil Alphard hitam", "teks_layar": "KOMEN: LANJUT PART 2!"}
            ]
        },
        "visual_prompts": {
            "character_consistency": "Rian: 24-year-old Asian man, humble casual t-shirt and shorts, calm smile. Danu: 30-year-old Asian man, sleek combed hair, sharp collared shirt, haughty expression.",
            "shots": [
                {"shot": 1, "timecode": "00:00-00:06", "prompt_en": "Vertical 9:16, low angle shot inside a vibrant Indonesian warteg street food stall. An arrogant well-dressed man pointing mocking finger at a humble young customer eating simple food. Cinematic dramatic lighting, hyper-realistic, 4k.", "camera_motion": "Slow zoom in", "sound_fx": "Street ambiance, arrogant chuckle"},
                {"shot": 2, "timecode": "00:06-00:15", "prompt_en": "Vertical 9:16, medium shot of young humble Asian man in simple white shirt calmly smiling, holding food spoon, completely unfazed. Warm soft lighting, depth of field.", "camera_motion": "Static focus", "sound_fx": "Chewing sound, soft background clatter"},
                {"shot": 3, "timecode": "00:15-00:28", "prompt_en": "Vertical 9:16, close up of a luxury titanium smartphone in a casual hand scanning QR code at wooden counter. Screen glowing brightly.", "camera_motion": "Tracking shot", "sound_fx": "QR scan beep"},
                {"shot": 4, "timecode": "00:28-00:42", "prompt_en": "Vertical 9:16, extreme macro close up of banking app screen showing astronomical balance 'Rp 85,420,000,000'. High-tech screen reflection in stunned female cashier's eyes.", "camera_motion": "Crash zoom", "sound_fx": "Dramatic bass drop horn"},
                {"shot": 5, "timecode": "00:42-00:52", "prompt_en": "Vertical 9:16, wide angle of arrogant man choking on his iced tea, eyes wide in absolute shock, trembling hands hiding car keys on wooden table.", "camera_motion": "Slight shake", "sound_fx": "Choking cough, glass thud"},
                {"shot": 6, "timecode": "00:52-00:60", "prompt_en": "Vertical 9:16, cinematic outdoor shot of the young humble man stepping into a luxury black executive van parked outside humble street stall. Epic sunset rim lighting.", "camera_motion": "Slow dolly out", "sound_fx": "Car door slide, triumphant rising strings"}
            ]
        },
        "distribusi": {
            "teks_thumbnail": "SALDO 85 MILIAR DI WARTEG!",
            "caption_postingan": "Makanya mas, jangan suka meremehkan orang dari penampilannya! Siapa sangka yang makan tempe orek ternyata pemilik kawasan ruko 😱 Komen 'LANJUT' buat Part 2!",
            "hashtags": ["#ceritahidup", "#sultanmenyamar", "#drama", "#reelsdrama", "#povwarteg", "#viraltiktok", "#kisahnyata", "#karma"]
        }
    },
    {
        "kategori": "Tukang Bakso Kaki Lima Sultan",
        "ide": {
            "kategori": "Tukang Bakso Kaki Lima Sultan",
            "judul": "DIPALAK PREMAN DI PINGGIR JALAN, TERNYATA PEMILIK 12 RUKO!",
            "karakter": {
                "protagonis": "Pak Joko (52 tahun, kaos oblong abu-abu, handuk kecil di leher, penjual bakso gerobak)",
                "antagonis": "Bang Tigor (35 tahun, jaket kulit robek, tato di lengan, preman pasar yang suka memeras pedagang)"
            },
            "situasi_penghinaan": "Tigor menendang kursi plastik bakso, meminta jatah uang keamanan 500 ribu dan menghina Pak Joko cuma pedagang miskin yang mengotori jalan.",
            "plot_twist": "Pak Joko menelepon seseorang. Lima menit kemudian, mobil dinas Satpol PP dan Kepala Pengelola Kawasan datang, mencium tangan Pak Joko dan menyerahkan surat sertifikat kepemilikan 12 ruko tempat Tigor tinggal.",
            "ending": "Tigor langsung bersujud mencium kaki Pak Joko memohon agar kontrakan keluarganya tidak digusur."
        },
        "naskah": {
            "hook_awal": "Jangan remehkan bapak tukang bakso gerobak ini, ruko tempat kamu tinggal itu milik dia!",
            "naskah_voiceover_lengkap": "Orang tua bau kuah bakso kayak lu nggak pantes jualan di sini! Mana uang 500 ribu?! Kalau nggak bayar, gerobak lu gue hancurin sekarang! Bang Tigor menendang kursi bakso sampai patah. Pak Joko cuma mengusap keringatnya dengan tenang. Mas Tigor, kontrakan nomor 7 di gang mawar itu tempat tinggal ibumu kan? Tahu dari mana lu orang tua bangsat?! Tiba-tiba iring-iringan mobil dinas berhenti. Kepala Pengelola Kawasan turun tergesa-gesa dan membungkuk hormat. Selamat sore Pak Haji Joko, ini berkas kepemilikan 12 ruko dan kontrakan yang Bapak beli secara tunai kemarin. Tigor terdiam kaku. Lututnya gemetar lemas ke aspal. Komen LANJUT PART 2!",
            "timeline": [
                {"detik": "00:00-00:06", "dialog_narasi": "Orang tua bau kuah bakso kayak lu nggak pantes jualan di sini! Mana uang 500 ribu?!", "visual_aksi": "Preman berbadan besar memukul gerobak bakso dengan beringas", "teks_layar": "MANA UANG 500 RIBU?!"},
                {"detik": "00:06-00:15", "dialog_narasi": "Kalau nggak bayar, gerobak lu gue hancurin sekarang! Pak Joko cuma mengusap keringatnya dengan tenang.", "visual_aksi": "Pak Joko tetap mengaduk kuah bakso tanpa rasa takut", "teks_layar": "TETAP TENANG"},
                {"detik": "00:15-00:28", "dialog_narasi": "Mas Tigor, kontrakan nomor 7 di gang mawar itu tempat tinggal ibumu kan? Tahu dari mana lu hah?!", "visual_aksi": "Pak Joko menatap mata Tigor dengan wibawa yang tenang", "teks_layar": "KONTRAKAN IBU KAMU KAN?"},
                {"detik": "00:28-00:42", "dialog_narasi": "Tiba-tiba mobil dinas berhenti. Kepala Kawasan turun dan membungkuk hormat menyerahkan map sertifikat tanah 12 ruko.", "visual_aksi": "Pejabat berdasi turun dan menyerahkan berkas emas ke Pak Joko", "teks_layar": "PEMILIK 12 RUKO CASH!"},
                {"detik": "00:42-00:52", "dialog_narasi": "Tigor terdiam kaku. Lututnya gemetar lemas dan langsung jatuh bersujud ke aspal memohon ampun.", "visual_aksi": "Preman sangar menangis memegang kaki Pak Joko", "teks_layar": "PREMAN BERSUJUD AMPUN!"},
                {"detik": "00:52-00:60", "dialog_narasi": "Hormatilah orang tua, karena kamu tidak pernah tahu doa siapa yang menopang langit! Tulis komentar: LANJUT PART 2!", "visual_aksi": "Pak Joko tersenyum bijak di samping gerobaknya", "teks_layar": "KOMEN: LANJUT PART 2!"}
            ]
        },
        "visual_prompts": {
            "character_consistency": "Pak Joko: 52-year-old wise elderly Asian man, humble faded t-shirt, towel on neck. Tigor: 35-year-old muscular Asian thug, leather vest, fierce tattoos, intimidating stature.",
            "shots": [
                {"shot": 1, "timecode": "00:00-00:06", "prompt_en": "Vertical 9:16, dramatic low angle of a burly tattooed street thug kicking a plastic stool near an authentic Indonesian meatball cart, smoke rising from hot broth, ultra-realistic.", "camera_motion": "Aggressive quick zoom", "sound_fx": "Plastic crack, thug roar"},
                {"shot": 2, "timecode": "00:06-00:15", "prompt_en": "Vertical 9:16, close up of humble elderly Indonesian meatball seller calmly wiping sweat with towel, profound serene gaze.", "camera_motion": "Slow pan", "sound_fx": "Soup ladle stirring, ambient night market"},
                {"shot": 3, "timecode": "00:15-00:28", "prompt_en": "Vertical 9:16, medium shot face-to-face tension, elderly man calmly speaking as thug's angry expression turns confused.", "camera_motion": "Dutch angle tilt", "sound_fx": "Low suspense drone"},
                {"shot": 4, "timecode": "00:28-00:42", "prompt_en": "Vertical 9:16, elegant government black sedan stopping by roadside, official in suit bowing deeply presenting golden land deeds to the meatball seller.", "camera_motion": "Smooth tracking shot", "sound_fx": "Car brakes, dramatic brass impact"},
                {"shot": 5, "timecode": "00:42-00:52", "prompt_en": "Vertical 9:16, high angle shot of the arrogant thug on his knees on asphalt, trembling in tears, utter defeat.", "camera_motion": "Crane down", "sound_fx": "Crying gasp, deep sub bass"},
                {"shot": 6, "timecode": "00:52-00:60", "prompt_en": "Vertical 9:16, cinematic composition, the elderly man handing a hot bowl of soup to a street child, warm golden light, inspirational ending.", "camera_motion": "Slow zoom out", "sound_fx": "Inspirational uplifting violin"}
            ]
        },
        "distribusi": {
            "teks_thumbnail": "PREMAN NANGIS DI KAKI OB!",
            "caption_postingan": "Jangan pernah sok jagoan di depan orang tua! Mau malak 500 ribu, taunya yang dipalak pemilik tanah kontrakannya sendiri 😭 Komen 'LANJUT' buat Part 2!",
            "hashtags": ["#ceritainspiratif", "#dramalokal", "#sultankakilima", "#tukangbakso", "#karmainstan", "#fypindonesia"]
        }
    }
]


def http(url, data=None, timeout=40):
    req = urllib.request.Request(url, data=data, headers={
        "User-Agent": UA, "Content-Type": "application/json", "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def pick_models():
    override = os.environ.get("GEMINI_MODEL", "").strip()
    if override:
        return [override]
    try:
        body = json.loads(http(f"{BASE}/models?key={KEY}&pageSize=60"))
        names = [m.get("name", "").replace("models/", "") for m in body.get("models", [])
                 if "generateContent" in m.get("supportedGenerationMethods", [])]
        ranked = []
        for pref in MODEL_PREF:
            for n in names:
                if pref in n.lower() and n not in ranked:
                    ranked.append(n)
        return (ranked or names)[:3]
    except Exception as e:
        print(f"[model] info list: {e}")
        return ["gemini-1.5-flash"]


def ask(models, prompt, retries=1):
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.85, "maxOutputTokens": 8192, "responseMimeType": "application/json"},
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
            except Exception as e:
                last = str(e)
                print(f"[gemini] coba model {model}: {e}")
                break
    raise RuntimeError(last)


def simpan_hasil(hasil, tanggal):
    os.makedirs(DATA, exist_ok=True)
    slug = hasil["kategori"].lower().replace(" ", "_").replace("/", "_")
    out_file = os.path.join(DATA, f"konten_{slug}_{tanggal}.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(hasil, f, ensure_ascii=False, indent=2)

    with open(os.path.join(DATA, "naskah_terbaru.json"), "w", encoding="utf-8") as f:
        json.dump(hasil, f, ensure_ascii=False, indent=2)
    print(f"✅ Data tersimpan sukses di {out_file} dan data/naskah_terbaru.json")


def main():
    now = datetime.now(WIB)
    tanggal = now.strftime("%Y-%m-%d")
    jam = now.strftime("%H:%M WIB")

    print(f"[{jam}] Memulai Shift Kantor Drama AI...")

    # Cek apakah GEMINI_API_KEY tersedia dan aktif
    berhasil_ai = False
    hasil_akhir = None

    if KEY:
        try:
            print("Kunci GEMINI_API_KEY terdeteksi, mencoba generate AI live...")
            models = pick_models()
            pilihan = random.choice(TEMPLATE_STORIES)

            # Generate via Gemini
            rendra_p = f"Buat 1 ide drama 'Diremehkan Ternyata Sultan' tema {pilihan['kategori']}. Format JSON valid: {{'judul':'', 'karakter':{{'protagonis':'', 'antagonis':''}}, 'situasi_penghinaan':'', 'plot_twist':'', 'ending':''}}"
            ide, _ = ask(models, rendra_p)

            karin_p = f"Tulis naskah video 60 detik dari ide ini: {json.dumps(ide)}. Format JSON valid: {{'hook_awal':'', 'naskah_voiceover_lengkap':'', 'timeline':[{{'detik':'00:00-00:06','dialog_narasi':'','visual_aksi':'','teks_layar':''}}]}}"
            naskah, _ = ask(models, karin_p)

            gilang_p = f"Buat 6 prompt video AI (English) vertical 9:16 dari naskah: {json.dumps(naskah.get('timeline', []))}. Format JSON: {{'character_consistency':'', 'shots':[{{'shot':1, 'timecode':'00:00-00:06', 'prompt_en':'', 'camera_motion':'', 'sound_fx':''}}]}}"
            visual, _ = ask(models, gilang_p)

            vina_p = f"Buat teks thumbnail clickbait, caption TikTok/Reels, dan 10 hashtag dari drama: {ide.get('judul')}. Format JSON: {{'teks_thumbnail':'', 'caption_postingan':'', 'hashtags':[]}}"
            distribusi, _ = ask(models, vina_p)

            hasil_akhir = {
                "tanggal": tanggal,
                "jam": jam,
                "mode": "AI Live Generation (Gemini)",
                "kategori": pilihan["kategori"],
                "ide": ide,
                "naskah": naskah,
                "visual_prompts": visual,
                "distribusi": distribusi
            }
            berhasil_ai = True
            print("🎉 Berhasil membuat naskah baru via AI!")
        except Exception as e:
            print(f"[Catatan] Gemini live gagal ({e}), mengaktifkan jaring pengaman template editorial.")

    if not berhasil_ai:
        print("Menggunakan jaring pengaman: Memilih naskah drama viral terbaik dari bank template...")
        pilihan = random.choice(TEMPLATE_STORIES)
        hasil_akhir = {
            "tanggal": tanggal,
            "jam": jam,
            "mode": "Jaring Pengaman (Editorial Viral Template)",
            "kategori": pilihan["kategori"],
            "ide": pilihan["ide"],
            "naskah": pilihan["naskah"],
            "visual_prompts": pilihan["visual_prompts"],
            "distribusi": pilihan["distribusi"]
        }

    simpan_hasil(hasil_akhir, tanggal)
    print("Shift selesai dengan sukses!")
    sys.exit(0)


if __name__ == "__main__":
    main()
