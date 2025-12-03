import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from difflib import SequenceMatcher
import logging
import re

# Configurar logging detallado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Crear la instancia de Flask
app = Flask(__name__)
CORS(app)  # Habilitar CORS

# Variables globales para almacenar los datos JSON
productos_combined = []
productos_meli = []
productos_page = []

def cargar_archivos_json():
    """Cargar los 3 archivos JSON de productos"""
    global productos_combined, productos_meli, productos_page
    
    try:
        # Cargar combined.json
        try:
            with open('combined.json', 'r', encoding='utf-8') as f:
                productos_combined = json.load(f)
            logger.info(f"✅ combined.json cargado: {len(productos_combined)} productos")
        except FileNotFoundError:
            logger.warning("⚠️ combined.json no encontrado")
            productos_combined = []
        
        # Cargar prod_meli.json
        try:
            with open('prod_meli.json', 'r', encoding='utf-8') as f:
                productos_meli = json.load(f)
            logger.info(f"✅ prod_meli.json cargado: {len(productos_meli)} productos")
        except FileNotFoundError:
            logger.warning("⚠️ prod_meli.json no encontrado")
            productos_meli = []
        
        # Cargar prod_page.json
        try:
            with open('prod_page.json', 'r', encoding='utf-8') as f:
                productos_page = json.load(f)
            logger.info(f"✅ prod_page.json cargado: {len(productos_page)} productos")
        except FileNotFoundError:
            logger.warning("⚠️ prod_page.json no encontrado")
            productos_page = []
            
    except Exception as e:
        logger.error(f"❌ Error cargando archivos JSON: {e}")

def limpiar_texto(texto):
    """Limpiar y normalizar texto para búsqueda"""
    texto = texto.lower()
    # Remover acentos
    texto = re.sub(r'[áàäâ]', 'a', texto)
    texto = re.sub(r'[éèëê]', 'e', texto)
    texto = re.sub(r'[íìïî]', 'i', texto)
    texto = re.sub(r'[óòöô]', 'o', texto)
    texto = re.sub(r'[úùüû]', 'u', texto)
    texto = re.sub(r'[ñ]', 'n', texto)
    return texto.strip()

def similarity(a, b):
    """Calcular similitud entre dos strings"""
    return SequenceMatcher(None, limpiar_texto(a), limpiar_texto(b)).ratio()

def buscar_por_palabras_clave(mensaje_lower, producto):
    """Buscar coincidencias por palabras clave específicas"""
    score = 0
    
    # Palabras clave importantes
    palabras_mensaje = mensaje_lower.split()
    
    # Campos donde buscar
    campos_busqueda = [
        producto.get('nombre', ''),
        producto.get('descripcion', ''),
        producto.get('detalle_prod', ''),
        producto.get('beneficios', ''),
        ' '.join(producto.get('categorias', [])) if isinstance(producto.get('categorias'), list) else ''
    ]
    
    texto_completo = ' '.join(campos_busqueda).lower()
    
    # Buscar cada palabra del mensaje
    for palabra in palabras_mensaje:
        if len(palabra) > 3:  # Solo palabras significativas
            palabra_limpia = limpiar_texto(palabra)
            
            # Coincidencia exacta en nombre = alto score
            if palabra_limpia in limpiar_texto(producto.get('nombre', '')):
                score += 2.0
            
            # Coincidencia en descripción
            elif palabra_limpia in limpiar_texto(producto.get('descripcion', '')):
                score += 1.0
            
            # Coincidencia en otros campos
            elif palabra_limpia in limpiar_texto(texto_completo):
                score += 0.5
    
    return score

def buscar_productos_relevantes(mensaje, limite=5):
    """Buscar productos relevantes según el mensaje del cliente"""
    mensaje_lower = limpiar_texto(mensaje)
    productos_encontrados = []
    
    logger.info(f"🔍 Buscando productos para: '{mensaje}'")
    
    # Buscar en productos_combined
    for producto in productos_combined:
        score = 0
        
        # Búsqueda por similitud en nombre
        nombre_similarity = similarity(mensaje_lower, producto.get('nombre', ''))
        if nombre_similarity > 0.3:
            score += nombre_similarity * 3  # Peso alto al nombre
        
        # Búsqueda por similitud en descripción
        desc_similarity = similarity(mensaje_lower, producto.get('descripcion', ''))
        if desc_similarity > 0.2:
            score += desc_similarity * 1.5
        
        # Búsqueda por palabras clave
        keyword_score = buscar_por_palabras_clave(mensaje_lower, producto)
        score += keyword_score
        
        if score > 0.5:  # Umbral mínimo más alto
            productos_encontrados.append({
                'producto': producto,
                'score': score,
                'fuente': 'combined'
            })
    
    # Buscar en productos_page
    for producto in productos_page:
        score = 0
        
        nombre_similarity = similarity(mensaje_lower, producto.get('nombre', ''))
        if nombre_similarity > 0.3:
            score += nombre_similarity * 3
        
        desc_similarity = similarity(mensaje_lower, producto.get('descripcion', ''))
        if desc_similarity > 0.2:
            score += desc_similarity * 1.5
        
        keyword_score = buscar_por_palabras_clave(mensaje_lower, producto)
        score += keyword_score
        
        if score > 0.5:
            productos_encontrados.append({
                'producto': producto,
                'score': score,
                'fuente': 'page'
            })
    
    # Ordenar por score y eliminar duplicados por nombre
    productos_encontrados.sort(key=lambda x: x['score'], reverse=True)
    
    # Eliminar duplicados basándose en nombres similares
    productos_unicos = []
    nombres_vistos = set()
    
    for item in productos_encontrados:
        nombre = limpiar_texto(item['producto'].get('nombre', ''))
        if nombre not in nombres_vistos:
            nombres_vistos.add(nombre)
            productos_unicos.append(item)
    
    resultado = productos_unicos[:limite]
    logger.info(f"✅ Encontrados {len(resultado)} productos únicos relevantes")
    
    return resultado

def generar_contexto_optimizado(productos):
    """Generar contexto resumido y optimizado con productos"""
    if not productos:
        return ""
    
    contexto_partes = ["=== PRODUCTOS RELEVANTES ===\n"]
    
    for idx, item in enumerate(productos[:5], 1):  # Top 5 productos
        producto = item['producto']
        
        contexto_partes.append(f"{idx}. PRODUCTO: {producto.get('nombre', 'Sin nombre')}")
        
        # Precio (si existe)
        if 'precio' in producto and producto['precio']:
            precio = producto['precio']
            # Manejar diferentes formatos de precio
            if isinstance(precio, (int, float)):
                contexto_partes.append(f"   💰 Precio: ${precio:,.2f} MXN")
            else:
                contexto_partes.append(f"   💰 Precio: {precio}")
        
        # Descripción corta
        descripcion = producto.get('descripcion', '')[:200]
        if descripcion:
            contexto_partes.append(f"   📝 {descripcion}...")
        
        # Beneficios (si existen)
        beneficios = producto.get('beneficios', '')[:150]
        if beneficios:
            contexto_partes.append(f"   ✨ Beneficios: {beneficios}...")
        
        # Detalles (si existen)
        detalles = producto.get('detalle_prod', '')[:150]
        if detalles:
            contexto_partes.append(f"   🔍 Detalles: {detalles}...")
        
        # Presentación (si existe)
        presentacion = producto.get('presentacion', '')
        if presentacion:
            contexto_partes.append(f"   📦 Presentación: {presentacion}")
        
        contexto_partes.append("")  # Línea en blanco entre productos
    
    return "\n".join(contexto_partes)

@app.route('/consultar', methods=['POST'])
def consultar():
    """
    Endpoint principal para recibir consultas de n8n y devolver contexto relevante
    """
    try:
        # Obtener el mensaje del cliente
        data = request.get_json()
        
        logger.info(f"📨 Petición recibida: {data}")
        
        if not data:
            logger.warning("⚠️ No se recibió JSON")
            return jsonify({
                'error': 'No se recibió un JSON válido'
            }), 400
        
        if 'message' not in data:
            logger.warning("⚠️ Falta el campo 'message'")
            return jsonify({
                'error': 'Falta el campo "message" en la solicitud'
            }), 400
        
        mensaje = data['message'].strip()
        
        if not mensaje:
            logger.warning("⚠️ Mensaje vacío")
            return jsonify({
                'error': 'El mensaje no puede estar vacío'
            }), 400
        
        logger.info(f"💬 Procesando consulta: '{mensaje}'")
        
        # Buscar productos relevantes
        productos_relevantes = buscar_productos_relevantes(mensaje)
        
        # Generar contexto optimizado
        contexto = generar_contexto_optimizado(productos_relevantes)
        
        # Si no se encontró nada específico, dar información general
        if not contexto.strip():
            contexto = """=== INFORMACIÓN GENERAL TIA ===

Somos TIA (Tecnología en Ingredientes Alimenticios, S.A de C.V), empresa 100% mexicana.

🏭 NUESTROS PRODUCTOS:
• Mejoradores para tortillas y pan
• Conservadores para mayor vida útil
• Productos antiadherentes
• Aditivos especializados para panadería
• Insumos para tortillería

💡 Para ayudarte mejor, por favor especifica:
- ¿Qué tipo de producto buscas?
- ¿Para qué aplicación? (tortillas, pan, etc.)
- ¿Tienes alguna necesidad específica?"""
        
        logger.info(f"✅ Contexto generado: {len(contexto)} caracteres, {len(productos_relevantes)} productos encontrados")
        
        respuesta = {
            'contexto': contexto,
            'productos_encontrados': len(productos_relevantes),
            'status': 'success',
            'mensaje_original': mensaje
        }
        
        logger.info(f"📤 Enviando respuesta exitosa")
        
        return jsonify(respuesta), 200
        
    except Exception as e:
        logger.error(f"❌ Error en /consultar: {e}", exc_info=True)
        return jsonify({
            'error': f'Error interno del servidor: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/', methods=['GET'])
def inicio():
    """Endpoint de inicio para verificar que el servidor está funcionando"""
    return jsonify({
        'mensaje': '🚀 Servidor Flask de consultas TIA funcionando correctamente',
        'version': '2.0',
        'endpoints_disponibles': {
            '/consultar': 'POST - Consultar productos',
            '/health': 'GET - Health check',
            '/productos/stats': 'GET - Estadísticas de productos'
        },
        'archivos_cargados': {
            'productos_combined': len(productos_combined),
            'productos_meli': len(productos_meli),
            'productos_page': len(productos_page),
            'total': len(productos_combined) + len(productos_meli) + len(productos_page)
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check para monitoreo"""
    total_productos = len(productos_combined) + len(productos_meli) + len(productos_page)
    
    status = 'ok' if total_productos > 0 else 'warning'
    
    return jsonify({
        'status': status,
        'archivos_json': {
            'productos_combined': len(productos_combined),
            'productos_meli': len(productos_meli),
            'productos_page': len(productos_page),
            'total': total_productos
        },
        'mensaje': 'Servidor funcionando correctamente' if status == 'ok' else 'No hay productos cargados'
    })

@app.route('/productos/stats', methods=['GET'])
def productos_stats():
    """Endpoint para ver estadísticas de productos cargados"""
    return jsonify({
        'total_productos': len(productos_combined) + len(productos_meli) + len(productos_page),
        'por_fuente': {
            'combined': len(productos_combined),
            'mercadolibre': len(productos_meli),
            'pagina_web': len(productos_page)
        },
        'muestra_productos': [
            p.get('nombre', 'Sin nombre') 
            for p in (productos_combined + productos_page)[:10]
        ]
    })

# Cargar archivos JSON al iniciar la aplicación
cargar_archivos_json()

if __name__ == '__main__':
    logger.info("="*60)
    logger.info("🚀 Iniciando servidor Flask para consultas TIA")
    logger.info("="*60)
    logger.info("📍 Endpoint principal: POST /consultar")
    logger.info("🏥 Health check: GET /health")
    logger.info("📊 Estadísticas: GET /productos/stats")
    logger.info("="*60)
    
    # Mostrar resumen de productos cargados
    total = len(productos_combined) + len(productos_meli) + len(productos_page)
    logger.info(f"📦 Total productos cargados: {total}")
    logger.info(f"   - Combined: {len(productos_combined)}")
    logger.info(f"   - MercadoLibre: {len(productos_meli)}")
    logger.info(f"   - Página Web: {len(productos_page)}")
    logger.info("="*60)
    
    # Ejecutar servidor
    app.run(debug=True, host='0.0.0.0', port=5000)
