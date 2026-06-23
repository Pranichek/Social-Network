

## Instaling Python
 Якщо ви ніколи не встановлювали Python, це для вас:
 1.  Завантажте інсталятор Python
 2. Перейдіть на офіційний [Python website](https://www.python.org)
 3. Перейдіть до розділу "Завантаження/Downloads".Сайт автоматично визназнає вашу операційну систему, тому покаже правильну версію.
- рекомендується встановити останню версію, але якщо вона не працює, встановіть попередну або іншу версію.
4. Запустіть інсталятор
    - Натисніть кнопку Завантажити Python.
    - Поставте галочку на кнопку 'Додати python до PATH' у нижній частині вікна інсталятора.Це потрібно щоб швидко запускати Python з командного рядка.

    - Щоб налаштувати інсталяцію, натисніть кнопку 'налаштувати інсталяцію', так ви зможете вибрати якісь додаткові параметри.Їх можна не добавляти томущо звичайна інсталяції працює добре.
5. Встановлення
    - Натисніть 'Встановити зараз/Install Now' та дочекайтися поки воно встановлюється.
6. Перевірка
    - Після встановлення відкрийте командний рядок або термінал
        <details>
        <summary> Operating system</summary>
        - On Windows: Press Win + R, type cmd, and press Enter.
        - On macOS/Linux: Open the Terminal application.
        </details>
    - Напишіть ```python --version``` або ```python3 --version``` та натисніть Enter
    - Якщо python встановився у PATH то вам покаже поточну версію Python
    <h6>Якщо у вас вже був встановлений Python в PATH,тоді не рекомендується встановлювати новий Python у PATH

Можете подивиться як встановити Python та як встановити Visual Studio Code [тут](https://www.youtube.com/watch?v=uge4A1LHsNk)

## Instaling this Project

1. Клонування проєкту с github
    - Перейдіть на сторінку проєкту на github
    - Настисніть на зелену кнопку 'Code'
    - Виберіть там параметр HTTPS та скопіюйте url адресу проєкту
2. Відкрийте Visual Studio Code
    - Підготуйте нову пусту Папку(на робочому столі, тощо)
    - Виберіть опцію 'Відкрити папку' та відкрийте папку яку ви створили, 
    - Натисніть кнопки Control + J або натисніть кнопку Terminal щоб створити новий термінал
    - в термінал напишіть це:
        ```python
            git clone https://github.com/Pranichek/ShipsBattle.git
        ```
3. Підготовка проєкту 
    - Щоб перейти в папку проєкта, напишіть в термінал це:
        ```python  
            cd Social-Network
        ```
4. Створення Віртуального оточення(venv)
    <h6> Для Windows</h6>
        Для створення віртуального оточення у Python на Windows потрібно скористатися модулем venv.

    - Створення Віртуального Оточення: відрийте термінал та напишіть команду: python -m venv ім'я_оточення (приклад: python -m venv venv)

    - Активуйте віртуальне оточення: напишіть команду ім'я_оточення/Scripts/activate (приклад: venv/Scripts/activate)

    <h6> Для Mac OS </h6>
        Для створення віртуального оточення у Python на Mac OS потрібно скористатися модулем venv.

    - Створення Віртуального Оточення: відрийте термінал та напишіть команду: python3 -m venv ім'я_оточення (приклад: python3 -m venv venv)

    - Активуйте віртуальне оточення: напишіть команду ім'я_оточення/bin/activate (приклад: venv/bin/activate)
5. Встановлення модулів Проєкту
 - Коли віртуальне середовище стане активним,інсталюйте бібліотеки, написавши в термінал:

    ```python 
        pip install -r requirements.txt 
    ```
6. Запуск Сервера
 - В Терміналі напишіть цю команду:
    ```
        cd Social_network
    ```
 - Після цього в терміналі напишіть цю команду:
    ```
    python manage.py runserver
    ```
    
<details>
<summary>English version</summary>

If you've never installed Python before, this is for you:
 1. Download the Python installer
 2. Go to the official [Python website](https://www.python.org)
 3. Go to the “Downloads” section. The site automatically detects your operating system, so it will show you the correct version.
- It’s recommended to install the latest version, but if it doesn’t work, install the previous version or another version.
4. Run the installer
    - Click the “Download Python” button.
    - Check the “Add Python to PATH” box at the bottom of the installer window. This is necessary to quickly run Python from the command line.
    - To customize the installation, click the ‘Customize Installation’ button; this will allow you to select additional options. You don’t need to add them because the default installation works fine.
5. Installation
    - Click ‘Install Now’ and wait for it to install.
6. Verification
    - After installation, open a command prompt or terminal
        <details>
        <summary> Operating system</summary>
        - On Windows: Press Win + R, type cmd, and press Enter.
        - On macOS/Linux: Open the Terminal application.
        </details>
    - Type ```python --version``` or ```python3 --version``` and press Enter
    - If Python is installed in your PATH, it will display the current Python version
    <h6>If you already have Python installed in your PATH, it is not recommended to install a new version of Python in the PATH
You can find out how to install Python and how to install Visual Studio Code [here](https://www.youtube.com/watch?v=uge4A1LHsNk)
## Installing This Project
1. Clone the project from GitHub
    - Go to the project page on GitHub
    - Click the green “Code” button
    - Select the HTTPS option and copy the project's URL
2. Open Visual Studio Code
    - Create a new empty folder (on your desktop, etc.)
    - Select the ‘Open Folder’ option and open the folder you created, 
    - Press Control + J or click the Terminal button to open a new terminal
    - In the terminal, type the following:
        ```python
            git clone https://github.com/Pranichek/ShipsBattle.git
        ```
3. Setting up the project 
    - To navigate to the project folder, type the following in the terminal:
        ```python  
            cd Social-Network
        ```
4. Creating a Virtual Environment (venv)
    <h6> For Windows</h6>
        To create a virtual environment in Python on Windows, you need to use the venv module.
    - Creating a Virtual Environment: Open the terminal and enter the command: python -m venv environment_name (example: python -m venv venv)
    - Activate the virtual environment: Enter the command environment_name/Scripts/activate (example: venv/Scripts/activate)
    <h6>For Mac OS </h6>
        To create a virtual environment in Python on Mac OS, you need to use the venv module.
    - Creating a Virtual Environment: Open a terminal and enter the command: python3 -m venv environment_name (example: python3 -m venv venv)
    - Activate the virtual environment: enter the command environment_name/bin/activate (example: venv/bin/activate)
5. Installing Project Modules
 - Once the virtual environment is active, install the libraries by typing the following in the terminal:
    ```python 
        pip install -r requirements.txt 
    ```
6. Starting the Server
 - In the Terminal, enter this command:
    ```
        cd Social_network
    ```
 - Then, in the Terminal, enter this command:
    ```
    python manage.py runserver
    ```
</details>





