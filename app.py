import json
from flask import Flask, request, jsonify
from difflib import SequenceMatcher

# Crear la instancia de Flask
app = Flask(__name__)

# Variables globales para almacenar los datos JSON
productos_combined = []
productos_meli = []
productos_page = []

def cargar_archivos_json():
    """Cargar los 3 archivos JSON de productos"""
    global productos_combined, productos_meli, productos_page
    
    try:
        # Cargar combined.json
        with open('combined.json', 'r', encoding='utf-8') as f:
            productos_combined = json.load(f)
        
        # Cargar prod_meli.json
        with open('prod_meli.json', 'r', encoding='utf-8') as f:
            productos_meli = json.load(f)
        
        # Cargar prod_page.json
        with open('prod_page.json', 'r', encoding='utf-8') as f:
            productos_page = json.load(f)
            
        print("Archivos JSON de productos cargados exitosamente")
        
    except Exception as e:
        print(f"Error cargando archivos JSON: {e}")

def similarity(a, b):
    """Calcular similitud entre dos strings"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def buscar_productos_relevantes(mensaje, limite=5):
    """Buscar productos relevantes segun el mensaje del cliente"""
    mensaje_lower = mensaje.lower()
    productos_encontrados = []
    
    # Buscar en productos_combined
    for producto in productos_combined:
        score = 0
        
        # Buscar en nombre
        if similarity(mensaje_lower, producto.get('nombre', '')) > 0.3:
            score += similarity(mensaje_lower, producto.get('nombre', '')) * 2
        
        # Buscar en descripcion
        if similarity(mensaje_lower, producto.get('descripcion', '')) > 0.2:
            score += similarity(mensaje_lower, producto.get('descripcion', ''))
        
        # Buscar en detalles
        if similarity(mensaje_lower, producto.get('detalle_prod', '')) > 0.2:
            score += similarity(mensaje_lower, producto.get('detalle_prod', ''))
        
        # Buscar palabras clave especificas
        palabras_mensaje = mensaje_lower.split()
        for palabra in palabras_mensaje:
            if len(palabra) > 3:  # Solo palabras de mas de 3 caracteres
                if palabra in producto.get('nombre', '').lower():
                    score += 0.5
                if palabra in producto.get('descripcion', '').lower():
                    score += 0.3
        
        if score > 0.2:
            productos_encontrados.append({
                'producto': producto,
                'score': score,
                'fuente': 'combined'
            })
    
    # Buscar en productos_page
    for producto in productos_page:
        score = 0
        
        if similarity(mensaje_lower, producto.get('nombre', '')) > 0.3:
            score += similarity(mensaje_lower, producto.get('nombre', '')) * 2
        
        if similarity(mensaje_lower, producto.get('descripcion', '')) > 0.2:
            score += similarity(mensaje_lower, producto.get('descripcion', ''))
        
        palabras_mensaje = mensaje_lower.split()
        for palabra in palabras_mensaje:
            if len(palabra) > 3:
                if palabra in producto.get('nombre', '').lower():
                    score += 0.5
                if palabra in producto.get('descripcion', '').lower():
                    score += 0.3
        
        if score > 0.2:
            productos_encontrados.append({
                'producto': producto,
                'score': score,
                'fuente': 'page'
            })
    
    # Ordenar por score y limitar resultados
    productos_encontrados.sort(key=lambda x: x['score'], reverse=True)
    return productos_encontrados[:limite]

def generar_contexto_optimizado(productos):
    """Generar contexto resumido y optimizado solo con productos"""
    contexto_partes = []
    
    # Agregar productos mas relevantes
    if productos:
        contexto_partes.append("=== PRODUCTOS RELEVANTES ===")
        for item in productos[:5]:  # Los 5 mas relevantes
            producto = item['producto']
            contexto_partes.append(f"PRODUCTO: {producto.get('nombre', 'Sin nombre')}")
            if 'precio' in producto and producto['precio']:
                contexto_partes.append(f"Precio: ${producto['precio']}")
            contexto_partes.append(f"Descripcion: {producto.get('descripcion', '')[:200]}...")
            if 'beneficios' in producto and producto['beneficios']:
                contexto_partes.append(f"Beneficios: {producto['beneficios'][:150]}...")
            if 'detalle_prod' in producto and producto['detalle_prod']:
                contexto_partes.append(f"Detalles: {producto['detalle_prod'][:150]}...")
            contexto_partes.append("")
    
    return "\n".join(contexto_partes)

@app.route('/consultar', methods=['POST'])
def consultar():
    """
    Endpoint principal para recibir consultas de n8n y devolver contexto relevante
    """
    try:
        # Obtener el mensaje del cliente
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'error': 'Falta el campo "message" en la solicitud'
            }), 400
        
        mensaje = data['message'].strip()
        
        if not mensaje:
            return jsonify({
                'error': 'El mensaje no puede estar vacio'
            }), 400
        
        print(f"Consulta recibida: {mensaje}")
        
        # Buscar productos relevantes
        productos_relevantes = buscar_productos_relevantes(mensaje)
        
        # Generar contexto optimizado
        contexto = generar_contexto_optimizado(productos_relevantes)
        
        # Si no se encontro nada especifico, dar informacion general
        if not contexto.strip():
            contexto = """=== PRODUCTOS DISPONIBLES ===
Contamos con una amplia gama de productos para tortillerias y panaderias.
Por favor, se mas especifico en tu consulta para ayudarte mejor.
Puedes preguntar sobre productos, precios, beneficios o caracteristicas especificas."""
        
        print(f"Contexto generado: {len(contexto)} caracteres")
        
        return jsonify({
            'contexto': contexto,
            'productos_encontrados': len(productos_relevantes)
        })
        
    except Exception as e:
        print(f"Error en /consultar: {e}")
        return jsonify({
            'error': f'Error interno del servidor: {str(e)}'
        }), 500

@app.route('/', methods=['GET'])
def inicio():
    """Endpoint de inicio para verificar que el servidor esta funcionando"""
    return jsonify({
        'mensaje': 'Servidor Flask de consultas TIA funcionando correctamente',
        'endpoints_disponibles': ['/consultar'],
        'archivos_cargados': {
            'productos_combined': len(productos_combined),
            'productos_meli': len(productos_meli),
            'productos_page': len(productos_page)
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check para monitoreo"""
    return jsonify({
        'status': 'ok',
        'archivos_json': {
            'productos_combined': len(productos_combined),
            'productos_meli': len(productos_meli),
            'productos_page': len(productos_page)
        }
    })

# Cargar archivos JSON al iniciar la aplicacion
cargar_archivos_json()

if __name__ == '__main__':
    print("Iniciando servidor Flask para consultas TIA...")
    print("Endpoint principal: POST /consultar")
    print("Health check: GET /health")
    
    # Ejecutar en modo debug para desarrollo
    app.run(debug=True, host='0.0.0.0', port=5000)