import PySimpleGUI as sg
import json
import os
import PySimpleGUI as sg
import pandas as pd
import json

# Nome do arquivo onde os dados serão salvos
json_file = 'dados_salvos.json'
class AgendaApp:
    def __init__(self):
        self.filename = "agenda.json"
        self.tasks = self.load_tasks()
        self.setup_agenda()

    def setup_agenda(self):
        layout = [
            [sg.Text("Data", font=("Arial", 12)), sg.Input(key='-DATE-', size=(12, 1), font=("Arial", 12), disabled=True), sg.CalendarButton("Selecionar Data", target='-DATE-', format="%d/%m/%Y", font=("Arial", 12))],
            [sg.Text("Tarefa", font=("Arial", 12)), sg.Input(key='-TASK-', font=("Arial", 12), size=(40, 1))],
            [sg.Text("Horário", font=("Arial", 12)), sg.Input(key='-TIME-', font=("Arial", 12), size=(10, 1))],
            [sg.Button("Adicionar", font=("Arial", 12)), sg.Button("Remover Tarefa", font=("Arial", 12))],
            [sg.Listbox(values=self.tasks, key='-TASKLIST-', font=("Arial", 12), size=(60, 10), select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)]
        ]

        self.window = sg.Window("Agenda", layout)

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return json.load(file)
        return []

    def save_tasks(self):
        with open(self.filename, 'w') as file:
            json.dump(self.window['-TASKLIST-'].get_list_values(), file)

    def add_task(self, date, task, time):
        if date and task and time:
            formatted_task = f"{date} - {task} - {time}"
            current_tasks = self.window['-TASKLIST-'].get_list_values()
            updated_tasks = current_tasks + [formatted_task]
            self.window['-TASKLIST-'].update(updated_tasks)
            self.save_tasks()

    def remove_task(self):
        selected_task = self.window['-TASKLIST-'].get_indexes()
        if selected_task:
            current_tasks = self.window['-TASKLIST-'].get_list_values()
            del current_tasks[selected_task[0]]
            self.window['-TASKLIST-'].update(current_tasks)
            self.save_tasks()

    def run(self):
        while True:
            event, values = self.window.read()

            if event == sg.WIN_CLOSED:
                break
            elif event == "Adicionar":
                self.add_task(values['-DATE-'], values['-TASK-'], values['-TIME-'])
            elif event == "Remover Tarefa":
                self.remove_task()

        self.window.close()


# Dados iniciais para a planilha (DataFrame)
data = {
    "1": [""] * 35,
    "2": [""] * 35,
    "3": [""] * 35,
    "4": [""] * 35,
    "5": [""] * 35,
    "6": [""] * 35,
    "7": [""] * 35,
    "8": [""] * 35,
    "9": [""] * 35,
    "10": [""] * 35,
    "11": [""] * 35,
    "12": [""] * 35,
}
# Tenta carregar os dados salvos de um arquivo JSON
try:
    with open(json_file, 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    pass  # Se o arquivo não existir, usa os dados iniciais

df = pd.DataFrame(data)

# Layout para exibir e editar cada célula da planilha
layout = []
for i in range(len(df)):
    row = []
    for col in df.columns:
        # Adiciona campos de entrada para cada célula
        row.append(sg.InputText(default_text=df[col][i], key=(i, col), size=(20, 1)))
    layout.append(row)

layout.append([sg.Button('Salvar'), sg.Button('Carregar'), sg.Button('Limpar'), sg.Button('Sair')])
usu = ''

# Função para obter o valor do saldo para o usuário atual
def saldo_valor():
    global usu
    if not os.path.exists('valores.json'):
        return 'Saldo não disponível'
    
    with open('valores.json', 'r') as valor_json:
        dados = json.load(valor_json)
        return dados.get(usu, 'Saldo não disponível')

# Função para obter dados das pessoas
def dados_pessoas():
    if not os.path.exists('dados.json'):
        return {}
    
    with open('dados.json', 'r') as valor_json:
        dados = json.load(valor_json)
        return dados

def academia():
    if not os.path.exists('arquivos.json'):
        return 'Nome da Academia não registrado'
    
    with open('arquivos.json', 'r') as valor_json:
        dados = json.load(valor_json)
        return dados.get('nome', 'Nome da Academia não registrado')

# Layout para o cadastro de pessoas
def cadastro_pessoas():
    return [
    [sg.Text(academia(), font=('Arial', 14, 'bold'))],
    [sg.Text('Nome:'), sg.Input(key='nome', size=(40, 1))],
    [sg.Text('Tel:'), sg.Input(key='tel', size=(20, 1))],
    [sg.Text('OBS:'), sg.Input(key='obs', size=(50, 1))],
    [sg.Text('CAMINHADA MIN:'), sg.Radio('5', 'CAMINHADA', key='caminhada_5'), sg.Radio('10', 'CAMINHADA', key='caminhada_10'), sg.Radio('15', 'CAMINHADA', key='caminhada_15'), sg.Radio('20', 'CAMINHADA', key='caminhada_20')],
    [sg.Text('BICICLETA MIN:'), sg.Radio('5', 'BICICLETA', key='bicicleta_5'), sg.Radio('10', 'BICICLETA', key='bicicleta_10'), sg.Radio('15', 'BICICLETA', key='bicicleta_15'), sg.Radio('20', 'BICICLETA', key='bicicleta_20')],
    [sg.Text('EXERCÍCIOS')],
    [sg.Frame(layout=[
        [sg.Checkbox('AGACHAMENTO', key='agachamento'), sg.Checkbox('AFUNDO', key='afundo')],
        [sg.Checkbox('LEG PRESS', key='leg_press'), sg.Checkbox('EXTENSORA', key='extensora')],
        [sg.Checkbox('FLEXORA', key='flexora'), sg.Checkbox('CADEIRA ABDUTORA', key='cadeira_abdutora')],
        [sg.Checkbox('PANTURRILHA', key='panturrilha')],
    ], title='COXAS E GLÚTEOS')],
    [sg.Frame(layout=[
        [sg.Checkbox('ROSCA DIRETA', key='rosca_direta'), sg.Checkbox('ROSCA SCOTT', key='rosca_scott')],
        [sg.Checkbox('MARTELA', key='martelo'), sg.Checkbox('ROSCA CONCENTRADA', key='rosca_concentrada')],
    ], title='BÍCEPS')],
    [sg.Frame(layout=[
        [sg.Checkbox('DESENVOLVIMENTO', key='desenvolvimento'), sg.Checkbox('ELEVAÇÃO LATERAL', key='elevacao_lateral')],
        [sg.Checkbox('ELEVAÇÃO FRONTAL', key='elevacao_frontal'), sg.Checkbox('ENCOLHIMENTO', key='encolhimento')],
    ], title='OMBROS')],
    [sg.Frame(layout=[
        [sg.Checkbox('ROSCA INVERTIDA', key='rosca_invertida'), sg.Checkbox('TRÍCEPS PULLEY', key='triceps_pulley')],
        [sg.Checkbox('TRÍCEPS TESTA', key='triceps_testa'), sg.Checkbox('MESA FLEXORA', key='mesa_flexora')],
    ], title='ANTEBRAÇO')],
    [sg.Text('IMC', font=('Arial', 12, 'bold'))],
    [sg.Text('Altura', size=(20, 1)), sg.Input(key='altura', enable_events=True), sg.Text('', size=(20, 1), key='imc')],
    [sg.Text('Peso', size=(20, 1)), sg.Input(key='peso', enable_events=True)],
    [sg.Button('Enviar'), sg.Button('Cancelar')]
]

# Layout para visualizar fichas
def layout_view_1():
     return [
    [sg.Listbox(values=[], size=(50, 20), key='lista_fichas')],
    [sg.Button('Visualizar'), sg.Button('Fechar')]
]

sg.theme('DarkBlue')

# Função para exibir detalhes da ficha
def mostrar_ficha(ficha):
    return [
        [sg.Text(academia(), font=('Arial', 14, 'bold'))],
        [sg.Text(f"Nome: {ficha.get('nome', 'N/A')}")],
        [sg.Text(f"Tel: {ficha.get('tel', 'N/A')}")],
        [sg.Text(f"OBS: {ficha.get('obs', 'N/A')}")],
        [sg.Text(f'IMC: {ficha.get("IMC","N/A")}')],
        [sg.Text(f"CAMINHADA MIN: {ficha.get('caminhada', 'N/A')}")],
        [sg.Text(f"BICICLETA MIN: {ficha.get('bicicleta', 'N/A')}")],
        [sg.Text('COXAS E GLÚTEOS', font=('Arial', 12, 'bold'))],
        [sg.Text('\n'.join([ex for ex in ficha.get('exercicios', []) if ex in ('agachamento', 'afundo', 'leg_press', 'extensora', 'flexora', 'cadeira_abdutora', 'panturrilha')]))],
        [sg.Text('BÍCEPS', font=('Arial', 12, 'bold'))],
        [sg.Text('\n'.join([ex for ex in ficha.get('exercicios', []) if ex in ('rosca_direta', 'rosca_scott', 'martelo', 'rosca_concentrada')]))],
        [sg.Text('OMBROS', font=('Arial', 12, 'bold'))],
        [sg.Text('\n'.join([ex for ex in ficha.get('exercicios', []) if ex in ('desenvolvimento', 'elevacao_lateral', 'elevacao_frontal', 'encolhimento')]))],
        [sg.Text('ANTEBRAÇO', font=('Arial', 12, 'bold'))],
        [sg.Text('\n'.join([ex for ex in ficha.get('exercicios', []) if ex in ('rosca_invertida', 'triceps_pulley', 'triceps_testa', 'mesa_flexora')]))],
        [sg.Button('Fechar')]
    ]

# Função para carregar fichas do arquivo JSON
def carregar_fichas():
    if os.path.exists('fichas.json'):
        with open('fichas.json', 'r') as file:
            return json.load(file)
    return []

# Função para salvar fichas no arquivo JSON
def salvar_fichas(fichas):
    with open('fichas.json', 'w') as file:
        json.dump(fichas, file, indent=4)

def nome_academia():
    return [
        [sg.Text('Nome da academia')],
        [sg.Input(key='nome')],
        [sg.Button('Adicionar'), sg.Button('Cancelar')]
    ]

try:
    with open(json_file, 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    pass  # Se o arquivo não existir, usa os dados iniciais

df = pd.DataFrame(data)

# Layout para exibir e editar cada célula da planilha
def criar_layout_planilha():
    layout = []
    for i in range(len(df)):
        row = []
        for col in df.columns:
            # Adiciona campos de entrada para cada célula usando iloc
            row.append(sg.InputText(default_text=df[col].iloc[i], key=(i, col), size=(20, 1)))
        layout.append(row)
    layout.append([sg.Button('Salvar'), sg.Button('Carregar'), sg.Button('Limpar'), sg.Button('Sair')])
    return layout

def criar_layout_planilha():
    layout = []
    for i in range(len(df)):
        row = []
        for col in df.columns:
            # Adiciona campos de entrada para cada célula usando iloc
            row.append(sg.InputText(default_text=df[col].iloc[i], key=(i, col), size=(20, 1)))
        layout.append(row)
    layout.append([sg.Button('Salvar'), sg.Button('Carregar'), sg.Button('Limpar'), sg.Button('Sair')])
    return layout

# Função para exibir a janela da planilha
def exibir_planilha():
    layout = criar_layout_planilha()
    window = sg.Window('Planilha Interativa e Editável', layout)

    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED or event == 'Sair':
            break
        
        if event == 'Salvar':
            # Coletar os dados editados
            for i in range(len(df)):
                for col in df.columns:
                    # Verifica se a chave (i, col) existe em 'values' antes de tentar acessá-la
                    if (i, col) in values:
                        df.at[i, col] = values[(i, col)]
            
            # Salvar os dados editados em um arquivo JSON
            with open(json_file, 'w') as f:
                json.dump(df.to_dict(), f)
            sg.popup('Dados salvos com sucesso!')
        
        if event == 'Carregar':
            # Carregar os dados salvos do arquivo JSON
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                for i in range(len(df)):
                    for col in df.columns:
                        if (i, col) in window.AllKeysDict:  # Verifica se a chave existe
                            window[(i, col)].update(data[col][str(i)])
                sg.popup('Dados carregados com sucesso!')
            except FileNotFoundError:
                sg.popup('Nenhum arquivo salvo encontrado!')

        if event == 'Limpar':
            # Limpar os campos de entrada
            for i in range(len(df)):
                for col in df.columns:
                    if (i, col) in window.AllKeysDict:  # Verifica se a chave existe
                        window[(i, col)].update("")
            sg.popup('Dados limpos!')

    window.close()

# Função principal para iniciar o programa
def iniciar_programa():
    sg.theme('DarkBlue')
    janela = sg.Window('Nome da Academia', tela_inicial(), size=(480, 300))

    while True:
        eventos, valores = janela.read()

        if eventos == sg.WIN_CLOSED:
            break
        if eventos == '-excel-':
            janela.hide()
            exibir_planilha()
            janela.un_hide()

    janela.close()

def tela_inicial():
    return [
        [sg.Button('?')],
        [sg.Text('                             '), sg.Text(saldo_valor())],  # Placeholder para mais ícones e funções
        [sg.Text('Pesquisa'), sg.Input(key='-pesquisa-')],
        [sg.Text('')],
        [sg.Button('Agenda', key='-agenda-'), sg.Button('Cadastro de Pessoas', key='-cadastro-')],
        [sg.Button('Banco', key='-banco-'), sg.Button('Planilha', key='-excel-')],
        [sg.Button('email alunos ', key='-email-'), sg.Button('Visualizar Fichas')]
    ]

# Inicializa a janela principal
janela = sg.Window(academia(), tela_inicial(), size=(480, 300))

while True:
    eventos, valores = janela.read()

    if eventos == sg.WIN_CLOSED:
        break
    if eventos == '?':
        janela.close()
        janela = sg.Window('Adicionar nome a academia', nome_academia())
        while True:
            evento, valor = janela.read()
            if evento == sg.WIN_CLOSED or evento == 'Cancelar':
                janela.close()
                janela = sg.Window(academia(), tela_inicial(), size=(480, 300))
                break
            if evento == 'Adicionar':
                if not valor['nome']:
                    sg.popup('Por favor, preencha todos os campos.')
                else:
                    with open('arquivos.json', 'w') as arquivo_json:
                        json.dump({'nome': valor['nome']}, arquivo_json, indent=4)
                    sg.popup('Nome da academia registrado com sucesso.')
                    janela.close()
                    janela = sg.Window(academia(), tela_inicial(), size=(480, 300))
                    break
    if eventos == '-agenda-':
      
            app = AgendaApp()
            app.run()
        
   
    if eventos =='-excel-':
        
         iniciar_programa()



    if eventos == '-cadastro-':
        janela.hide()
        janela_cadastro = sg.Window('Cadastro de Pessoas', cadastro_pessoas())
        while True:
            evento_cadastro, valores_cadastro = janela_cadastro.read()
            if evento_cadastro == sg.WIN_CLOSED or evento_cadastro == 'Cancelar':
                break
            
            # Cálculo do IMC
            if evento_cadastro == 'altura' or evento_cadastro == 'peso':
                try:
                    altura = float(valores_cadastro['altura']) / 100  # Convertendo para metros
                    peso = float(valores_cadastro['peso'])
                    imc = peso / (altura ** 2)
                    janela_cadastro['imc'].update(f'IMC: {imc:.2f}')
                except:
                    janela_cadastro['imc'].update('IMC: N/A')
            
            if evento_cadastro == 'Enviar':
              if not  valores_cadastro['nome'] and not valores_cadastro['tel']:
                  sg.popup('Por favor, preencha todos os campos.')
              else:
                try :
                    ficha = {
                        'nome': valores_cadastro['nome'],
                        'tel': valores_cadastro['tel'],
                        'obs': valores_cadastro['obs'],
                        'caminhada': [int(k.split('_')[1]) for k in valores_cadastro if 'caminhada_' in k and valores_cadastro[k]][0],
                        'bicicleta': [int(k.split('_')[1]) for k in valores_cadastro if 'bicicleta_' in k and valores_cadastro[k]][0],
                        'exercicios': [key for key, value in valores_cadastro.items() if value is True and key not in ('Enviar', 'Cancelar', 'altura', 'peso', 'imc')],
                        'IMC': janela_cadastro['imc'].get().split(':')[1].strip()
                    }
                    
                    fichas = carregar_fichas()
                    fichas.append(ficha)
                    salvar_fichas(fichas)
                    sg.popup('Ficha cadastrada com sucesso!', title='Sucesso')
                    break
                except:
                    sg.popup('Erro ao cadastrar ficha!', title='Erro')

        janela_cadastro.close()
        janela.un_hide()

    if eventos == 'Visualizar Fichas':
        fichas = carregar_fichas()
        fichas_nomes = [ficha['nome'] for ficha in fichas]
        janela.hide()
        janela_view = sg.Window('Visualizar Fichas', layout_view_1(), finalize=True)
        janela_view['lista_fichas'].update(values=fichas_nomes)

        while True:
            evento_view, valores_view = janela_view.read()
            if evento_view == sg.WIN_CLOSED or evento_view == 'Fechar':
                break

            if evento_view == 'Visualizar':
                ficha_selecionada = valores_view['lista_fichas'][0]
                ficha_detalhes = next((ficha for ficha in fichas if ficha['nome'] == ficha_selecionada), None)

                if ficha_detalhes:
                    janela_view.hide()
                    janela_detalhes = sg.Window('Ficha Detalhada', mostrar_ficha(ficha_detalhes))
                    janela_detalhes.read()
                    janela_detalhes.close()
                    janela_view.un_hide()

        janela_view.close()
        janela.un_hide()

janela.close()
