import requests
import json

# Probar el endpoint exacto de ngrok
url = "https://viceless-kristel-untaxied.ngrok-free.dev/consultar"
data = {"message": "busco conservadores para pan"}

print(f"🌐 Probando: {url}")
print(f"📝 Datos: {json.dumps(data, indent=2)}")

try:
    response = requests.post(url, json=data, timeout=30)
    print(f"📊 Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("🎉 ¡FUNCIONA PERFECTAMENTE!")
        print(f"📦 Productos encontrados: {result.get('productos_encontrados')}")
        print(f"📄 Contexto: {len(result.get('contexto', ''))} caracteres")
    else:
        print(f"❌ Error: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")

print(f"\n✅ URL PARA N8N: {url}")