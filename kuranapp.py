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

@st.cache_data
def load_corpus(path='corpus.txt'):
    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()

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
    # Sıklığa göre azalan sırala
    return sorted(fiil_sayaci.items(), key=lambda x: x[1], reverse=True)

st.title("Sûredeki Fiil Köklerini Bul")

corpus = load_corpus()

sure_no = st.text_input("Kaçıncı sûredeki fiil köklerini görmek istiyorsunuz?", "56")

if sure_no.strip().isdigit():
    fiiller = fiil_koklerini_bul(sure_no.strip(), corpus)
    if fiiller:
        st.markdown(f"### {sure_no}. sûredeki fiil kökleri (kullanım sıklığına göre en çoktan aza):")
        for fiil, sayi in fiiller:
            arapca = latin2arabic(fiil)
            st.write(f"{arapca} : {sayi}")
    else:
        st.warning(f"{sure_no}. sûre içinde fiil kökü bulunamadı.")
else:
    st.warning("Lütfen geçerli bir sûre numarası giriniz.")
