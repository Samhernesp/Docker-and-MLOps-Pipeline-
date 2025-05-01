import streamlit as st

def diagnosticar(edad, genero, tipo_sangre, presion_sistolica, presion_diastolica, ejercicio_mensual):
    # Lógica ampliada del modelo simulado
    riesgo_base = 0
    
    # Factor de riesgo por edad
    if edad > 60:
        riesgo_base += 1
    elif edad > 40:
        riesgo_base += 0.5
        
    # Factor de riesgo por género
    if genero == "Masculino":
        riesgo_base += 0.3
        
    # Factor de riesgo por tipo de sangre
    if tipo_sangre in ["AB", "B"]:
        riesgo_base += 0.4
        
    # Clasificación presión arterial
    if presion_sistolica >= 180 or presion_diastolica >= 120:
        return "CRISIS HIPERTENSIVA"
    elif (130 <= presion_sistolica < 180) or (80 <= presion_diastolica < 120):
        riesgo_base += 1.5
    else:
        riesgo_base -= 0.5
        
    # Factor de ejercicio
    if ejercicio_mensual < 8:
        riesgo_base += 0.7
    elif ejercicio_mensual < 15:
        riesgo_base += 0.3
        
    # Determinación final
    if riesgo_base >= 2.5:
        return "ENFERMEDAD AGUDA"
    elif riesgo_base >= 1.8:
        return "ENFERMEDAD CRÓNICA"
    elif riesgo_base >= 1.0:
        return "ENFERMEDAD LEVE"
    else:
        return "NO ENFERMO"


st.set_page_config(page_title="Diagnóstico Médico", page_icon="🩺")

st.title("Sistema de Diagnóstico Médico")
st.markdown("Ingrese los datos del paciente:")

with st.form("diagnostico_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        edad = st.number_input("Edad (años)", min_value=0, max_value=120, step=1)
        genero = st.selectbox("Género", ["Masculino", "Femenino"])
        tipo_sangre = st.selectbox("Tipo de sangre", ["A", "B", "AB", "O"])
        
    with col2:
        sistolica = st.number_input("Presión Sistólica (mm Hg)", 
                                   min_value=50, max_value=300, 
                                   step=1, help="Valor superior de la presión arterial")
        diastolica = st.number_input("Presión Diastólica (mm Hg)", 
                                    min_value=30, max_value=200, 
                                    step=1, help="Valor inferior de la presión arterial")
        ejercicio = st.number_input("Días de ejercicio al mes", 
                                   min_value=0, max_value=31, 
                                   step=1, help="Días promedio de actividad física")
    
    submitted = st.form_submit_button("Generar diagnóstico")
    
    if submitted:
        resultado = diagnosticar(edad, genero, tipo_sangre, sistolica, diastolica, ejercicio)
        st.subheader("Resultado del diagnóstico:")
        
        if resultado == "NO ENFERMO":
            st.success(f"✅ {resultado}")
        elif resultado == "ENFERMEDAD LEVE":
            st.warning(f"⚠️ {resultado} - Recomendación: Control periódico")
        elif resultado == "ENFERMEDAD CRÓNICA":
            st.error(f"🚨 {resultado} - Recomendación: Tratamiento especializado")
        else:
            st.error(f"⛑️ {resultado} - Recomendación: Atención inmediata")
