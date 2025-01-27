import psutil
import time
from tkinter import *
from tkinter import scrolledtext




def append_log(msg):
    texto_log.config(state='normal')
    texto_log.insert(END, msg + '\n')
    texto_log.see(END)
    texto_log.config(state='disabled')

def find_pid_by_name(process_name):
    """Retorna o PID do primeiro processo encontrado com o nome especificado."""
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] == process_name:
                return proc.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None


def set_affinity_one_cpu_by_name(process_name):
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

def start_affinity():
    set_affinity_one_cpu_by_name('RainbowSix_BE.exe')
    set_affinity_one_cpu_by_name('RainbowSix.exe')



janela = Tk()
janela.geometry('400x400')

Label(janela, text='OPERAÇÃO AFINIDADE R6', font='Arial 12 bold').grid(row=0, column=0, padx=20, pady=20, sticky='NEWS')

btn_afin = Button(janela, text='START', font='Arial 12 bold', bg='green', fg='white', width=37, command=start_affinity)
btn_afin.grid(row=1, column=0, sticky='NEWS', padx=10)

texto_log = scrolledtext.ScrolledText(janela, width=40,height=15, state=DISABLED)
texto_log.grid(row=2, column=0, padx=10, pady=10, sticky='NEWS')



janela.mainloop()



