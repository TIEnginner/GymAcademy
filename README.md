import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime

# Funções para manipular os arquivos JSON
def load_users():
    if os.path.exists('arquivos/users.json'):
        with open('arquivos/users.json', 'r') as file:
            return json.load(file)
    return {'cliente': {}, 'personal': {}, 'todos': {}}

def save_users(users):
    with open('arquivos/users.json', 'w') as file:
        json.dump(users, file, indent=4)

# Exercícios por parte do corpo
exercises = {
    "Peito": ["Supino Reto com Barra", "Supino Inclinado com Halteres", "Crucifixo com Halteres", "Flexões", "Peck Deck", "Supino Declinado com Barra", "Supino com Halteres em Banco Declinado", "Crucifixo Inclinado com Halteres", "Flexões com Pegada Larga", "Cross-over na Polia"],
    "Costas": ["Remada Curvada com Barra", "Puxada na Polia Alta", "Remada Unilateral com Halteres", "Remada na Máquina", "Puxada com Pegada Neutra", "Puxada com Pegada Aberta", "Remada Sentada na Polia", "Pullover com Halteres", "Remada com Pegada Fechada", "Puxada no Cabo com Pegada Inversa"],
    "Pernas": ["Agachamento com Barra", "Leg Press", "Extensão de Pernas", "Flexão de Pernas", "Afundo", "Agachamento Hack", "Elevação de Panturrilha em Pé", "Elevação de Panturrilha Sentado", "Agachamento Sumô", "Cadeira Abdutora"],
    "Biceps": ["Rosca Direta com Barra", "Rosca Alternada com Halteres", "Rosca Martelo", "Rosca Scott", "Rosca Concentrada", "Rosca Inversa", "Rosca no Banco Inclinado", "Rosca com Pegada Supinada", "Rosca com Corda na Polia", "Rosca 21"],
    "Triceps": ["Tríceps na Polia Alta", "Tríceps Testa", "Mergulho entre Bancos", "Extensão de Tríceps com Halteres", "Tríceps na Polia com Pegada Fechada", "Tríceps Francês", "Tríceps com Corda na Polia", "Tríceps no Banco", "Kickback com Halteres", "Tríceps na Máquina"],
    "Antebraço": ["Rosca Inversa", "Rosca de Pulley", "Extensão de Pulso", "Rosca de Pulso com Halteres", "Pronação e Supinação com Halteres", "Rosca Inversa na Polia", "Rosca de Pulso com Barra", "Farmer's Walk", "Flexão de Pulso com Pegada Inversa", "Flexão de Pulso com Pegada Supinada"],
    "Ombro": ["Desenvolvimento com Barra", "Desenvolvimento com Halteres", "Elevação Lateral com Halteres", "Elevação Frontal com Halteres", "Remada Alta", "Encolhimento de Ombros com Barra", "Encolhimento de Ombros com Halteres", "Elevação Lateral na Máquina", "Desenvolvimento Arnold", "Desenvolvimento Militar"],
    "Abdominal": ["Crunch", "Elevação de Pernas", "Prancha", "Abdominal na Bola", "Crunch Invertido", "Abdominal com Peso", "Bicicleta no Ar", "Abdominal Oblíquo", "Elevação de Pernas Suspenso","Abdominal no Banco Inclinado"],
    "Panturrilha": ["Elevação de Panturrilha em Pé", "Elevação de Panturrilha Sentado", "Elevação de Panturrilha Unilateral", "Elevação de Panturrilha com Barra", "Elevação de Panturrilha na Prensa", "Elevação de Panturrilha com Halteres", "Elevação de Panturrilha em Pé com Pé em V", "Elevação de Panturrilha Sentado com Peso", "Elevação de Panturrilha com Pegada Neutra", "Elevação de Panturrilha na Máquina"],
    "Trapézio": ["Encolhimento de Ombros com Barra", "Encolhimento de Ombros com Halteres", "Remada Alta", "Encolhimento de Ombros na Máquina", "Remada Curvada com Barra", "Remada na Polia Alta", "Encolhimento de Ombros com Pegada Neutra", "Encolhimento com Barra na Frente", "Remada com Halteres na Inclinação", "Remada com Pegada Larga"]
}

# Função para abrir a tela principal do personal
def open_personal_main_app(cpf):
    personal_main_app = tk.Toplevel(root)
    personal_main_app.title("Tela Principal do Personal")
    personal_main_app.geometry("1080x800")
    center_window(personal_main_app, 1080, 800)

    tk.Label(personal_main_app, text="Bem-vindo à Tela Principal do Personal", font=('Arial', 14)).pack(pady=20)

    def view_clients():
        clients = load_users()['cliente']
        client_list_window = tk.Toplevel(personal_main_app)
        client_list_window.title("Lista de Clientes")
        client_list_window.geometry("600x400")
        center_window(client_list_window, 600, 400)
 
        tk.Label(client_list_window, text="Lista de Clientes", font=('Arial', 14)).pack(pady=10)
        client_list = tk.Listbox(client_list_window)
        client_list.pack(pady=10, fill=tk.BOTH, expand=True)
        for cpf in clients:
            client_list.insert(tk.END, f"{clients[cpf]['name']} - CPF: {cpf}")

    tk.Button(personal_main_app, text='Visualizar clientes', font=("Arial, 12"), command=view_clients).pack(pady=20)
    # Botão para criar ficha de treino
    tk.Button(personal_main_app, text="Criar Ficha de Treino", command=lambda: open_create_workout(cpf), font=('Arial', 12)).pack(pady=20)

    # Botão para visualizar fichas de treino
    def view_workouts():
        users = load_users()
        selected_client = client_var.get()
        if not selected_client:
            messagebox.showerror("Erro", "Selecione um cliente.")
            return

        workouts = users['cliente'].get(selected_client, {}).get('workouts', [])
        if not workouts:
            messagebox.showinfo("Visualizar Fichas de Treino", "Nenhuma ficha de treino encontrada.")
        else:
            workout_info = "\n".join([f"Data: {w['date']}\nExercícios: {', '.join(w['exercises'])}" for w in workouts])
            messagebox.showinfo("Visualizar Fichas de Treino", workout_info)

    tk.Button(personal_main_app, text="Visualizar Fichas de Treino", command=view_workouts, font=('Arial', 12)).pack(pady=20)

# Função para abrir a tela de criação de ficha de treino
def open_create_workout(cpf):
    global client_var
    create_workout_window = tk.Toplevel(root)
    create_workout_window.title("Criar Ficha de Treino")
    create_workout_window.geometry("1080x800")
    center_window(create_workout_window, 1080, 800)

    tk.Label(create_workout_window, text="Criar Ficha de Treino", font=('Arial', 14)).pack(pady=20)

    tk.Label(create_workout_window, text="Escolher Cliente", font=('Arial', 12)).pack(pady=10)
    client_var = tk.StringVar()
    client_dropdown = ttk.Combobox(create_workout_window, textvariable=client_var)
    clients = list(load_users()['cliente'].keys())
    client_dropdown['values'] = clients
    client_dropdown.pack(pady=10)

    tk.Label(create_workout_window, text="Escolher Parte do Corpo", font=('Arial', 12)).pack(pady=10)
    body_parts = list(exercises.keys())
    body_part_var = tk.StringVar()
    body_part_dropdown = ttk.Combobox(create_workout_window, textvariable=body_part_var)
    body_part_dropdown['values'] = body_parts
    body_part_dropdown.pack(pady=10)

    exercise_frames = {}
    exercise_vars = {}
    selected_body_parts = set()

    def update_exercises(*args):
        body_part = body_part_var.get()
        if body_part in exercises:
            exercise_frame = exercise_frames.get(body_part)
            if exercise_frame:
                exercise_frame.destroy()
            exercise_frame = tk.Frame(create_workout_window)
            exercise_frames[body_part] = exercise_frame
            exercise_frame.pack(pady=10)

            exercise_vars[body_part] = {}
            for exercise in exercises[body_part]:
                var = tk.BooleanVar()
                tk.Checkbutton(exercise_frame, text=exercise, variable=var).pack(anchor='w')
                exercise_vars[body_part][exercise] = var

            selected_body_parts.add(body_part)
        else:
            if body_part in exercise_frames:
                exercise_frames[body_part].destroy()
                exercise_frames.pop(body_part)
                selected_body_parts.discard(body_part)

    body_part_var.trace("w", update_exercises)

    def build_workout():
        selected_client = client_var.get()
        if not selected_client:
            messagebox.showerror("Erro", "Selecione um cliente.")
            return
        
        workout = []
        for body_part in selected_body_parts:
            if body_part in exercises:
                selected_exercises = exercise_vars.get(body_part, {})
                workout.extend([exercise for exercise, var in selected_exercises.items() if var.get()])

        if not workout:
            messagebox.showerror("Erro", "Selecione pelo menos um exercício.")
            return

        users = load_users()
        if selected_client not in users['cliente']:
            users['cliente'][selected_client] = {'workouts': []}
        elif 'workouts' not in users['cliente'][selected_client]:
            users['cliente'][selected_client]['workouts'] = []

        workout_entry = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'exercises': workout
        }

        users['cliente'][selected_client]['workouts'].append(workout_entry)
        save_users(users)
        messagebox.showinfo("Sucesso", "Ficha de treino criada com sucesso!")
        return

    tk.Button(create_workout_window, text="Criar Ficha de Treino", command=build_workout, font=('Arial', 12)).pack(pady=20)

# Função para abrir a tela principal do cliente
def open_client_main_app(cpf):
    client_main_app = tk.Toplevel(root)
    client_main_app.title("Tela Principal do Cliente")
    client_main_app.geometry("1080x800")
    center_window(client_main_app, 1080, 800)

    tk.Label(client_main_app, text="Bem-vindo à Tela Principal do Cliente", font=('Arial', 14)).pack(pady=20)

    # Verificar mensagens
    def check_messages():
        users = load_users()
        messages = users['personal'].get(cpf, {}).get('messages', [])
        if not messages:
            messagebox.showinfo("Verificar Mensagens", "Nenhuma mensagem recebida.")
        else:
            message_info = "\n".join([f"De: {msg['from']}, Data: {msg['date']}, Mensagem: {msg['message']}" for msg in messages])
            messagebox.showinfo("Verificar Mensagens", message_info)

    tk.Button(client_main_app, text="Verificar Mensagens", command=check_messages, font=('Arial', 12)).pack(pady=20)

    # Visualizar ficha de treino
    def view_workouts():
        users = load_users()
        workouts = users['cliente'].get(cpf, {}).get('workouts', [])
        if not workouts:
            messagebox.showinfo("Visualizar Fichas de Treino", "Nenhuma ficha de treino encontrada.")
        else:
            workout_info = "\n".join([f"Data: {w['date']}\nExercícios: {', '.join(w['exercises'])}" for w in workouts])
            messagebox.showinfo("Visualizar Fichas de Treino", workout_info)

    tk.Button(client_main_app, text="Visualizar Fichas de Treino", command=view_workouts, font=('Arial', 12)).pack(pady=20)

# Função para registrar novo usuário
def register():
    global register_window, user_type_var_register
    register_window = tk.Toplevel(root)
    register_window.title("Registro")
    register_window.geometry("1080x1000")
    center_window(register_window, 1080, 1000)

    tk.Label(register_window, text="Tela de cadastro", font=('Arial', 14)).pack(pady=20)

    tk.Label(register_window, text="Nome", font=('Arial', 10)).pack(pady=10)
    global name_register_entry
    name_register_entry = tk.Entry(register_window, font=('Arial', 10))
    name_register_entry.pack(pady=5)

    tk.Label(register_window, text="CPF", font=('Arial', 10)).pack(pady=10)
    global cpf_register_entry
    cpf_register_entry = tk.Entry(register_window, font=('Arial', 10))
    cpf_register_entry.pack(pady=5)

    tk.Label(register_window, text="Senha", font=('Arial', 10)).pack(pady=10)
    global password_register_entry
    password_register_entry = tk.Entry(register_window, font=('Arial', 10), show='*')
    password_register_entry.pack(pady=5)

    tk.Label(register_window, text="Tipo de Usuário", font=('Arial', 12)).pack(pady=10)
    user_type_var_register = tk.StringVar(value="cliente")
    tk.Radiobutton(register_window, text="Cliente", variable=user_type_var_register, value="cliente", font=('Arial', 10)).pack(pady=5)
    tk.Radiobutton(register_window, text="Personal", variable=user_type_var_register, value="personal", font=('Arial', 10)).pack(pady=5)

    tk.Button(register_window, text="Registrar", command=save_registration, font=('Arial', 12)).pack(pady=20)

def save_registration():
    user_type = user_type_var_register.get()
    name = name_register_entry.get()
    cpf = cpf_register_entry.get()
    password = password_register_entry.get()

    if not name or not cpf or not password:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
        return

    users = load_users()

    if user_type not in users:
        users[user_type] = {}

    if cpf in users[user_type]:
        messagebox.showerror("Erro", "Usuário já cadastrado")
    else:
        users[user_type][cpf] = {'name': name, 'password': password}
        save_users(users)
        messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso")
        register_window.destroy()

# Função para centralizar a janela
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) / 2
    y = (screen_height - height) / 2
    window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

# Função de login
def login():
    user_type = user_type_var.get()
    cpf = cpf_login_entry.get()
    password = password_login_entry.get()

    if not cpf or not password:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
        return

    users = load_users()

    if user_type in users and cpf in users[user_type] and users[user_type][cpf]['password'] == password:
        if user_type == 'cliente':
            open_client_main_app(cpf)
        elif user_type == 'personal':
            open_personal_main_app(cpf)
        root.withdraw()  # Oculta a janela principal após o login
    else:
        messagebox.showerror("Erro", "CPF ou senha inválidos.")

# Configuração da tela inicial
root = tk.Tk()
root.title("Sistema de Gestão de Treinos")
root.geometry("1080x800")
center_window(root, 1080, 800)

tk.Label(root, text="Sistema de Gestão de Treinos", font=('Arial', 14)).pack(pady=20)

tk.Label(root, text="Nome", font=('Arial', 10)).pack(pady=10)
cpf_login_entry = tk.Entry(root, font=('Arial', 10))
cpf_login_entry.pack(pady=5)

tk.Label(root, text="CPF", font=('Arial', 10)).pack(pady=10)
cpf_login_entry = tk.Entry(root, font=('Arial', 10), show='*')
cpf_login_entry.pack(pady=5)

tk.Label(root, text="Senha", font=('Arial', 10)).pack(pady=10)
password_login_entry = tk.Entry(root, font=('Arial', 10), show='*')
password_login_entry.pack(pady=5)

tk.Label(root, text="Tipo de Usuário", font=('Arial', 10)).pack(pady=10)
user_type_var = tk.StringVar(value="cliente")
tk.Radiobutton(root, text="Cliente", variable=user_type_var, value="cliente", font=('Arial', 10)).pack(pady=5)
tk.Radiobutton(root, text="Personal", variable=user_type_var, value="personal", font=('Arial', 10)).pack(pady=5)

tk.Button(root, text="Login", command=login, font=('Arial', 10)).pack(pady=10)
tk.Button(root, text="Cadastrar", command=register, font=('Arial', 10)).pack(pady=10)

root.mainloop()
