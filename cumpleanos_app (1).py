import streamlit as st
import json
import io
from datetime import datetime
from pathlib import Path
import cloudinary
import cloudinary.uploader
import cloudinary.api

# ─── Configuración de página ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Feliz Cumpleaños, mi amor 🌹",
    page_icon="🌹",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Conectar con Cloudinary ───────────────────────────────────────────────────
@st.cache_resource
def init_cloudinary():
    cloudinary.config(
        cloud_name=st.secrets["cloudinary"]["cloud_name"],
        api_key=st.secrets["cloudinary"]["api_key"],
        api_secret=st.secrets["cloudinary"]["api_secret"],
        secure=True
    )

init_cloudinary()

# ─── Metadata en Cloudinary (como JSON en un raw file) ────────────────────────
METADATA_PUBLIC_ID = "cumpleanos/metadata"

def load_metadata():
    try:
        import urllib.request
        url = cloudinary.CloudinaryImage(METADATA_PUBLIC_ID).build_url(resource_type="raw")
        with urllib.request.urlopen(url + f"?t={int(datetime.now().timestamp())}") as r:
            return json.loads(r.read().decode("utf-8"))
    except:
        return []

def save_metadata(data):
    content = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
    cloudinary.uploader.upload(
        io.BytesIO(content),
        public_id=METADATA_PUBLIC_ID,
        resource_type="raw",
        overwrite=True,
        invalidate=True
    )

def upload_media(file_bytes, filename, tipo):
    ext = Path(filename).suffix.lower()
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    public_id = f"cumpleanos/{'fotos' if tipo == 'foto' else 'videos'}/{timestamp_str}"
    resource_type = "video" if tipo == "video" else "image"
    result = cloudinary.uploader.upload(
        file_bytes,
        public_id=public_id,
        resource_type=resource_type,
        overwrite=False
    )
    return result["public_id"], result["secure_url"]

def delete_media(public_id, tipo):
    resource_type = "video" if tipo == "video" else "image"
    cloudinary.uploader.destroy(public_id, resource_type=resource_type)

def cloudinary_video_url(public_id):
    return cloudinary.CloudinaryVideo(public_id).build_url(
        resource_type="video",
        format="mp4"
    )

def cloudinary_image_url(public_id, width=900):
    return cloudinary.CloudinaryImage(public_id).build_url(
        width=width, crop="limit", quality="auto", fetch_format="auto"
    )

# ─── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400&display=swap');

.stApp {
    background: linear-gradient(135deg, #1a0a0f 0%, #2d0a1a 40%, #1a0510 100%);
    min-height: 100vh;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; max-width: 1100px; }

.hero-header { text-align: center; padding: 4rem 2rem 3rem; position: relative; }
.hero-header::before {
    content: '✦ ✦ ✦'; display: block; color: #c9956c;
    font-size: 1rem; letter-spacing: 1rem; margin-bottom: 1.5rem; opacity: 0.7;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.8rem, 6vw, 5rem); font-weight: 700;
    color: #f5e6d8; line-height: 1.1; margin: 0;
    text-shadow: 0 0 60px rgba(201, 149, 108, 0.4);
}
.hero-title em { color: #c9956c; font-style: italic; }
.hero-subtitle {
    font-family: 'Lato', sans-serif; font-weight: 300; font-size: 1.1rem;
    color: #a07060; letter-spacing: 0.3rem; text-transform: uppercase; margin-top: 1.2rem;
}
.hero-divider {
    width: 120px; height: 1px;
    background: linear-gradient(90deg, transparent, #c9956c, transparent);
    margin: 2rem auto;
}
.love-message {
    background: rgba(255,255,255,0.03); border: 1px solid rgba(201, 149, 108, 0.2);
    border-radius: 2px; padding: 2.5rem 3rem; margin: 1rem 2rem 3rem;
    font-family: 'Playfair Display', serif; font-style: italic;
    font-size: 1.25rem; color: #d4b896; line-height: 1.9;
    text-align: center; position: relative;
}
.love-message::before {
    content: '"'; font-size: 5rem; color: rgba(201, 149, 108, 0.15);
    position: absolute; top: -1rem; left: 1.5rem;
    font-family: Georgia, serif; line-height: 1;
}
.section-title {
    font-family: 'Playfair Display', serif; font-size: 1.8rem;
    color: #f0d8c0; text-align: center; margin: 3rem 0 0.5rem;
}
.section-subtitle {
    font-family: 'Lato', sans-serif; font-weight: 300; color: #7a5545;
    text-align: center; font-size: 0.85rem; letter-spacing: 0.2rem;
    text-transform: uppercase; margin-bottom: 2rem;
}
.media-card {
    background: rgba(255,255,255,0.03); border: 1px solid rgba(201, 149, 108, 0.15);
    border-radius: 4px; overflow: hidden; margin-bottom: 0.5rem;
}
.media-card-header {
    padding: 0.8rem 1.2rem; background: rgba(201, 149, 108, 0.08);
    border-bottom: 1px solid rgba(201, 149, 108, 0.1);
}
.media-date {
    font-family: 'Lato', sans-serif; font-weight: 300; font-size: 0.75rem;
    color: #c9956c; letter-spacing: 0.15rem; text-transform: uppercase;
}
.media-caption {
    font-family: 'Playfair Display', serif; font-style: italic;
    font-size: 1rem; color: #c8a882; margin-top: 0.2rem;
}
.timeline-year {
    font-family: 'Playfair Display', serif; font-size: 3rem;
    color: rgba(201, 149, 108, 0.15); font-weight: 700;
    text-align: center; margin: 2rem 0 -0.5rem; line-height: 1;
}
.timeline-connector {
    width: 1px; height: 40px;
    background: linear-gradient(180deg, transparent, rgba(201,149,108,0.4), transparent);
    margin: 0 auto;
}
.stButton > button {
    background: transparent; border: 1px solid rgba(201, 149, 108, 0.5);
    color: #c9956c; font-family: 'Lato', sans-serif; font-weight: 300;
    letter-spacing: 0.15rem; text-transform: uppercase; font-size: 0.8rem;
    padding: 0.6rem 1.5rem; border-radius: 0;
}
.stButton > button:hover {
    background: rgba(201, 149, 108, 0.1); border-color: #c9956c; color: #f0d8c0;
}
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stDateInput > div > div > input {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(201, 149, 108, 0.25) !important;
    color: #d4b896 !important; border-radius: 2px !important;
}
label {
    font-family: 'Lato', sans-serif !important; font-weight: 300 !important;
    font-size: 0.75rem !important; letter-spacing: 0.15rem !important;
    text-transform: uppercase !important; color: #7a5545 !important;
}
.stFileUploader > div {
    background: rgba(201, 149, 108, 0.04);
    border: 1px dashed rgba(201, 149, 108, 0.3) !important; border-radius: 2px;
}
.stats-row { display: flex; justify-content: center; gap: 3rem; margin: 2rem 0; }
.stat-item { text-align: center; }
.stat-number {
    font-family: 'Playfair Display', serif; font-size: 2.5rem;
    color: #c9956c; display: block; line-height: 1;
}
.stat-label {
    font-family: 'Lato', sans-serif; font-weight: 300; font-size: 0.7rem;
    color: #7a5545; letter-spacing: 0.2rem; text-transform: uppercase; margin-top: 0.4rem;
}
.petals { text-align: center; font-size: 1.5rem; opacity: 0.5; letter-spacing: 1rem; margin: 1rem 0; }
video { border-radius: 4px; width: 100%; max-height: 420px; background: #000; }
</style>
""", unsafe_allow_html=True)

# ─── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <h1 class="hero-title">Feliz <em>Cumpleaños</em>,<br>mi amor</h1>
    <p class="hero-subtitle">Dos años a tu lado · Un regalo que crece contigo</p>
    <div class="hero-divider"></div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="love-message">
    Cada foto, cada vídeo, cada momento guardado aquí es un testimonio 
    de lo que hemos construido juntos. Hoy, en tu cumpleaños, 
    quiero que tengas un lugar donde vivir todos nuestros recuerdos 
    para siempre. Este es nuestro álbum, nuestra historia.
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="petals">🌹 ✦ 🌹 ✦ 🌹</div>', unsafe_allow_html=True)

# ─── Cargar metadata ───────────────────────────────────────────────────────────
if "metadata" not in st.session_state:
    with st.spinner("Cargando recuerdos..."):
        st.session_state.metadata = load_metadata()

metadata = st.session_state.metadata

# ─── Estadísticas ─────────────────────────────────────────────────────────────
fotos = sum(1 for m in metadata if m.get("tipo") == "foto")
videos = sum(1 for m in metadata if m.get("tipo") == "video")
st.markdown(f"""
<div class="stats-row">
    <div class="stat-item"><span class="stat-number">{fotos}</span><span class="stat-label">Fotos</span></div>
    <div class="stat-item"><span class="stat-number">{videos}</span><span class="stat-label">Vídeos</span></div>
    <div class="stat-item"><span class="stat-number">{len(metadata)}</span><span class="stat-label">Recuerdos</span></div>
</div>
""", unsafe_allow_html=True)

# ─── Subida ────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-title">Añadir un Recuerdo</p>', unsafe_allow_html=True)
st.markdown('<p class="section-subtitle">Sube fotos o vídeos y cuéntame cuándo fue</p>', unsafe_allow_html=True)

col1, col2 = st.columns([1.2, 1])
with col1:
    archivos = st.file_uploader(
        "Selecciona fotos o vídeos",
        type=["jpg", "jpeg", "png", "gif", "webp", "mp4", "mov", "avi", "mkv", "webm"],
        accept_multiple_files=True,
        key="uploader"
    )
with col2:
    fecha_recuerdo = st.date_input("¿Cuándo fue este momento?", value=datetime.today())
    descripcion = st.text_area("Cuéntame este recuerdo (opcional)", placeholder="Ese día en que...", height=100)

if archivos:
    if st.button("✦ Guardar en nuestro álbum"):
        progress = st.progress(0, text="Subiendo a Cloudinary...")
        nuevos = 0
        for i, archivo in enumerate(archivos):
            ext = Path(archivo.name).suffix.lower()
            tipo = "video" if ext in [".mp4", ".mov", ".avi", ".mkv", ".webm"] else "foto"
            file_bytes = archivo.read()
            public_id, secure_url = upload_media(file_bytes, archivo.name, tipo)
            metadata.append({
                "public_id": public_id,
                "secure_url": secure_url,
                "nombre_original": archivo.name,
                "tipo": tipo,
                "fecha": str(fecha_recuerdo),
                "descripcion": descripcion,
                "subido": datetime.now().isoformat()
            })
            nuevos += 1
            progress.progress((i + 1) / len(archivos), text=f"Subiendo {i+1}/{len(archivos)}...")
        save_metadata(metadata)
        st.session_state.metadata = metadata
        st.success(f"✦ {nuevos} recuerdo(s) guardado(s) con amor")
        st.rerun()

# ─── Línea del tiempo ──────────────────────────────────────────────────────────
if metadata:
    st.markdown('<p class="section-title">Nuestra Línea del Tiempo</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Cada momento, en su lugar</p>', unsafe_allow_html=True)

    sorted_media = sorted(metadata, key=lambda x: x.get("fecha", ""), reverse=True)
    año_actual = None

    for item in sorted_media:
        fecha_str = item.get("fecha", "")
        try:
            fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d")
            año = fecha_obj.year
            fecha_display = fecha_obj.strftime("%d de %B de %Y")
        except:
            año = "?"
            fecha_display = fecha_str

        if año != año_actual:
            año_actual = año
            st.markdown(f'<div class="timeline-year">{año}</div>', unsafe_allow_html=True)
            st.markdown('<div class="timeline-connector"></div>', unsafe_allow_html=True)

        tipo = item.get("tipo", "foto")
        descripcion_item = item.get("descripcion", "")
        public_id = item.get("public_id", "")
        secure_url = item.get("secure_url", "")

        col_img, col_info = st.columns([1.6, 1])

        with col_img:
            st.markdown(f"""
            <div class="media-card">
                <div class="media-card-header">
                    <div class="media-date">{'📷 Fotografía' if tipo == 'foto' else '🎥 Vídeo'} · {fecha_display}</div>
                    {f'<div class="media-caption">{descripcion_item}</div>' if descripcion_item else ''}
                </div>
            </div>
            """, unsafe_allow_html=True)

            if tipo == "foto":
                img_url = cloudinary_image_url(public_id)
                st.image(img_url, use_container_width=True)
            else:
                video_url = cloudinary_video_url(public_id)
                st.markdown(f"""
                <video controls preload="metadata">
                    <source src="{video_url}" type="video/mp4">
                </video>
                """, unsafe_allow_html=True)

        with col_info:
            st.markdown(f"""
            <div style="padding:1.5rem 1rem;">
                <p style="font-family:'Playfair Display',serif;font-size:1.4rem;color:#c9956c;margin:0 0 0.8rem;">{fecha_display}</p>
                <p style="font-family:'Lato',sans-serif;font-weight:300;color:#7a5545;font-size:0.75rem;letter-spacing:0.1rem;text-transform:uppercase;margin:0 0 1rem;">
                    {'📷 FOTOGRAFÍA' if tipo == 'foto' else '🎥 VÍDEO'}
                </p>
                {f'<p style="font-family:\'Playfair Display\',serif;font-style:italic;color:#d4b896;font-size:1rem;line-height:1.7;">{descripcion_item}</p>' if descripcion_item else '<p style="font-family:Lato,sans-serif;font-weight:300;color:rgba(122,85,69,0.5);font-size:0.85rem;font-style:italic;">Sin descripción</p>'}
            </div>
            """, unsafe_allow_html=True)

            if st.button("✕ Eliminar", key=f"del_{public_id}"):
                try:
                    delete_media(public_id, tipo)
                except:
                    pass
                metadata.remove(item)
                save_metadata(metadata)
                st.session_state.metadata = metadata
                st.rerun()

        st.markdown('<hr style="border:none;border-top:1px solid rgba(201,149,108,0.08);margin:1rem 0 1.5rem;">', unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="text-align:center;padding:4rem 2rem;opacity:0.5;">
        <div style="font-size:3rem;margin-bottom:1rem;">🌹</div>
        <p style="font-family:'Playfair Display',serif;font-style:italic;color:#7a5545;font-size:1.1rem;">
            Aún no hay recuerdos guardados.<br>Sube el primero y empieza nuestra historia.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;padding:3rem 0 2rem;margin-top:3rem;border-top:1px solid rgba(201,149,108,0.1);">
    <p style="font-family:'Playfair Display',serif;font-style:italic;color:rgba(201,149,108,0.4);font-size:0.95rem;">
        Hecho con amor · Para ti · Siempre
    </p>
    <div style="font-size:1.2rem;opacity:0.3;margin-top:0.5rem;">✦</div>
</div>
""", unsafe_allow_html=True)
