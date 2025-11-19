# Servidor Flask para Consultas de Productos TIA

## Descripción
Servidor Flask que recibe mensajes desde n8n (por POST), lee archivos JSON con información de la empresa y productos, busca información relevante según el mensaje del cliente, y devuelve un texto filtrado optimizado para reducir el uso de tokens en OpenAI.

## Archivos JSON Procesados
- **empresa.json**: Datos generales de la empresa (servicios, horarios, contacto, etc.)
- **respuestas.json**: Respuestas específicas a preguntas frecuentes con mapeo de palabras clave
- **combined.json**: Catálogo completo de productos con detalles, precios, beneficios
- **prod_meli.json**: Productos con información de MercadoLibre
- **prod_page.json**: Productos con información de la página web

## Endpoint Principal

### POST /consultar
Recibe consultas de clientes y devuelve contexto relevante.

**Request:**
```json
{
  "message": "texto del cliente"
}
```

**Response:**
```json
{
  "contexto": "Información relevante encontrada y filtrada",
  "productos_encontrados": 3,
  "respuestas_encontradas": 1,
  "info_empresa_encontrada": 1
}
```

## Endpoints Adicionales

### GET /health
Health check del servidor.

**Response:**
```json
{
  "status": "ok",
  "archivos_json": {
    "empresa": true,
    "respuestas": true,
    "productos_combined": 150,
    "productos_meli": 200,
    "productos_page": 100
  }
}
```

### GET /
Información básica del servidor.

## Funcionalidades de Búsqueda

### 1. Búsqueda de Productos
- **Algoritmo**: Similitud de texto usando SequenceMatcher
- **Campos analizados**: nombre, descripción, detalles del producto
- **Score mínimo**: 0.2 para considerar relevante
- **Límite de resultados**: 5 productos más relevantes

### 2. Búsqueda de Respuestas Frecuentes
- **Mapeo de palabras clave**: Categorías predefinidas en respuestas.json
- **Coincidencias**: Búsqueda en keywords_mapping
- **Ejemplo**: "precio" → categoría "precios" → respuesta sobre costos

### 3. Búsqueda de Información de Empresa
- **Secciones disponibles**: contacto, horarios, servicios, equipo, certificaciones
- **Activación**: Por palabras clave específicas en la consulta

## Optimización de Contexto

El sistema genera contexto optimizado para reducir tokens:

1. **Límite de productos**: Máximo 3 productos más relevantes
2. **Límite de respuestas**: Máximo 2 respuestas frecuentes
3. **Truncado inteligente**: Descripciones limitadas a 150-200 caracteres
4. **Estructura clara**: Separado en secciones bien definidas

## Ejemplos de Uso

### Consulta de Productos
```bash
POST /consultar
{
  "message": "Necesito un mejorador para tortillas de maíz"
}
```

**Contexto generado:**
```
=== PRODUCTOS RELEVANTES ===
PRODUCTO: MEJORADOR 3M PLUS
Precio: $299.0
Descripción: Mejorador en polvo con formula balanceada para masa de 100% harina de maíz, mixteo o de 100% nixtamal...
Beneficios: Sin rastros de sabor y ni olor en la tortilla | Potencializa el sabor y olor a maíz...
```

### Consulta de Precios
```bash
POST /consultar
{
  "message": "¿Cuánto cuesta desarrollar una aplicación?"
}
```

**Contexto generado:**
```
=== RESPUESTAS FRECUENTES ===
Q: ¿Cuánto cuesta desarrollar una aplicación web?
A: El precio de desarrollo varía según la complejidad. Proyectos básicos desde $5,000...
```

### Consulta de Contacto
```bash
POST /consultar
{
  "message": "Información de contacto"
}
```

**Contexto generado:**
```
=== INFORMACIÓN DE LA EMPRESA ===
CONTACTO: {'telefono': '+1 (555) 123-4567', 'email': 'contacto@techsolutions.com'...}
```

## Instalación y Ejecución

### 1. Instalar dependencias
```bash
pip install Flask==2.3.3 requests
```

### 2. Ejecutar servidor
```bash
python app.py
```

### 3. Verificar funcionamiento
```bash
# Health check
GET http://localhost:5000/health

# Consulta de prueba
POST http://localhost:5000/consultar
Content-Type: application/json
{
  "message": "productos para tortillas"
}
```

## Testing

### Prueba Directa de Funcionalidades
```bash
python test_directo.py
```

### Prueba Simple del Endpoint
```bash
python test_simple.py
```

### Prueba Completa del API
```bash
python test_api.py
```

## Estructura de Archivos

```
Frask/
├── app.py              # Servidor Flask principal
├── requirements.txt    # Dependencias
├── empresa.json        # Datos de la empresa
├── respuestas.json     # Respuestas frecuentes
├── combined.json       # Productos completos
├── prod_meli.json      # Productos MercadoLibre  
├── prod_page.json      # Productos página web
├── test_directo.py     # Pruebas directas
├── test_simple.py      # Prueba simple
├── test_api.py         # Prueba completa API
└── README.md           # Este documento
```

## Características Técnicas

- **Framework**: Flask 2.3.3
- **Puerto**: 5000
- **Host**: 0.0.0.0 (todas las interfaces)
- **Modo Debug**: Habilitado para desarrollo
- **Encoding**: UTF-8 para caracteres especiales
- **Timeout**: 10 segundos para requests HTTP

## Configuración para Producción

Para usar en producción, modificar:

1. **Secret Key**: Cambiar `app.config['SECRET_KEY']`
2. **Debug Mode**: Establecer `debug=False`
3. **WSGI Server**: Usar Gunicorn o uWSGI
4. **Environment Variables**: Externalizar configuraciones
5. **Logging**: Implementar logging estructurado

## Logs del Sistema

El servidor muestra logs informativos:
- ✅ Carga exitosa de archivos JSON
- 📩 Consultas recibidas
- 📤 Contexto generado con tamaño
- ❌ Errores de procesamiento

¡Servidor Flask optimizado para consultas de productos TIA funcionando correctamente! 🚀