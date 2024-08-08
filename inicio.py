import mysql.connector
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw, ImageOps
import os

class LanguageApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Traductor")
        self.geometry("1280x720")

        try:
            self.db_connection = mysql.connector.connect(
                host="localhost",
                port=3307,
                user="root",
                password="",
                database="LenguajeLeap"
            )
            self.cursor = self.db_connection.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Error de conexión", f"No se puede conectar a la base de datos: {err}")
            self.destroy()
            return

        self.sidebar_frame = tk.Frame(self, width=200, bg='#1E90FF', height=720, relief='sunken', borderwidth=2)
        self.sidebar_frame.pack_propagate(False)
        self.main_frame = tk.Frame(self, bg='white')
        self.main_frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.bg_images = {
            "language_selection": self.load_image("mundooo.png"),
            "home": self.load_image("mundooooo.png"),
            "lessons": self.load_image("mundooo.png"),
            "levels": self.load_image("mundooo.png")
        }

        self.show_language_selection()

    def load_image(self, path):
        image = Image.open(path)
        image = image.resize((1280, 720), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def set_background(self, image_key):
        self.clear_main_frame()
        bg_photo = self.bg_images[image_key]
        bg_label = tk.Label(self.main_frame, image=bg_photo)
        bg_label.place(relwidth=1, relheight=1)
        bg_label.lower()

    def clear_sidebar(self):
        for widget in self.sidebar_frame.winfo_children():
            widget.destroy()

    def show_language_selection(self):
        self.set_background("language_selection")
        label = tk.Label(self.main_frame, text="Seleccione un idioma para aprender", font=("Arial", 24), bg='blue')
        label.place(relx=0.5, rely=0.1, anchor='center')

        language_frame = tk.Frame(self.main_frame, bg='#1E90FF', highlightthickness=0)
        language_frame.place(relx=0.5, rely=0.2, anchor='n')

        languages = [("Español", "Español"),
                     ("Inglés", "Inglés"),
                     ("Portugués", "Portugués"),
                     ("Francés", "Francés")]

        for lang_name, lang_code in languages:
            lang_button = tk.Button(language_frame, text=lang_name, width=20,
                                    command=lambda code=lang_code: self.show_home(code),
                                    bg='#1E90FF', fg='white', relief='flat', borderwidth=0)
            lang_button.pack(pady=5)

    def show_home(self, selected_language):
        self.sidebar_frame.place(x=0, y=0, relheight=1)
        self.main_frame.place(x=200, y=0, relwidth=0.87, relheight=1)
        self.set_background("home")
        self.clear_sidebar()

        welcome_label = tk.Label(self.main_frame, text=f" {selected_language}", font=("Arial", 24))
        welcome_label.place(relx=0.5, rely=0.1, anchor='center')

        buttons = [
            ("Inicio", "inicio.png", lambda: self.show_home(selected_language)),
            ("Progreso", "progreso.png", self.show_progress),
            ("Perfil", "perfil.png", self.show_profile),
            ("Ajustes", "ajustes.png", self.show_settings)
        ]

        for name, icon_path, command in buttons:
            if not os.path.isfile(icon_path):
                print(f"Error: La imagen {icon_path} no se encontró.")
                continue
            try:
                img = Image.open(icon_path)
                img = img.resize((32, 32), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error al cargar la imagen {icon_path}: {e}")
                continue

            button_frame = tk.Frame(self.sidebar_frame, bg='#1E90FF')
            button_frame.pack(pady=10, padx=10)

            button = tk.Button(button_frame, image=photo, command=command, bg='#1E90FF', relief='flat')
            button.photo = photo
            button.pack()

            label = tk.Label(button_frame, text=name, bg='#1E90FF', fg='white')
            label.pack()

        self.hover_label = tk.Label(self.sidebar_frame, text="", bg='#1E90FF', fg='white', anchor='w')
        self.hover_label.pack(fill='x', pady=5)

        circle_positions = [(82, 118), (416, 21), (753, 25), (941, 8), (1080.3, 230.3)]
        for i, (x, y) in enumerate(circle_positions, start=1):
            lesson_button = tk.Button(self.main_frame, text=f"Lección {i}", command=lambda i=i: self.show_lessons(i), relief='flat', borderwidth=0)
            lesson_button.place(x=x, y=y, width=80, height=80)
            self.make_button_circular(lesson_button)

    def make_button_circular(self, button):
        width = 80
        height = 80
        radius = min(width, height) // 2

        circle_image = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(circle_image)
        draw.ellipse((0, 0, width, height), fill='blue')

        mask = Image.new('L', (width, height), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, width, height), fill=255)
        circle_image.putalpha(mask)

        circle_image = ImageOps.fit(circle_image, (width, height), centering=(0.5, 0.5))
        circle_image_tk = ImageTk.PhotoImage(circle_image)

        button.config(image=circle_image_tk, compound='center', text=button.cget('text'), highlightthickness=0, bd=0)
        button.image = circle_image_tk

    def show_lessons(self, lesson_number):
        self.set_background("lessons")
        label = tk.Label(self.main_frame, text=f"Lección {lesson_number}", font=("Arial", 24), bg='white')
        label.place(relx=0.5, rely=0.1, anchor='center')

        lesson_frame = tk.Frame(self.main_frame, bg='white')
        lesson_frame.place(relx=0.5, rely=0.2, anchor='n')

        query = """
            SELECT niveles.nivel_id, niveles.nombre_nivel 
            FROM lecciones
            JOIN niveles ON lecciones.leccion_id = niveles.leccion_id
            WHERE lecciones.tipo_leccion = %s
        """
        
        try:
            self.cursor.execute(query, (f'leccion{lesson_number}',))
            levels = self.cursor.fetchall()
            if levels:
                for level in levels:
                    level_button = tk.Button(lesson_frame, text=f"Nivel {level[1]}", width=10, command=lambda l=level[0]: self.show_level(lesson_number, l))
                    level_button.pack(pady=5)
            else:
                messagebox.showinfo("Información", "No se encontraron niveles para esta lección.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error de base de datos", f"Error al consultar la base de datos: {err}")

    def show_level(self, lesson_number, level_id):
        self.set_background("levels")
        label = tk.Label(self.main_frame, text=f"Lección {lesson_number} - Nivel {level_id}", font=("Arial", 24), bg='white')
        label.place(relx=0.5, rely=0.1, anchor='center')

        query = """
            SELECT palabras.palabra, palabras.traduccion, ejercicios.tipo_ejercicio, ejercicios.descripcion
            FROM actividades
            JOIN palabras ON actividades.palabra_id = palabras.palabra_id
            JOIN ejercicios ON actividades.ejercicio_id = ejercicios.ejercicio_id
            WHERE actividades.nivel_id = %s
        """
        
        try:
            self.cursor.execute(query, (level_id,))
            actividades = self.cursor.fetchall()
            if actividades:
                for palabra, traduccion, tipo_ejercicio, descripcion in actividades:
                    if tipo_ejercicio == "Traducir palabra":
                        self.create_translation_activity(palabra, traduccion)
                    elif tipo_ejercicio == "Emparejar palabras":
                        self.create_matching_activity(palabra, traduccion)
                    elif tipo_ejercicio == "Escribir la palabra":
                        self.create_writing_activity(palabra, traduccion)
            else:
                messagebox.showinfo("Información", "No se encontraron actividades para este nivel.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error de base de datos", f"Error al consultar la base de datos: {err}")

    def create_translation_activity(self, palabra, traduccion):
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Traduce la siguiente palabra:", font=("Arial", 18), bg='white').pack(pady=20)
        
        tk.Label(self.main_frame, text=palabra, font=("Arial", 24), bg='white').pack(pady=20)
        
        self.translation_entry = tk.Entry(self.main_frame, font=("Arial", 18))
        self.translation_entry.pack(pady=20)
        
        submit_button = tk.Button(self.main_frame, text="Enviar", command=lambda: self.check_translation(traduccion))
        submit_button.pack(pady=20)

    def check_translation(self, correct_translation):
        user_translation = self.translation_entry.get()
        if user_translation.strip().lower() == correct_translation.lower():
            messagebox.showinfo("Correcto", "¡Respuesta correcta!")
        else:
            messagebox.showerror("Incorrecto", f"Respuesta incorrecta. La respuesta correcta es '{correct_translation}'.")

    def create_matching_activity(self, palabra, traduccion):
        pass

    def create_writing_activity(self, palabra, traduccion):
        pass

    def show_progress(self):
        self.set_background("home")
        label = tk.Label(self.main_frame, text="Progreso del Usuario", font=("Arial", 24), bg='white')
        label.place(relx=0.5, rely=0.1, anchor='center')

    def show_profile(self):
        self.clear_main_frame()
        label = tk.Label(self.main_frame, text="Perfil del Usuario", font=("Arial", 24), bg='white')
        label.place(relx=0.5, rely=0.1, anchor='center')

        profile_frame = tk.Frame(self.main_frame, bg='white')
        profile_frame.place(relx=0.5, rely=0.2, anchor='n')

        options = [("Información Personal", self.edit_personal_info),
                   ("Estadísticas de Aprendizaje", self.show_learning_stats),
                   ("Configuración de Cuenta", self.account_settings)]

        for option, command in options:
            option_button = tk.Button(profile_frame, text=option, width=25, command=command)
            option_button.pack(pady=5)

    def edit_personal_info(self):
        self.clear_main_frame()
        label = tk.Label(self.main_frame, text="Editar Información Personal", font=("Arial", 24), bg='white')
        label.place(relx=0.5, rely=0.1, anchor='center')

    def show_learning_stats(self):
        self.clear_main_frame()
        label = tk.Label(self.main_frame, text="Estadísticas de Aprendizaje", font=("Arial", 24), bg='white')
        label.place(relx=0.5, rely=0.1, anchor='center')

    def account_settings(self):
        self.clear_main_frame()
        label = tk.Label(self.main_frame, text="Configuración de Cuenta", font=("Arial", 24), bg='white')
        label.place(relx=0.5, rely=0.1, anchor='center')

    def show_settings(self):
        self.clear_main_frame()
        label = tk.Label(self.main_frame, text="Ajustes", font=("Arial", 24), bg='white')
        label.place(relx=0.5, rely=0.1, anchor='center')

        settings_frame = tk.Frame(self.main_frame, bg='white')
        settings_frame.place(relx=0.5, rely=0.2, anchor='n')

        sections = [("General", self.show_general_settings),
                    ("Cuenta", self.show_account_settings),
                    ("Apariencia", self.show_appearance_settings),
                    ("Audio", self.show_audio_settings),
                    ("Ayuda", self.show_help_settings)]

        for section, command in sections:
            section_button = tk.Button(settings_frame, text=section, width=20, command=command)
            section_button.pack(pady=5)

    def show_general_settings(self):
        self.clear_main_frame()
        label = tk.Label(self.main_frame, text="Ajustes Generales", font=("Arial", 24), bg='white')
        label.place(relx=0.5, rely=0.1, anchor='center')

        general_frame = tk.Frame(self.main_frame, bg='white')
        general_frame.place(relx=0.5, rely=0.2, anchor='n')

        options = [("Idioma de la Interfaz", self.change_interface_language),
                   ("Notificaciones", self.toggle_notifications),
                   ("Privacidad", self.show_privacy_settings),
                   ("Restablecer Progreso", self.reset_progress)]

        for option, command in options:
            option_button = tk.Button(general_frame, text=option, width=30, command=command)
            option_button.pack(pady=5)

    def change_interface_language(self):
        messagebox.showinfo("Idioma de la Interfaz", "Para cambiar el idioma de la interfaz")

    def toggle_notifications(self):
        messagebox.showinfo("Notificaciones", "Para configurar las notificaciones")

    def show_privacy_settings(self):
        messagebox.showinfo("Privacidad", "Para ajustar la configuración de privacidad")

    def reset_progress(self):
        if messagebox.askyesno("Restablecer Progreso", "¿Está seguro de que desea restablecer su progreso?"):
            messagebox.showinfo("Progreso Restablecido", "Su progreso ha sido restablecido.")

    def show_account_settings(self):
        self.clear_main_frame()
        label = tk.Label(self.main_frame, text="Ajustes de Cuenta", font=("Arial", 24), bg='white')
        label.place(relx=0.5, rely=0.1, anchor='center')

        account_frame = tk.Frame(self.main_frame, bg='white')
        account_frame.place(relx=0.5, rely=0.2, anchor='n')

        options = [("Información del Perfil", self.edit_profile_info),
                   ("Cambiar Contraseña", self.change_password),
                   ("Vinculación de Cuentas", self.link_accounts),
                   ("Cerrar Sesión", self.logout)]

        for option, command in options:
            option_button = tk.Button(account_frame, text=option, width=30, command=command)
            option_button.pack(pady=5)

    def edit_profile_info(self):
        messagebox.showinfo("Información del Perfil", "esto es para editar la información de su perfil")

    def change_password(self):
        messagebox.showinfo("Cambiar Contraseña", "esto es para cambiar la contraseña")

    def link_accounts(self):
        messagebox.showinfo("Vinculación de Cuentas", "esto es para vincular sus cuentas de Google, Facebook, etc")

    def logout(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro de que desea cerrar sesión?"):
            messagebox.showinfo("Sesión Cerrada", "Ha cerrado sesión exitosamente.")

    def show_appearance_settings(self):
        self.clear_main_frame()
        label = tk.Label(self.main_frame, text="Ajustes de Apariencia", font=("Arial", 24), bg='white')
        label.place(relx=0.5, rely=0.1, anchor='center')

        appearance_frame = tk.Frame(self.main_frame, bg='white')
        appearance_frame.place(relx=0.5, rely=0.2, anchor='n')

        options = [("Tema", self.change_theme),
                   ("Tamaño de Fuente", self.change_font_size)]

        for option, command in options:
            option_button = tk.Button(appearance_frame, text=option, width=30, command=command)
            option_button.pack(pady=5)

    def change_theme(self):
        messagebox.showinfo("Tema", "esto es para cambiar el tema de la aplicación")

    def change_font_size(self):
        messagebox.showinfo("Tamaño de Fuente", "esto es para cambiar el tamaño de la fuente")

    def show_audio_settings(self):
        self.clear_main_frame()
        label = tk.Label(self.main_frame, text="Ajustes de Audio", font=("Arial", 24), bg='white')
        label.place(relx=0.5, rely=0.1, anchor='center')

        audio_frame = tk.Frame(self.main_frame, bg='white')
        audio_frame.place(relx=0.5, rely=0.2, anchor='n')

        options = [("Volumen", self.change_volume),
                   ("Velocidad de Reproducción", self.change_playback_speed),
                   ("Tipo de Voz", self.change_voice_type)]

        for option, command in options:
            option_button = tk.Button(audio_frame, text=option, width=30, command=command)
            option_button.pack(pady=5)

    def change_volume(self):
        messagebox.showinfo("Volumen", "esto es para ajustar el volumen")

    def change_playback_speed(self):
        messagebox.showinfo("Velocidad de Reproducción", "esto es para cambiar la velocidad de reproducción del audio")

    def change_voice_type(self):
        messagebox.showinfo("Tipo de Voz", "esto es para seleccionar el tipo de voz (masculina/femenina)")

    def show_help_settings(self):
        self.clear_main_frame()
        label = tk.Label(self.main_frame, text="Ayuda y Soporte", font=("Arial", 24), bg='white')
        label.place(relx=0.5, rely=0.1, anchor='center')

        help_frame = tk.Frame(self.main_frame, bg='white')
        help_frame.place(relx=0.5, rely=0.2, anchor='n')

        options = [("Centro de Ayuda", self.open_help_center),
                   ("Reportar un Problema", self.report_problem),
                   ("Contactar Soporte", self.contact_support)]

        for option, command in options:
            option_button = tk.Button(help_frame, text=option, width=30, command=command)
            option_button.pack(pady=5)

    def open_help_center(self):
        messagebox.showinfo("Centro de Ayuda", "esto es para acceder al centro de ayuda")

    def report_problem(self):
        messagebox.showinfo("Reportar un Problema", "esto es para reportar un problema")

    def contact_support(self):
        messagebox.showinfo("Contactar Soporte", "contactar al soporte técnico")

if __name__ == "__main__":
    app = LanguageApp()
    app.mainloop()
