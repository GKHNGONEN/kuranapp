import streamlit as st

# Harf dönüşüm tablosu
harf_cevir = {
    'A': 'ا', 'b': 'ب', 't': 'ت', 'v': 'ث', 'j': 'ج', 'H': 'ح', 'x': 'خ',
    'd': 'د', '*': 'ذ', 'r': 'ر', 'z': 'ز', 's': 'س', '$': 'ش', 'S': 'ص',
    'D': 'ض', 'T': 'ط', 'Z': 'ظ', 'E': 'ع', 'g': 'غ', 'f': 'ف', 'q': 'ق',
    'k': 'ك', 'l': 'ل', 'm': 'م', 'n': 'ن', 'h': 'ة', 'w': 'و', 'y': 'ي',
    'a': 'ى', 'i': 'ئ', 'u': 'ؤ'
}

def latin2arabic(kok):
    return ''.join(harf_cevir.get(h, h) for h in kok)

def fiil_koklerini_bul(sure_no, corpus_lines):
    fiil_sayaci = {}
    for satir in corpus_lines:
        if satir.startswith("LOCATION") or "\t" not in satir:
            continue
        parcalar = satir.strip().split("\t")
        if len(parcalar) < 4:
            continue
        konum, form, tag, ozellikler = parcalar
        if not konum.startswith(f"({sure_no}:"):
            continue
        if "POS:V" in ozellikler and "ROOT:" in ozellikler:
            root_kisim = [x for x in ozellikler.split("|") if x.startswith("ROOT:")]
            if root_kisim:
                root = root_kisim[0].split(":")[1]
                fiil_sayaci[root] = fiil_sayaci.get(root, 0) + 1
    return sorted(fiil_sayaci.items(), key=lambda x: x[1])

# Streamlit Arayüzü
st.title("Sûredeki Fiil Köklerini Bul")

uploaded_file = st.file_uploader("Lütfen 'corpus.txt' dosyasını yükleyin", type="txt")

sure_no = st.text_input("Kaçıncı sûredeki fiil köklerini görmek istiyorsunuz?", value="56")

if uploaded_file and sure_no.strip().isdigit():
    corpus_lines = uploaded_file.read().decode("utf-8").splitlines()
    fiiller = fiil_koklerini_bul(sure_no.strip(), corpus_lines)
    
    if fiiller:
        st.markdown(f"### {sure_no}. sûre içindeki fiil kökleri (sıklık artan sırayla):")
        for fiil, sayi in fiiller:
            arapca = latin2arabic(fiil)
            st.write(f"{arapca} : {sayi}")
    else:
        st.warning(f"{sure_no}. sûre içinde fiil kökü bulunamadı.")
