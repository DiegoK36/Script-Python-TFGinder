# Script desarrollado para la gestión de la Base de Datos, el Storage y el Auth de TFGinder.
# Todo ello para la gestión óptima de Firebase en la asignatura PCD.
# Desarrollado por el grupo dos dirgido por el jefe de grupod Diego Rodríguez.

# Importamos la librería de Firebase
import pyrebase
import sys

# Menu de opciones
def menu():
  print("-----MENU DE GESTION DE DATOS DE TFGINDER-----")
  print("""
  [1] Añadir un Profesor a la Database
  [2] Crear un Usuario en el Sistema de Atentificacion
  [3] Editar información de un Profesor de la Database
  [4] Eliminar un profesor de la Database
  [5] Salir
  """)

# Cabezera del Script
def cabezera():
  print("""

   _____ _____ ____ ___ _   _ ____  _____ ____  
  |_   _|  ___/ ___|_ _| \ | |  _ \| ____|  _ \ 
    | | | |_ | |  _ | ||  \| | | | |  _| | |_) |
    | | |  _|| |_| || || |\  | |_| | |___|  _ < 
    |_| |_|   \____|___|_| \_|____/|_____|_| \_\ 
                         <Developed by Group 2 PCD>\n                       
  """)
  # Aviso previo de el programa
  print("""-----IMPORTANTE-----\n 
  Asegurate de que la información que introduces es CORRECTA.
  Si no es correcta, podría generar conflicto con la aplicacion TFGinder.
  """)

def crearProfesor():
  # Añadir elementos al Storage
  print("\n-----INSERTAR AVATAR DEL PROFESOR EN STORAGE-----\n")
  filename = input("Introduce el directorio del archivo que deseas subir [tfginder/assets/avatars/]: ")
  cloudfilename = input("Introduce el directorio donde deseas guaradar tu archivo en la nube [Avatars/]: ")
  storage.child(cloudfilename).put(filename)
  print("El archivo ubicado en [" + filename + "] se ha guardado existosamente!\n")

  # Muestra la URL donde se almacena el Archivo
  print("-----URL DEL ARCHIVO ALMACENADO-----\n")
  print(storage.child(cloudfilename).get_url(None))
  # Guardamos la URL para asignarla al profesor
  url = storage.child(cloudfilename).get_url(None)

  # Añadir Profesores en la Database
  print("\n-----INSERTAR INFORMACION DEL PROFESOR EN LA DATABASE-----\n")
  id = input("Introduce el ID del profesor: ")
  name = input("Introduce el nombre del profesor: ")
  surname = input("Introduce los apellidos del profesor: ")
  mail = input("Introduce el correo del profesor: ")
  cv = input("Introduce el CV del profesor: ")
  area = input("Introduce las areas de experiencia del profesor: ")
  doc = input("¿Tiene un doctorado?: ")
  cred = input("Introduce la acreditación del profesor: ")

  # Almacenamos la inoformación en un diccionario de DATA
  data = {
    'ID': id,
    'Nombre': name,
    'Apellidos': surname,
    'Correo': mail,
    'Breve CV': cv,
    'Area Experiencia': area,
    'Doctorado': doc,
    'Acreditación': cred,
    'Avatar': url
  }

  # Subimos la información a la nube
  db.child('Usuarios').child('Profesores').child(id).set(data)
  print("La información del profesor " + name + " " + surname + " se ha guardado existosamente!\n")

def crearUsuario():
  # Creación de un usuario vinculado al correo en cuestión
  print("\n-----REGISTRO DE USUARIOS-----\n")
  mail = input("Introduce tu correo: ")
  passwd = input("Introduce una contraseña: ")
  confpasswd = input("Confirma tu contraseña: ")
  if passwd == confpasswd:
    try:
      auth.create_user_with_email_and_password(mail, passwd)
      print("Se ha creado una cuenta para vinculada al correo: " + mail)
    except:
      print("Ya existe una cuenta vinculada al correo")
  else:
    print("No coinciden las contraseñas, vuleve a intentarlo más tarde")

def modificarProfesor():
  print("\n-----MODIFICACION DE PROFESORES EN LA DATABASE-----\n")
  print("Listado de Profesores en la Database:")
  profesores = db.child("Usuarios").child("Profesores").get()
  for profesor in profesores.each():
    print("Profesor con ID [" + profesor.key() + "] Y Nombre [" + profesor.val()['Nombre'] + " " + profesor.val()[
      'Apellidos'] + "]\n")
  Num = input("Introduce el ID del usuario Profesor que deseas editar: ")
  for profesor in profesores.each():
    if profesor.val()['ID'] == Num:
      edit = input(
        "Introduce el campo que deseas editar [Nombre|Apellidos|Correo|Doctorado|Area Experiencia|Acreditación]: ")
      edit2 = input("Indroduce los cambios que deseas guardar: ")
      db.child("Usuarios").child("Profesores").child(profesor.key()).update({edit: edit2})

def eliminarProfesor():
  print("\n-----ELIMINACION DE PROFESORES EN LA DATABASE-----\n")
  print("Listado de Profesores en la Database:")
  profesores = db.child("Usuarios").child("Profesores").get()
  for profesor in profesores.each():
    print("Profesor con ID [" + profesor.key() + "] Y Nombre [" + profesor.val()['Nombre'] + " " + profesor.val()[
      'Apellidos'] + "]\n")
  Num = input("Introduce el ID del usuario Profesor que deseas eliminar: ")
  for profesor in profesores.each():
    if profesor.val()['ID'] == Num:
      db.child("Usuarios").child("Profesores").child(profesor.key()).remove()

# Establecemos las credenciales de aplicación Firebase
firebaseConfig = {
  'apiKey': "AIzaSyCHmoCZc9F1jd7uSTEebu-DJ8G892gY0fw",
  'authDomain': "ue22167749-254dc.firebaseapp.com",
  'databaseURL': "https://ue22167749-254dc-default-rtdb.firebaseio.com",
  'projectId': "ue22167749-254dc",
  'storageBucket': "ue22167749-254dc.appspot.com",
  'messagingSenderId': "291262583611",
  'appId': "1:291262583611:web:2740e3e475136634e99d1e",
  'measurementId': "G-NG4813ZWTC" }

# Conectamos con la aplicación a través de las credenciales
firebase=pyrebase.initialize_app(firebaseConfig)

# Instanciamos la Database, el Storage y Athentication
db=firebase.database()
storage=firebase.storage()
auth=firebase.auth()

cabezera()
menu()
opc = input("Introduce el número de la opcion que deseas: ")

match opc:
  case '0':
    menu()

  case '1':
    crearProfesor()

  case '2':
    crearUsuario()

  case '3':
    modificarProfesor()

  case '4':
    eliminarProfesor()

  case '5':
    sys.exit()

print("\nFinalizando la ejecucion del SCRIPT de TFGinder")
