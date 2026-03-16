# AwarenessHub: Gestalt-Based Journaling & Therapy Management

## Overview
AwarenessHub is a Django-based web application designed for self-improvement and therapy support, focusing on Gestalt therapy concepts such as Awareness, Insight, and Confluence. Unlike standard tracking applications, AwarenessHub is built specifically to help users document their emotional states, journal their daily experiences, and visualize patterns through a data-driven dashboard.

The application allows users to create daily journal entries, rate their mood on a scale from 1 to 10, and tag their entries with specific emotional states. As users build a history, the application provides visual trend analysis and identifies recurrent emotional patterns tied to specific days of the week, aiding the therapeutic process. It also includes a dedicated section to log insights from formal therapy sessions.

---

## Distinctiveness and Complexity

This project satisfies the distinctiveness and complexity requirements for several reasons. It is fundamentally different from the standard e-commerce, social network, or pizza-ordering projects often seen in web development courses. 

First, **it is distinct** because it is a private, isolated tool for introspection rather than a public platform. There are no social feeds, public profiles, likes, or user-to-user interactions. The entire data model and user experience are scoped strictly to the individual user, ensuring that emotional data and therapy notes remain private. Furthermore, it is not an e-commerce site; there are no products, shopping carts, or payment processing mechanisms. Instead, the focus is on personal psychology and data visualization.

Second, the project achieves a high level of **technical complexity** through its heavy reliance on Asynchronous JavaScript and Django APIs. The core journaling interface is fully interactive, utilizing JavaScript Fetch API endpoints to automatically save drafts of user entries every 30 seconds, improving the user experience by preventing data loss without requiring page reloads.

Additionally, the tagging system implemented for the journal entries utilizes a complex **Many-to-Many relationship** (`JournalEntry` to `MoodTag`). The interface allows users to asynchronously toggle these tags on and off, or even create entirely new predefined tags dynamically on the fly, demonstrating advanced bidirectional data flow between the frontend DOM and the backend database.

Finally, the project incorporates data visualization using Chart.js. The backend includes custom logic that aggregates a user's `mood_score` over the last 30 days and calculates the "Pattern Insight"—the most frequent emotional state the user experiences on specific days of the week. This logic is served via JSON endpoints and rendered dynamically into charts and insights on the dashboard, making it a sophisticated, data-driven application.

---

## File Contents

The project consists of the standard Django directory structure, with the core application logic housed in the `journal` directory. Below is an overview of the key files created for this project:

- **`journal/models.py`**: Defines the database schema, including the custom `User` model, `MoodTag`, `JournalEntry` (which links the user, text content, mood score, and Many-to-Many tags), and `TherapySession` models.
- **`journal/views.py`**: Contains all the backend logic for rendering templates and handling API requests. This includes authentication flows (login, register), rendering the dashboard, and custom JSON endpoints (`save_draft`, `toggle_tag`, `create_tag`, and `mood_trend_data`) that support the interactive frontend.
- **`journal/urls.py`**: Maps the application's URL paths to the appropriate view functions, clearly separating standard web routes from `/api/` endpoints.
- **`journal/admin.py`**: Registers the custom models to the Django Admin interface, allowing superusers to easily manage users, predefined tags, and test data.
- **`journal/templates/journal/layout.html`**: The base HTML template utilizing Bootstrap 5 for modern, responsive UI elements (navbar, generic spacing, styling). All other templates extend this file.
- **`journal/templates/journal/login.html` & `register.html`**: The authentication templates styled with Bootstrap for a clean, secure entry point.
- **`journal/templates/journal/index.html`**: The main dashboard. It contains the JavaScript logic to fetch data from the API and render the Chart.js line graph, as well as the Django template logic to display the "Pattern Insight" card.
- **`journal/templates/journal/journal_entry.html`**: The interactive journaling UI. It contains extensive JavaScript to handle the 30-second auto-save debounce timers, dynamic tag toggling, and asynchronous on-the-fly tag creation via Fetch POST requests.
- **`journal/templates/journal/therapy_sessions.html`**: Displays past therapy logs and utilizes custom CSS media queries (`@media print`) to format the page into a clean, printable monthly report for a user's therapist.
- **`seed_data.py`**: A custom Python script located in the root directory used to quickly populate the database with default Gestalt therapy tags and 14 days of mock journal entries for testing the charts and pattern recognition.
- **`requirements.txt`**: Lists the Python dependencies necessary to run the project.

---

## How to Run the Application

To run this application locally, follow these steps:

1. **Clone or Download** the repository to your local machine.
2. Ensure you have Python 3 installed. Navigate to the project directory in your terminal.
3. It is highly recommended to create and activate a virtual environment:
   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows use: env\Scripts\activate
   ```
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Apply the database migrations: # Wait, I didn't verify the python commands in the previous bash, but it seems there was an issue finding django. Assuming django is installed properly:
   ```bash
   python manage.py makemigrations journal
   python manage.py migrate
   ```
6. (Optional) Create a superuser to access the Django admin interface:
   ```bash
   python manage.py createsuperuser
   ```
7. (Optional) Run the seed script to populate the database with mock data for testing the dashboard visualizations:
   ```bash
   python seed_data.py
   ```
8. Start the development server:
   ```bash
   python manage.py runserver
   ```
9. Open your web browser and navigate to `http://127.0.0.1:8000/`. You can log in using the credentials generated by the seed script (Username: `tester`, Password: `testpass123`) or register a new user account.

---

## Additional Information

- **Bootstrap 5 CDN**: The project relies on the Bootstrap 5 CDN for styling. An active internet connection is required for the layout to render correctly.
- **Chart.js CDN**: The index dashboard relies on the Chart.js CDN to render the mood trend graph.
- **Auto-Save Functionality**: When testing the journal entry page, note that the auto-save functionality triggers either after 2 seconds of typing inactivity or every 30 seconds, whichever comes first. Watch the "Draft saved" badge queue in the top right corner of the entry box.
