import psutil
import time
from ttkbootstrap import *
from ttkbootstrap.constants import *

# Função para adicionar mensagens ao log de maneira controlada
def append_log(msg):
    """
    Adiciona uma mensagem ao log exibido na interface.
    """
    texto_log.config(state=NORMAL)  # Permite edição temporária
    texto_log.insert(END, msg + '\n')  # Insere a mensagem no final
    texto_log.see(END)  # Rola automaticamente para o final
    texto_log.config(state=DISABLED)  # Bloqueia a edição novamente

# Função para encontrar o PID de um processo pelo nome
def find_pid_by_name(process_name):
    """
    Retorna o PID do primeiro processo encontrado com o nome especificado.
    """
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] == process_name:
                return proc.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass  # Ignora erros ao acessar processos
    return None

# Função principal para gerenciar afinidade de CPU
def set_affinity_one_cpu_by_name(process_name):
    """
    Altera a afinidade do processo para usar apenas uma CPU, 
    e depois restaura a configuração original.
    """
    append_log('--- AFINIDADE INICIADA ---')
    append_log(f'Processo: {process_name}')
    try:
        # Encontra o PID pelo nome do processo
        pid = find_pid_by_name(process_name)
        if pid is None:
            append_log(f"Processo '{process_name}' não encontrado.")
            return

        append_log(f"PID encontrado: {pid}")
        
        # Trabalha com o PID encontrado
        process = psutil.Process(pid)
        all_cpus = process.cpu_affinity()  # Salva a afinidade original
        append_log(f"Afinidade original: {all_cpus}")

        # Define a afinidade para apenas um CPU (o primeiro da lista)
        process.cpu_affinity([all_cpus[0]])
        append_log(f"Afinidade definida para apenas CPU {all_cpus[0]}")

        # Simula algum tempo antes de restaurar (apenas para demonstração)
        time.sleep(2)

        # Restaura a afinidade original
        process.cpu_affinity(all_cpus)
        append_log("--- AFINIDADE CONCLUÍDA ---")
    except psutil.AccessDenied:
        append_log("Permissão negada para alterar a afinidade do processo. Execute como administrador.")
    except psutil.NoSuchProcess:
        append_log("O processo não existe.")
    except Exception as e:
        append_log(f"Ocorreu um erro: {e}")
    append_log('\n')

# Função chamada ao clicar no botão para iniciar a operação
def start_affinity():
    """
    Inicia a alteração de afinidade para processos específicos.
    """
    set_affinity_one_cpu_by_name('RainbowSix_BE.exe')
    set_affinity_one_cpu_by_name('RainbowSix.exe')

# Configuração da interface gráfica
style = Style('darkly')  # Você pode alterar o tema para outros como 'cosmo', 'flatly', 'morph', etc.
janela = style.master
janela.title("Operação Afinidade R6")
janela.geometry('400x400')

# Título
label_title = Label(janela, text='OPERAÇÃO AFINIDADE R6', font='Arial 14 bold', bootstyle=PRIMARY)
label_title.grid(row=0, column=0, sticky='NS', pady=10, padx=10)

# Botão para iniciar a afinidade
btn_afin = Button(janela, text='START', bootstyle=(SUCCESS, OUTLINE), command=start_affinity, width=59)
btn_afin.grid(row=1, column=0, sticky='NEWS', pady=10, padx=10)

# Caixa de texto para logs
texto_log = Text(janela, width=50, height=18, state=DISABLED)
texto_log.grid(row=2, column=0, sticky='NEWS', pady=10, padx=10)

# Inicia o loop principal da interface
janela.mainloop()
