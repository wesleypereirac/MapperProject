import pyautogui
from pynput import keyboard

is_aimming = False
alt_holding = False
is_script_paused = False
logs_on = False

def log(msg, type='Log'):
    global logs_on
    
    if logs_on:
        compl = None
        if type == 'status':
            compl = 'Status: '
            

        elif type == 'Log':
            compl = 'Log: '
        print(f'* {compl}{msg}')

    else:
        return

def on_press(key):
    global is_aimming, alt_holding, is_script_paused

    if key == keyboard.Key.delete:
        is_script_paused = False if is_script_paused else True
        log(f'Teclado pausado: {is_script_paused}')

    if not is_script_paused:
        #verifica se é control
        if key in (keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
            if is_aimming:
                pyautogui.mouseUp(button='right')
                log('soltando btn direito')
                is_aimming = False
                
            else:
                pyautogui.mouseDown(button='right')
                log('segurando btn direito')
                is_aimming = True

        #controla disparos de armas
        elif key in (keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r):
            if not alt_holding:
                
                #primeiro clica dps segura, pois unico clique nao atira
                pyautogui.click(button='left')
                pyautogui.mouseDown(button='left')  
                log('click + segurar btn esquerdo')
                alt_holding = True

#falta add a condição de is_script_paused
def on_release(key):
    global alt_holding

    if key in (keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r):
        if alt_holding:
            
            pyautogui.mouseUp(button='left')
            log('soltando btn esquerdo')
            alt_holding = False


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    log('Running', 'status')
    listener.join()
