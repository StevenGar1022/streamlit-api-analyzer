import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Configuración de la interfaz de la aplicación
st.set_page_config(page_title="Analizador de Datos API", layout="wide")

st.title("Panel de Análisis de Publicaciones (JSONPlaceholder)")
st.write("Esta aplicación descarga datos reales de publicaciones de usuarios de internet y analiza sus métricas.")

# INTERACCIÓN
st.sidebar.header("Controles de Usuario")

# Selector interactivo para definir el color de la gráfica
color_grafico = st.sidebar.selectbox(
    "Selecciona el color del gráfico:",
    ["emerald", "crimson", "purple", "darkorange"]
)

# Mapeo de colores amigables para Matplotlib
colores_dict = {
    "emerald": "#2ecc71",
    "crimson": "#e74c3c",
    "purple": "#9b59b6",
    "darkorange": "#e67e22"
}

# Botón interactivo principal para ejecutar el proceso
boton_cargar = st.sidebar.button("Descargar y Analizar Datos")

if not boton_cargar:
    st.info("Presiona el botón 'Descargar y Analizar Datos' en la barra lateral para conectar con la API.")
else:
    #CONSULTA DIRECTA A LA API
    url_api = "https://jsonplaceholder.typicode.com/posts"
    
    with st.spinner("Conectando con los servidores de JSONPlaceholder..."):
        try:
            respuesta = requests.get(url_api, timeout=10)
            
            # Validación estricta del estado de conexión HTTP
            if respuesta.status_code == 200:
                datos_raw = respuesta.json()
                
                #PROCESAMOS LOS DATOS
                # Convertimos la lista de objetos JSON directamente en un DataFrame de Pandas
                df_posts = pd.DataFrame(datos_raw)
                
                # Traducimos las columnas originales para mostrarlas de manera organizada
                df_mostrar = df_posts.rename(columns={
                    "userId": "ID de Usuario",
                    "id": "ID de Publicación",
                    "title": "Título del Post",
                    "body": "Contenido"
                })
                
                # Calculamos el total de posts agrupados por cada ID de usuario
                conteo_usuarios = df_posts["userId"].value_counts().sort_index()
                
                # Creamos el diseño simétrico en dos columnas de Streamlit
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Base de Datos Adquirida")
                    # Desplegamos la tabla nativa de Pandas ajustable
                    st.dataframe(df_mostrar[["ID de Usuario", "ID de Publicación", "Título del Post"]], use_container_width=True)
                    
                with col2:
                    st.subheader("Gráfico de Rendimiento por Usuario")
                    
                    #GRÁFICAMOS
                    fig, ax = plt.subplots(figsize=(6, 4))
                    
                    # Creamos un gráfico de barras con el color seleccionado por el usuario
                    ax.bar(
                        [f"User {uid}" for uid in conteo_usuarios.index], 
                        conteo_usuarios.values, 
                        color=colores_dict[color_grafico], 
                        edgecolor="black"
                    )
                    
                    # Configuración estética de títulos y etiquetas del modelo
                    ax.set_title("Cantidad de Publicaciones Creadas por Usuario", fontsize=11, fontweight='bold')
                    ax.set_xlabel("Identificador de Usuario")
                    ax.set_ylabel("Total de Posts Escritos")
                    ax.set_ylim(0, max(conteo_usuarios.values) + 3)
                    ax.grid(axis='y', linestyle='--', alpha=0.5)
                    
                    # Ajustamos las etiquetas del eje X para que sean perfectamente legibles
                    plt.xticks(rotation=45, ha="right")
                    plt.tight_layout()
                    
                    # Desplegamos el gráfico sin errores dentro de la web
                    st.pyplot(fig)
            else:
                st.error(f"Error al conectar: El servidor respondió con código {respuesta.status_code}")
                
        except Exception as e:
            st.error(f"Error crítico de red: No se pudo establecer la conexión con la API pública: {e}")



            

