# derenmind
This is an AI-based note-taking application that I completed during my internship.

## Overview
This project is part of my internship, and it includes multiple components such as Python scripts, templates, static files, and dependencies managed through `Node.js`. 
This project's main purpose is that it creates a personalized AI-based note-taking application for the user. Using the user's profile data and his/her notes, a list of suggestions and a summary of notes are kept...


## Installation

To run this project, you will need to have the following installed on your system:
- [Python](https://www.python.org/downloads/)
- [Node.js and npm](https://nodejs.org/) (for managing frontend dependencies)
- [Django](https://www.djangoproject.com/)

1. Clone the repository:
    ```bash
    git clone https://github.com/derenece/derenmind.git
    ```
2. Navigate to the project directory:
    ```bash
    cd derenmind
    ```
3. Install the Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Install the Node.js dependencies (if applicable for any frontend build tools):
    ```bash
    npm install
    ```


## Running the App
To run the application locally, follow these steps:

1. Start the Django development server:
    ```bash
    python manage.py runserver
    ```
2. Open your web browser and navigate to `http://127.0.0.1:8000/` to access derenmind app.


## Project Structure
Here’s a quick overview of the folder structure:
/derenmind         
│
├── __pycache__/ 
├── derenmind/
      ├── _init_.py/
      ├── asgi.py/
      ├── settings.py/
      ├──urls.py/
      ├── wsgi.py/
├── node_modules/
├── note/                 # Main app directory for handling notes
│   ├── migrations/
|   ├── _init_.py/
│   ├── admin.py 
│   ├── apps.py 
│   ├── forms.py 
│   ├── models.py 
│   ├── services.py 
│   ├── signals.py 
│   ├── serizlizers.py 
│   ├── tasks.py 
│   ├── views.py          
│   ├── tests.py          
│   ├── urls.py          
│
├── static/               
│   ├── javascript.js              
│
├── templates/            # Global templates directory for rendering HTML pages
│   └── about.html
│   └── base.html 
│   └── frontpage.html 
│   └── login.html 
│   └── note_detail.html 
│   └── notes.html 
│   └── signup.html 
│
├── db.sqlite3            # SQLite database file (ignored in Git, used for local development)
├── manage.py             # Django’s main management script (used for running server, migrations, etc.)
├── package.json          # Defines the Node.js dependencies (if frontend uses npm)
├── package-lock.json     # Locks the versions of Node.js dependencies
├── maip_builder.py       # Script for handling various app components (explain its specific role)
├── maip_client.py        # Script for managing client-side interactions (explain its specific role)
├── maip_context.py       # Script for handling application context (explain its specific role)
├── maip_resolver.py      # Script for resolving note-related logic (explain its specific role)
└── README.md  

## Features
- **Create Notes**: Users can create notes with a title and content.
- **Edit Notes**: In-place editing functionality, allowing users to update notes without reloading the page.
- **Delete Notes**: Users can delete notes they no longer need.
- **User Authentication**: The app includes user login and registration features.
- **Sum Notes**: Provides a summary of the user's notes and displays them on the home screen
- **Suggest**: Creates 4 different types of suggestion lists for the user's notes

## License
This project is licensed under the [MIT License](LICENSE).



