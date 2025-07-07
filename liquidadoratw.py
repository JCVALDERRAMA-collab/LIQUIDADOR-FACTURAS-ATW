import streamlit as st
from PIL import Image
import urllib.parse
import json # Importa el módulo json para escapar el texto

st.set_page_config(page_title="Calculadora de Facturas ATW", layout="centered")

# --- Agrega esta sección para el logo ---
try:
    logo = Image.open('LOGO 2.png')
    st.image(logo, width=200)
except FileNotFoundError:
    st.warning("⚠️ No se encontró el archivo del logo. Asegúrate de que el nombre del archivo sea correcto y esté en la misma carpeta.")
# ----------------------------------------

st.title("💰 Calculadora de Valor a Pagar por Cliente ATW")
st.markdown("---")
st.write("¡Hola Equipo ATW! Usa esta herramienta para calcular el valor final a pagar de tus facturas.")

st.header("1. Ingreso de Valores de la Factura")
subtotal_descuento = st.number_input("Por favor, ingrese el **SUBTOTAL - DESCUENTO**:", min_value=0.0, format="%.2f", value=0.0, key="subtotal")
iva = st.number_input("Ahora, ingrese el **valor del IVA**:", min_value=0.0, format="%.2f", value=0.0, key="iva")

st.markdown("---")
st.header("2. Preguntas sobre Descuentos y Retenciones")
st.write("Marca las casillas si aplican las siguientes condiciones:")

tiene_rete_fuente = st.checkbox("¿El cliente tiene **Retención en la Fuente**?")
tiene_rete_iva = st.checkbox("¿El cliente tiene **Retención de IVA**?")
tiene_descuento_pp = st.checkbox("¿El cliente tiene **Descuento por Pronto Pago (PP)**?")

porcentaje_descuento_pp = 0.0
if tiene_descuento_pp:
    porcentaje_descuento_pp = st.number_input(
        "Ingrese el número del porcentaje de Descuento por Pronto Pago (Máximo el **3%**):",
        min_value=0.0,
        max_value=3.0,
        value=0.0,
        format="%.2f",
        key="descuento_pp_perc"
    )
    if porcentaje_descuento_pp > 3.0:
        st.warning("⚠️ El porcentaje de Descuento por Pronto Pago no debe exceder el 3%.")
    if porcentaje_descuento_pp < 0:
        st.warning("⚠️ El porcentaje de Descuento por Pronto Pago no puede ser negativo.")

# --- Cálculos antes de mostrar los resultados ---
valor_rete_fuente = 0.0
if tiene_rete_fuente:
    if subtotal_descuento >= 498000.00:
        valor_rete_fuente = subtotal_descuento * 0.025
    else:
        st.warning("⚠️ El Subtotal - Descuento debe ser mayor o igual a $498,000 para aplicar Retención en la Fuente.")
        tiene_rete_fuente = False

valor_rete_iva = 0.0
if tiene_rete_iva:
    valor_rete_iva = iva * 0.15

valor_descuento_pp = 0.0
if tiene_descuento_pp:
    valor_descuento_pp = subtotal_descuento * (porcentaje_descuento_pp / 100)
else:
    porcentaje_descuento_pp = 0.0
    valor_descuento_pp = 0.0

subtotal_neto = subtotal_descuento - valor_rete_fuente - valor_descuento_pp
iva_neto = iva - valor_rete_iva
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

nit = st.text_input("Ingrese el **NIT** del cliente:", key="nit_cliente")
numero_factura = st.text_input("Ingrese el **Número de Factura**:", key="num_factura")

campos_obligatorios_completos = bool(nit) and bool(numero_factura)

if not campos_obligatorios_completos:
    st.warning("Por favor, complete los campos de **NIT** y **Número de Factura** para habilitar los botones.")

st.markdown("---")

whatsapp_message_content = f"""
¡Hola! Aquí está el resumen de la factura:

* **NIT del Cliente:** {nit if nit else 'No especificado'}
* **Número de Factura:** {numero_factura if numero_factura else 'No especificado'}
* **Subtotal - Descuento inicial:** ${subtotal_descuento:,.2f}
* **IVA inicial:** ${iva:,.2f}

---
**Detalle de Cálculos:**
* Valor Retención en la Fuente: -${valor_rete_fuente:,.2f}
* Valor Retención de IVA: -${valor_rete_iva:,.2f}
* Valor Descuento por Pronto Pago: -${valor_descuento_pp:,.2f}

---
**Valores Netos:**
* Valor Final del Subtotal: ${subtotal_neto:,.2f}
* Valor Final del IVA: ${iva_neto:,.2f}

---
**VALOR TOTAL A PAGAR POR EL CLIENTE: ${valor_a_pagar:,.2f}**

¡Gracias!
"""

# Botón para WhatsApp Cartera
if st.button("Enviar a WhatsApp Cartera", disabled=not campos_obligatorios_completos):
    encoded_message = urllib.parse.quote(whatsapp_message_content)
    whatsapp_url = f"https://wa.me/573173003834?text={encoded_message}"
    st.markdown(f'<a href="{whatsapp_url}" target="_blank" style="display: inline-block; padding: 12px 20px; background-color: #25D366; color: white; text-align: center; text-decoration: none; font-size: 16px; border-radius: 8px; border: none; cursor: pointer;">Abrir WhatsApp con el resumen (Cartera)</a>', unsafe_allow_html=True)

# Botón para WhatsApp Cliente
if st.button("Enviar a WhatsApp Cliente", disabled=not campos_obligatorios_completos):
    encoded_message = urllib.parse.quote(whatsapp_message_content)
    whatsapp_url = f"https://wa.me/?text={encoded_message}"
    st.markdown(f'<a href="{whatsapp_url}" target="_blank" style="display: inline-block; padding: 12px 20px; background-color: #25D366; color: white; text-align: center; text-decoration: none; font-size: 16px; border-radius: 8px; border: none; cursor: pointer;">Abrir WhatsApp con el resumen (Cliente)</a>', unsafe_allow_html=True)

st.markdown("---")

# --- Nuevo Botón para Copiar al Portapapeles (Estrategia Mejorada) ---

# 1. Escapar el texto para que sea seguro dentro de un atributo HTML 'data-*'
#    json.dumps() es perfecto para esto, ya que convierte la cadena de Python
#    en una representación de cadena JSON válida, escapando comillas, saltos de línea, etc.
escaped_text_for_html = json.dumps(whatsapp_message_content)

# Crea un ID único para el botón
button_id = "copyButton"
message_div_id = "copyMessage"

# Inyecta el botón y el script JavaScript
st.markdown(f"""
    <button id="{button_id}" 
            data-text-to-copy='{escaped_text_for_html}' 
            style="background-color: #007bff; color: white; padding: 12px 20px; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; transition: background-color 0.3s ease;"
            {"disabled" if not campos_obligatorios_completos else ""}>
        Copiar Resumen al Portapapeles
    </button>
    <div id="{message_div_id}" style="margin-top: 10px; color: green; font-weight: bold;"></div>

    <script>
        const copyButton = document.getElementById('{button_id}');
        const copyMessage = document.getElementById('{message_div_id}');
        
        // Asignar el evento onclick SOLO si el botón existe (para evitar errores en la carga inicial)
        if (copyButton) {{
            copyButton.onclick = async function() {{
                // Leer el texto del atributo data-text-to-copy
                // JSON.parse() es necesario para "desescapar" la cadena JSON a una cadena JavaScript normal
                const text = JSON.parse(this.dataset.textToCopy); 
                
                try {{
                    await navigator.clipboard.writeText(text);
                    copyMessage.textContent = '¡Copiado al portapapeles!';
                    setTimeout(() => {{
                        copyMessage.textContent = '';
                    }}, 2000);
                }} catch (err) {{
                    console.error('Error al copiar:', err);
                    copyMessage.textContent = 'Error al copiar. Asegúrate de estar en HTTPS o localhost.';
                    copyMessage.style.color = 'red';
                    // Mensajes de error específicos para el usuario
                    if (err.name === 'NotAllowedError') {{
                        copyMessage.textContent = 'Permiso denegado para copiar. Habilita el permiso en tu navegador.';
                    }} else if (window.location.protocol !== 'https:' && window.location.hostname !== 'localhost') {{
                         copyMessage.textContent = 'Error: La copia solo funciona en HTTPS o localhost.';
                    }}
                }}
            }};
        }} else {{
            console.error("No se encontró el botón de copiar con ID:", '{button_id}');
        }}
    </script>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption("Hecho por Cartera ATW Internacional.")
