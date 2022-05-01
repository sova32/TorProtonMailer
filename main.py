import asyncio
import os
import subprocess
from selenium.webdriver.common.by import By
from tbselenium.tbdriver import TorBrowserDriver

import asyncio
import time
import sys


driver = None
torexe = None
subject = 'My Test Mail'
message = 'This is the body of the mail'


def try_to_load_page(link_to_load):
    print('Загружаю сторінку')
    try:
        driver.get(link_to_load)
    except:
        close_programm('Сторінка не знайдена. Перевірте посилання.')



def try_to_find_and_click_New_message_button():
    print('Шукаю кнопку "Новое сообщение"')
    try:
        object_to_find = driver.find_element(By.XPATH, '//button[text()="Новое сообщение"]').click()
        print('Знайшов і нажав')
    except:
        print('Не зміг знайти кнопку')
        close_programm('Программа не може далі працювати!')



def close_programm(message):
    print(message)
    print('Программа завершена.')
    sys.exit(0)



async def main():
    global driver
    global torexe
    async def cleanup():
        driver.quit()
        print(torexe.pid)
        torexe.kill()

    def init_tor():
        global driver
        global torexe

        path_to_tor = input('Введіть щлях до папки з TOR браузером та натисніть Enter (типу C:\\tor-browser_ru):')

        # if linux
        if sys.platform.startswith('linux'):
            path_to_tor_bin = path_to_tor + r'/Browser/TorBrowser/Tor/tor'
            torexe = subprocess.Popen(os.path.expandvars(path_to_tor_bin))
            driver = TorBrowserDriver(tbb_logfile_path='/dev/null', tbb_path=path_to_tor)
            print(path_to_tor_bin)

        # if windows
        elif sys.platform.startswith('win32'):
            path_to_tor_exe = path_to_tor + r'\Browser\TorBrowser\Tor\tor'
            torexe = subprocess.Popen(os.path.expandvars(path_to_tor + r'\Browser\TorBrowser\Tor\tor'))
            driver = TorBrowserDriver(tbb_logfile_path='NUL', tbb_path=path_to_tor)
            print(path_to_tor_exe)

    try:
        init_tor()

        link_to_load = 'https://mail.protonmailrmez3lotccipshtkleegetolb73fuirgj7r4o4vfu7ozyd.onion/'
        try_to_load_page(link_to_load)

        yn = input('Пройдіть авторизацію, та введіть капчу, якщо потрібно і натисніть "Y": ')
        while not (yn == 'Y' or yn == 'y'):
            yn = input('Не правильна відповідь. Введііть "Y" чи "y", або закрийте программу\nАвторизувались?: ')

        try_to_find_and_click_New_message_button()
        input('Программа завершена успішно.')
    except Exception as e:
        print(e, type(e))
    finally:
        await cleanup()
        print('Не забудьте закрити tor!')
        close_programm('')


if __name__ == "__main__":
    asyncio.run(main())