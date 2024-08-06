import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

def load_users():
    if os.path.exists('arquivos/users.json'):
        with open('arquivos/users.json', 'r') as file:
            return json.load(file)
    return {'cliente': {}, 'personal': {}, 'todos': {}}

def save_users(users):
    with open('arquivos/users.json', 'w') as file:
        json.dump(users, file, indent=4)

def login():
    user_type = user_type_var.get()
    cpf = cpf_login_entry.get()
    password = password_login_entry.get()
    users = load_users()

    if user_type in users and cpf in users[user_type] and users[user_type][cpf]['password'] == password:
        messagebox.showinfo("Sucesso", f"Bem-vindo, {users[user_type][cpf]['name']}!")
        if user_type == "cliente":
            open_client_main_app(cpf)
        else:
            open_personal_main_app(cpf)
    else:
        messagebox.showerror("Erro", "Usuário não cadastrado ou senha incorreta")

def open_client_main_app(cpf):
    client_main_app = tk.Toplevel(root)
    client_main_app.title("Tela Principal do Cliente")
    client_main_app.geometry("1080x1000")
    center_window(client_main_app, 1080, 1000)

    tk.Label(client_main_app, text="Bem-vindo à Tela Principal do Cliente", font=('Arial', 14)).pack(pady=20)

    def schedule_workout():
        num_workouts = workout_var.get()
        plan = plan_var.get()
        start_date = start_date_entry.get()
        cost = 50 * num_workouts
        if plan == "Mensal":
            cost *= 4
        elif plan == "Anual":
            cost *= 52
        messagebox.showinfo("Agendar Treino", f"Treinos agendados: {num_workouts}\nPlano: {plan}\nData de início: {start_date}\nCusto total: R$ {cost}")

    tk.Label(client_main_app, text="Número de treinos na semana", font=('Arial', 10)).pack(pady=5)
    workout_var = tk.IntVar(value=1)
    for i in range(1, 6):
        tk.Radiobutton(client_main_app, text=f"{i} treino(s) na semana", variable=workout_var, value=i, font=('Arial', 10)).pack(pady=5)

    tk.Label(client_main_app, text="Data de início dos treinos (DD/MM/AAAA)", font=('Arial', 10)).pack(pady=5)
    start_date_entry = tk.Entry(client_main_app, font=('Arial', 10))
    start_date_entry.pack(pady=5)

    tk.Label(client_main_app, text="Plano", font=('Arial', 10)).pack(pady=5)
    plan_var = tk.StringVar(value="diário")
    tk.Radiobutton(client_main_app, text="Plano Diário", variable=plan_var, value="diário", font=('Arial', 10)).pack(pady=5)
    tk.Radiobutton(client_main_app, text="Plano Mensal", variable=plan_var, value="mensal", font=('Arial', 10)).pack(pady=5)
    tk.Radiobutton(client_main_app, text="Plano Anual", variable=plan_var, value="anual", font=('Arial', 10)).pack(pady=5)

    tk.Button(client_main_app, text="Agendar Treino", command=schedule_workout, font=('Arial', 12)).pack(pady=20)

    def check_payments():
        messagebox.showinfo("Verificar Pagamento", "Aqui você pode verificar se o pagamento foi realizado.")

    tk.Button(client_main_app, text="Verificar Pagamento", command=check_payments, font=('Arial', 12)).pack(pady=20)

def open_personal_main_app(cpf):
    personal_main_app = tk.Toplevel(root)
    personal_main_app.title("Tela Principal do Personal")
    personal_main_app.geometry("1080x1000")
    center_window(personal_main_app, 1080, 1000)

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

    tk.Button(personal_main_app, text="Visualizar Lista de Clientes", command=view_clients).pack(pady=20)

    def view_payments():
        messagebox.showinfo("Clientes que Pagaram", "Aqui você pode visualizar clientes que pagaram e não pagaram.")

    tk.Button(personal_main_app, text="Visualizar Pagamentos", command=view_payments).pack(pady=20)

    def create_client_profile():
        profile_window = tk.Toplevel(personal_main_app)
        profile_window.title("Criar Ficha do Cliente")
        profile_window.geometry("600x600")
        center_window(profile_window, 600, 600)

        tk.Label(profile_window, text="Criar Ficha do Cliente", font=('Arial', 14)).pack(pady=10)

        clients = load_users()['cliente']
        client_names = list(clients.keys())
        client_var = tk.StringVar()
        client_combobox = ttk.Combobox(profile_window, textvariable=client_var, values=client_names)
        client_combobox.pack(pady=10)

        def update_exercise_options(event):
            selected_client = client_var.get()
            if selected_client:
                for widget in profile_window.winfo_children():
                    if isinstance(widget, tk.Frame):
                        widget.pack_forget()
                exercise_frames[selected_client] = {}
                for muscle_group in exercises.keys():
                    tk.Label(profile_window, text=f"{muscle_group.capitalize()}:", font=('Arial', 10)).pack(pady=5)
                    muscle_exercises = exercises[muscle_group]
                    exercise_frame = tk.Frame(profile_window)
                    exercise_frame.pack(pady=5)
                    exercise_frames[selected_client][muscle_group] = exercise_frame

                    for exercise in muscle_exercises:
                        tk.Checkbutton(exercise_frame, text=exercise).pack(anchor='w')
                        tk.Label(exercise_frame, text="Séries:", font=('Arial', 8)).pack(anchor='w')
                        series_entry = tk.Entry(exercise_frame, font=('Arial', 8))
                        series_entry.pack(pady=2)
                        tk.Label(exercise_frame, text="Repetições:", font=('Arial', 8)).pack(anchor='w')
                        reps_entry = tk.Entry(exercise_frame, font=('Arial', 8))
                        reps_entry.pack(pady=2)
                        series_entries[exercise] = series_entry
                        reps_entries[exercise] = reps_entry

        tk.Label(profile_window, text="Escolha o cliente", font=('Arial', 10)).pack(pady=5)
        client_combobox.bind("<<ComboboxSelected>>", update_exercise_options)
        exercise_frames = {}
        series_entries = {}
        reps_entries = {}

        def save_profile():
            selected_client = client_var.get()
            if not selected_client:
                messagebox.showerror("Erro", "Selecione um cliente")
                return
            profile = {}
            for muscle_group, frame in exercise_frames[selected_client].items():
                profile[muscle_group] = {}
                for widget in frame.winfo_children():
                    if isinstance(widget, tk.Checkbutton) and widget.var.get() == 1:
                        exercise_name = widget.cget("text")
                        profile[muscle_group][exercise_name] = {
                            "series": series_entries[exercise_name].get(),
                            "reps": reps_entries[exercise_name].get()
                        }
            users = load_users()
            if 'todos' not in users:
                users['todos'] = {}
            users['todos'][selected_client] = profile
            save_users(users)
            messagebox.showinfo("Sucesso", "Ficha do cliente criada com sucesso!")

        tk.Button(profile_window, text="Salvar Ficha", command=save_profile).pack(pady=20)

def register():
    register_window = tk.Toplevel(root)
    register_window.title("Cadastro")
    register_window.geometry("1080x1000")
    center_window(register_window, 1080, 1000)

    tk.Label(register_window, text="Cadastrar", font=('Arial', 14)).pack(pady=10)
    tk.Label(register_window, text="Nome", font=('Arial', 10)).pack(pady=5)
    name_register_entry = tk.Entry(register_window, font=('Arial', 10))
    name_register_entry.pack(pady=5)

    tk.Label(register_window, text="CPF", font=('Arial', 10)).pack(pady=5)
    cpf_register_entry = tk.Entry(register_window, font=('Arial', 10), show='*')
    cpf_register_entry.pack(pady=5)

    tk.Label(register_window, text="Senha", font=('Arial', 10)).pack(pady=5)
    password_register_entry = tk.Entry(register_window, font=('Arial', 10), show='*')
    password_register_entry.pack(pady=5)

    user_type_var_register = tk.StringVar(value="cliente")
    tk.Radiobutton(register_window, text=   "Cliente", variable=user_type_var_register, value="cliente", font=('Arial', 10)).pack(pady=5)
    tk.Radiobutton(register_window, text="Personal", variable=user_type_var_register, value="personal", font=('Arial', 10)).pack(pady=5)

    def save_registration():
        user_type = user_type_var_register.get()
        name = name_register_entry.get()
        cpf = cpf_register_entry.get()
        password = password_register_entry.get()
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

    tk.Button(register_window, text="Registrar", command=save_registration, font=('Arial', 12)).pack(pady=20)

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

exercises = {
    "ombro": [
        "Desenvolvimento com Barra",
        "Desenvolvimento com Halteres",
        "Elevação Lateral com Halteres",
        "Elevação Frontal com Halteres",
        "Remada Alta",
        "Encolhimento de Ombros com Barra",
        "Encolhimento de Ombros com Halteres",
        "Elevação Lateral na Máquina",
        "Desenvolvimento Arnold",
        "Desenvolvimento Militar"
    ],
    "perna": [
        "Agachamento com Barra",
        "Leg Press",
        "Extensão de Pernas",
        "Flexão de Pernas",
        "Afundo",
        "Agachamento Hack",
        "Elevação de Panturrilha em Pé",
        "Elevação de Panturrilha Sentado",
        "Agachamento Sumô",
        "Cadeira Abdutora"
    ],
    "biceps": [
        "Rosca Direta com Barra",
        "Rosca Alternada com Halteres",
        "Rosca Martelo",
        "Rosca Scott",
        "Rosca Concentrada",
        "Rosca Inversa",
        "Rosca no Banco Inclinado",
        "Rosca com Pegada Supinada",
        "Rosca com Corda na Polia",
        "Rosca 21"
    ],
    "triceps": [
        "Tríceps na Polia Alta",
        "Tríceps Testa",
        "Mergulho entre Bancos",
        "Extensão de Tríceps com Halteres",
        "Tríceps na Polia com Pegada Fechada",
        "Tríceps Francês",
        "Tríceps com Corda na Polia",
        "Tríceps no Banco",
        "Kickback com Halteres",
        "Tríceps na Máquina"
    ],
    "costas": [
        "Remada Curvada com Barra",
        "Puxada na Polia Alta",
        "Remada Unilateral com Halteres",
        "Remada na Máquina",
        "Puxada com Pegada Neutra",
        "Puxada com Pegada Aberta",
        "Remada Sentada na Polia",
        "Pullover com Halteres",
        "Remada com Pegada Fechada",
        "Puxada no Cabo com Pegada Inversa"
    ],
    "abdominal": [
        "Crunch",
        "Elevação de Pernas",
        "Prancha",
        "Abdominal na Bola",
        "Crunch Invertido",
        "Abdominal com Peso",
        "Bicicleta no Ar",
        "Abdominal Oblíquo",
        "Elevação de Pernas Suspenso",
        "Abdominal no Banco Inclinado"
    ],
    "panturrilha": [
        "Elevação de Panturrilha em Pé",
        "Elevação de Panturrilha Sentado",
        "Elevação de Panturrilha Unilateral",
        "Elevação de Panturrilha com Barra",
        "Elevação de Panturrilha na Prensa",
        "Elevação de Panturrilha com Halteres",
        "Elevação de Panturrilha em Pé com Pé em V",
        "Elevação de Panturrilha Sentado com Peso",
        "Elevação de Panturrilha com Pegada Neutra",
        "Elevação de Panturrilha na Máquina"
    ],
    "antebraço": [
        "Rosca Inversa",
        "Rosca de Pulley",
        "Extensão de Pulso",
        "Rosca de Pulso com Halteres",
        "Pronação e Supinação com Halteres",
        "Rosca Inversa na Polia",
        "Rosca de Pulso com Barra",
        "Farmer's Walk",
        "Flexão de Pulso com Pegada Inversa",
        "Flexão de Pulso com Pegada Supinada"
    ],
    "peitoral": [
        "Supino Reto com Barra",
        "Supino Inclinado com Halteres",
        "Crucifixo com Halteres",
        "Flexões",
        "Peck Deck",
        "Supino Declinado com Barra",
        "Supino com Halteres em Banco Declinado",
        "Crucifixo Inclinado com Halteres",
        "Flexões com Pegada Larga",
        "Cross-over na Polia"
    ],
    "trapézio": [
        "Encolhimento de Ombros com Barra",
        "Encolhimento de Ombros com Halteres",
        "Remada Alta",
        "Encolhimento de Ombros na Máquina",
        "Remada Curvada com Barra",
        "Remada na Polia Alta",
        "Encolhimento de Ombros com Pegada Neutra",
        "Encolhimento com Barra na Frente",
        "Remada com Halteres na Inclinação",
        "Remada com Pegada Larga"
    ]
}

root = tk.Tk()
root.title("Login")
root.geometry("1080x1000")
center_window(root, 1080, 1000)

user_type_var = tk.StringVar(value="cliente")

tk.Label(root, text="Login", font=('Arial', 14)).pack(pady=10)

tk.Label(root, text="Nome", font=('Arial', 10)).pack(pady=5)
cpf_login_entry = tk.Entry(root, font=('Arial', 10))
cpf_login_entry.pack(pady=5)

tk.Label(root, text="CPF", font=('Arial', 10)).pack(pady=5)
cpf_login_entry = tk.Entry(root, font=('Arial', 10), show='*')
cpf_login_entry.pack(pady=5)

tk.Label(root, text="Senha", font=('Arial', 10)).pack(pady=5)
password_login_entry = tk.Entry(root, font=('Arial', 10), show='*')
password_login_entry.pack(pady=5)

tk.Radiobutton(root, text="Cliente", variable=user_type_var, value="cliente", font=('Arial', 10)).pack(pady=5)
tk.Radiobutton(root, text="Personal", variable=user_type_var, value="personal", font=('Arial', 10)).pack(pady=5)

tk.Button(root, text="Login", command=login, font=('Arial', 10)).pack(pady=20)
tk.Button(root, text="Cadastrar", command=register, font=('Arial', 10)).pack(pady=10)

root.mainloop()










