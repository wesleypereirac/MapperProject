import pygetwindow as gw
from pynput import keyboard
import subprocess, time, pyautogui

class ScriptManager:
    is_script_paused = False
    logs_mode = {'on':True, 'mode':'important'}
    is_mouse_sensi_medium = True
    
    def pause_keyboard_listener():
        is_script_paused = ScriptManager.is_script_paused 
        ScriptManager.is_script_paused  = False if is_script_paused else True
        ScriptManager.log(f'Teclado pausado: {is_script_paused}')
        
    def log(msg, type='Log'):
        
        if ScriptManager.logs_mode['on']:
            compl = None
            if type == 'status' and not ScriptManager.logs_mode['mode'] == 'important':
                compl = 'Msg:'
                

            elif type == 'Log' and ScriptManager.logs_mode['mode'] == 'important':
                compl = 'Log:'
            print(f'* {compl} {msg}')

        else:
            return
        
    def manage_config(mode='start'):
        if mode == 'start':
            subprocess.run(['start', 'ms-settings:'], shell=True)
            ScriptManager.is_cfg_running = True
        
        else:
            subprocess.call(["taskkill", "/IM", "SystemSettings.exe", "/F"])
            ScriptManager.is_cfg_running = False
        
    def change_mouse_sensi():
        ScriptManager.manage_config('start')
        
        time.sleep(2)
        
        #alterar sensi
        pyautogui.click(583,27)
        
        ##search app
        word = 'touch'
        for i in word:
            pyautogui.press(i)
        
        time.sleep(0.5)
        pyautogui.press('Enter', presses=3)
        
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
                ScriptManager.log('click + segurar btn esquerdo')
                Actions.alt_holding = True
                
    def release_alt():
        if Actions.alt_holding:
            
            pyautogui.mouseUp(button='left')
            ScriptManager.log('soltando btn esquerdo')
            Actions.alt_holding = False
            
    def switch_aim():
        #verifica se é control, e alterna btn direito do mouse
        if Actions.is_aimming:
                pyautogui.mouseUp(button='right')
                ScriptManager.log('soltando btn direito')
                Actions.is_aimming = False
                
        else:
            pyautogui.mouseDown(button='right')
            ScriptManager.log('segurando btn direito')
            Actions.is_aimming = True
            
    def switch_window(to_last_win=False, title='24PILOT'):
        if not to_last_win:
            last_win = None
            current_win = gw.getActiveWindow()
            windows = gw.getAllTitles()
            
            for titulo in windows:
                if title in titulo:
                    Actions.last_window = current_win.title
                    
                    janela = gw.getWindowsWithTitle(title)[0]
                    janela.activate()
                    break
            ScriptManager.log('Alternando janela', 'Log')
            
        else:
           Actions.switch_back()
                        # janela = gw.getWindowsWithTitle(Actions.last_window)[0]
                        # janela.restore()
                        # janela.activate()
                        # ScriptManager.log(f'Alternando pra janela anterior\nnome: {Actions.last_window}', 'Log')
    
    def switch_back():
        try:
            windows = gw.getWindowsWithTitle(Actions.last_window)
            janela = windows[0]

            if not janela:
                ScriptManager.log('Nenhuma janela salva', 'Erro')
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

            ScriptManager.log('Alternando pra janela anterior', 'Log')

        except Exception as e:
            ScriptManager.log(f'Erro real ao trocar janela: {e}', 'Erro')                     
            


def on_press(key):
  
    if key == keyboard.Key.delete:
       ScriptManager.pause_keyboard_listener()
       
    #finalizar
    if key == keyboard.Key.f3:
        ScriptManager.change_mouse_sensi()
        ScriptManager.log('Finalizada execução, pressionar tecla', 'log')
        return False
    
    if not ScriptManager.is_script_paused:
        if key == keyboard.Key.enter:
            if ScriptManager.response_to_enter_key[0]:
                #chama função no indice 1
                #passa parametro p/ a função identificar oq fazer? (alternar dnv)
                pass
            
            
        elif key in (keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
            Actions.switch_aim()

        elif key in (keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r):
           Actions.hold_alt()
        
        #abrir notas
        elif key == keyboard.Key.f2:
            # -função alternar janela
            #     -pegar a active window, armazenar (p/ voltar!)
            #     -alternar p/ 24pilot
            #     -cliques e "esperar" o enter
            # -clicar na aba notas
            # -clicar no campo de entrada
            
            pass
            

def on_release(key):
    if not ScriptManager.is_script_paused:
        if key in (keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r):
            Actions.release_alt()

#trocar config
Actions.switch_window()
time.sleep(2)
Actions.switch_window(True)


##DESCOMENTAR ISSO: ScriptManager.change_mouse_sensi()

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    ScriptManager.log('Running', 'log')
    ScriptManager.log('delete: pausar\nf3: finalizar', 'log')
    listener.join()
