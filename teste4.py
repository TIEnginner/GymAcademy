import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime
from PIL import Image, ImageTk
from tkinter import filedialog

DATA_DIR = 'data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def load_data(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            return json.load(file)
    return []

def save_data(data, filename):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)
    
users_data = load_data('users.json')
appointments_data = load_data('appointments.json')
payments_data = load_data('payments.json')
workouts_data = load_data('workouts.json')
inventory_data = load_data('inventory.json')

def load_users():
    if os.path.exists('arquivos/users.json'):
        with open('arquivos/users.json', 'r') as file:
            return json.load(file)
    return {'cliente': {}, 'personal': {}, 'todos': {}}

def save_users(users):
    with open('arquivos/users.json', 'w') as file:
        json.dump(users, file, indent=4)

def load_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
    if file_path:
        img = Image.open(file_path)
        img = ImageTk.PhotoImage(img)
        image_label.configure(image=img)
        image_label.image = img


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

def main():
    global image_label

    root = tk.Tk()
    root.title("Visualizador de Imagens")
    root.geometry("1080x1000")
    center_window(root, 1080, 1000)

    image_label = tk.Label(root)
    image_label.pack(expand=True)

    menu = tk.Menu(root)
    root.config(menu=menu)
    file_menu = tk.Menu(menu)
    menu.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Open Image", command=load_image)

def create_appointments_window():
    window = tk.Toplevel()
    window.title("Agendamento de Compromissos")
    window.geometry("1080x1000")
    center_window(window, 1080, 1000)

    tk.Label(window, text="Adicionar Compromisso", font=('Arial', 14)).pack(pady=10)

    tk.Label(window, text="Escolher Cliente", font=('Arial', 12)).pack(pady=10)
    client_var = tk.StringVar()
    client_dropdown = ttk.Combobox(window, textvariable=client_var)
    clients = list(load_users()['cliente'].keys())
    client_dropdown['values'] = clients
    client_dropdown.pack(pady=10)

    tk.Label(window, text="Data e Hora", font=('Arial', 12)).pack(pady=5)
    date_entry = tk.Entry(window, font=('Arial', 12))
    date_entry.pack(pady=5)
    tk.Label(window, text="Padrão: DD-MM-YYYY HH:MM", font=('Arial', 10)).pack(pady=5)

    tk.Label(window, text="Descrição", font=('Arial', 12)).pack(pady=5)
    description_entry = tk.Entry(window, font=('Arial', 12))
    description_entry.pack(pady=5)

    def save_appointment():
        client = client_var.get()
        date_time = date_entry.get()
        description = description_entry.get()

        if not client or not date_time or not description:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        appointment = {
            'client': client,
            'date_time': date_time,
            'description': description,
            'created_at': datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }

        appointments_data.append(appointment)
        save_data(appointments_data, 'appointments.json')
        messagebox.showinfo("Sucesso", "Compromisso salvo com sucesso!")
        window.destroy()

    tk.Button(window, text="Salvar", command=save_appointment, font=('Arial', 12)).pack(pady=10)

def create_appointments_window():
    window = tk.Toplevel()
    window.title("Agendamento de Compromissos")
    window.geometry("1080x1000")
    center_window(window, 1080, 1000)

    tk.Label(window, text="Adicionar Compromisso", font=('Arial', 14)).pack(pady=10)

    tk.Label(window, text="Escolher Cliente", font=('Arial', 12)).pack(pady=10)
    client_var = tk.StringVar()
    client_dropdown = ttk.Combobox(window, textvariable=client_var)
    clients = list(load_users()['cliente'].keys())
    client_dropdown['values'] = clients
    client_dropdown.pack(pady=10)

    tk.Label(window, text="Data e Hora", font=('Arial', 12)).pack(pady=5)
    date_entry = tk.Entry(window, font=('Arial', 12))
    date_entry.pack(pady=5)
    tk.Label(window, text="Padrão: DD-MM-YYYY HH:MM", font=('Arial', 10)).pack(pady=5)

    tk.Label(window, text="Descrição", font=('Arial', 12)).pack(pady=5)
    description_entry = tk.Entry(window, font=('Arial', 12))
    description_entry.pack(pady=5)

    def save_appointment():
        client = client_var.get()
        date_time = date_entry.get()
        description = description_entry.get()

        if not client or not date_time or not description:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        appointment = {
            'client': client,
            'date_time': date_time,
            'description': description,
            'created_at': datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }

        appointments_data.append(appointment)
        save_data(appointments_data, 'appointments.json')
        messagebox.showinfo("Sucesso", "Compromisso salvo com sucesso!")
        window.destroy()

    tk.Button(window, text="Salvar", command=save_appointment, font=('Arial', 12)).pack(pady=10)

def create_payments_window():
    window = tk.Toplevel()
    window.title("Gerenciamento de Pagamentos")
    window.geometry("1080x1000")
    center_window(window, 1080, 1000)

    tk.Label(window, text="Registrar Pagamento", font=('Arial', 14)).pack(pady=10)

    tk.Label(window, text="Escolher Cliente", font=('Arial', 12)).pack(pady=10)
    client_var = tk.StringVar()
    client_dropdown = ttk.Combobox(window, textvariable=client_var)
    clients = list(load_users()['cliente'].keys())
    client_dropdown['values'] = clients
    client_dropdown.pack(pady=10)

    tk.Label(window, text="Valor", font=('Arial', 12)).pack(pady=5)
    amount_entry = tk.Entry(window, font=('Arial', 12))
    amount_entry.pack(pady=5)

    tk.Label(window, text="Data do Pagamento", font=('Arial', 12)).pack(pady=5)
    date_entry = tk.Entry(window, font=('Arial', 12))
    date_entry.pack(pady=5)
    tk.Label(window, text="Padrão: DD-MM-YYYY", font=('Arial', 10)).pack(pady=5)

    tk.Label(window, text="Descrição", font=('Arial', 12)).pack(pady=5)
    description_entry = tk.Entry(window, font=('Arial', 12))
    description_entry.pack(pady=5)

    def save_payment():
        client = client_var.get()
        amount = amount_entry.get()
        payment_date = date_entry.get()
        description = description_entry.get()

        if not client or not amount or not payment_date or not description:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        payment = {
            'client': client,
            'amount': amount,
            'payment_date': payment_date,
            'description': description,
            'recorded_at': datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }

        payments_data.append(payment)
        save_data(payments_data, 'payments.json')
        messagebox.showinfo("Sucesso", "Pagamento registrado com sucesso!")
        window.destroy()

    tk.Button(window, text="Salvar", command=save_payment, font=('Arial', 12)).pack(pady=10)

def create_inventory_window():
    window = tk.Toplevel()
    window.title("Gerenciamento de Inventário")
    window.geometry("1080x1000")
    center_window(window, 1080, 1000)

    tk.Label(window, text="Adicionar Item ao Inventário", font=('Arial', 14)).pack(pady=10)

    tk.Label(window, text="Nome do Item", font=('Arial', 12)).pack(pady=5)
    item_name_entry = tk.Entry(window, font=('Arial', 12))
    item_name_entry.pack(pady=5)

    tk.Label(window, text="Quantidade", font=('Arial', 12)).pack(pady=5)
    quantity_entry = tk.Entry(window, font=('Arial', 12))
    quantity_entry.pack(pady=5)

    tk.Label(window, text="Descrição", font=('Arial', 12)).pack(pady=5)
    description_entry = tk.Entry(window, font=('Arial', 12))
    description_entry.pack(pady=5)

    def save_inventory():
        item_name = item_name_entry.get()
        quantity = quantity_entry.get()
        description = description_entry.get()

        if not item_name or not quantity or not description:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        item = {
            'item_name': item_name,
            'quantity': quantity,
            'description': description,
            'added_at': datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }

        inventory_data.append(item)
        save_data(inventory_data, 'inventory.json')
        messagebox.showinfo("Sucesso", "Item adicionado ao inventário com sucesso!")
        window.destroy()

    tk.Button(window, text="Salvar", command=save_inventory, font=('Arial', 12)).pack(pady=10)

def create_progress_tracking_window():
    window = tk.Toplevel()
    window.title("Registro de Evolução")
    window.geometry("1080x1000")
    center_window(window, 1080, 1000)

    tk.Label(window, text="Registrar Evolução do Aluno", font=('Arial', 14)).pack(pady=10)

    tk.Label(window, text="Escolher Cliente", font=('Arial', 12)).pack(pady=10)
    client_var = tk.StringVar()
    client_dropdown = ttk.Combobox(window, textvariable=client_var)
    clients = list(load_users()['cliente'].keys())
    client_dropdown['values'] = clients
    client_dropdown.pack(pady=10)

    tk.Label(window, text="Data", font=('Arial', 12)).pack(pady=5)
    date_entry = tk.Entry(window, font=('Arial', 12))
    date_entry.pack(pady=5)
    tk.Label(window, text="Padrão: DD-MM-YYYY", font=('Arial', 10)).pack(pady=5)

    tk.Label(window, text="Observações", font=('Arial', 12)).pack(pady=5)
    observations_entry = tk.Entry(window, font=('Arial', 12))
    observations_entry.pack(pady=5)
    
    tk.Label(window, text="Anexar Imagem/Vídeo", font=('Arial', 12)).pack(pady=5)
    tk.Button(window, text="Anexar", command=load_image, font=('Arial', 10)).pack(pady=5)

    def save_progress():
        client = client_var.get()
        date = date_entry.get()
        observations = observations_entry.get()

        if not client or not date or not observations:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        progress = {
            'client': client,
            'date': date,
            'observations': observations,
            'recorded_at': datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }

        save_data(progress, 'progress.json')
        messagebox.showinfo("Sucesso", "Evolução registrada com sucesso!")
        window.destroy()

    tk.Button(window, text="Salvar", command=save_progress, font=('Arial', 12)).pack(pady=10)

def create_communication_window():
    window = tk.Toplevel()
    window.title("Comunicação com Alunos")
    window.geometry("1080x1000")
    users = load_users()
    center_window(window, 1080, 1000)
 
    tk.Label(window, text="Enviar Mensagem", font=('Arial', 14)).pack(pady=10)
 
    tk.Label(window, text="Escolher Cliente", font=('Arial', 12)).pack(pady=10)
    client_var = tk.StringVar()
    client_dropdown = ttk.Combobox(window, textvariable=client_var)
    clients = list(users['cliente'].keys())
    client_dropdown['values'] = clients
    client_dropdown.pack(pady=10)
 
    tk.Label(window, text="Assunto", font=('Arial', 12)).pack(pady=5)
    subject_entry = tk.Entry(window, font=('Arial', 12))
    subject_entry.pack(pady=5)
 
    tk.Label(window, text="Mensagem", font=('Arial', 12)).pack(pady=5)
    message_text = tk.Text(window, height=10, width=50, font=('Arial', 12))
    message_text.pack(pady=5)
 
    def send_message():
        client = client_var.get()
        subject = subject_entry.get()
        message = message_text.get("1.0", tk.END).strip()
 
        if not client or not subject or not message:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return
 
        messagebox.showinfo("Sucesso", "Mensagem enviada com sucesso!")
        window.destroy()
 
    tk.Button(window, text="Enviar", command=send_message, font=('Arial', 12)).pack(pady=10)
def create_reports_window():
    window = tk.Toplevel()
    window.title("Geração de Relatórios")
    window.geometry("1080x1000")
    center_window(window, 1080, 1000)

    tk.Label(window, text="Gerar Relatório", font=('Arial', 14)).pack(pady=10)

    tk.Label(window, text="Tipo de Relatório", font=('Arial', 12)).pack(pady=5)
    report_type = tk.StringVar(window)
    report_type.set("Selecione")
    tk.OptionMenu(window, report_type, "Progresso dos Alunos", "Pagamentos", "Inventário", "Compromissos").pack(pady=5)

    def generate_report():
        selected_report = report_type.get()

        if selected_report == "Selecione":
            messagebox.showerror("Erro", "Selecione um tipo de relatório.")
            return

        messagebox.showinfo("Sucesso", f"Relatório de '{selected_report}' gerado com sucesso!")
        window.destroy()

    tk.Button(window, text="Gerar Relatório", command=generate_report, font=('Arial', 12)).pack(pady=10)

def open_personal_main_app(cpf):
    personal_main_app = tk.Toplevel(root)
    personal_main_app.title("Tela Principal do Personal")
    personal_main_app.geometry("1080x800")
    center_window(personal_main_app, 1080, 1000)

    tk.Label(personal_main_app, text="Bem-vindo à Tela Principal do Personal", font=('Arial', 14)).pack(pady=20)


    tk.Button(personal_main_app, text='Visualizar clientes', font=("Arial, 12"), command=view_clients).pack(pady=20)
    tk.Button(personal_main_app, text="Criar Ficha de Treino", command=lambda: open_create_workout(cpf), font=('Arial', 12)).pack(pady=20)
    tk.Button(personal_main_app, text="Agendamento de Compromissos", command=create_appointments_window, font=('Arial', 12)).pack(pady=10)
    tk.Button(personal_main_app, text="Gerenciamento de Pagamentos", command=create_payments_window, font=('Arial', 12)).pack(pady=10)
    tk.Button(personal_main_app, text="Gerenciamento de Inventário", command=create_inventory_window, font=('Arial', 12)).pack(pady=10)
    tk.Button(personal_main_app, text="Registro de Evolução", command=create_progress_tracking_window, font=('Arial', 12)).pack(pady=10)
    tk.Button(personal_main_app, text="Comunicação com Alunos", command=create_communication_window, font=('Arial', 12)).pack(pady=10)
    tk.Button(personal_main_app, text="Relatórios Detalhados", command=create_reports_window, font=('Arial', 12)).pack(pady=10)

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

def view_clients():
    clients = load_users()['cliente']
    client_list_window = tk.Toplevel()
    client_list_window.title("Lista de Clientes")
    client_list_window.geometry("1080x1000")
    center_window(client_list_window, 1080, 1000)

    tk.Label(client_list_window, text="Lista de Clientes", font=('Arial', 14)).pack(pady=10)
    client_list = tk.Listbox(client_list_window)
    client_list.pack(pady=10, fill=tk.BOTH, expand=True)
    for cpf in clients:
        client_list.insert(tk.END, f"{clients[cpf]['Nome']} - CPF: {cpf} - Contato: {cpf} - Sexo: {cpf} - Peso: {cpf} - Altura: {cpf}\n")

def open_create_workout(cpf):
    global client_var
    create_workout_window = tk.Toplevel(root)
    create_workout_window.title("Criar Ficha de Treino")
    create_workout_window.geometry("1080x800")
    center_window(create_workout_window, 1080, 1000)

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
            'date': datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            'exercises': workout
        }

        users['cliente'][selected_client]['workouts'].append(workout_entry)
        save_users(users)
        messagebox.showinfo("Sucesso", "Ficha de treino criada com sucesso!")
        create_workout_window.destroy()

    tk.Button(create_workout_window, text="Criar Ficha de Treino", command=build_workout, font=('Arial', 12)).pack(pady=20)

def register():
    global register_window, user_type_var_register_client
    register_window = tk.Toplevel(root)
    register_window.title("Registro")
    register_window.geometry("1080x1000")
    center_window(register_window, 1080, 1000)

    tk.Label(register_window, text="Tela de cadastro de Alunos", font=('Arial', 14)).pack(pady=20)

    tk.Label(register_window, text="Nome", font=('Arial', 10)).pack(pady=10)
    global name_register_entry
    name_register_entry = tk.Entry(register_window, font=('Arial', 10))
    name_register_entry.pack(pady=5)

    tk.Label(register_window, text="CPF", font=('Arial', 10)).pack(pady=10)
    global cpf_register_entry
    cpf_register_entry = tk.Entry(register_window, font=('Arial', 10))
    cpf_register_entry.pack(pady=5)

    tk.Label(register_window, text="Contato", font=('Arial', 10)).pack(pady=10)
    global contato_register_entry
    contato_register_entry = tk.Entry(register_window, font=('Arial', 10))
    contato_register_entry.pack(pady=5)

    tk.Label(register_window, text="Genero", font=('Arial', 10)).pack(pady=10)
    global option_combobox
    selected_option = tk.StringVar()
    genero_register_entry = ['Masculino', 'Feminino', 'Outros']
    option_combobox = ttk.Combobox(register_window, textvariable=selected_option, values=genero_register_entry)
    option_combobox.pack(pady=10)

    tk.Label(register_window, text="Peso (KG)", font=('Arial', 10)).pack(pady=10)
    global peso_register_entry
    peso_register_entry = tk.Entry(register_window, font=('Arial', 10))
    peso_register_entry.pack(pady=5)

    tk.Label(register_window, text="Altura (metros)", font=('Arial', 10)).pack(pady=10)
    global altura_register_entry
    altura_register_entry = tk.Entry(register_window, font=('Arial', 10))
    altura_register_entry.pack(pady=5)

    user_type_var_register_client = tk.StringVar(value="cliente")

    tk.Button(register_window, text="Registrar", command=save_registration_client, font=('Arial', 12)).pack(pady=20)

def register_personal():
    global register_window
    register_window = tk.Toplevel(root)
    register_window.title("Registro")
    register_window.geometry("1080x1000")
    center_window(register_window, 1080, 1000)

    tk.Label(register_window, text="Tela de cadastro de Personal", font=('Arial', 14)).pack(pady=20)

    tk.Label(register_window, text="Nome", font=('Arial', 10)).pack(pady=10)
    global name_register_entry
    name_register_entry = tk.Entry(register_window, font=('Arial', 10))
    name_register_entry.pack(pady=5)

    tk.Label(register_window, text="Senha", font=('Arial', 10)).pack(pady=10)
    global password_register_entry
    password_register_entry = tk.Entry(register_window, font=('Arial', 10), show='*')
    password_register_entry.pack(pady=5)

    global user_type_var_register_personal
    user_type_var_register_personal = tk.StringVar(value='personal')

    tk.Button(register_window, text="Registrar", command=save_registration_personal, font=('Arial', 12)).pack(pady=20)

def save_registration_personal():
    user_type = user_type_var_register_personal.get()
    name = name_register_entry.get()
    password = password_register_entry.get()

    if not name or not password:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
        return
    
    users = load_users()
    
    if name in users[user_type] and password in users[user_type]:
        messagebox.showerror("Erro", "Usuário já cadastrado")
    else:
        users[user_type][name] = {'Nome': name, 'Senha': password}
        save_users(users)
        messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso")
        register_window.destroy()

def save_registration_client():
    user_type_client = user_type_var_register_client.get()
    name = name_register_entry.get()
    cpf = cpf_register_entry.get()
    contato = contato_register_entry.get()
    genero = option_combobox.get()
    peso = peso_register_entry.get()
    altura = altura_register_entry.get()

    if not name or not cpf or not contato or not genero or not peso or not altura:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
        return

    users = load_users()

    if user_type_client not in users:
        users[user_type_client] = {}

    if cpf in users[user_type_client]:
        messagebox.showerror("Erro", "Usuário já cadastrado")
    else:
        users[user_type_client][cpf] = {'Nome': name, 'CPF': cpf, 'Contato':contato, 'Sexo': genero, 'Peso': peso, 'Altura': altura}
        save_users(users)
        messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso")
        register_window.destroy()

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) / 2
    y = (screen_height - height) / 2
    window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

def login():
    user_type_var_register_personal = tk.StringVar(value='personal')
    user_type_personal = user_type_var_register_personal.get()
    nome = name_login_entry.get().strip()
    password = password_login_entry.get().strip()
    users = load_users()

    if not nome or not password:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
        return

    if user_type_personal in users and nome in users['personal'] and users['personal'][nome]['Senha'] == password:
        if user_type_personal == "personal":
            messagebox.showinfo("Sucesso", f"Bem-vindo, {users['personal'][nome]['Nome']}!")
            open_personal_main_app(nome)
        else:
            messagebox.showerror("Erro", "Tipo de usuário inválido.")
    else:
        messagebox.showerror("Erro", "Usuario ou senha inválidos.")
    root.withdraw()

root = tk.Tk()
root.title("Sistema de Gestão de Treinos")
root.geometry("1080x800")
center_window(root, 1080, 800)

tk.Label(root, text="Sistema de Gestão de Treinos", font=('Arial', 14)).pack(pady=20)

tk.Label(root, text="Nome", font=('Arial', 10)).pack(pady=10)
name_login_entry = tk.Entry(root, font=('Arial', 10))
name_login_entry.pack(pady=5)

tk.Label(root, text="Senha", font=('Arial', 10)).pack(pady=10)
password_login_entry = tk.Entry(root, font=('Arial', 10), show='*')
password_login_entry.pack(pady=5)

tk.Button(root, text="Login", command=login, font=('Arial', 10)).pack(pady=10)
tk.Button(root, text="Cadastrar alunos", command=register, font=('Arial', 10)).pack(pady=10)
tk.Button(root, text="Cadastrar personal", command=register_personal, font=('Arial', 10)).pack(pady=10)

root.mainloop()
