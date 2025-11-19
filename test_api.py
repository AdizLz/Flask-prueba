#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba completo para la API Flask TIA
Prueba todos los endpoints y genera reporte
"""
import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:5000"

# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def print_header(texto, char="="):
    """Imprimir encabezado decorado"""
    print(f"\n{char*70}")
    print(f"  {texto}")
    print(f"{char*70}")

def print_subheader(texto):
    """Imprimir subencabezado"""
    print(f"\n{'─'*70}")
    print(f"  {texto}")
    print(f"{'─'*70}")

# ============================================================================
# PRUEBAS DE ENDPOINTS
# ============================================================================

def test_health_check():
    """Probar health check"""
    print_header("🏥 HEALTH CHECK", "=")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Servidor funcionando correctamente\n")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            return True
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor")
        print("\n💡 SOLUCIÓN:")
        print("   1. Abre otra terminal")
        print("   2. Ejecuta: python app.py")
        print("   3. Espera a que diga 'Running on http://127.0.0.1:5000'")
        print("   4. Vuelve a ejecutar este script")
        return False
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_stats():
    """Probar endpoint de estadísticas"""
    print_header("📊 ESTADÍSTICAS DEL SISTEMA", "=")
    
    try:
        response = requests.get(f"{BASE_URL}/stats", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(f"❌ Error {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_consulta(mensaje, mostrar_contexto=True):
    """
    Probar una consulta específica
    
    Args:
        mensaje: Consulta a enviar
        mostrar_contexto: Si mostrar el contexto completo
    """
    print_subheader(f"🔍 CONSULTA: '{mensaje}'")
    
    url = f"{BASE_URL}/consultar"
    payload = {"message": mensaje}
    
    try:
        # Medir tiempo de respuesta
        inicio = time.time()
        response = requests.post(url, json=payload, timeout=10)
        tiempo = (time.time() - inicio) * 1000  # En milisegundos
        
        if response.status_code == 200:
            data = response.json()
            
            # Mostrar métricas
            print(f"\n⏱️  Tiempo de respuesta: {tiempo:.0f}ms")
            print(f"📦 Productos encontrados: {data.get('productos_encontrados', 0)}")
            print(f"💬 Respuestas frecuentes: {data.get('respuestas_encontradas', 0)}")
            print(f"📝 Caracteres: {data.get('caracteres', 0)}")
            print(f"🎫 Tokens estimados: ~{data.get('tokens_estimados', 0)}")
            
            # Mostrar contexto
            if mostrar_contexto:
                contexto = data.get('contexto', 'Sin contexto')
                print(f"\n📄 CONTEXTO GENERADO:")
                print("┌" + "─"*68 + "┐")
                for linea in contexto.split('\n'):
                    # Truncar líneas muy largas
                    if len(linea) > 66:
                        linea = linea[:63] + "..."
                    print(f"│ {linea:<66} │")
                print("└" + "─"*68 + "┘")
            
            return {
                'success': True,
                'tiempo_ms': tiempo,
                'productos': data.get('productos_encontrados', 0),
                'tokens': data.get('tokens_estimados', 0)
            }
            
        else:
            print(f"\n❌ Error {response.status_code}")
            print(f"   {response.text}")
            return {'success': False}
            
    except requests.exceptions.Timeout:
        print("\n❌ Timeout - El servidor tardó más de 10 segundos")
        return {'success': False}
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return {'success': False}

# ============================================================================
# SUITE DE PRUEBAS
# ============================================================================

def run_test_suite():
    """Ejecutar suite completa de pruebas"""
    
    print_header("🧪 SUITE DE PRUEBAS - API FLASK TIA", "🚀")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. Health Check
    if not test_health_check():
        print("\n⛔ No se puede continuar sin conexión al servidor")
        return
    
    time.sleep(1)
    
    # 2. Estadísticas
    test_stats()
    
    time.sleep(1)
    
    # 3. Consultas de prueba
    print_header("🔬 PRUEBAS DE CONSULTAS", "=")
    
    consultas_test = [
        # Consultas de productos específicos
        "Necesito un mejorador para tortillas de maíz",
        "Busco conservadores para pan",
        "Antiadherente para comales",
        "Base para pan de hamburguesa",
        
        # Consultas generales
        "Productos para panadería",
        "¿Qué productos tienen para tortillerías?",
        
        # Consultas sobre precios/info
        "¿Cuánto cuestan sus productos?",
        "¿Qué tecnologías utilizan?",
        "Información de contacto",
        "Horarios de atención",
    ]
    
    resultados = []
    
    for i, consulta in enumerate(consultas_test, 1):
        print(f"\n{'='*70}")
        print(f"PRUEBA {i}/{len(consultas_test)}")
        
        resultado = test_consulta(consulta, mostrar_contexto=True)
        resultados.append({
            'consulta': consulta,
            **resultado
        })
        
        time.sleep(0.5)  # Pausa entre consultas
    
    # 4. Resumen final
    print_header("📈 RESUMEN DE PRUEBAS", "=")
    
    exitosas = sum(1 for r in resultados if r.get('success'))
    fallidas = len(resultados) - exitosas
    
    if exitosas > 0:
        tiempo_promedio = sum(r.get('tiempo_ms', 0) for r in resultados if r.get('success')) / exitosas
        tokens_promedio = sum(r.get('tokens', 0) for r in resultados if r.get('success')) / exitosas
        productos_promedio = sum(r.get('productos', 0) for r in resultados if r.get('success')) / exitosas
    else:
        tiempo_promedio = 0
        tokens_promedio = 0
        productos_promedio = 0
    
    print(f"\n✅ Pruebas exitosas: {exitosas}/{len(resultados)}")
    print(f"❌ Pruebas fallidas: {fallidas}/{len(resultados)}")
    print(f"\n📊 Promedios:")
    print(f"   • Tiempo de respuesta: {tiempo_promedio:.0f}ms")
    print(f"   • Tokens por consulta: ~{tokens_promedio:.0f}")
    print(f"   • Productos encontrados: {productos_promedio:.1f}")
    
    # Calcular ahorro de tokens
    tokens_sin_optimizar = 2000  # Estimación si enviaras todo el catálogo
    ahorro_porcentaje = ((tokens_sin_optimizar - tokens_promedio) / tokens_sin_optimizar) * 100
    
    print(f"\n💰 AHORRO ESTIMADO:")
    print(f"   • Tokens sin optimizar: ~{tokens_sin_optimizar}")
    print(f"   • Tokens optimizados: ~{tokens_promedio:.0f}")
    print(f"   • Ahorro: {ahorro_porcentaje:.1f}%")
    
    print_header("✅ PRUEBAS COMPLETADAS", "🎉")
    
    # Instrucciones para n8n
    print("\n📋 SIGUIENTE PASO - CONFIGURAR N8N:")
    print("─"*70)
    print("\n1. En n8n, agrega un nodo 'HTTP Request'")
    print("\n2. Configura:")
    print("   • Method: POST")
    print("   • URL: http://localhost:5000/consultar")
    print("   • Body: JSON")
    print('   • Body Content: {"message": "{{ $json.mensaje_usuario }}"}')
    print("\n3. El contexto estará en: {{ $json.contexto }}")
    print("   Envía este contexto a OpenAI para ahorrar tokens")
    print("\n4. ¡Listo! Tu chatbot usará solo la info relevante 🚀")
    print("─"*70)

# ============================================================================
# EJECUCIÓN PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    try:
        run_test_suite()
    except KeyboardInterrupt:
        print("\n\n⚠️  Pruebas interrumpidas por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error fatal: {e}")