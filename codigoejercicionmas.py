import streamlit as st
import pandas as pd
import requests

# Configuración inicial
st.set_page_config(page_title="App Multi-páginas", layout="wide")

# Función para cargar datos desde una URL
def load_data(url):
    try:
        # Obtener datos desde la URL
        response = requests.get(url)
        response.raise_for_status()  # Verifica si hubo errores en la solicitud

        # Convertir JSON a DataFrame
        data = pd.json_normalize(response.json())

        # Traducir las columnas al español
        translations = {
            "name.common": "Nombre",
            "name.official": "Nombre Oficial",
            "population": "Población",
            "area": "Área",
            "flag": "Bandera",
            "currencies": "Monedas",
            "languages": "Idiomas",
            "capital": "Capital",
            "region": "Región",
            "subregion": "Subregión",
            "borders": "Fronteras",
            "timezones": "Husos Horarios",
            "demonyms.eng.f": "Gentilicio (Femenino)",
            "demonyms.eng.m": "Gentilicio (Masculino)"
        }
        data.rename(columns=translations, inplace=True)

        # Intentar convertir columnas numéricas
        for col in ["Población", "Área"]:
            if col in data.columns:
                data[col] = pd.to_numeric(data[col], errors="coerce")

        return data, None
    except Exception as e:
        return None, str(e)

# Página de inicio
def home():
    st.title("Visualizacion intreractiva de datos con streamlit y REST countries API")
    st.write("Usa el menú de la izquierda para navegar entre las secciones.")
    st.write("1. Carga datos desde una URL en la página 'Cargar Datos'.")
    st.write("2. Visualiza gráficos en la página 'Gráficos'.")
    st.image(
        "data:image/png;base64,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",
        use_column_width=True,
    )

# Página para cargar datos
def cargar_datos():
    st.title("Cargar Datos desde una URL")
    default_url = "https://restcountries.com/v3.1/all?fields=name,population,area,flag,currencies,languages,capital,region,subregion,borders,timezones,demonyms"
    url = st.text_input("Introduce la URL de los datos:", value=default_url)
    if st.button("Cargar Datos"):
        if url:
            data, error = load_data(url)
            if error:
                st.error(f"Error al cargar los datos: {error}")
            else:
                st.session_state["data"] = data
                st.success("Datos cargados exitosamente.")
                st.write("Vista previa de los datos:")
                st.dataframe(data)
        else:
            st.warning("Por favor, introduce una URL válida.")

# Página para gráficos
def graficos():
    st.title("Visualización de Gráficos")
    if "data" not in st.session_state:
        st.warning("Primero carga datos en la página 'Cargar Datos'.")
        return

    data = st.session_state["data"]
    numeric_columns = data.select_dtypes(include=["float64", "int64"]).columns

    if numeric_columns.empty:
        st.warning("El dataset no contiene columnas numéricas para graficar.")
        return

    selected_columns = st.multiselect(
        "Selecciona las columnas numéricas para graficar:",
        options=numeric_columns,
        format_func=lambda x: x.replace("_", " ")  # Formato legible
    )

    chart_type = st.selectbox(
        "Selecciona el tipo de gráfico:",
        ["Selecciona una opción", "Línea", "Barras", "Histograma", "Dispersión"],
    )

    if st.button("Generar Gráfico"):
        if selected_columns and chart_type != "Selecciona una opción":
            fig, ax = plt.subplots()
            if chart_type == "Línea":
                for col in selected_columns:
                    ax.plot(data.index, data[col], label=col)
                ax.legend()
                ax.set_title("Gráfico de Línea")
            elif chart_type == "Barras":
                if len(selected_columns) == 1:
                    ax.bar(data.index, data[selected_columns[0]])
                    ax.set_title("Gráfico de Barras")
                else:
                    st.warning("Selecciona solo una columna para un gráfico de barras.")
            elif chart_type == "Histograma":
                for col in selected_columns:
                    ax.hist(data[col].dropna(), bins=20, alpha=0.5, label=col)
                ax.legend()
                ax.set_title("Histograma")
            elif chart_type == "Dispersión":
                if len(selected_columns) == 2:
                    ax.scatter(data[selected_columns[0]], data[selected_columns[1]])
                    ax.set_xlabel(selected_columns[0])
                    ax.set_ylabel(selected_columns[1])
                    ax.set_title("Gráfico de Dispersión")
                else:
                    st.warning("Selecciona exactamente dos columnas para un gráfico de dispersión.")
            st.pyplot(fig)
        else:
            st.warning("Por favor, selecciona columnas y un tipo de gráfico.")

# Configuración de navegación
pages = {
    "Inicio": home,
    "Cargar Datos": cargar_datos,
    "Gráficos": graficos,
}

st.sidebar.title("Navegación")
selected_page = st.sidebar.radio("Selecciona una página:", list(pages.keys()))
pages[selected_page]()
