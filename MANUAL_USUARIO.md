# 📖 MANUAL DE USO - API TIA CONSULTA PRODUCTOS

## 🎯 Objetivo
Este es un sistema automático que recibe consultas por WhatsApp y devuelve información sobre productos (tortillas, harinas, etc.) de TIA usando IA.

---

## 📋 REQUISITOS PREVIOS
- Python 3.13.5 o superior
- ngrok (descargado)
- Node.js (para npm, opcional)
- Virtual environment configurado (venv)

---

## ⚡ COMANDOS ESENCIALES

### 1️⃣ INICIAR EL SISTEMA (ORDEN CORRECTO)

#### Paso 1: Abrir PowerShell
```powershell
# Presiona Windows + R y escribe:
powershell
```

#### Paso 2: Navegar al directorio
```powershell
cd "C:\Users\Soporte\Documents\Frask"
```

#### Paso 3: ACTIVAR el entorno virtual (IMPORTANTE)
```powershell
.\venv\Scripts\Activate.ps1
```
**Deberías ver `(venv)` al inicio de la terminal**

#### Paso 4: INICIAR FLASK
```powershell
python app.py
```

**Verás esto si funciona:**
```
Archivos JSON de productos cargados exitosamente
Iniciando servidor Flask para consultas TIA...
Endpoint principal: POST /consultar
Health check: GET /health
* Running on http://127.0.0.1:5000
```

✅ **¡Flask está corriendo!**

---

### 2️⃣ INICIAR NGROK (EN OTRA TERMINAL)

#### Paso 1: Abrir NUEVA ventana de PowerShell
```powershell
# NO cierres la anterior. Abre una nueva ventana
Windows + Shift + N  (en PowerShell)
# O abre PowerShell nuevamente
```

#### Paso 2: Navegar al directorio
```powershell
cd "C:\Users\Soporte\Documents\Frask"
```

#### Paso 3: INICIAR NGROK
```powershell
.\ngrok.exe http 5000
```

**Verás esto si funciona:**
```
Session Status                online
Forwarding                    https://viceless-kristel-untaxied.ngrok-free.dev -> http://localhost:5000
```

✅ **¡ngrok está conectado!**

**Copia la URL HTTPS** (ejemplo: `https://viceless-kristel-untaxied.ngrok-free.dev`)

---

## 🔗 CONFIGURAR EN N8N

### Paso 1: Abrir n8n en tu navegador
```
https://n8n.cloud  (o tu instancia local)
```

### Paso 2: En el nodo "HTTP Request", configura:
- **Method:** `POST`
- **URL:** `https://viceless-kristel-untaxied.ngrok-free.dev/consultar`
- **Headers:** `Content-Type: application/json`
- **Body:** 
```json
{
  "message": "{{$node['Capture de texto'].json.text}}"
}
```

### Paso 3: Ejecuta el workflow
El endpoint responderá con productos relevantes automáticamente.

---

## ❌ SOLUCIÓN DE PROBLEMAS

### Problema 1: Error "ERR_NGROK_3200" en n8n
**Significa:** ngrok se desconectó (timeout del plan gratuito)

**Solución:**
```powershell
# En la terminal de ngrok, presiona Ctrl+C
Ctrl+C

# Espera 2 segundos y reinicia
.\ngrok.exe http 5000

# Copia la NUEVA URL y actualiza en n8n
```

---

### Problema 2: Error "404 Not Found" en n8n
**Significa:** Flask no está corriendo

**Solución:**
```powershell
# En la terminal de Flask, verifica que ves:
# "Running on http://127.0.0.1:5000"

# Si NO ves eso, presiona Ctrl+C y reinicia:
Ctrl+C

# Asegúrate de activar venv primero:
.\venv\Scripts\Activate.ps1

# Luego inicia Flask:
python app.py
```

---

### Problema 3: Error "ModuleNotFoundError: No module named 'flask'"
**Significa:** El entorno virtual no está activado

**Solución:**
```powershell
# Verifica que veas (venv) al inicio
# Si NO ves (venv), activa el entorno:
.\venv\Scripts\Activate.ps1

# Intenta nuevamente:
python app.py
```

---

### Problema 4: ngrok dice "Session Status offline"
**Significa:** Perdiste conexión a internet o token expiró

**Solución:**
```powershell
# Verifica tu conexión a internet
# Luego reinicia ngrok:
Ctrl+C
.\ngrok.exe http 5000

# Si el token expiró, actualízalo:
.\ngrok.exe config add-authtoken TU_TOKEN_AQUI
```

---

### Problema 5: "Address already in use" (Port 5000)
**Significa:** Otro proceso ya está usando el puerto 5000

**Solución:**
```powershell
# Detén todos los procesos Python:
Get-Process -Name "*python*" | Stop-Process -Force

# Espera 5 segundos y reinicia Flask:
Start-Sleep -Seconds 5
python app.py
```

---

## ✅ LISTA DE VERIFICACIÓN DIARIA

Antes de usar el sistema:

- [ ] **Terminal 1 (Flask):** ¿Ves "Running on http://127.0.0.1:5000"?
- [ ] **Terminal 2 (ngrok):** ¿Ves "Session Status online"?
- [ ] **ngrok:** ¿Copiaste la URL HTTPS correcta?
- [ ] **n8n:** ¿Actualizaste la URL en el nodo HTTP Request?
- [ ] **n8n:** ¿Hiciste clic en "Ejecutar paso"?

Si todas están ✅, ¡el sistema funciona!

---

## 📱 FLUJO COMPLETO

```
Cliente escribe en WhatsApp
         ↓
n8n recibe el mensaje
         ↓
n8n envía POST a ngrok (https://...)
         ↓
ngrok redirige a Flask (http://localhost:5000)
         ↓
Flask busca productos en JSON
         ↓
Flask genera respuesta con IA
         ↓
n8n recibe respuesta
         ↓
n8n envía respuesta a WhatsApp
         ↓
Cliente recibe recomendación de productos
```

---

## 🆘 SOPORTE RÁPIDO

| Problema | Comando |
|----------|---------|
| Flask no inicia | `.\venv\Scripts\Activate.ps1` luego `python app.py` |
| ngrok offline | `Ctrl+C` luego `.\ngrok.exe http 5000` |
| Puerto ocupado | `Get-Process -Name "*python*" \| Stop-Process -Force` |
| Ver logs Flask | `python -u app.py` |
| Ver logs ngrok | `.\ngrok.exe http 5000 --log stdout` |

---

## 📞 CONTACTO TÉCNICO

Si algo no funciona:
1. Revisa la sección "SOLUCIÓN DE PROBLEMAS"
2. Verifica los logs de Flask y ngrok
3. Reinicia ambos servicios
4. Espera 10 segundos antes de probar

---

## 📝 NOTAS IMPORTANTES

⚠️ **El token de ngrok es personal** - No lo compartas
⚠️ **La URL de ngrok cambia cada vez** - Cópiala correctamente
⚠️ **Mantén ambas terminales abiertas** - No cierres Flask ni ngrok
⚠️ **Plan gratuito ngrok = 2 horas máximo** - Reinicia si se desconecta

---

**¡Listo! Ahora puedes compartir este manual con tu amiga.** 🚀
