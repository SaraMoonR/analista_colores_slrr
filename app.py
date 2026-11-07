# -*- coding: utf-8 -*-
"""Analista Colores SLRR — interfaz futurista y colorida."""

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="SLRR · Color Lab",
    page_icon="🌈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------
# Motor de cálculo: se mantienen las fórmulas y umbrales del proyecto.
# ---------------------------------------------------------------------
def normalizar_canal_srgb(canal_255: int) -> float:
    c_norm = canal_255 / 255.0
    if c_norm <= 0.04045:
        return c_norm / 12.92
    return ((c_norm + 0.055) / 1.055) ** 2.4


def calcular_luminancia_relativa(r: int, g: int, b: int) -> float:
    r_lin = normalizar_canal_srgb(r)
    g_lin = normalizar_canal_srgb(g)
    b_lin = normalizar_canal_srgb(b)
    return (0.2126 * r_lin) + (0.7152 * g_lin) + (0.0722 * b_lin)


def calcular_ratio_contraste(lum1: float, lum2: float) -> float:
    l1, l2 = max(lum1, lum2), min(lum1, lum2)
    return (l1 + 0.05) / (l2 + 0.05)


def clasificar_accesibilidad_wcag(ratio: float) -> tuple[str, str]:
    if ratio >= 7.0:
        return (
            "SUPERIOR · AAA",
            "Contraste alto: supera el umbral de 7:1 para texto.",
        )
    if ratio >= 4.5:
        return (
            "ALTO · AA",
            "Cumple el umbral de 4.5:1 para texto de tamaño normal.",
        )
    if ratio >= 3.0:
        return (
            "BÁSICO · 3:1",
            "Alcanza 3:1: puede ser válido para texto grande; verifica el criterio aplicable.",
        )
    return (
        "NO CUMPLE",
        "Contraste inferior a 3:1. Ajusta la luminosidad de uno de los colores.",
    )


def hex_a_rgb(color_hex: str) -> tuple[int, int, int]:
    color_hex = color_hex.lstrip("#")
    return tuple(int(color_hex[i:i + 2], 16) for i in (0, 2, 4))


def analizar_colores(fondo: tuple[int, int, int], texto: tuple[int, int, int]):
    lum_fondo = calcular_luminancia_relativa(*fondo)
    lum_texto = calcular_luminancia_relativa(*texto)
    ratio = calcular_ratio_contraste(lum_fondo, lum_texto)
    nivel, recomendacion = clasificar_accesibilidad_wcag(ratio)
    return ratio, nivel, recomendacion


def etiqueta_estado(ratio: float) -> str:
    if ratio >= 7:
        return "AAA"
    if ratio >= 4.5:
        return "AA"
    if ratio >= 3:
        return "3:1"
    return "Revisar"


def bloque_color(nombre: str, color_hex: str, rgb: tuple[int, int, int]):
    st.markdown(
        f"""
        <div class="swatch-row">
          <span class="swatch" style="background:{color_hex};"></span>
          <span><b>{nombre}</b><small>{color_hex.upper()} &nbsp;·&nbsp; RGB {rgb}</small></span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def mostrar_resultado(fondo_hex: str, texto_hex: str, fondo_rgb, texto_rgb):
    ratio, nivel, recomendacion = analizar_colores(fondo_rgb, texto_rgb)
    estado = etiqueta_estado(ratio)
    st.markdown(
        f"""
        <div class="preview-card" style="background:{fondo_hex};color:{texto_hex};">
          <div class="preview-kicker">VISTA PREVIA DE CONTRASTE</div>
          <div class="preview-title">Diseño accesible para todas las personas</div>
          <div class="preview-copy">Una combinación de color debe facilitar la lectura y mantener una jerarquía clara.</div>
          <div class="preview-foot">{fondo_hex.upper()} &nbsp; × &nbsp; {texto_hex.upper()}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    a, b, c = st.columns(3)
    a.metric("Ratio de contraste", f"{ratio:.2f}:1")
    b.metric("Nivel alcanzado", estado)
    c.metric("AA · texto normal", "Cumple" if ratio >= 4.5 else "No cumple")

    if ratio >= 4.5:
        st.success(f"**{nivel}** · {recomendacion}")
    elif ratio >= 3:
        st.warning(f"**{nivel}** · {recomendacion}")
    else:
        st.error(f"**{nivel}** · {recomendacion}")
    return ratio


# ---------------------------------------------------------------------
# Sistema visual
# ---------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
      --ink: #f7f7ff;
      --muted: #b8bfd9;
      --glass: rgba(255,255,255,.075);
      --line: rgba(255,255,255,.16);
      --cyan: #52e7f2;
      --pink: #ff5cc8;
      --violet: #9b83ff;
      --lime: #c6ff6b;
    }
    html, body, [class*="css"] {font-family:'Manrope',sans-serif;}
    .stApp {
      color:var(--ink);
      background:
        radial-gradient(ellipse at 8% 7%, rgba(255,72,190,.20), transparent 29%),
        radial-gradient(ellipse at 92% 12%, rgba(44,222,244,.17), transparent 27%),
        radial-gradient(ellipse at 72% 88%, rgba(132,91,255,.19), transparent 34%),
        linear-gradient(135deg,#090d20 0%,#11152e 48%,#0a1024 100%);
      background-attachment:fixed;
    }
    [data-testid="stHeader"] {background:rgba(8,12,29,.42);}
    [data-testid="stSidebar"] {
      background:linear-gradient(180deg,rgba(23,29,62,.88),rgba(12,17,39,.92));
      border-right:1px solid var(--line);
    }
    [data-testid="stSidebar"] > div {padding-top:1.5rem;}
    .block-container {max-width:1240px;padding-top:2.2rem;padding-bottom:3.5rem;}
    h1,h2,h3,h4,p,label,small {color:var(--ink);}
    .hero {
      position:relative; overflow:hidden; padding:2rem 2.2rem;
      border:1px solid rgba(255,255,255,.20); border-radius:26px;
      background:linear-gradient(115deg,rgba(255,255,255,.13),rgba(255,255,255,.045));
      backdrop-filter:blur(18px); -webkit-backdrop-filter:blur(18px);
      box-shadow:0 18px 60px rgba(0,0,0,.22); margin-bottom:1.7rem;
    }
    .hero:after {
      content:"";position:absolute;width:260px;height:260px;right:-70px;top:-120px;
      border-radius:50%;background:linear-gradient(135deg,var(--cyan),var(--pink));
      filter:blur(65px);opacity:.32;pointer-events:none;
    }
    .eyebrow,.mono {
      font-family:'DM Mono',monospace;letter-spacing:.13em;text-transform:uppercase;
    }
    .eyebrow {font-size:.72rem;color:var(--cyan);font-weight:500;}
    .hero h1 {font-size:clamp(2rem,4vw,3.3rem);line-height:1.05;font-weight:800;margin:.55rem 0 .65rem;}
    .hero p {color:#cbd2ed;font-size:1rem;max-width:760px;margin:0;}
    .hero-orb {
      display:inline-flex;align-items:center;gap:8px;padding:7px 12px;border-radius:999px;
      background:rgba(82,231,242,.10);border:1px solid rgba(82,231,242,.28);
      color:#a8f7fb;font-size:.75rem;margin-top:1.1rem;
    }
    .section-kicker {color:var(--pink);font:500 .72rem 'DM Mono',monospace;letter-spacing:.13em;text-transform:uppercase;}
    .section-title {font-size:1.45rem;font-weight:800;margin:.25rem 0 .2rem;}
    .section-copy {color:var(--muted);margin-bottom:1rem;}
    .glass-panel {
      border:1px solid var(--line);border-radius:20px;padding:1.2rem 1.25rem;
      background:var(--glass);backdrop-filter:blur(16px);
      box-shadow:0 12px 34px rgba(0,0,0,.12);margin:.3rem 0 1rem;
    }
    .swatch-row {display:flex;align-items:center;gap:12px;margin:.7rem 0 1rem;color:var(--ink);}
    .swatch {width:48px;height:42px;border-radius:12px;border:1px solid rgba(255,255,255,.35);box-shadow:0 5px 18px rgba(0,0,0,.2);}
    .swatch-row small {display:block;color:#bfc7e2;font: .72rem 'DM Mono',monospace;margin-top:3px;}
    .preview-card {padding:2rem;border-radius:20px;border:1px solid rgba(255,255,255,.22);margin:1rem 0 1.2rem;box-shadow:0 12px 35px rgba(0,0,0,.18);}
    .preview-kicker {font:500 .68rem 'DM Mono',monospace;letter-spacing:.14em;opacity:.75;margin-bottom:1rem;}
    .preview-title {font-size:clamp(1.5rem,3vw,2.15rem);font-weight:800;line-height:1.15;max-width:780px;}
    .preview-copy {font-size:1rem;line-height:1.55;margin-top:.65rem;max-width:720px;}
    .preview-foot {font: .7rem 'DM Mono',monospace;letter-spacing:.08em;margin-top:1.4rem;opacity:.7;}
    div[data-testid="stMetric"] {
      background:rgba(255,255,255,.075);border:1px solid var(--line);
      padding:1rem 1.1rem;border-radius:17px;backdrop-filter:blur(12px);
    }
    div[data-testid="stMetricLabel"] {color:#bfc7e2;}
    div[data-testid="stMetricValue"] {color:#fff;font-weight:800;}
    .stButton > button {
      border:1px solid rgba(82,231,242,.48);border-radius:13px;
      background:linear-gradient(100deg,#7259ed,#c34bc5 55%,#ec5c9f);
      color:white;font-weight:800;min-height:3rem;box-shadow:0 8px 24px rgba(153,83,231,.22);
      transition:transform .18s ease,filter .18s ease;
    }
    .stButton > button:hover {transform:translateY(-2px);filter:brightness(1.12);border-color:#a8f7fb;color:white;}
    .stTextInput input,.stNumberInput input {
      background:rgba(255,255,255,.08);color:white;border:1px solid var(--line);border-radius:11px;
    }
    div[data-baseweb="input"] {background:rgba(255,255,255,.06);border-radius:11px;}
    div[data-testid="stExpander"] {background:rgba(255,255,255,.045);border:1px solid var(--line);border-radius:14px;}
    div[data-testid="stDataFrame"] {border:1px solid var(--line);border-radius:14px;overflow:hidden;}
    .stRadio label,.stMarkdown p,.stCaption {color:#d3d8ed;}
    hr {border-color:rgba(255,255,255,.13);}
    [data-testid="stAlert"] {border-radius:14px;border:1px solid var(--line);}
    footer {visibility:hidden;}
    @media(max-width:700px) {
      .hero {padding:1.45rem;border-radius:20px;}
      .preview-card {padding:1.3rem;}
      .block-container {padding-left:1rem;padding-right:1rem;}
    }
    </style>
    <div class="hero">
      <div class="eyebrow">SLRR / DESIGN TOOLS / 001</div>
      <h1>Color Lab<span style="color:#52e7f2;">.</span></h1>
      <p>Un laboratorio visual para explorar combinaciones cromáticas y comprobar su contraste con los umbrales WCAG implementados en el proyecto.</p>
      <div class="hero-orb">✦ &nbsp; CONTRASTE · COLOR · ACCESIBILIDAD</div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown('<div class="eyebrow">SLRR / PANEL DE CONTROL</div>', unsafe_allow_html=True)
    st.markdown("## ✳ Color Lab")
    st.caption("Selecciona un modo para comenzar tu análisis.")
    modo = st.radio(
        "MODO DE ANÁLISIS",
        ["Combinación individual", "Paleta completa"],
        label_visibility="collapsed",
    )
    st.divider()
    st.markdown("**01 / Motor cromático**")
    st.caption("Cálculo de luminancia relativa y ratio de contraste.")
    st.markdown("**02 / Referencia**")
    st.caption("Umbrales AA y AAA incluidos en el proyecto.")
    st.divider()
    st.caption("PROYECTO ACADÉMICO · ANALISTA COLORES SLRR")

if modo == "Combinación individual":
    st.markdown('<div class="section-kicker">01 / Single pair analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Explora una combinación</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-copy">Elige el color del fondo y el color del texto para visualizar y medir su contraste.</div>', unsafe_allow_html=True)

    left, right = st.columns(2, gap="large")
    with left:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("**◉ COLOR DE FONDO**")
        fondo_hex = st.color_picker("Selecciona el fondo", "#11152E", key="fondo_individual")
        fondo_rgb = hex_a_rgb(fondo_hex)
        bloque_color("Fondo", fondo_hex, fondo_rgb)
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("**◉ COLOR DEL TEXTO**")
        texto_hex = st.color_picker("Selecciona el texto", "#52E7F2", key="texto_individual")
        texto_rgb = hex_a_rgb(texto_hex)
        bloque_color("Texto", texto_hex, texto_rgb)
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("✦ ANALIZAR COMBINACIÓN", type="primary", use_container_width=True):
        st.divider()
        mostrar_resultado(fondo_hex, texto_hex, fondo_rgb, texto_rgb)

else:
    st.markdown('<div class="section-kicker">02 / Palette audit</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Evalúa tu sistema de color</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-copy">Define un fondo principal y añade hasta doce colores para revisar cada combinación.</div>', unsafe_allow_html=True)

    fondo_hex = st.color_picker("Color de fondo principal", "#11152E", key="fondo_paleta")
    fondo_rgb = hex_a_rgb(fondo_hex)
    bloque_color("Fondo principal", fondo_hex, fondo_rgb)

    cantidad = st.number_input(
        "CANTIDAD DE ELEMENTOS", min_value=1, max_value=12, value=3, step=1
    )
    st.markdown("#### Colores de la paleta")
    colores = []
    defaults = ["#52E7F2", "#FF5CC8", "#9B83FF", "#C6FF6B", "#FFB86B", "#F7F7FF"]
    for i in range(int(cantidad)):
        with st.expander(f"✳  ELEMENTO {i + 1}", expanded=(i < 3)):
            a, b = st.columns([1, 2])
            with a:
                nombre = st.text_input(
                    "Nombre o función", value=f"Elemento {i + 1}", key=f"nombre_{i}"
                )
            with b:
                color_hex = st.color_picker(
                    "Color", defaults[i % len(defaults)], key=f"color_{i}"
                )
            rgb = hex_a_rgb(color_hex)
            bloque_color(nombre or f"Elemento {i + 1}", color_hex, rgb)
            colores.append({
                "Elemento": nombre or f"Elemento {i + 1}",
                "Color": color_hex.upper(),
                "RGB": str(rgb),
                "_rgb": rgb,
            })

    if st.button("✦ EVALUAR PALETA COMPLETA", type="primary", use_container_width=True):
        st.divider()
        st.markdown("### Reporte de accesibilidad")
        resultados = []
        aprobados = 0
        for elemento in colores:
            ratio, nivel, recomendacion = analizar_colores(fondo_rgb, elemento["_rgb"])
            cumple = ratio >= 4.5
            if cumple:
                aprobados += 1
            resultados.append({
                "Elemento": elemento["Elemento"],
                "Color": elemento["Color"],
                "RGB": elemento["RGB"],
                "Ratio": f"{ratio:.2f}:1",
                "Nivel": nivel,
                "AA · texto normal": "Cumple" if cumple else "No cumple",
                "Recomendación": recomendacion,
            })
        df = pd.DataFrame(resultados)
        st.dataframe(df, use_container_width=True, hide_index=True)
        porcentaje = (aprobados / len(colores)) * 100
        m1, m2, m3 = st.columns(3)
        m1.metric("Cumplimiento AA", f"{porcentaje:.1f}%")
        m2.metric("Combinaciones AA", f"{aprobados}/{len(colores)}")
        m3.metric("Colores evaluados", str(len(colores)))
        st.download_button(
            "↓ DESCARGAR REPORTE CSV",
            data=df.to_csv(index=False).encode("utf-8-sig"),
            file_name="reporte_contraste_slrr.csv",
            mime="text/csv",
            use_container_width=True,
        )
        if aprobados == len(colores):
            st.success("✦ Todas las combinaciones alcanzan 4.5:1 para texto normal.")
        else:
            st.warning("Hay combinaciones que requieren ajustes para alcanzar 4.5:1 en texto normal.")

st.divider()
st.markdown(
    """
    <div style="display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;">
      <span class="mono" style="font-size:.68rem;color:#8e9abf;">SLRR · COLOR LAB</span>
      <span style="font-size:.72rem;color:#9da8c9;">Herramienta de apoyo. Verifica siempre el criterio WCAG aplicable al tamaño y tipo de elemento.</span>
    </div>
    """,
    unsafe_allow_html=True,
)
