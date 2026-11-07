# -*- coding: utf-8 -*-
"""Analista Colores SLRR - Analizador de contraste y accesibilidad WCAG 2.1."""

import streamlit as st

st.set_page_config(
    page_title="Analista Colores SLRR",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# Lógica original del proyecto: se conservan las fórmulas de cálculo.
# -----------------------------------------------------------------------------
def normalizar_canal_srgb(canal_255: int) -> float:
    """Convierte un canal RGB (0-255) a luminancia linealizada según WCAG."""
    c_norm = canal_255 / 255.0
    if c_norm <= 0.04045:
        return c_norm / 12.92
    return ((c_norm + 0.055) / 1.055) ** 2.4


def calcular_luminancia_relativa(r: int, g: int, b: int) -> float:
    """Calcula la luminancia relativa de un color RGB."""
    r_lin = normalizar_canal_srgb(r)
    g_lin = normalizar_canal_srgb(g)
    b_lin = normalizar_canal_srgb(b)
    return (0.2126 * r_lin) + (0.7152 * g_lin) + (0.0722 * b_lin)


def calcular_ratio_contraste(lum1: float, lum2: float) -> float:
    """Calcula el ratio de contraste entre dos luminancias."""
    l1, l2 = max(lum1, lum2), min(lum1, lum2)
    return (l1 + 0.05) / (l2 + 0.05)


def clasificar_accesibilidad_wcag(ratio: float) -> tuple[str, str]:
    """Clasifica el contraste según los umbrales implementados en el proyecto."""
    if ratio >= 7.0:
        nivel = "SUPERIOR (AAA)"
        recomendacion = "Excelente legibilidad. Apto para todo tipo de texto y componentes."
    elif ratio >= 4.5:
        nivel = "ALTO (AA - Texto Normal)"
        recomendacion = "Cumple la norma estándar. Apto para cuerpo de texto y títulos."
    elif ratio >= 3.0:
        nivel = "BÁSICO (AA - Texto Grande / UI)"
        recomendacion = "Permitido solo para texto grande (>18pt / >14pt negrita) e íconos."
    else:
        nivel = "NO CUMPLE (Inaccesible)"
        recomendacion = "Contraste insuficiente. Ajusta la claridad de uno de los colores."
    return nivel, recomendacion


def hex_a_rgb(color_hex: str) -> tuple[int, int, int]:
    """Convierte un color hexadecimal (#RRGGBB) a una tupla RGB."""
    color_hex = color_hex.lstrip("#")
    return tuple(int(color_hex[i:i + 2], 16) for i in (0, 2, 4))


def analizar_colores(fondo: tuple[int, int, int], texto: tuple[int, int, int]):
    lum_fondo = calcular_luminancia_relativa(*fondo)
    lum_texto = calcular_luminancia_relativa(*texto)
    ratio = calcular_ratio_contraste(lum_fondo, lum_texto)
    nivel, recomendacion = clasificar_accesibilidad_wcag(ratio)
    return ratio, nivel, recomendacion


def mostrar_muestra_color(nombre: str, color_hex: str, rgb: tuple[int, int, int]):
    st.markdown(
        f"<div style='display:flex;align-items:center;gap:12px;margin:5px 0 12px;'>"
        f"<div style='width:48px;height:42px;border-radius:9px;background:{color_hex};"
        f"border:1px solid rgba(128,128,128,.45);'></div>"
        f"<div><strong>{nombre}</strong><br><code>{color_hex.upper()}</code> · RGB {rgb}</div></div>",
        unsafe_allow_html=True,
    )


def mostrar_resultado(fondo_hex: str, texto_hex: str, fondo_rgb, texto_rgb, nombre="Texto"):
    ratio, nivel, recomendacion = analizar_colores(fondo_rgb, texto_rgb)
    aprobado_aa = ratio >= 4.5
    st.markdown("#### Vista previa de la combinación")
    st.markdown(
        f"<div style='background:{fondo_hex};color:{texto_hex};padding:28px 22px;"
        f"border-radius:14px;border:1px solid rgba(128,128,128,.35);margin-bottom:16px;'>"
        f"<div style='font-size:12px;letter-spacing:.08em;text-transform:uppercase;opacity:.8;'>"
        f"{nombre}</div><div style='font-size:27px;font-weight:700;line-height:1.25;'>"
        f"Diseño accesible para todas las personas</div>"
        f"<div style='font-size:15px;margin-top:8px;'>Una combinación de color debe facilitar la lectura.</div></div>",
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3)
    c1.metric("Ratio de contraste", f"{ratio:.2f}:1")
    c2.metric("Clasificación", "AAA" if ratio >= 7 else "AA" if aprobado_aa else "Revisar")
    c3.metric("Texto estándar AA", "Cumple" if aprobado_aa else "No cumple")

    if ratio >= 7:
        st.success(f"**{nivel}** — {recomendacion}")
    elif ratio >= 4.5:
        st.success(f"**{nivel}** — {recomendacion}")
    elif ratio >= 3:
        st.warning(f"**{nivel}** — {recomendacion}")
    else:
        st.error(f"**{nivel}** — {recomendacion}")
    return ratio


# -----------------------------------------------------------------------------
# Interfaz Streamlit
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .block-container {padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1180px;}
    .hero {padding: 1.5rem 1.7rem; border-radius: 18px;
           background: linear-gradient(120deg, #211E4D 0%, #39336F 100%);
           color: white; margin-bottom: 1.5rem;}
    .hero p {color: #E7E5F5; margin-bottom: 0;}
    div[data-testid="stMetric"] {border: 1px solid rgba(128,128,128,.25);
        padding: 12px 14px; border-radius: 12px;}
    </style>
    <div class="hero">
      <div style="font-size:12px;letter-spacing:.13em;text-transform:uppercase;opacity:.8;">
        Diseño gráfico · UI/UX · Accesibilidad
      </div>
      <h1 style="color:white;margin:.35rem 0;">Analista de Contraste Cromático</h1>
      <p>Evalúa combinaciones de color y revisa su nivel de contraste según los criterios WCAG 2.1.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("⚙️ Herramienta")
    modo = st.radio(
        "Selecciona el tipo de análisis:",
        ["Combinación individual", "Paleta completa"],
    )
    st.divider()
    st.caption("Los valores RGB se calculan a partir de los colores seleccionados.")
    st.caption("Proyecto académico · Analista Colores SLRR")

if modo == "Combinación individual":
    st.subheader("01 · Análisis individual")
    st.write("Compara un color de fondo con un color de texto.")
    col_fondo, col_texto = st.columns(2)
    with col_fondo:
        st.markdown("**Color de fondo**")
        fondo_hex = st.color_picker("Selecciona el fondo", "#FFFFFF", key="fondo_individual")
        fondo_rgb = hex_a_rgb(fondo_hex)
        mostrar_muestra_color("Fondo", fondo_hex, fondo_rgb)
    with col_texto:
        st.markdown("**Color del texto**")
        texto_hex = st.color_picker("Selecciona el texto", "#211E4D", key="texto_individual")
        texto_rgb = hex_a_rgb(texto_hex)
        mostrar_muestra_color("Texto", texto_hex, texto_rgb)

    if st.button("Analizar combinación", type="primary", use_container_width=True):
        st.divider()
        mostrar_resultado(fondo_hex, texto_hex, fondo_rgb, texto_rgb)

else:
    st.subheader("02 · Evaluación de paleta")
    st.write("Define un fondo principal y evalúa varios colores de texto o componentes de interfaz.")
    fondo_hex = st.color_picker("Color de fondo principal", "#FFFFFF", key="fondo_paleta")
    fondo_rgb = hex_a_rgb(fondo_hex)
    mostrar_muestra_color("Fondo principal", fondo_hex, fondo_rgb)

    cantidad = st.number_input(
        "¿Cuántos elementos deseas evaluar?", min_value=1, max_value=12,
        value=3, step=1,
    )
    st.markdown("#### Colores de la paleta")
    colores = []
    defaults = ["#211E4D", "#9C181C", "#726D37", "#777777", "#FFFFFF", "#E7A94B"]
    for i in range(int(cantidad)):
        with st.expander(f"Elemento {i + 1}", expanded=(i < 3)):
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
            mostrar_muestra_color(nombre or f"Elemento {i + 1}", color_hex, rgb)
            colores.append({"nombre": nombre or f"Elemento {i + 1}", "hex": color_hex, "rgb": rgb})

    if st.button("Evaluar paleta completa", type="primary", use_container_width=True):
        st.divider()
        st.markdown("### Reporte de accesibilidad")
        resultados = []
        aprobados = 0
        for elemento in colores:
            ratio, nivel, recomendacion = analizar_colores(fondo_rgb, elemento["rgb"])
            cumple = ratio >= 4.5
            if cumple:
                aprobados += 1
            resultados.append({
                "Elemento": elemento["nombre"],
                "Color": elemento["hex"].upper(),
                "RGB": str(elemento["rgb"]),
                "Ratio": f"{ratio:.2f}:1",
                "Nivel WCAG": nivel,
                "AA texto normal": "Cumple" if cumple else "No cumple",
                "Recomendación": recomendacion,
            })
        st.dataframe(resultados, use_container_width=True, hide_index=True)
        porcentaje = (aprobados / len(colores)) * 100
        m1, m2 = st.columns(2)
        m1.metric("Cumplimiento AA para texto estándar", f"{porcentaje:.1f}%")
        m2.metric("Elementos que cumplen AA", f"{aprobados} de {len(colores)}")
        if aprobados == len(colores):
            st.success("🌟 ¡Paleta 100% accesible para texto estándar AA!")
        else:
            st.warning("Revisa los elementos que no cumplen AA antes de llevar la paleta a producción.")

st.divider()
st.caption("Analista Colores SLRR · Cálculo de contraste basado en las fórmulas WCAG 2.1 implementadas en el proyecto.")
