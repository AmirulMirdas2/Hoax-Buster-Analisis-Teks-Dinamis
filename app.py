import streamlit as st
import pandas as pd
from transformers import pipeline

st.set_page_config(layout="wide")
st.title("🕵️‍♂️ Hoax Buster: Analisis Teks Dinamis")
st.write("""
Aplikasi ini menggunakan model AI canggih (Zero-Shot Classification) untuk menganalisis dan mengklasifikasikan teks Anda. 
Cukup masukkan sebuah artikel atau paragraf, tentukan sendiri kategori yang relevan, dan biarkan AI yang bekerja!
""")

@st.cache_resource
def load_classifier():
    return pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

classifier = load_classifier()

col1, col2 = st.columns([0.5, 0.5], gap="medium")

with col1:
    st.subheader("📝 Masukkan Teks Anda di Sini")
    text_input = st.text_area("Ketik atau tempel artikel/berita:", height=300, 
                              placeholder="Contoh: Pemerintah mengumumkan kebijakan baru terkait subsidi BBM yang akan berlaku mulai bulan depan...")

    st.subheader("🏷️ Tentukan Label/Kategori Anda")
    candidate_labels = st.text_input("Masukkan kategori dipisahkan oleh koma", 
                                     value="Hoax, Fakta, Opini, Satir, Promosi")

    analyze_button = st.button("Analisis Sekarang", type="primary", use_container_width=True)

with col2:
    st.subheader("📊 Hasil Analisis")
    
    if analyze_button:
        if text_input and candidate_labels:
            with st.spinner("AI sedang berpikir... mohon tunggu sebentar..."):
                labels = [label.strip() for label in candidate_labels.split(',')]
                
                results = classifier(text_input, labels)

                st.write("Teks yang Dianalisis:")
                st.info(results['sequence'])

                df = pd.DataFrame({
                    'Kategori': results['labels'],
                    'Skor Kepercayaan': results['scores']
                })

                st.write("Grafik Skor Kepercayaan untuk Setiap Kategori:")
                st.bar_chart(df.set_index('Kategori'))

                st.write("Detail Skor:")
                st.dataframe(df)
        else:
            st.error("Harap masukkan teks dan setidaknya satu label untuk dianalisis.")
    else:
        st.info("Hasil analisis akan muncul di sini setelah Anda menekan tombol 'Analisis Sekarang'.")