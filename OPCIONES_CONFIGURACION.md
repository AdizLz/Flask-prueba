# 🚀 GUÍA: Usar tu API sin ngrok (configuración local)

## ✅ Tu API está funcionando perfectamente

**URL Local:** http://127.0.0.1:5000/consultar
**Estado:** ✅ Funcionando (probado exitosamente)

---

## 🔧 CONFIGURACIÓN PARA N8N LOCAL

### Si tienes n8n instalado localmente:

1. **En tu workflow de n8n:**
   - **HTTP Request URL:** `http://127.0.0.1:5000/consultar`
   - **Method:** POST
   - **Body:** `{"message": "={{ $json.body.mensaje }}"}`

2. **Esto funcionará si:**
   - ✅ n8n está en la misma máquina
   - ✅ Tu Flask está corriendo
   - ✅ Usas localhost/127.0.0.1

---

## 🌐 ALTERNATIVA: ngrok mediante descarga manual

Si quieres acceso desde internet:

### Opción 1: Descargar desde navegador
1. Ve a: https://ngrok.com/download
2. Descarga "Windows (amd64)"
3. Extrae ngrok.exe en tu carpeta
4. Ejecuta desde PowerShell:
   ```powershell
   .\ngrok.exe config add-authtoken TU_TOKEN
   .\ngrok.exe http 5000
   ```

### Opción 2: Crear archivo por lotes
Crea `iniciar_ngrok.bat`:
```batch
@echo off
cd /d "C:\Users\Soporte\Documents\Frask"
start cmd /k ".\venv\Scripts\python.exe app.py"
timeout 3
start cmd /k ".\ngrok.exe http 5000"
```

---

## 🧪 PROBAR TU CONFIGURACIÓN ACTUAL

### Terminal 1: Flask (ya corriendo)
```powershell
cd "C:\Users\Soporte\Documents\Frask"
.\venv\Scripts\python.exe app.py
```

### Terminal 2: Probar API
```powershell
# Probar con curl (si disponible)
curl -X POST http://127.0.0.1:5000/consultar -H "Content-Type: application/json" -d '{"message": "tortillas"}'

# O usar nuestro script de prueba
.\venv\Scripts\python.exe test_completo.py
```

---

## 📱 CONFIGURACIÓN N8N CLOUD

Si usas n8n.cloud (en internet), NECESITAS ngrok porque tu Flask está en local.

**Flujo:**
```
n8n.cloud → ngrok URL → tu Flask local
```

**Sin ngrok:**
```
n8n.cloud → ❌ NO PUEDE acceder a 127.0.0.1
```

---

## 🎯 PRÓXIMOS PASOS

### Opción A: Continuar sin ngrok (n8n local)
- ✅ Tu API ya funciona
- ✅ Configurar n8n para usar http://127.0.0.1:5000/consultar
- ✅ Probar workflow completo

### Opción B: Instalar ngrok correctamente
1. Descargar manualmente desde ngrok.com
2. Configurar token
3. Exponer API al internet
4. Usar URL de ngrok en n8n cloud

---

## 💡 RECOMENDACIÓN

**Para desarrollo:** Usa configuración local (sin ngrok)
**Para producción:** Usa ngrok o despliega en la nube

¿Cuál prefieres probar primero?