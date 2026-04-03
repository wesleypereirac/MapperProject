import pygetwindow as gw
from pynput import keyboard
import subprocess, time, pyautogui

class ScriptManager:
    is_script_paused = True
    #mode: important ou understand_flow
    logs_mode = {'on':True, 'mode':'important'}
    is_mouse_sensi_medium = True
    is_running_as_test = False
    
    def pause_keyboard_listener():
        is_script_paused = ScriptManager.is_script_paused 
        ScriptManager.is_script_paused  = False if is_script_paused else True
        
        ScriptManager.manage_log(f'Teclado pausado: {ScriptManager.is_script_paused}')
        
    #se for passar msg q precisa de qubra de linha, passar cada frase numa lista
    def manage_log(msg, msg_type='understand_flow'):
        
        if ScriptManager.logs_mode['on']:
            compl = None
            will_log = False
            if msg_type == 'understand_flow' and ScriptManager.logs_mode['mode'] == 'understand_flow':
                compl = 'flow:'
                will_log = True

            elif msg_type == 'important' and ScriptManager.logs_mode['mode'] == 'important':
                compl = 'Log:'
                will_log = True

            if will_log:            
                ScriptManager.log(compl, msg) 
        return
        
    def log(*args):
        msg = args[1]
        
        if type(msg) == list:
                for i in msg:
                    print(f'* {i}')
        else:
            print(f'*{msg}')
                
    def manage_config(mode='start'):
        if mode == 'start':
            subprocess.run(['start', 'ms-settings:'], shell=True)
            ScriptManager.is_cfg_running = True
        
        else:
            subprocess.call(["taskkill", "/IM", "SystemSettings.exe", "/F"])
            ScriptManager.is_cfg_running = False
        
    def change_mouse_sensi():
        
        #para nao executar sem necessidade
        if not ScriptManager.is_running_as_test:
            ScriptManager.manage_config('start')
            
            time.sleep(2)
            
            ##pesquisar opção
            pyautogui.click(583,27) 
            
            word = 'touch'
            for i in word:
                pyautogui.press(i)
            
            time.sleep(1.5)
            pyautogui.press('Enter')
            
            ##alterar sensi
            time.sleep(1)
            pyautogui.click(805,401)
            
            time.sleep(1)
            
            pyautogui.click(1194,461)
            
            time.sleep(1)
            
            if ScriptManager.is_mouse_sensi_medium == True:
                pyautogui.press('up',presses=3)
            else:
                pyautogui.press('down',presses=2)
                
            time.sleep(1)
            pyautogui.press('enter')
            
            
            ###para orientar sobre o estado
            bool = False if ScriptManager.is_mouse_sensi_medium == True else True
            
            ScriptManager.is_mouse_sensi_medium = bool
            
            #fechar a config para nao dar erro de coordenada
            ScriptManager.manage_config('kill')
            
        else:
            ScriptManager.manage_log('rodando como teste:Não irá abrir a cfg.')
            

class Actions:
    is_aimming = False
    alt_holding = False
    last_window = None
    response_to_enter_key = [False, 'function']
    #criar aq metodo referente à configuração? ex: ativar/desativasr funções, log e/ou função q muda sensi do touch
    
    #controla disparos de armas
    def hold_alt():
         if not Actions.alt_holding:
                
                #primeiro clica dps segura, pois unico clique nao atira
                pyautogui.click(button='left')
                pyautogui.mouseDown(button='left')  
                ScriptManager.manage_log('click + segurar btn esquerdo')
                Actions.alt_holding = True
                
    def release_alt():
        if Actions.alt_holding:
            
            pyautogui.mouseUp(button='left')
            ScriptManager.manage_log('soltando btn esquerdo')
            Actions.alt_holding = False
            
    def switch_aim():
        #verifica se é control, e alterna btn direito do mouse
        if Actions.is_aimming:
                pyautogui.mouseUp(button='right')
                ScriptManager.manage_log('soltando btn direito')
                Actions.is_aimming = False
                
        else:
            pyautogui.mouseDown(button='right')
            ScriptManager.manage_log('segurando btn direito')
            Actions.is_aimming = True
            
    def switch_window(title='24PILOT'):
        to_last_win = Actions.response_to_enter_key[0]
        
        if not to_last_win:
            current_win = gw.getActiveWindow()
            windows = gw.getAllTitles()
            
            for titulo in windows:
                if title in titulo:
                    Actions.last_window = current_win.title
                    
                    janela = gw.getWindowsWithTitle(title)[0]
                    janela.activate()
                    break
            ScriptManager.manage_log('Alternando janela')
            
        else:
            Actions.switch_back()
                        # janela = gw.getWindowsWithTitle(Actions.last_window)[0]
                        # janela.restore()
                        # janela.activate()
            ScriptManager.manage_log(
                ['Alternando pra janela anterior.', f'Nome: {Actions.last_window}']
                )
    
    def switch_back():
        try:
            windows = gw.getWindowsWithTitle(Actions.last_window)
            janela = windows[0]

            if not janela:
                ScriptManager.manage_log('Nenhuma janela salva', 'Erro')
                return

            # força estado válido
            if janela.isMinimized:
                janela.restore()
                time.sleep(0.2)

            # hack clássico do Windows
            try:
                janela.activate()
            except:
                janela.minimize()
                time.sleep(0.2)
                janela.restore()
                time.sleep(0.2)
                janela.activate()

            ScriptManager.manage_log('Alternando pra janela anterior', 'Log')

        except Exception as e:
            ScriptManager.manage_log(f'Erro real ao trocar janela: {e}', 'Erro')                     
            


def on_press(key):
  
    if key == keyboard.Key.delete:
       ScriptManager.pause_keyboard_listener()
       
    #finalizar
    if key == keyboard.Key.f3:
        ScriptManager.change_mouse_sensi()
        ScriptManager.manage_log('Finalizada execução, pressionar tecla', 'log')
        return False
    
    if not ScriptManager.is_script_paused:
        if key == keyboard.Key.enter:
            if Actions.response_to_enter_key[0]:
                #chama função no indice 1
                #passa parametro p/ a função identificar oq fazer? (alternar dnv)
                Actions.response_to_enter_key[1]()
                ScriptManager.manage_log('terminou de anotar', 'log')
                
            
            
        elif key in (keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
            Actions.switch_aim()

        elif key in (keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r):
           Actions.hold_alt()
        
        #abrir notas
        elif key == keyboard.Key.f2:
            # -clicar na aba notas
            # -clicar no campo de entrada
            Actions.response_to_enter_key = [True]
            Actions.switch_window()
            
            #aba notas
            pyautogui.click(736,202)
            
            #entrar no campo
            pyautogui.click(714,435)
            

def on_release(key):
    if not ScriptManager.is_script_paused:
        if key in (keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r):
            Actions.release_alt()

#trocar config


ScriptManager.change_mouse_sensi()

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    ScriptManager.manage_log('Running\n', 'important')
    ScriptManager.manage_log(['delete: pausar.','f3: finalizar', 'f2: abrir 24pilot', 'ctrl: btn direito', 'alt: btn direito\n'], 'important')
    listener.join()
