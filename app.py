import streamlit as st
from pymongo import MongoClient
import pandas as pd
from datetime import datetime

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================

st.set_page_config(
    page_title="Biblioteca CBTis 134",
    page_icon="📚",
    layout="wide"
)

# ==========================================
# CONEXIÓN A MONGODB ATLAS
# ==========================================

URI = st.secrets["MONGO_URI"]

@st.cache_resource
def init_connection():
    return MongoClient(URI)

try:
    cliente = init_connection()

    db = cliente["ProyectoAndy"]

    coleccion_libros = db["Libros"]
    coleccion_usuarios = db["Usuarios"]
    coleccion_prestamos = db["Prestamos"]

except Exception as e:
    st.error(f"Error al conectar con MongoDB: {e}")

# ==========================================
# CARGAR DATOS
# ==========================================

libros = list(coleccion_libros.find())
usuarios = list(coleccion_usuarios.find())
prestamos = list(coleccion_prestamos.find())

df_libros = pd.DataFrame(libros)
df_usuarios = pd.DataFrame(usuarios)
df_prestamos = pd.DataFrame(prestamos)

# ==========================================
# TITULO
# ==========================================

st.title("📚 Sistema de Gestión de Biblioteca")
st.write("Dashboard Analítico desarrollado con MongoDB Atlas, Pandas y Streamlit")

st.divider()

# ==========================================
# MÉTRICAS
# ==========================================

total_libros = len(df_libros)
total_usuarios = len(df_usuarios)
total_prestamos = len(df_prestamos)

libros_disponibles = 0

if "disponible" in df_libros.columns:
    libros_disponibles = len(
        df_libros[df_libros["disponible"] == True]
    )

col1, col2, col3, col4 = st.columns(4)

col1.metric("📚 Libros", total_libros)
col2.metric("👤 Usuarios", total_usuarios)
col3.metric("📖 Préstamos", total_prestamos)
col4.metric("✅ Disponibles", libros_disponibles)

st.divider()

# ==========================================
# MENÚ PRINCIPAL
# ==========================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Dashboard",
    "👤 Usuarios",
    "📚 Libros",
    "ℹ️ Acerca"
])

# ==========================================
# DASHBOARD
# ==========================================

with tab1:

    st.header("📊 Estadísticas Generales")

    col_a, col_b = st.columns(2)

    with col_a:

        st.subheader("📚 Libros por Categoría")

        if "categoria" in df_libros.columns:

            categorias = (
                df_libros["categoria"]
                .value_counts()
            )

            st.bar_chart(categorias)

    with col_b:

        st.subheader("👤 Usuarios por Tipo")

        if "tipo_usuario" in df_usuarios.columns:

            tipos = (
                df_usuarios["tipo_usuario"]
                .value_counts()
            )

            st.bar_chart(tipos)

    st.divider()

    st.subheader("📖 Estado de Préstamos")

    if "estado" in df_prestamos.columns:

        estados = (
            df_prestamos["estado"]
            .value_counts()
        )

        st.bar_chart(estados)

# ==========================================
# USUARIOS
# ==========================================

with tab2:

    subtab1, subtab2 = st.tabs([
        "🔍 Ver Usuarios",
        "➕ Agregar Usuario"
    ])

    # -------------------------
    # VER USUARIOS
    # -------------------------

    with subtab1:

        st.header("Lista de Usuarios")

        if not df_usuarios.empty:

            mostrar = df_usuarios.copy()

            if "_id" in mostrar.columns:
                mostrar["_id"] = mostrar["_id"].astype(str)

            st.dataframe(
                mostrar,
                use_container_width=True
            )

        else:
            st.warning("No hay usuarios registrados.")

    # -------------------------
    # AGREGAR USUARIO
    # -------------------------

    with subtab2:

        st.header("Registrar Nuevo Usuario")

        with st.form("form_usuario"):

            col1, col2 = st.columns(2)

            with col1:

                nombre = st.text_input("Nombre")
                apellido = st.text_input("Apellido")

                tipo_usuario = st.selectbox(
                    "Tipo de Usuario",
                    [
                        "estudiante",
                        "docente",
                        "administrativo"
                    ]
                )

            with col2:

                telefono = st.text_input("Teléfono")
                correo = st.text_input("Correo")
                direccion = st.text_input("Dirección")

            guardar = st.form_submit_button(
                "Guardar Usuario"
            )

            if guardar:

                nuevo_usuario = {

                    "nombre": nombre,
                    "apellido": apellido,
                    "tipo_usuario": tipo_usuario,
                    "telefono": telefono,
                    "correo": correo,
                    "direccion": direccion,
                    "fecha_registro": datetime.now().strftime("%Y-%m-%d"),
                    "activo": True
                }

                coleccion_usuarios.insert_one(
                    nuevo_usuario
                )

                st.success(
                    "✅ Usuario agregado correctamente"
                )

                st.balloons()

# ==========================================
# LIBROS
# ==========================================

with tab3:

    st.header("📚 Catálogo de Libros")

    if not df_libros.empty:

        mostrar_libros = df_libros.copy()

        if "_id" in mostrar_libros.columns:
            mostrar_libros["_id"] = mostrar_libros["_id"].astype(str)

        st.dataframe(
            mostrar_libros,
            use_container_width=True
        )

    else:
        st.warning("No hay libros registrados.")

# ==========================================
# ACERCA DEL PROYECTO
# ==========================================

with tab4:

    st.header("ℹ️ Información del Proyecto")

    st.info("""
    Sistema de Gestión de Biblioteca desarrollado
    con Python, MongoDB Atlas, Pandas y Streamlit.

    Funciones principales:

    ✅ Gestión de usuarios

    ✅ Visualización de libros

    ✅ Estadísticas analíticas

    ✅ Conexión en la nube con MongoDB Atlas

    ✅ Dashboard interactivo
    """)

    st.success(
        "Proyecto Final - CBTis 134 📚"
    )
