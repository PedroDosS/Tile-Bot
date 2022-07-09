from PIL import ImageGrab
from PIL import Image
import pyautogui
import mouse
import time
import sys

pyautogui.FAILSAFE = False

#If you want to run this for yourself, replace these coordinates with the ones that apply to your screen
game_screen = (666, 100, 1254, 1047) #coordinates for the game screen (top left to bottom right)
restart_coords = (1000, 550) #coordinates for the restart button

path_to_folder = '/home/pedro/Documents/scripts/python/Piano\ Tiles/Pictures' #Put where you want the pictures to be stored here.

screen_slice = (game_screen[2] - game_screen[0])//8
x_coords = [screen_slice * ((2 * index) + 1) for index in range(4)]

loss_count = 0
click_count = 0

run_start_time = time.time()

def click_pixel():
    global click_count

    im = ImageGrab.grab(bbox = game_screen)
    im_width, im_height = im.size
    pixels = im.load()

    for y_coord in reversed(range(im_height)):
        for x_coord in x_coords:
            if pixels[x_coord,y_coord] == (0,0,0):
                pyautogui.mouseDown(x = x_coord + game_screen[0], y = y_coord + game_screen[1] - 1, _pause = False)
                time.sleep(0.05)
                pyautogui.mouseUp()
                click_count += 1
                return
            elif pixels[x_coord,y_coord] == (253,18,1):
                save_and_display_results()
                return

def save_and_display_results(resetting = True):
    global click_count
    global run_start_time
    global click_count
    global loss_count

    im = ImageGrab.grabb()
    im.save(f'{path_to_folder}/attempt_{loss_count}_{time.time()}.png')

    start_time = time.strftime('%a, %d %b %Y %H:%M:%S', time.gmtime(run_start_time))
    end_time = time.strftime('%a, %d %b %Y %H:%M:%S', time.gmtime(time.time()))
    run_time = time.strftime('%H:%M:%S', time.gmtime(time.time() - run_start_time))

    if resetting:
        print('Lost Detected... Restarting in 10 seconds.')
    else:
        print("Shutting Down...")

    print('=========Stats=========')
    print(f'Start Time: {start_time}')
    print(f'End Time: {end_time}')
    print(f'Run time: {run_time}')
    print(f'Clicks: {click_count}')

    with open(f'Piano Tiles Stats.txt', 'a') as file:
        file.write(f'=========Stats=========\n')
        file.write(f'Start Time: {start_time}\n')
        file.write(f'End Time: {end_time}\n')
        file.write(f'Run time: {run_time}\n')
        file.write(f'Clicks: {click_count}\n')
        file.write(f'Automatic Reset: {resetting}\n\n')

    if resetting:
        run_start_time = time.time()
        click_count = 0
        loss_count += 1
        time.sleep(9)
        pyautogui.click(restart_coords)
        time.sleep(1)

while not mouse.is_pressed('right'):
    frame_start_time = time.time()
    click_pixel()
    print(f'Frame took {time.time() - frame_start_time}')

save_and_display_results(resetting = False)


#This section here is for testing. If you want to find specific pixels on the screen, comment out everything else and uncomment this
'''
#im = ImageGrab.grab(bbox = game_screen)
#im.save('test.png')
'''

'''
exit = False
mouse_is_pressed = False

while not exit:
    if not mouse_is_pressed:
        mouse.on_click(lambda: print(f'{mouse.get_position()}'))
    if mouse.is_pressed('right'):
        exit = True
    time.sleep(0.1)
    mouse_is_pressed = mouse.is_pressed
'''
