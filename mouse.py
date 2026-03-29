import pyautogui
from pynput import keyboard

class ScriptManager:
    is_script_paused = False
    logs_on = False

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
    
    if Actions.logs_on:
        compl = None
        if type == 'status':
            compl = 'Status: '
            

        elif type == 'Log':
            compl = 'Log: '
        print(f'* {compl}{msg}')

    else:
        return

def on_press(key):
    is_script_paused = ScriptManager.is_script_paused 
    
    if key == keyboard.Key.delete:
        
        is_script_paused = False if is_script_paused else True
        log(f'Teclado pausado: {is_script_paused}')

    if not is_script_paused:
        if key in (keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
            Actions.switch_aim()

        elif key in (keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r):
           Actions.hold_alt()


#falta add a condição de is_script_paused
def on_release(key):
    if not ScriptManager.is_script_paused:
        if key in (keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r):
            Actions.release_alt()


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    log('Running', 'status')
    listener.join()
