# Соціальна мережа/Social network

## Мета проекту

Цей проєкт розроблено для ознайомлення із роботою сучасного веб-додатку, принципом отримання та обробки даних від сервера, а також організацією даних у реальному проєкті.

<details>
<summary>English version</summary>
This project is designed to introduce you to the workings of a modern web application, the principle of receiving and processing data from the server, as well as the organization of data in a real project.
</details>

#

Він корисний для початківця, бо показує, як працюють ключові аспекти побудови соціальної мережі в <a href="https://docs.djangoproject.com/en/6.0/">Django</a>:
- робота з сервером Django та управління моделями, запитами й формами;
- авторизація, реєстрація та управління профілями користувачів;
- обробка даних з бази даних і логіка збереження інформації про пости, коментарі та підписки;
- застосування <a href="https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API">WebSocket</a> через <a href="https://channels.readthedocs.io/en/latest/">Django Channels</a> для реального чату та повідомлень;
- передача повідомлень та чатів у форматі <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON">JSON</a>, обробка повідомлень на клієнті та сервері;
- завантаження, збереження та відображення медіафайлів (зображення для постів і повідомлень);
- побудова інтерфейсу з шаблонами, маршрутизацією та сучасним UX.

Цей проєкт допоможе розібратися у таких темах:
- як налаштовується взаємодія клієнта і сервера у Django;
- як працюють асинхронні повідомлення та миттєве оновлення контенту в чатах;
- як структурувати дані для соціальної мережі та обробляти їх у backend;
- як реалізувати систему друзів, приватних та групових чатів;
- як зберігати медіафайли й організовувати доступ до них.

Проєкт адаптований для тих, хто хоче зрозуміти, як створюється веб-застосунок із реальними користувацькими сценаріями та як застосовувати отримані знання у власних проектах.

<details>
<summary>English version</summary>
It's useful for a beginner because it shows how the key aspects of building a social network in <a href="https://docs.djangoproject.com/en/6.0/">Django</a> work:

- working with the Django server and managing models, requests and forms;
- authorization, registration and management of user profiles;
- data processing from the database and the logic of saving information about posts, comments and subscriptions;
- use of <a href="https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API">WebSocket</a> through <a href="https://channels.readthedocs.io/en/latest/">Django Channels</a> for real chat and messages;
- transmission of messages and chats in <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON">JSON</a> format, processing of messages on the client and server;
- downloading, saving and displaying media files (images for posts and messages);
- building an interface with templates, routing and modern UX.

This project will help you understand the following topics:

- how client and server interaction is configured in Django;
- how asynchronous messages and instant content updates in chats work;
- how to structure data for the social network and process it in the backend;
- how to implement a system of friends, private and group chats;
- how to store media files and organize access to them.

The project is adapted for those who want to understand how to create a web application with real user scenarios and how to apply the knowledge gained in their own projects.
</details>

#

<b><a href='#content'>До змісту ⬆️</a></b>

##

## Information about our team

1. GitHub - <a href="https://github.com/Pranichek">Volodymyr Hrinchenko</a>
2. GitHub - <a href="https://github.com/MaksymmS">Maksym Selifanov</a>
3. GitHub - <a href="https://github.com/VolodymyrYakovets2">Volodymyr Yakovets</a>
4. GitHub - <a href="https://github.com/Valentin5944">Valentin Portyanko</a>
5. GitHub - <a href="https://github.com/Vadim-Kobzar2010">Vadim Kobzar</a>


<!-- ------------------ ВОЛОДИМИР -->

#  Українська версія / Ukrainian Version

## Зміст
* [Основний функціонал та перелік модулів](#-основний-функціонал-та-перелік-модулів)
* [Стек технологій та аналіз залежностей](#-стек-технологій-та-аналіз-залежностей)


## Основний функціонал та перелік модулів

Проєкт побудований за модульною архітектурою Django, де кожний додаток створено окремо для виконання різноманітних функцій та логіки проєкта :

* **`Social_network` (Головний модуль  нашого проєкту):** Містить кореневі налаштування проєкту `settings.py`, маршрутизацію URL-адрес `urls.py` та конфігурацію асинхронного ASGI-сервера `asgi.py` для обробки WebSocket-з'єднань
* **`chat_app` (Модуль месенджера):** Реалізує логіку обмену повідомленнями в реальному часі через WebSockets. Включає асинхронні консюмери `consumers.py`, маршрутизацію сокетів `routing.py` та відокремлений сервісний шар `services/` для кастомної пагінації чатів, груп і повідомлень
* **`user_app` (Модуль користувачів та автентифікації):** Відповідає за кастомну модель користувача, реєстрацію, AJAX-авторизацію, керування сесіями та верифікацію через email-коди. Містить власний шар сервісів (`services/`) для обробки соціальних зв'язків та генерації наших токенів.
* **`profile_app` (Модуль профілів користувачів):** Керує персональними сторінками користувачів, відображенням інформації про користувачів і тд, налаштуваннями профілю `settings.html` та списками друзів.
* **`post_app` (Модуль публікацій нашого додатку):** Відповідає за створення постів, обробку тегів та в принципі взаємодію з контентом що знаходиться у додатку
* **`home_app` (Модуль головної сторінки):** Реалізує фід-ленту з динамічним завантаженням публікацій без перезавантаження сторінки за допомогою AJAX `post_load.js`

---

## Стек технології

### Ключові технології нашого проєкту які ми використовували
* **Django:** Головний високорівневий  веб-фреймворк на Python для швидкої та безпечної розробки 
* **Django Channels & Daphne:** Асинхронне розширення для Django, що дозволяє обробляти не лише HTTP, а й довготривалі з'єднання, такі як WebSockets. Daphne виступає як ASGI-сервер
* **WebSockets:** Протокол двостороннього обміну даними в реальному часі між браузером та сервером (використовується для чатів та онлайн-статусів)

### Детальний розбір `requirements.txt`

Бібліотека / Пакет | Для чого їх використовують у проєкті?

**`Django`** : Основа проєкту. Забезпечує роботу ORM бази даних, маршрутизацію URL, обробку запитів Views та рендеринг HTML-шаблонів
**`channels`** : Інтегрує підтримку асинхронних протоколів у Django, дозволяючи створювати `Consumers` для WebSocket-з'єднань
**`daphne`** : Асинхронний ASGI-сервер, який запускає проєкт замість стандартного WSGI, щоб підтримувати HTTP та WebSockets в одночас
**`Pillow`** " Бібліотека для обробки зображень. Необхідна Django для валідації та збереження файлів у полях `ImageField` (аватари користувачів, та вся медіа яка знаходиться в постах)
**`asgiref`** : Набір інструментів для взаємодії між асинхронним (async) та синхронним (sync) кодом в Python. Використовується для виклику ORM-запитів у сокетах


# Англійська версія / English Version

## Table of Contents
* Main Functionality & Modules List(#main-functionality--modules-list)
* Technology Stack & Dependencies Breakdown(#technology-stack--dependencies-breakdown)


## Main Functionality & Modules List

The project follows a modular Django architecture, where each application is created separately to perform various functions and project logic:

* **`Social_network` (Core module of our project):** Contains root project settings `settings.py`, URL routing `urls.py`, and the asynchronous ASGI server configuration `asgi.py` to handle WebSocket connections
* **`chat_app` (Messenger module):** Implements real-time messaging logic via WebSockets. Includes async consumers `consumers.py`, socket routing `routing.py`, and a dedicated service layer `services/` for custom pagination of chats, groups, and messages
* **`user_app` (User & Authentication module):** Handles the custom user model, registration, AJAX authentication, session management, and email verification codes. Contains its own service layer (`services/`) for handling social graph queries and generating our tokens
* **`profile_app` (User Profiles module):** Manages user personal pages, user data display, etc., settings (`settings.html`), and friend lists
* **`post_app` (Our application's Publications module):** Responsible for post creation, tag processing, and overall interaction with the content located within the application
* **`home_app` (Home Page module):** Implements the news feed with dynamic post loading using AJAX (`post_load.js`) without full page reloads

---

## Technology Stack

### Core technologies of our project that we used
* **Django:** The main high-level Python Web framework used for rapid and secure development
* **Django Channels & Daphne:** An async extension for Django that enables handling long-lived connections like WebSockets, in addition to HTTP. Daphne acts as the primary ASGI server
* **WebSockets:** A protocol providing full-duplex communication channels over a single TCP connection between the browser and the server (used for chat rooms and online status tracking)

### Detailed `requirements.txt` Breakdown

Library / Package | What are they used for in the project? 

**`Django`** : The core framework. Provides the ORM database access, URL routing, Request/Response handling (Views), and HTML template rendering
**`channels`** : Integrates asynchronous protocol support into Django, enabling WebSocket `Consumers`. 
**`daphne`** : An ASGI-compatible web server that runs the project instead of standard WSGI to support both HTTP and WebSockets simultaneously
**`Pillow`** : Image processing library. Required by Django to validate and save files in `ImageField` models (user avatars and all media within posts)
**`asgiref`** : A set of tools for dual async/sync Python development. Used to safely run synchronous Django ORM queries inside async consumers


<!-- Валентин -->


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




