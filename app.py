from flask import Flask, render_template, request, redirect, url_for, jsonify
import csv
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from PIL import Image
import time

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024 # 100MB max
app.config['UPLOAD_FOLDER_CAFETERIAS'] = 'static/uploads/cafeterias'
app.config['UPLOAD_FOLDER_CITAS'] = 'static/uploads/citas'

# Crear carpetas si no existen
os.makedirs(app.config['UPLOAD_FOLDER_CAFETERIAS'], exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER_CITAS'], exist_ok=True)

CAFETERIAS_FILE = 'data/cafeterias.csv'
CITAS_FILE = 'data/citas.csv'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'mp4', 'webm', 'mov', 'avi'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_cafeterias_data():
    """Lee los datos de cafeterías del CSV"""
    if not os.path.exists(CAFETERIAS_FILE):
        return []
    cafeterias = []
    with open(CAFETERIAS_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cafeterias.append(row)
    return cafeterias

def get_citas_data():
    """Lee los datos de citas del CSV"""
    if not os.path.exists(CITAS_FILE):
        return []
    citas = []
    with open(CITAS_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            citas.append(row)
    return citas

def find_cafeteria(id):
    """Busca una cafetería por ID"""
    cafeterias = get_cafeterias_data()
    for cafe in cafeterias:
        if cafe.get('id') == str(id):
            return cafe
    return None

def find_cita(id):
    """Busca una cita por ID"""
    citas = get_citas_data()
    for cita in citas:
        if cita.get('id') == str(id):
            return cita
    return None

def update_cafeteria_field(id, field, value):
    """Actualiza un campo de una cafetería en el CSV"""
    cafeterias = get_cafeterias_data()
    fieldnames = cafeterias[0].keys() if cafeterias else []
    
    # Si el campo no existe, agregarlo
    for cafe in cafeterias:
        if field not in cafe:
            cafe[field] = ''
    
    if field not in fieldnames:
        fieldnames = list(fieldnames) + [field]
    
    # Actualizar valor
    for cafe in cafeterias:
        if cafe.get('id') == str(id):
            cafe[field] = value
            break
    
    # Guardar
    with open(CAFETERIAS_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cafeterias)

def update_cita_field(id, field, value):
    """Actualiza un campo de una cita en el CSV"""
    citas = get_citas_data()
    fieldnames = citas[0].keys() if citas else []
    
    # Si el campo no existe, agregarlo
    for cita in citas:
        if field not in cita:
            cita[field] = ''
    
    if field not in fieldnames:
        fieldnames = list(fieldnames) + [field]
    
    # Actualizar valor
    for cita in citas:
        if cita.get('id') == str(id):
            cita[field] = value
            break
    
    # Guardar
    with open(CITAS_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(citas)

# ============================================
# RUTAS PRINCIPALES
# ============================================

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/citas')
def citas():
    data = get_citas_data()
    return render_template('citas.html', citas=data)

@app.route('/cafeteria/<id>')
def cafeteria_detail(id):
    cafeteria = find_cafeteria(id)
    if not cafeteria:
        return "Cafetería no encontrada", 404
    return render_template('cafeteria_detalle.html', cafeteria=cafeteria)

@app.route('/cita/<id>')
def cita_detail(id):
    cita = find_cita(id)
    if not cita:
        return "Cita no encontrada", 404
    return render_template('cita_detalle.html', cita=cita)

@app.route('/edit-cafeteria/<id>', methods=['GET', 'POST'])
def edit_cafeteria(id):
    cafeteria = find_cafeteria(id)
    if not cafeteria:
        return "Cafetería no encontrada", 404
    
    if request.method == 'POST':
        update_cafeteria_field(id, 'nombre', request.form.get('nombre'))
        update_cafeteria_field(id, 'ubicacion', request.form.get('ubicacion'))
        update_cafeteria_field(id, 'google_maps_url', request.form.get('google_maps_url'))
        update_cafeteria_field(id, 'visitada', request.form.get('visitada', 'False'))
        update_cafeteria_field(id, 'fecha_visita', request.form.get('fecha_visita', ''))
        return redirect(url_for('cafeteria_detail', id=id))
    
    return render_template('cafeteria_edit.html', cafeteria=cafeteria)

@app.route('/edit-cita/<id>', methods=['GET', 'POST'])
def edit_cita(id):
    cita = find_cita(id)
    if not cita:
        return "Cita no encontrada", 404
    
    if request.method == 'POST':
        update_cita_field(id, 'nombre', request.form.get('nombre'))
        update_cita_field(id, 'ubicacion', request.form.get('ubicacion'))
        update_cita_field(id, 'fecha', request.form.get('fecha'))
        update_cita_field(id, 'realizada', request.form.get('realizada', 'False'))
        update_cita_field(id, 'fecha_realizada', request.form.get('fecha_realizada', ''))
        return redirect(url_for('cita_detail', id=id))
    
    return render_template('cita_edit.html', cita=cita)

# ============================================
# RUTAS PARA ELIMINAR
# ============================================

@app.route('/delete-cafeteria/<id>', methods=['POST'])
def delete_cafeteria(id):
    """Elimina una cafetería del CSV"""
    try:
        cafeterias = get_cafeterias_data()
        fieldnames = cafeterias[0].keys() if cafeterias else []
        
        # Eliminar cafetería con ID coincidente
        cafeterias = [cafe for cafe in cafeterias if cafe.get('id') != str(id)]
        
        # Guardar
        if cafeterias:
            with open(CAFETERIAS_FILE, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(cafeterias)
        
        return redirect(url_for('cafeterias'))
    except Exception as e:
        print(f"Error eliminando cafetería: {e}")
        return redirect(url_for('cafeteria_detail', id=id))

@app.route('/delete-cita/<id>', methods=['POST'])
def delete_cita(id):
    """Elimina una cita del CSV"""
    try:
        citas = get_citas_data()
        fieldnames = citas[0].keys() if citas else []
        
        # Eliminar cita con ID coincidente
        citas = [cita for cita in citas if cita.get('id') != str(id)]
        
        # Guardar
        if citas:
            with open(CITAS_FILE, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(citas)
        
        return redirect(url_for('citas'))
    except Exception as e:
        print(f"Error eliminando cita: {e}")
        return redirect(url_for('cita_detail', id=id))

# ============================================
# RUTAS PARA EVALUACIONES (CAFETERÍAS)
# ============================================

@app.route('/cafeteria/<id>/save-evaluation', methods=['POST'])
def save_cafeteria_evaluation(id):
    """Guarda la evaluación Likert de la cafetería"""
    cafeteria = find_cafeteria(id)
    if not cafeteria:
        return "Cafetería no encontrada", 404
    
    update_cafeteria_field(id, 'food_quality', request.form.get('food_quality', ''))
    update_cafeteria_field(id, 'ambiance', request.form.get('ambiance', ''))
    update_cafeteria_field(id, 'want_return', request.form.get('want_return', ''))
    
    return redirect(url_for('cafeteria_detail', id=id))

# ============================================
# RUTAS PARA SUBIR IMÁGENES DE PORTADA
# ============================================

@app.route('/cafeteria/<id>/upload-image', methods=['POST'])
def upload_cafeteria_image(id):
    """Subir foto de portada para cafetería"""
    try:
        cafeteria = find_cafeteria(id)
        if not cafeteria:
            return redirect(url_for('cafeterias'))
        
        if 'imagen' not in request.files:
            return redirect(url_for('cafeteria_detail', id=id))
        
        file = request.files['imagen']
        if file.filename == '':
            return redirect(url_for('cafeteria_detail', id=id))
        
        if not allowed_file(file.filename):
            return redirect(url_for('cafeteria_detail', id=id))
        
        # Generar nombre seguro
        filename = secure_filename(f"cafeteria_{id}_{os.urandom(8).hex()}.jpg")
        filepath = os.path.join(app.config['UPLOAD_FOLDER_CAFETERIAS'], filename)
        
        # Guardar y optimizar imagen
        img = Image.open(file.stream)
        img = img.convert('RGB')
        img.thumbnail((800, 800))
        img.save(filepath, 'JPEG', quality=85)
        
        # Actualizar CSV
        update_cafeteria_field(id, 'imagen', filename)
        
        return redirect(url_for('cafeteria_detail', id=id))
    except Exception as e:
        print(f"Error subiendo imagen cafetería: {e}")
        return redirect(url_for('cafeteria_detail', id=id))


@app.route('/cita/<id>/upload-image', methods=['POST'])
def upload_cita_image(id):
    """Subir foto de portada para cita"""
    try:
        cita = find_cita(id)
        if not cita:
            return redirect(url_for('citas'))
        
        if 'imagen' not in request.files:
            return redirect(url_for('cita_detail', id=id))
        
        file = request.files['imagen']
        if file.filename == '':
            return redirect(url_for('cita_detail', id=id))
        
        if not allowed_file(file.filename):
            return redirect(url_for('cita_detail', id=id))
        
        # Generar nombre seguro
        filename = secure_filename(f"cita_{id}_{os.urandom(8).hex()}.jpg")
        filepath = os.path.join(app.config['UPLOAD_FOLDER_CITAS'], filename)
        
        # Guardar y optimizar imagen
        img = Image.open(file.stream)
        img = img.convert('RGB')
        img.thumbnail((800, 800))
        img.save(filepath, 'JPEG', quality=85)
        
        # Actualizar CSV
        update_cita_field(id, 'imagen', filename)
        
        return redirect(url_for('cita_detail', id=id))
    except Exception as e:
        print(f"Error subiendo imagen cita: {e}")
        return redirect(url_for('cita_detail', id=id))

# ============================================
# RUTAS PARA GOOGLE PHOTOS
# ============================================

@app.route('/cafeteria/<id>/save-google-photos', methods=['POST'])
def save_cafeteria_google_photos(id):
    """Guarda el link de Google Fotos para una cafetería"""
    cafeteria = find_cafeteria(id)
    if not cafeteria:
        return "Cafetería no encontrada", 404
    
    google_photos_link = request.form.get('google_photos_link', '')
    update_cafeteria_field(id, 'google_photos_link', google_photos_link)
    
    return redirect(url_for('cafeteria_detail', id=id))

@app.route('/cita/<id>/save-google-photos', methods=['POST'])
def save_cita_google_photos(id):
    """Guarda el link de Google Fotos para una cita"""
    cita = find_cita(id)
    if not cita:
        return "Cita no encontrada", 404
    
    google_photos_link = request.form.get('google_photos_link', '')
    update_cita_field(id, 'google_photos_link', google_photos_link)
    
    return redirect(url_for('cita_detail', id=id))

# ============================================
# RUTAS PARA MULTIMEDIA (CAFETERÍAS)
# ============================================

@app.route('/cafeteria/<id>/upload-media', methods=['POST'])
def upload_cafeteria_media(id):
    """Sube fotos/videos para una cafetería"""
    cafeteria = find_cafeteria(id)
    if not cafeteria:
        return "Cafetería no encontrada", 404
    
    files = request.files.getlist('media_files')
    saved_files = []
    
    # Obtener archivos existentes
    existing_media = cafeteria.get('media_files', '')
    existing_list = [f.strip() for f in existing_media.split(',') if f.strip()]
    
    for file in files:
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
            file.save(os.path.join(app.config['UPLOAD_FOLDER_CAFETERIAS'], filename))
            saved_files.append(filename)
    
    # Combinar archivos nuevos con existentes
    all_files = existing_list + saved_files
    media_string = ','.join(all_files)
    
    update_cafeteria_field(id, 'media_files', media_string)
    
    return redirect(url_for('cafeteria_detail', id=id))

# ============================================
# RUTAS PARA MULTIMEDIA (CITAS)
# ============================================

@app.route('/cita/<id>/upload-media', methods=['POST'])
def upload_cita_media(id):
    """Sube fotos/videos para una cita"""
    cita = find_cita(id)
    if not cita:
        return "Cita no encontrada", 404
    
    files = request.files.getlist('media_files')
    saved_files = []
    
    # Obtener archivos existentes
    existing_media = cita.get('media_files', '')
    existing_list = [f.strip() for f in existing_media.split(',') if f.strip()]
    
    for file in files:
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
            file.save(os.path.join(app.config['UPLOAD_FOLDER_CITAS'], filename))
            saved_files.append(filename)
    
    # Combinar archivos nuevos con existentes
    all_files = existing_list + saved_files
    media_string = ','.join(all_files)
    
    update_cita_field(id, 'media_files', media_string)
    
    return redirect(url_for('cita_detail', id=id))

@app.route('/add-cafeteria', methods=['POST'])
def add_cafeteria():
    """Crea una nueva cafetería con datos básicos y redirige a editar"""
    nuevo_id = str(int(time.time()))
    nueva_cafeteria = {
        'id': nuevo_id, 
        'nombre': 'Nueva Cafetería', 
        'ubicacion': '', 
        'visitada': 'False', 
        'imagen': '', 
        'fecha_visita': '',
        'google_maps_url': '', 
        'food_quality': '', 
        'ambiance': '', 
        'want_return': '', 
        'google_photos_link': '', 
        'media_files': ''
    }
    
    cafeterias = get_cafeterias_data()
    # Usamos las llaves del diccionario nuevo como nombres de columna si el archivo está vacío
    fieldnames = list(cafeterias[0].keys()) if cafeterias else list(nueva_cafeteria.keys())
    
    with open(CAFETERIAS_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if os.path.getsize(CAFETERIAS_FILE) == 0:
            writer.writeheader()
        writer.writerow(nueva_cafeteria)
    
    return redirect(url_for('edit_cafeteria', id=nuevo_id))

CITAS_FIELDS = ['id', 'nombre', 'ubicacion', 'realizada', 'imagen', 'fecha', 'fecha_realizada', 'google_photos_link', 'media_files']

@app.route('/add-cita', methods=['POST'])
def add_cita():
    """Crea una entrada NUEVA en el CSV y redirige a edición"""
    # Generamos un ID único para la nueva cita
    nuevo_id = str(int(time.time()))
    
    # Creamos el diccionario con la estructura exacta de tu CSV
    nueva_cita = {
        'id': nuevo_id,
        'nombre': 'Nueva Cita',
        'ubicacion': '',
        'realizada': 'False',
        'imagen': '',
        'fecha': '',
        'fecha_realizada': '',
        'google_photos_link': '',
        'media_files': ''
    }
    
    # Guardamos la nueva fila al final del archivo citas.csv
    with open(CITAS_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CITAS_FIELDS)
        if os.path.getsize(CITAS_FILE) == 0:
            writer.writeheader()
        writer.writerow(nueva_cita)
    
    # Una vez creada, enviamos al usuario a editar los detalles de esta NUEVA cita
    return redirect(url_for('edit_cita', id=nuevo_id))

@app.route('/cafeterias')
def cafeterias(): # El nombre de la función debe ser 'cafeterias'
    data = get_cafeterias_data()
    sort_type = request.args.get('sort', 'default')

    # Función para calcular el promedio de las 3 métricas
    def get_rating_avg(cafe):
        try:
            fq = int(cafe.get('food_quality', 0) or 0)
            amb = int(cafe.get('ambiance', 0) or 0)
            wr = int(cafe.get('want_return', 0) or 0)
            return (fq + amb + wr) / 3
        except (ValueError, TypeError):
            return 0

    # Ordenar de mayor a menor si se selecciona 'rating'
    if sort_type == 'rating':
        data = sorted(data, key=get_rating_avg, reverse=True)

    return render_template('cafeterias.html', cafeterias=data, current_sort=sort_type)

if __name__ == '__main__':
    app.run(debug=True)
