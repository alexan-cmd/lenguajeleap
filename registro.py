import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, auth
import mysql.connector
from firebase_auth import get_access_token, get_user_info  # Asegúrate de que firebase_auth.py esté en el mismo directorio

# Inicializa Firebase
cred = credentials.Certificate("c:/Users/alexj/Downloads/lenguajeleap-firebase-adminsdk-qm3sl-a3cb6e358c.json")
firebase_admin.initialize_app(cred)

def login():
    username = entry_username.get()
    password = entry_password.get()

    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3307,
            user="root",
            password="",
            database="lenguajeleap"
        )
        cursor = conn.cursor()
        query = "SELECT * FROM iniciosesion WHERE usuario=%s AND contraseña=%s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            messagebox.showinfo("Inicio de sesión", "Inicio de sesión exitoso")
            create_welcome_frame() 
        else:
            messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos")

    except mysql.connector.Error as err:
        messagebox.showerror("Error de conexión", f"Error: {err}")

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def register():
    email = entry_reg_email.get()
    username = entry_reg_username.get()
    password = entry_reg_password.get()
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3307,
            user="root",
            password="",
            database="lenguajeleap"
        )
        cursor = conn.cursor()
        query = "INSERT INTO iniciosesion (correo, contraseña, usuario, fecha) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (email, password, username, date))
        conn.commit()
        messagebox.showinfo("Registro", "Usuario registrado exitosamente")

    except mysql.connector.Error as err:
        messagebox.showerror("Error de conexión", f"Error: {err}")

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def show_register():
    login_frame.place_forget()
    register_frame.place(relx=0.5, rely=0.5, anchor="center")

def show_login():
    register_frame.place_forget()
    login_frame.place(relx=0.5, rely=0.5, anchor="center")

def create_welcome_frame():
    login_frame.place_forget()
    register_frame.place_forget()
    welcome_frame.place(relx=0.5, rely=0.5, anchor="center")

def start_interests():
    welcome_frame.place_forget()
    interests_frame.place(relx=0.5, rely=0.5, anchor="center")

def submit_interests():
    reason = reason_combo.get()
    time = time_combo.get()
    preference = preference_combo.get()
    language = language_combo.get()
    learning_time = learning_time_combo.get()

    if reason and time and preference and language and learning_time:
        messagebox.showinfo("Éxito", "Preferencias de aprendizaje guardadas exitosamente")
    else:
        messagebox.showerror("Error", "Por favor, completa todos los campos")

def login_with_google():
    try:
        token = get_access_token()
        user_info = get_user_info(token)
        email = user_info.get('email')

        # Si el correo electrónico está en la base de datos, iniciar sesión
        conn = mysql.connector.connect(
            host="localhost",
            port=3307,
            user="root",
            password="",
            database="lenguajeleap"
        )
        cursor = conn.cursor()
        query = "SELECT * FROM iniciosesion WHERE correo=%s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if user:
            messagebox.showinfo("Inicio de sesión con Google", "Inicio de sesión exitoso con Google")
            create_welcome_frame()
        else:
            messagebox.showerror("Error", "No se encontró el usuario en la base de datos")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo iniciar sesión con Google: {e}")

app = tk.Tk()
app.title("LenguajeLeap")
app.geometry("600x400")
app.configure(bg="#f0f0f0")

# Estilos
bg_color = "#f0f0f0"
frame_color = "#ffffff"
button_color = "#000000"
button_fg_color = "#ffffff"
highlight_bg = "#FFD700"
highlight_fg = "#FF4500"
font_title = ("Comic Sans MS", 24, "bold")
font_label = ("Comic Sans MS", 12)
font_button = ("Comic Sans MS", 10, "bold")

background_label = tk.Label(app, bg="#ADD8E6")
background_label.place(relwidth=1, relheight=1)

left_design = tk.Frame(app, bg="#FF4500", width=50)
left_design.place(relx=0, rely=0, relheight=1)
right_design = tk.Frame(app, bg="#FF4500", width=50)
right_design.place(relx=1, rely=0, relheight=1, anchor="ne")

login_frame = tk.Frame(app, bg=bg_color)

label_title = tk.Label(login_frame, text="LenguajeLeap", font=font_title, bg=bg_color, fg=highlight_fg)
label_title.pack(pady=10)

frame_form = tk.Frame(login_frame, bg=frame_color, bd=2, relief="groove")
frame_form.pack(pady=10, padx=20, fill="both", expand=True)

label_username = tk.Label(frame_form, text="Nombre de usuario", font=font_label, bg=frame_color)
label_username.grid(row=0, column=0, pady=10, padx=10, sticky="e")
entry_username = tk.Entry(frame_form, font=font_label)
entry_username.grid(row=0, column=1, pady=10, padx=10)

label_password = tk.Label(frame_form, text="Contraseña", font=font_label, bg=frame_color)
label_password.grid(row=1, column=0, pady=10, padx=10, sticky="e")
entry_password = tk.Entry(frame_form, show="*", font=font_label)
entry_password.grid(row=1, column=1, pady=10, padx=10)

button_login = tk.Button(login_frame, text="Iniciar sesión", font=font_button, bg=button_color, fg=button_fg_color, command=login)
button_login.pack(pady=5)

button_register = tk.Button(login_frame, text="Únete ahora", font=font_button, bg=highlight_bg, fg=highlight_fg, command=show_register)
button_register.pack(pady=5)

button_google_login = tk.Button(login_frame, text="Iniciar sesión con Google", font=font_button, bg=button_color, fg=button_fg_color, command=login_with_google)
button_google_login.pack(pady=5)

login_frame.place(relx=0.5, rely=0.5, anchor="center")

register_frame = tk.Frame(app, bg=bg_color)

label_reg_title = tk.Label(register_frame, text="Registrar", font=font_title, bg=bg_color, fg=highlight_fg)
label_reg_title.pack(pady=10)

frame_reg_form = tk.Frame(register_frame, bg=frame_color, bd=2, relief="groove")
frame_reg_form.pack(pady=10, padx=20, fill="both", expand=True)

label_reg_email = tk.Label(frame_reg_form, text="Correo electrónico", font=font_label, bg=frame_color)
label_reg_email.grid(row=0, column=0, pady=10, padx=10, sticky="e")
entry_reg_email = tk.Entry(frame_reg_form, font=font_label)
entry_reg_email.grid(row=0, column=1, pady=10, padx=10)

label_reg_username = tk.Label(frame_reg_form, text="Nombre de usuario", font=font_label, bg=frame_color)
label_reg_username.grid(row=1, column=0, pady=10, padx=10, sticky="e")
entry_reg_username = tk.Entry(frame_reg_form, font=font_label)
entry_reg_username.grid(row=1, column=1, pady=10, padx=10)

label_reg_password = tk.Label(frame_reg_form, text="Contraseña", font=font_label, bg=frame_color)
label_reg_password.grid(row=2, column=0, pady=10, padx=10, sticky="e")
entry_reg_password = tk.Entry(frame_reg_form, show="*", font=font_label)
entry_reg_password.grid(row=2, column=1, pady=10, padx=10)

button_register_submit = tk.Button(register_frame, text="Registrarse", font=font_button, bg=button_color, fg=button_fg_color, command=register)
button_register_submit.pack(pady=5)

button_back_to_login = tk.Button(register_frame, text="Volver al inicio de sesión", font=font_button, bg=highlight_bg, fg=highlight_fg, command=show_login)
button_back_to_login.pack(pady=5)

welcome_frame = tk.Frame(app, bg=bg_color)

label_welcome = tk.Label(welcome_frame, text="Bienvenido a LenguajeLeap", font=font_title, bg=bg_color, fg=highlight_fg)
label_welcome.pack(pady=20)

button_start = tk.Button(welcome_frame, text="Comenzar", font=font_button, bg=button_color, fg=button_fg_color, command=start_interests)
button_start.pack(pady=5)

interests_frame = tk.Frame(app, bg=bg_color)

label_interests_title = tk.Label(interests_frame, text="Intereses y Objetivos", font=font_title, bg=bg_color, fg=highlight_fg)
label_interests_title.pack(pady=10)

label_reason = tk.Label(interests_frame, text="¿Por qué quieres aprender un idioma?", font=font_label, bg=bg_color)
label_reason.pack(pady=5)
reason_combo = ttk.Combobox(interests_frame, values=["Trabajo", "Estudios", "Viajes"], font=font_label)
reason_combo.pack(pady=5)

label_time = tk.Label(interests_frame, text="¿Cuánto tiempo puedes dedicar diariamente?", font=font_label, bg=bg_color)
label_time.pack(pady=5)
time_combo = ttk.Combobox(interests_frame, values=["15 minutos", "30 minutos", "1 hora"], font=font_label)
time_combo.pack(pady=5)

label_preference = tk.Label(interests_frame, text="¿Prefieres aprender de forma práctica o teórica?", font=font_label, bg=bg_color)
label_preference.pack(pady=5)
preference_combo = ttk.Combobox(interests_frame, values=["Práctica", "Teórica"], font=font_label)
preference_combo.pack(pady=5)

label_language = tk.Label(interests_frame, text="¿Qué idioma te gustaría aprender?", font=font_label, bg=bg_color)
label_language.pack(pady=5)
language_combo = ttk.Combobox(interests_frame, values=["Portugués", "Francés", "Inglés"], font=font_label)
language_combo.pack(pady=5)

label_learning_time = tk.Label(interests_frame, text="¿En cuánto tiempo deseas aprenderlo?", font=font_label, bg=bg_color)
label_learning_time.pack(pady=5)
learning_time_combo = ttk.Combobox(interests_frame, values=["3 meses", "6 meses", "1 año"], font=font_label)
learning_time_combo.pack(pady=5)

button_submit_interests = tk.Button(interests_frame, text="Enviar", font=font_button, bg=button_color, fg=button_fg_color, command=submit_interests)
button_submit_interests.pack(pady=5)

app.mainloop()
