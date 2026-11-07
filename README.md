# Analista Colores SLRR

Aplicación web desarrollada con **Python y Streamlit** para analizar el contraste cromático entre colores de fondo y texto, y revisar paletas de diseño con los umbrales de accesibilidad WCAG 2.1 implementados en el proyecto.

## Funcionalidades

- **Análisis individual:** compara un color de fondo y un color de texto.
- **Evaluación de paleta:** compara un fondo principal con varios colores de texto o elementos de interfaz.
- **Vista previa:** muestra una simulación de texto sobre el color de fondo seleccionado.
- **Reporte:** presenta el ratio de contraste, la clasificación y una recomendación por combinación.

## Tecnologías

- Python
- Streamlit

## Ejecución local

1. Clona este repositorio o descarga sus archivos.
2. (Opcional, recomendado) Crea y activa un entorno virtual.
3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Ejecuta la aplicación:

   ```bash
   streamlit run app.py
   ```

5. Streamlit abrirá la aplicación en el navegador, normalmente en `http://localhost:8501`.

## Publicación en Streamlit Community Cloud

1. Sube `app.py`, `requirements.txt` y `README.md` a un repositorio de GitHub.
2. Entra a [Streamlit Community Cloud](https://share.streamlit.io/).
3. Selecciona **Create app** y conecta el repositorio.
4. Selecciona la rama que contiene el proyecto (normalmente `main`) y establece `app.py` como archivo principal.
5. Pulsa **Deploy**.

## Estructura del repositorio

```text
analista-colores-slrr/
├── app.py
├── README.md
└── requirements.txt
```

## Criterios de clasificación incluidos

La aplicación conserva los umbrales de clasificación que utiliza el código original:

- **7.0:1 o superior:** Superior (AAA).
- **4.5:1 o superior:** Alto (AA - texto normal).
- **3.0:1 o superior:** Básico (AA - texto grande / UI).
- **Menor que 3.0:1:** No cumple.

El porcentaje de cumplimiento de la paleta se calcula con el umbral de `4.5:1`, tal como en el programa original. Esta herramienta es un apoyo de evaluación; revisa también los requisitos aplicables al tamaño del texto y a los componentes de interfaz antes de aprobar una pieza.

## Proyecto

**Nombre:** Analista Colores SLRR  
**Área:** Diseño gráfico y desarrollo UI/UX  
**Tema:** Contraste cromático y accesibilidad
