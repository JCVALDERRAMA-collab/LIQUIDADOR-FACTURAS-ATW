import streamlit as st
from PIL import Image # Asegúrate de que Pillow esté instalado (pip install Pillow)
import urllib.parse # Para codificar la URL del mailto
from st_copy_to_clipboard import st_copy_to_clipboard # ¡Nuevo! Para copiar al portapapeles del navegador

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
    # Nueva condición: Subtotal - Descuento debe ser mayor o igual a 498,000
    if subtotal_descuento >= 498000.00:
        valor_rete_fuente = subtotal_descuento * 0.025  # 2.5% es 0.025
    else:
        st.warning("⚠️ El Subtotal - Descuento debe ser mayor o igual a $498,000 para aplicar Retención en la Fuente.")
        tiene_rete_fuente = False # Desactiva la retención si no cumple la condición

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
st.header("3. Resumen de Aplicaciones (informativo)")
st.write(f"Retención en la Fuente aplicada: **{'Sí' if tiene_rete_fuente else 'No'}**")
st.write(f"Retención de IVA aplicada: **{'Sí' if tiene_rete_iva else 'No'}**")
st.write(f"Descuento por Pronto Pago aplicado: **{'Sí' if tiene_descuento_pp else 'No'}**")
if tiene_descuento_pp:
    st.write(f"Porcentaje de Descuento PP ingresado: **{porcentaje_descuento_pp:.2f}%**")

st.markdown("---")
st.header("4. Resumen y Cálculo Final del Valor a Pagar")

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

st.markdown(f"## **VALOR TOTAL A PAGAR POR EL CLIENTE: ${valor_a_pagar:,.2f}**")

# Nuevos cuadros de texto para NIT y Número de Factura
nonbre razón social = st.text_input("Ingrese el **Razón Social** del cliente:", key="nom_razonsocial")
nit = st.text_input("Ingrese el **NIT** del cliente:", key="nit_cliente")
numero_factura = st.text_input("Ingrese el **Número de Factura**:", key="num_factura")

campos_obligatorios_completos = bool(nit) and bool(numero_factura)

if not campos_obligatorios_completos:
    st.warning("Por favor, complete los campos de **NIT** y **Número de Factura** para habilitar los botones de WhatsApp.")

st.markdown("---")

# Función para generar el mensaje de WhatsApp
def generar_whatsapp_message(nit_cliente, num_factura, sub_desc, iva_val, rete_fuente_val, rete_iva_val, desc_pp_val, sub_neto_val, iva_neto_val, total_pagar_val):
    return f"""
¡Hola! Aquí está el resumen de la factura:

* **NIT del Cliente:** {nit_cliente if nit_cliente else 'No especificado'}
* **Número de Factura:** {num_factura if num_factura else 'No especificado'}
* **Subtotal - Descuento inicial:** ${sub_desc:,.2f}
* **IVA inicial:** ${iva_val:,.2f}

---
**Detalle de Cálculos:**
* Valor Retención en la Fuente: -${rete_fuente_val:,.2f}
* Valor Retención de IVA: -${rete_iva_val:,.2f}
* Valor Descuento por Pronto Pago: -${desc_pp_val:,.2f}

---
**Valores Netos:**
* Valor Final del Subtotal: ${sub_neto_val:,.2f}
* Valor Final del IVA: ${iva_neto_val:,.2f}

---
**VALOR TOTAL A PAGAR POR EL CLIENTE: ${total_pagar_val:,.2f}**

¡Gracias!
"""

# Genera el mensaje una sola vez después de todos los cálculos
whatsapp_message_final = generar_whatsapp_message(
    nit, numero_factura, subtotal_descuento, iva,
    valor_rete_fuente, valor_rete_iva, valor_descuento_pp,
    subtotal_neto, iva_neto, valor_a_pagar
)

# Botón para WhatsApp Cartera
if st.button("Enviar a WhatsApp Cartera", disabled=not campos_obligatorios_completos):
    encoded_message = urllib.parse.quote(whatsapp_message_final)
    whatsapp_url = f"https://wa.me/573173003834?text={encoded_message}"
    st.markdown(f'<a href="{whatsapp_url}" target="_blank" style="display: inline-block; padding: 12px 20px; background-color: #25D366; color: white; text-align: center; text-decoration: none; font-size: 16px; border-radius: 8px; border: none; cursor: pointer;">Abrir WhatsApp Cartera con el resumen</a>', unsafe_allow_html=True)

# Botón para WhatsApp Cliente
if st.button("Enviar a WhatsApp Cliente", disabled=not campos_obligatorios_completos):
    encoded_message = urllib.parse.quote(whatsapp_message_final)
    whatsapp_url = f"https://wa.me/?text={encoded_message}" # Sin número específico para que el usuario elija
    st.markdown(f'<a href="{whatsapp_url}" target="_blank" style="display: inline-block; padding: 12px 20px; background-color: #25D366; color: white; text-align: center; text-decoration: none; font-size: 16px; border-radius: 8px; border: none; cursor: pointer;">Abrir WhatsApp Cliente con el resumen</a>', unsafe_allow_html=True)

# --- Nuevo botón para copiar al portapapeles ---
if st.button("Copiar Información", disabled=not campos_obligatorios_completos):
    # Ya no necesitamos el try-except de pyperclip, st_copy_to_clipboard maneja esto internamente
    st_copy_to_clipboard(whatsapp_message_final)
    st.success("¡Mensaje copiado al portapapeles! Ya puedes pegarlo donde necesites.")

st.markdown("---")
st.caption("Hecho por Cartera ATW Internacional.")
