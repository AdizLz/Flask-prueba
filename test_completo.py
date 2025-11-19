import requests
import json

def test_api_local():
    """Probar tu API Flask local"""
    print("=== PROBANDO TU API FLASK ===")
    
    # URL de tu API
    url = "http://127.0.0.1:5000/consultar"
    
    # Datos de prueba
    data = {
        "message": "busco mejoradores para tortillas de maiz"
    }
    
    try:
        print(f"📡 Enviando POST a: {url}")
        print(f"📝 Datos: {json.dumps(data, indent=2)}")
        
        # Hacer la petición
        response = requests.post(url, json=data, timeout=10)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ RESPUESTA EXITOSA:")
            print(f"📦 Productos encontrados: {result.get('productos_encontrados', 0)}")
            print(f"📄 Contexto generado: {len(result.get('contexto', ''))} caracteres")
            print("\n📋 CONTEXTO (primeros 500 caracteres):")
            print(result.get('contexto', '')[:500] + "...")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"📝 Respuesta: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: No se puede conectar al servidor Flask")
        print("💡 SOLUCIÓN: Asegúrate de que 'python app.py' esté ejecutándose")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_health_check():
    """Probar el endpoint de health"""
    print("\n=== PROBANDO HEALTH CHECK ===")
    
    try:
        response = requests.get("http://127.0.0.1:5000/health", timeout=5)
        if response.status_code == 200:
            result = response.json()
            print("✅ Health check OK")
            print(f"📊 Estado: {result.get('status')}")
            print(f"📁 Archivos JSON cargados:")
            for archivo, cantidad in result.get('archivos_json', {}).items():
                print(f"   - {archivo}: {cantidad} elementos")
            return True
        else:
            print(f"❌ Health check falló: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error en health check: {e}")
        return False

if __name__ == "__main__":
    print("🚀 PROBANDO TU API FLASK LOCAL")
    print("=" * 50)
    
    # Probar health check
    health_ok = test_health_check()
    
    if health_ok:
        # Probar endpoint principal
        api_ok = test_api_local()
        
        if api_ok:
            print("\n🎉 ¡TU API FUNCIONA PERFECTAMENTE!")
            print("✅ Lista para conectar con n8n")
            print("📍 URL para n8n: http://127.0.0.1:5000/consultar")
        else:
            print("\n❌ Hay problemas con el endpoint principal")
    else:
        print("\n❌ El servidor Flask no responde")
    
    print("\n" + "=" * 50)