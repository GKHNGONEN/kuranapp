import streamlit as st
import re
import requests

# GitHub ham linkler (bunları kendi repo adresine göre düzenlemelisin)
GITHUB_RAW_BASE_URL = "https://raw.githubusercontent.com/kullaniciadi/reposu/main/"
CORPUS_URL = GITHUB_RAW_BASE_URL + "cospus.txt"
KURAN_URL = GITHUB_RAW_BASE_URL + "kuran-arapca.txt"

# Ebced değerleri
ebced_degerleri = {
    'ا': 1, 'ب': 2, 'ج': 3, 'د': 4, 'ه': 5, 'و': 6, 'ز': 7, 'ح': 8, 'ط': 9,
    'ي': 10, 'ك': 20, 'ل': 30, 'م': 40, 'ن': 50, 'س': 60, 'ع': 70, 'ف': 80,
    'ص': 90, 'ق': 100, 'ر': 200, 'ش': 300, 'ت': 400, 'ث': 500, 'خ': 600,
    'ذ': 700, 'ض': 800, 'ظ': 900, 'غ': 1000
}
arap_harfleri = set(ebced_degerleri.keys())

def harf_duzelt(harf):
    if harf in ['أ', 'إ', 'آ']:
        return 'ا'
    elif harf == 'ى':
        return 'ي'
    elif harf in ['ؤ', 'ئ']:
        return 'و'
    else:
        return harf

def ayet_temizle(ayet):
    ayet = re.sub(r'\s+', '', ayet)
    ayet = ''.join(harf_duzelt(h) for h in ayet if harf_duzelt(h) in arap_harfleri)
    return ayet

def ebced_hesapla(ayet):
    return sum(ebced_degerleri.get(harf, 0) for harf in ayet)

st.title("Kur'an Fiil ve Ebced Aracı")

secim = st.sidebar.selectbox("İşlem Seç", ["Sürelerde Fiil Sayısı", "Ebced Değerine Göre Ayet Bul"])

if secim == "Sürelerde Fiil Sayısı":
    st.header("Sürelerde Kaç Farklı Fiil Kökü Var?")

    try:
        yanit = requests.get(CORPUS_URL)
        yanit.raise_for_status()
        icerik = yanit.text
        sure_kokleri = {}
        for satir in icerik.strip().split("\n"):
            try:
                kok, tur, konum = satir.strip().split()
                if tur != 'verb':
                    continue
                sure_no = konum.split(':')[0]
                if sure_no not in sure_kokleri:
                    sure_kokleri[sure_no] = set()
                sure_kokleri[sure_no].add(kok)
            except:
                continue
        st.write("### Fiil kökü sayısı (süre bazında):")
        for sure, kokler in sorted(sure_kokleri.items(), key=lambda x: int(x[0])):
            st.write(f"Sure {sure}: {len(kokler)} fiil kökü")
    except Exception as e:
        st.error(f"Dosya alınamadı: {e}")

elif secim == "Ebced Değerine Göre Ayet Bul":
    st.header("Ebced Değerine Göre Ayet Bul")
    hedef_deger = st.number_input("Hedef Ebced Değeri:", min_value=1, step=1)

    if hedef_deger:
        try:
            yanit = requests.get(KURAN_URL)
            yanit.raise_for_status()
            satirlar = yanit.text.strip().splitlines()
            duzgun_satirlar = []
            gecici = ''
            for satir in satirlar:
                satir = satir.strip()
                if not satir:
                    continue
                if '|' in satir:
                    if gecici:
                        duzgun_satirlar.append(gecici)
                    gecici = satir
                else:
                    gecici += ' ' + satir
            if gecici:
                duzgun_satirlar.append(gecici)

            eslesenler = []
            for satir in duzgun_satirlar:
                try:
                    sure, ayet, metin = satir.split('|', 2)
                    temiz = ayet_temizle(metin)
                    ebced = ebced_hesapla(temiz)
                    if ebced == hedef_deger:
                        eslesenler.append((sure, ayet, metin))
                except:
                    continue

            if eslesenler:
                st.write(f"### Ebced {hedef_deger} olan ayetler:")
                for sure, ayet, metin in eslesenler:
                    st.write(f"**{sure}:{ayet}** → {metin}")
            else:
                st.warning("Bu değerde ayet bulunamadı.")
        except Exception as e:
            st.error(f"Dosya alınamadı: {e}")
