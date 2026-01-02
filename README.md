# 📖 Our Adventures - Álbum Digital de Recuerdos

Una aplicación web estilo **"Our Adventures"** (de la película Up) para documentar y recordar visitas a cafeterías y citas especiales. Diseño minimalista con paleta de colores cafecito (beige, marrón, crema).

## 🎨 Características Principales

### 📋 Gestión de Contenido
- ☕ **Galería de Cafeterías**: Colecciona visitas a tus cafeterías favoritas
- 💕 **Galería de Citas**: Documenta momentos especiales
- 📊 **Evaluaciones Likert**: Califica comida, ambiente y ganas de volver
- 📸 **Multimedia**: Sube fotos y videos almacenados localmente
- 🗺️ **Google Maps**: Enlaces directos a ubicaciones
- 📷 **Google Fotos**: Integración de carpetas compartidas

### 💾 Almacenamiento
- **CSV local**: Todos los datos se guardan en archivos CSV
- **Servidor local**: Fotos y videos almacenados en servidor
- **Sin base de datos externa**: Completamente independiente

### 🎭 Diseño
- Estética nostálgica y acogedora
- Paleta de colores: Crema, Beige, Marrón claro, Marrón oscuro
- Responsive: Funciona en desktop y móvil
- Interactivo: Efectos hover, animaciones suaves

---

## 🚀 Instalación y Configuración

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes Python)
- Navegador moderno (Chrome, Firefox, Safari, Edge)

### Paso 1: Clonar o Descargar el Proyecto

```bash
# Descarga los archivos del proyecto en una carpeta
mkdir our_adventures
cd our_adventures
```

### Paso 2: Crear Entorno Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Crear Estructura de Carpetas

```bash
# El script creará las carpetas automáticamente, pero puedes crearlas manualmente:
mkdir -p data
mkdir -p uploads/cafeterias
mkdir -p uploads/citas
mkdir -p templates
mkdir -p static
```

### Paso 5: Copiar Archivos

Organiza los archivos de la siguiente manera:

```
our_adventures/
├── app.py                    # Aplicación Flask
├── requirements.txt          # Dependencias
├── data/                     # Se crea automáticamente
│   ├── cafeterias.csv
│   ├── citas.csv
│   ├── evaluaciones.csv
│   ├── multimedia.csv
│   └── google_fotos.csv
├── uploads/                  # Se crea automáticamente
│   ├── cafeterias/
│   └── citas/
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── cafeterias.html
│   ├── cafeteria_detalle.html
│   ├── citas.html
│   └── cita_detalle.html
└── static/
    └── styles.css
```

### Paso 6: Ejecutar la Aplicación

```bash
python app.py
```

**Output esperado:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://localhost:5000
```

### Paso 7: Acceder a la Aplicación

Abre tu navegador y ve a: **http://localhost:5000**

---

## 📖 Guía de Uso

### Página de Inicio
1. Verás la portada del álbum con dos opciones:
   - **☕ Ver Cafeterías**: Gestiona tus cafeterías
   - **💕 Ver Citas**: Gestiona tus citas especiales

### Sección Cafeterías

#### Agregar Cafetería
1. Haz clic en el botón flotante **+** (abajo a la derecha)
2. Ingresa:
   - Nombre de la cafetería
   - Ubicación
   - URL de Google Maps (opcional)
3. Haz clic en **Crear**

#### Ver Detalles
1. Haz clic en una cafetería para ver su detalle
2. Verás:
   - **Nombre y ubicación**
   - **Enlace a Google Maps**
   - **Indicador de visitada/no visitada**

#### Evaluar Cafetería
1. En la sección "Evaluaciones", califica de 1 a 5:
   - **Calidad de la comida**
   - **Ambiente del lugar**
   - **Ganas de volver a ir**
2. Haz clic en **Guardar Evaluaciones**

#### Subir Fotos/Videos
1. En la sección "Fotos y Videos":
   - Haz clic en **📁 Seleccionar archivos**
   - Elige una o más fotos/videos
   - (Opcional) Agrega enlace a carpeta Google Fotos
2. Haz clic en **Subir**

#### Agregar Google Fotos
1. Comparte una carpeta de Google Fotos públicamente
2. Copia el enlace compartido
3. En "Carpeta Google Fotos":
   - Nombre de la carpeta (opcional)
   - Pega la URL
4. Haz clic en **Subir**

#### Notas y Recuerdos
1. En la sección "Notas", escribe tus recuerdos
2. Marca como "Visitada" si ya fue
3. Haz clic en **Guardar Notas**

### Sección Citas

El flujo es similar al de cafeterías, pero sin evaluaciones Likert. Incluye:
- Nombre de la cita
- Ubicación
- Fecha
- Fotos y videos
- Google Fotos
- Notas y recuerdos
- Indicador de realizada/pendiente

---

## 📁 Estructura de Datos CSV

### cafeterias.csv
```csv
id,nombre,ubicacion,google_maps_url,imagen,visitada,notas
1,Cafeteria Luna,Coyoacán,"https://maps.google.com/?q=...",default.jpg,true,Excelente café
```

### citas.csv
```csv
id,nombre,ubicacion,fecha,imagen,realizada,notas
1,Primer Café,Condesa,2024-01-15,default.jpg,true,Momento especial
```

### evaluaciones.csv
```csv
id,tipo,item_id,categoria,calificacion
1,cafeteria,1,comida,5
2,cafeteria,1,ambiente,4
3,cafeteria,1,volver,5
```

### multimedia.csv
```csv
id,tipo,item_id,archivo,tipo_archivo,fecha_subida
1,cafeteria,1,cafeteria_20240115_120530.jpg,foto,2024-01-15T12:05:30
```

### google_fotos.csv
```csv
id,tipo,item_id,nombre_carpeta,url_google_fotos
1,cafeteria,1,Luna Fotos,https://photos.app.goo.gl/...
```

---

## 🎨 Personalización

### Cambiar Colores
Edita `static/styles.css` en la sección `:root`:

```css
:root {
    --color-cream: #FFF8F0;        /* Cambiar crema */
    --color-beige: #D4C4B0;        /* Cambiar beige */
    --color-brown-light: #A0826D;  /* Cambiar marrón claro */
    --color-brown-dark: #8B7355;   /* Cambiar marrón oscuro */
}
```

### Cambiar Tipografía
En `static/styles.css`:

```css
:root {
    --font-main: 'Segoe UI', sans-serif;           /* Fuente principal */
    --font-decorative: 'Georgia', serif;           /* Fuente títulos */
}
```

### Agregar Iconos Personalizados
En los templates HTML, usa emojis o iconos Unicode:
- ☕ Cafeterías
- 💕 Citas
- 📸 Fotos
- 📝 Notas
- 📊 Evaluaciones

---

## ⚙️ Configuración Avanzada

### Aumentar Límite de Archivo
En `app.py`, línea ~9:

```python
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
```

### Puerto Diferente
En `app.py`, última línea:

```python
app.run(debug=True, host='localhost', port=8080)  # Cambia 5000 a otro puerto
```

### Habilitar Acceso Remoto
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

---

## 🔧 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'flask'"
**Solución**: Asegúrate que el entorno virtual esté activado y las dependencias instaladas:
```bash
pip install -r requirements.txt
```

### Error: "Permission denied" al crear carpetas
**Solución**: El script crea carpetas automáticamente. Si hay problemas:
```bash
mkdir -p data uploads/cafeterias uploads/citas templates static
```

### Las imágenes no se cargan
**Solución**: 
1. Verifica que los archivos estén en `uploads/cafeterias/` o `uploads/citas/`
2. Comprueba que los nombres en CSV coincidan exactamente
3. Recarga la página (Ctrl+F5)

### Google Fotos no se visualiza
**Solución**:
1. Asegúrate que la carpeta está públicamente compartida
2. Copia el enlace completo desde "Compartir"
3. Algunos navegadores pueden bloquear iframes - prueba con otro navegador

### Puerto 5000 ya está en uso
**Solución**: Cambia el puerto en `app.py`:
```python
app.run(debug=True, host='localhost', port=8080)
```

---

## 📱 Características de Dispositivos Móviles

- ✅ Diseño responsive
- ✅ Botón flotante accesible
- ✅ Galería de fotos optimizada
- ✅ Formularios móvil-friendly
- ✅ Evaluaciones Likert táctiles

---

## 🔒 Privacidad y Seguridad

- **Datos locales**: Todo se almacena en tu servidor
- **Sin cloud**: No se envía información a servidores externos
- **Contraseña**: Esta versión no incluye autenticación
- **HTTPS**: Para producción, usa HTTPS (requiere SSL)

---

## 🚀 Despliegue en Producción

Para desplegar en un servidor:

1. Usa un servidor WSGI (Gunicorn):
```bash
pip install gunicorn
gunicorn app:app
```

2. Configura un proxy inverso (nginx)

3. Usa SSL/HTTPS (Let's Encrypt gratuito)

4. Backup regular de la carpeta `data/`

---

## 📝 Licencia y Atribuciones

- Inspirado en **"Our Adventures"** de la película **Up** (Pixar)
- Desarrollado con **Flask** y **Python**
- Estilos personalizados con CSS

---

## 🎯 Roadmap Futuro

- [ ] Autenticación de usuarios
- [ ] Base de datos SQLite
- [ ] Búsqueda y filtros avanzados
- [ ] Compartir álbum con otros usuarios
- [ ] API REST
- [ ] Exportar a PDF
- [ ] Sincronización con Google Drive
- [ ] App móvil (React Native)

---

## 💬 Soporte

Si encuentras problemas:

1. Revisa la sección "Solución de Problemas"
2. Verifica que todas las dependencias estén instaladas
3. Asegúrate que la estructura de carpetas sea correcta
4. Prueba en un navegador diferente

---

## 🎉 ¡Disfruta tu Álbum!

Tu "Our Adventures" digital está listo. ¡Comienza a documentar tus recuerdos cafecito y tus citas especiales! 📖☕💕
