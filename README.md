# SLRR · Color Lab

Aplicación web en Python y Streamlit para analizar contraste cromático entre un color de fondo y colores de texto o elementos de una paleta.

## Funcionalidades
- Análisis individual de una combinación fondo/texto.
- Evaluación de paletas de hasta 12 elementos.
- Vista previa de la combinación seleccionada.
- Reporte tabular y descarga CSV.
- Interfaz visual tipo laboratorio digital: gradientes, paneles translúcidos y acentos cromáticos.

## Ejecución local
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Publicación
Sube `app.py`, `requirements.txt` y `README.md` al repositorio conectado a Streamlit Community Cloud. Al hacer commit en la rama configurada, Streamlit detectará los cambios y actualizará la aplicación.

## Nota de accesibilidad
El proyecto calcula el ratio de contraste con la fórmula de luminancia relativa sRGB y conserva los umbrales implementados: 7:1, 4.5:1 y 3:1. El umbral 3:1 no debe interpretarse como aprobación universal de componentes UI: el criterio aplicable depende del tipo de contenido y del requisito WCAG correspondiente.
