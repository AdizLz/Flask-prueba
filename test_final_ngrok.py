import requests
import json

def test_ngrok_now():
    """Probar ngrok ahora que tanto Flask como ngrok están corriendo"""
    print("🚀 PROBANDO NGROK + FLASK")
    print("=" * 40)
    
    # URL más probable basada en el output de ngrok
    ngrok_url = "https://viceless-kristel-untaxied.ngrok-free.app"
    endpoint = f"{ngrok_url}/consultar"
    
    test_data = {
        "message": "busco mejoradores para tortillas"
    }
    
    print(f"🌐 URL de ngrok: {ngrok_url}")
    print(f"🎯 Endpoint: {endpoint}")
    
    try:
        print("🔍 Enviando petición...")
        response = requests.post(endpoint, json=test_data, timeout=20)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("🎉 ¡ÉXITO! Ngrok funcionando correctamente")
            print(f"📦 Productos encontrados: {result.get('productos_encontrados', 0)}")
            print(f"📄 Contexto generado: {len(result.get('contexto', ''))} caracteres")
            print(f"\n✅ URL PARA N8N: {endpoint}")
            return endpoint
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"📝 Respuesta: {response.text[:300]}")
            
            # Si es 404, probamos solo la raíz
            if response.status_code == 404:
                print(f"\n🔍 Probando URL base: {ngrok_url}")
                try:
                    base_response = requests.get(ngrok_url, timeout=10)
                    print(f"📊 Status de URL base: {base_response.status_code}")
                except Exception as e:
                    print(f"❌ Error en URL base: {e}")
            
    except requests.exceptions.ConnectTimeout:
        print("⏰ Timeout - ngrok puede estar lento")
    except requests.exceptions.ConnectionError:
        print("🔌 Error de conexión - verifica que ngrok esté corriendo")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return None

def verify_local_first():
    """Verificar primero que la API local funcione"""
    print("🏠 VERIFICANDO API LOCAL PRIMERO")
    print("=" * 35)
    
    try:
        response = requests.post("http://127.0.0.1:5000/consultar", 
                                json={"message": "test"}, timeout=5)
        if response.status_code == 200:
            print("✅ API local funcionando")
            return True
        else:
            print(f"❌ API local error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error con API local: {e}")
        return False

if __name__ == "__main__":
    # Verificar local primero
    if verify_local_first():
        # Esperar un poco para que ngrok se estabilice
        import time
        print("\n⏳ Esperando que ngrok se estabilice...")
        time.sleep(3)
        
        # Probar ngrok
        working_url = test_ngrok_now()
        
        if working_url:
            print(f"\n🎉 ¡TODO FUNCIONANDO PERFECTAMENTE!")
            print(f"🔗 Para n8n usa: {working_url}")
        else:
            print(f"\n⚠️ Problemas con ngrok")
            print(f"💡 Tu API local funciona en: http://127.0.0.1:5000/consultar")
    else:
        print("\n❌ Primero necesitas que tu API local funcione")