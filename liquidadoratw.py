import streamlit as st
from PIL import Image # Asegúrate de que Pillow esté instalado (pip install Pillow)

st.set_page_config(page_title="Calculadora de Facturas ATW", layout="centered")

# --- Agrega esta sección para el logo ---
try:
    logo = Image.open('LOGO 2.png')
    st.image(logo, width=200) # Ajusta el 'width' (ancho) si lo necesitas para que se vea bien
except FileNotFoundError:
    st.warning("⚠️ No se encontró el archivo del logo. Asegúrate de que el nombre del archivo sea correcto y esté en la misma carpeta.")
# ----------------------------------------

st.title("💰 Calculadora de Valor a Pagar por Cliente ATW")
st.markdown("---")
st.write("¡Hola Equipo ATW! Usa esta herramienta para calcular el valor final a pagar de tus facturas.")

st.header("1. Ingreso de Valores de la Factura")
# INGRESAR VALOR DE LA FACTURA
subtotal_descuento = st.number_input("Por favor, ingrese el **SUBTOTAL - DESCUENTO**:", min_value=0.0, format="%.2f", value=0.0, key="subtotal")
iva = st.number_input("Ahora, ingrese el **valor del IVA**:", min_value=0.0, format="%.2f", value=0.0, key="iva")

st.markdown("---")
st.header("2. Preguntas sobre Descuentos y Retenciones")
st.write("Marca las casillas si aplican las siguientes condiciones:")

# PREGUNTA SOBRE DESCUENTOS DE LA FACTURA
tiene_rete_fuente = st.checkbox("¿El cliente tiene **Retención en la Fuente**?")
tiene_rete_iva = st.checkbox("¿El cliente tiene **Retención de IVA**?")
tiene_descuento_pp = st.checkbox("¿El cliente tiene **Descuento por Pronto Pago (PP)**?")

porcentaje_descuento_pp = 0.0
if tiene_descuento_pp:
    porcentaje_descuento_pp = st.number_input(
        "Ingrese el número del porcentaje de Descuento por Pronto Pago (Máximo el **3%**):",
        min_value=0.0,
        max_value=3.0, # Límite superior del 3%
        value=0.0,
        format="%.2f",
        key="descuento_pp_perc"
    )
    if porcentaje_descuento_pp > 3.0:
        st.warning("⚠️ El porcentaje de Descuento por Pronto Pago no debe exceder el 3%.")
    if porcentaje_descuento_pp < 0:
        st.warning("⚠️ El porcentaje de Descuento por Pronto Pago no puede ser negativo.")

# --- Cálculos antes de mostrar los resultados ---
# RETE FUENTE
valor_rete_fuente = 0.0
if tiene_rete_fuente:
    valor_rete_fuente = subtotal_descuento * 0.025  # 2.5% es 0.025

# RETE IVA
valor_rete_iva = 0.0
if tiene_rete_iva:
    valor_rete_iva = iva * 0.15  # 15% es 0.15

# DESCUENTO PP
valor_descuento_pp = 0.0
if tiene_descuento_pp:
    valor_descuento_pp = subtotal_descuento * (porcentaje_descuento_pp / 100)
else: # Si no tiene descuento PP, aseguramos que el porcentaje y valor sean 0 para el cálculo final.
    porcentaje_descuento_pp = 0.0
    valor_descuento_pp = 0.0

# Realizar operaciones para obtener los valores netos
subtotal_neto = subtotal_descuento - valor_rete_fuente - valor_descuento_pp
iva_neto = iva - valor_rete_iva

# Calcular el valor total a pagar
valor_a_pagar = subtotal_neto + iva_neto

st.markdown("---")
st.header("3. Resumen y Cálculo Final del Valor a Pagar")

st.subheader("Detalle del Subtotal (sin IVA):")
st.write(f"- **Subtotal - Descuento inicial:** ${subtotal_descuento:,.2f}")
if tiene_rete_fuente:
    st.write(f"- **Retención en la Fuente (2.5%):** -${valor_rete_fuente:,.2f}")
if tiene_descuento_pp:
    st.write(f"- **Descuento por Pronto Pago ({porcentaje_descuento_pp:.2f}%):** -${valor_descuento_pp:,.2f}")
st.success(f"**Valor Final del Subtotal:** ${subtotal_neto:,.2f}")

st.subheader("Detalle del IVA:")
st.write(f"- **IVA inicial:** ${iva:,.2f}")
if tiene_rete_iva:
    st.write(f"- **Retención de IVA (15%):** -${valor_rete_iva:,.2f}")
st.success(f"**Valor Final del IVA:** ${iva_neto:,.2f}")

st.markdown("---")
st.markdown(f"## **VALOR TOTAL A PAGAR POR EL CLIENTE: ${valor_a_pagar:,.2f}**")

st.markdown("---")
st.header("4. Resumen de Aplicaciones (informativo)")
st.write(f"Retención en la Fuente aplicada: **{'Sí' if tiene_rete_fuente else 'No'}**")
st.write(f"Retención de IVA aplicada: **{'Sí' if tiene_rete_iva else 'No'}**")
st.write(f"Descuento por Pronto Pago aplicado: **{'Sí' if tiene_descuento_pp else 'No'}**")
if tiene_descuento_pp:
    st.write(f"Porcentaje de Descuento PP ingresado: **{porcentaje_descuento_pp:.2f}%**")
    
st.markdown("---")
st.caption("Hecho por Cartera ATW Internacional.")
