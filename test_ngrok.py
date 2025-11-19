import requests
import json
import time

def test_ngrok_api():
    """Probar la API a través de ngrok"""
    print("🌐 PROBANDO API A TRAVÉS DE NGROK")
    print("=" * 50)
    
    # Nota: La URL parece estar incompleta, vamos a probar diferentes formatos
    base_urls = [
        "https://viceless-kristel-untaxied.ngrok.io",
        "https://viceless-kristel-untaxied.ngrok-free.app",
        "https://viceless-kristel-untaxied.ngrok.app"
    ]
    
    test_data = {
        "message": "busco conservadores para pan"
    }
    
    for base_url in base_urls:
        endpoint = f"{base_url}/consultar"
        print(f"\n🔍 Probando: {endpoint}")
        
        try:
            # Hacer la petición
            response = requests.post(endpoint, json=test_data, timeout=15)
            
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ ¡FUNCIONA! Ngrok conectando correctamente")
                print(f"📦 Productos encontrados: {result.get('productos_encontrados', 0)}")
                print(f"📄 Contexto: {len(result.get('contexto', ''))} caracteres")
                print(f"\n🎯 URL PARA N8N: {endpoint}")
                return endpoint
            else:
                print(f"❌ Error: {response.status_code}")
                if response.text:
                    print(f"📝 Respuesta: {response.text[:200]}")
                
        except requests.exceptions.ConnectTimeout:
            print("⏰ Timeout - Puede ser que la URL no sea correcta")
        except requests.exceptions.ConnectionError:
            print("🔌 Error de conexión - URL probablemente incorrecta")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n💡 SUGERENCIA:")
    print("Ve a http://127.0.0.1:4040 para ver la URL completa de ngrok")
    return None

def test_local_api():
    """Verificar que la API local sigue funcionando"""
    print("\n🏠 VERIFICANDO API LOCAL")
    print("=" * 30)
    
    try:
        response = requests.get("http://127.0.0.1:5000/health", timeout=5)
        if response.status_code == 200:
            print("✅ API local funcionando")
            return True
        else:
            print(f"❌ API local con problemas: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error con API local: {e}")
        return False

if __name__ == "__main__":
    print("🚀 TESTING COMPLETO - LOCAL + NGROK")
    print("=" * 60)
    
    # Verificar API local
    local_ok = test_local_api()
    
    if local_ok:
        # Probar ngrok
        working_url = test_ngrok_api()
        
        if working_url:
            print(f"\n🎉 ¡TODO FUNCIONANDO!")
            print(f"🌐 URL pública: {working_url}")
            print(f"🔗 Para n8n usa: {working_url}")
        else:
            print(f"\n⚠️  Ngrok configurado pero URL no clara")
            print(f"👀 Verifica en: http://127.0.0.1:4040")
    else:
        print("\n❌ Problemas con la API local")
        print("💡 Asegúrate de que 'python app.py' esté ejecutándose")
    
    print("\n" + "=" * 60)