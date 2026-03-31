import pyautogui
from pynput import keyboard
import subprocess, time

class ScriptManager:
    is_script_paused = False
    logs_on = False
    is_mouse_sensi_medium = True
    
    def pause_keyboard_listener():
        is_script_paused = ScriptManager.is_script_paused 
        ScriptManager.is_script_paused  = False if is_script_paused else True
        log(f'Teclado pausado: {is_script_paused}')
        
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
    
    #criar aq metodo referente à configuração? ex: ativar/desativasr funções, log e/ou função q muda sensi do touch
    
    #controla disparos de armas
    def hold_alt():
         if not Actions.alt_holding:
                
                #primeiro clica dps segura, pois unico clique nao atira
                pyautogui.click(button='left')
                pyautogui.mouseDown(button='left')  
                log('click + segurar btn esquerdo')
                Actions.alt_holding = True
                
    def release_alt():
        if Actions.alt_holding:
            
            pyautogui.mouseUp(button='left')
            log('soltando btn esquerdo')
            Actions.alt_holding = False
            
    def switch_aim():
        #verifica se é control, e alterna btn direito do mouse
        if Actions.is_aimming:
                pyautogui.mouseUp(button='right')
                log('soltando btn direito')
                Actions.is_aimming = False
                
        else:
            pyautogui.mouseDown(button='right')
            log('segurando btn direito')
            Actions.is_aimming = True


def log(msg, type='Log'):
    
    if ScriptManager.logs_on:
        compl = None
        if type == 'status':
            compl = 'Status: '
            

        elif type == 'Log':
            compl = 'Log: '
        print(f'* {compl}{msg}')

    else:
        return

def on_press(key):
  
    if key == keyboard.Key.delete:
       ScriptManager.pause_keyboard_listener()
       
    if key == keyboard.Key.f3:
        return False
    
    if not ScriptManager.is_script_paused:
        if key in (keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
            Actions.switch_aim()

        elif key in (keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r):
           Actions.hold_alt()


def on_release(key):
    if not ScriptManager.is_script_paused:
        if key in (keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r):
            Actions.release_alt()

ScriptManager.change_mouse_sensi()
time.sleep(3)
ScriptManager.change_mouse_sensi()

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    log('Running', 'status')
    listener.join()
