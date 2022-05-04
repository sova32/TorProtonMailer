import asyncio
import os
import subprocess
import time
import sys
from random import random

from selenium.webdriver.common.by import By
from selenium.webdriver.common.devtools.v99.indexed_db import Key
from tbselenium.tbdriver import TorBrowserDriver

from email_validator import validate_email, EmailNotValidError
from pathlib import Path


driver = None
torexe = None

targets = set({})
subject = None
text = []


def check_emails():
    global targets
    temp = targets
    targets = set({})

    print('Форматування адрес скриньок та перевірка на доступність домену...')

    f = open('checked_emails.txt', 'w')

    for target in temp:
        try:
            emailObject = validate_email(target)
            targets.add(target)
            f.write(target + '\n')
        except EmailNotValidError as errorMsg:
            # If `testEmail` is not valid print a human readable error message
            print(str(errorMsg))

    f.close()
    print('Перевірені та робочі скриньки збарежено у файл: checked_emails.txt')



def open_files():
    global targets
    global subject
    global text
    global error_message



    # targets.txt
    print('Відкриваю і обробляю targets.txt')
    try:
        file = open('targets.txt')
    except Exception as exc:
        print('Помилка! Код помилки: ', exc)
        error_message = 'Перевірте файл "targets.txt" та спробуйте ще раз.'
        close_programm(error_message)
    for line in file.readlines():
        line = line.replace(' ', '')
        line = line.replace('\n', '')
        targets.add(line)
    file.close()
    print('Однакові скриньки відфільтровано, видалені лишні символи.')

    # subject.txt
    print('Відкриваю і обробляю subject.txt')
    try:
        file = open('subject.txt')
        stn = file.readlines()
        if len(stn) > 1:
            print("Викликаю Сатану! Зачекайте хвилинку...")
            time.sleep(3)
            print("Зараз, нажаль, відсутній зв'язок з вашим абонентом. Спробуйте будь ласка пізніше.")
            time.sleep(3)
        file.seek(0)
        subject = file.readline()
        file.close()

    except Exception as exc:
        print('Помилка! Код помилки: ', exc)
        error_message = 'Перевірте файл "subject.txt" та спробуйте ще раз.'
        close_programm(error_message)



    # text.txt
    print('Відкриваю і обробляю text.txt')
    try:
        file = open('text.txt')
    except Exception as exc:
        print('Помилка! Код помилки: ', exc)
        error_message = 'Перевірте файл "text.txt" та спробуйте ще раз.'
        close_programm(error_message)
    for line in file.readlines():
        text.append(line)
    file.close()



def close_programm(message):
    print(message)
    print('Програму завершено. Натисніть "Enter" ')
    input()
    sys.exit(0)


async def main():
    global driver
    global torexe
    global error_message

    global targets
    global subject
    global text


    async def cleanup():
        driver.quit()
        print(torexe.pid)
        torexe.kill()


    print('Слава Україні!')
    print('Русский военный корабль, иди нахуй!!!')

    open_files()
    check_emails()

    # Init drivers
    if not sys.platform.startswith('linux'):
        print("Дуже шкода але ця программа працює лише на Linux. Це не вина автора.\nУсі пред'яви до Білла Гейтса та no?fucked Стіва Джобса")
        close_programm('Программа завершена.')
    else:
        DEFAULT_TOR_PATH = str(Path.home()) + '/tor-browser_en-US/'
        if os.path.exists(DEFAULT_TOR_PATH):
            path_to_tor = DEFAULT_TOR_PATH
            path_to_tor_bin = path_to_tor + r'Browser/TorBrowser/Tor/tor'
        else:
            path_to_tor = input("Введіть щлях до папки з TOR браузером та натисніть Enter (типу /home/user/tor-browser_en-US/):\n")
            path_to_tor_bin = path_to_tor + r'Browser/TorBrowser/Tor/tor'

    try:
        torexe = subprocess.Popen(os.path.expandvars(path_to_tor_bin))
        driver = TorBrowserDriver(tbb_logfile_path='/dev/null', tbb_path=path_to_tor)
    except:
        await cleanup()
        close_programm('Не вдалось ініціалізувати драйвери.')


    try:
        # +++ TASK +++

        # Завантажую сторінку Protonmail
        link_to_load = 'https://mail.protonmailrmez3lotccipshtkleegetolb73fuirgj7r4o4vfu7ozyd.onion/'
        print('Завантажую сторінку Proton Mail...')
        try:
            driver.get(link_to_load)
        except:
            await cleanup()
            close_programm('Сторінка не знайдена. Перевірте посилання.')
        input('Пройдіть авторизацію, якщо потрібно введіть капчу і натисніть Enter: ')
        time.sleep(1)


        for target in targets:
            # +++ Основний цикл відправки +++

            # Find "New Mail" key
            print('Шукаю кнопку "Новое сообщение".')
            try:
                el = driver.find_element(By.XPATH, '//button[text()="Новое сообщение"]')
                el.click()
                print('Знайшов і нажав')
                print('Чекаєм секунду...')
                time.sleep(1)
            except:
                await cleanup()
                close_programm('Не спроможнє знайти кнопку "Новое сообщение".')

            # Find "To" field
            try:
                print('Шукаю поле "Кому".')
                el = driver.find_element(By.XPATH, "//input[contains(@id,'to-composer-')]")
                el.click()
                for i in target:
                    el.send_keys(i)
                    time.sleep(round(random(), 3) / 5 + 0.002)
                print('Ввів email адресата.')
                print('Чекаю секунду...')
                time.sleep(1)
            except:
                await cleanup()
                close_programm('Не спроможнє знайти поле "Кому".')


            # Find "Тема" field
            try:
                print('Шукаю поле "Тема".')
                el = driver.find_element(By.XPATH, "//input[contains(@id,'subject-composer')]")
                for j in subject:
                    el.send_keys(j)
                    time.sleep(round(random(), 3) / 5 + 0.002)
                print('Ввів тему листа.')
                print('Чекаю секунду...')
                time.sleep(1)
            except:
                await cleanup()
                close_programm('Не спроможнє знайти поле "Тема".')


            # Find Letter field
            try:
                print('Шукаю поле листа.')
                # Store iframe web element
                iframe = driver.find_element(By.XPATH, '//iframe')
                # # switch to selected iframe
                driver.switch_to.frame(iframe)
                el = driver.find_element(By.ID, 'rooster-editor')
                # el = driver.find_element(By.XPATH, '//div[contains(@id,"proton-editor-container")]')
                # el = driver.find_element(By.XPATH, '//div[@id="proton-editor-container"]')
                el.click()
                el.clear()
                for i in text:
                    for k in i:
                        el.send_keys(k)
                    # time.sleep(round(random(), 3) / 10 + 0.002)
                print('Ввів тему листа.')
                print('Чекаю секунду...')
                time.sleep(1)
                # Повернення із iframe:
                driver.switch_to.default_content()
            except:
                print('pizda 666')
                await cleanup()
                close_programm('Не спроможнє знайти поле "Лист".')



            # Find "Дополнительные параметры" key Работает
            # try:
            #     time.sleep(1)
            #     el = driver.find_element(By.XPATH, "//button[contains(@title, 'Дополнительные параметры')]")
            #     el.click()
            # except:
            #     await cleanup()
            #     close_programm('Не спроможнє знайти кнопку "Дополнительные параметры".')


            # Find Запросить уведомление о прочтении key !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # try:
            #     time.sleep(1)
            #     el = driver.find_element(By.XPATH, "//div[contains(@id, 'dropdown-']")
            #     # el = driver.find_element(By.XPATH, "/button[contains(., 'Запросить уведомление о прочтении')]")
            #     # driver.find_element(By.XPATH, "//button[contains(@class, 'ant-btn-primary') and contains(., 'OK')]").click()
            #     el.click()
            # except:
            #     input(' Ожидание для отладки...')
            #     await cleanup()
            #     close_programm('Не спроможнє знайти кнопку "Запросить уведомление о прочтении".')


            # Click "Send"
            try:
                print('Шукаю і натискаю кнопку "Отправить"')
                driver.find_element(By.XPATH, "//span[text()='Отправить']").click()
                print('Чекаємо 5 секунд перед відправкою нового листа...')
                time.sleep(5)
            except:
                await cleanup()
                close_programm('Не спроможнє знайти і натиснтути "Відправити".')


            # --- Основний цикл відправки ---


        error_message = 'Завдання виконано!\nСлава нації! Смерть рашиській педерації!'


        # --- TASK ---



    except Exception as e:
        print(e, type(e))
    finally:
        await cleanup()
        close_programm(error_message)


if __name__ == "__main__":
    asyncio.run(main())