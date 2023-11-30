from pystray import MenuItem as item
from PIL import Image
from datetime import datetime
import paho.mqtt.client as mqtt
import pystray, os, pyautogui, time, ctypes

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("powerpc/#")

def on_message(client, userdata, msg):
    str_date_time = datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")
    global last_msgbox
    last_msgbox = f'{str_date_time} | {msg.topic} | {str(msg.payload)[2:-1]}'
    print(last_msgbox)

    match msg.payload:
        case b"sleep":
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        case b"playpause":
            pyautogui.press("playpause")
        case b"nexttrack":
            pyautogui.press("nexttrack")
        case b"MonitorOff":
            ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, 2)
        case b"exit_mqtt_daemon":
            icon.stop() 

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.username_pw_set('логин', 'пароль')
    client.connect("192.168.1.5", 1883, 60)
    client.loop_start()

    image = Image.open("mqtt.ico")
    menu = (item('Закрыть', lambda icon, item: icon.stop()), item('Последнее сообщение', lambda icon, item: icon.notify(last_msgbox)))
    icon = pystray.Icon("name", image, "MQTT daemon", menu)
    icon.run()


    