# DeskReserve Backend API

The backend REST API for the Desk Reserve application (Assignment 1 ESE). This service manages workspaces across multiple floors, handles secure user bookings, prevents scheduling conflicts, and dispatches automated transactional emails.

Built with **Django** and **Django REST Framework (DRF)**.

---

## Features & Architecture

* **Secure Authentication:** Utilizes **JWT (JSON Web Tokens)** via `SimpleJWT` for stateless, secure session management.
* **Data Isolation:** Enforces strict user permissions so clients can only fetch, view, and delete their own personal bookings.
* **Conflict Prevention:** Database-level and view-level validation prevents double-booking of a single resource for overlapping times, and rejects invalid time ranges (e.g., end time before start time).
* **Automated Seed Data:** Includes custom database population logic to dynamically generate office layouts (e.g., 168 distinct workspaces distributed across 4 floors).
* **Comprehensive Testing:** Secured by an `APITestCase` suite that validates public vs. private access, data isolation, and business logic.

---

## API Endpoints

| Method | Endpoint | Auth Required | Description |
| :--- | :--- | :---: | :--- |
| `GET` | `/api/workspaces/` | ❌ | Fetches all active workspaces (Desks, Focus Pods, Boardrooms). |
| `GET` | `/api/bookings/` | ✅ | Fetches all active bookings belonging to the authenticated user. |
| `POST` | `/api/bookings/create/` | ✅ | Creates a new booking and triggers a confirmation email. |
| `DELETE`| `/api/bookings/<id>/delete/` | ✅ | Cancels/deletes a booking (only if owned by the requesting user). |

---

##  Local Development Setup

Before you start, ensure you do not have a VPN restricting access to local ports.

### 1. Activate the Virtual Environment
```bash
source venv/bin/activate
```
*(On Windows, use `venv\Scripts\activate`)*

### 2. Install Dependencies
Make sure you install the required packages, including Django, DRF, SimpleJWT, and `certifi` (for SSL resolution).
```bash
pip install -r requirements.txt
```

### 3. Apply Database Migrations
Create the SQLite database and apply the schema:
```bash
python manage.py migrate
```

### 4. Create a Superuser
You will need an admin account to access the dashboard and create test users. **Note:** Ensure you attach a valid email address to your admin user to test the email functionality.
```bash
python manage.py createsuperuser
```

### 5. Add SendGrid Configuration
To test email dispatch locally, ensure your `settings.py` is configured with your SendGrid API key and verified Sender Identity email. *(Note: Never commit your actual API key to version control in a production environment).*

### 6. Run the Server
```bash
python manage.py runserver
```

### 7. Access the Admin Panel
Navigate to `http://localhost:8000/admin` in your browser to manage Users, Workspaces, and Bookings.

---

## Running Tests

The application features a robust test suite verifying permissions, authentication, and booking conflict logic. Run the tests using:

```bash
python manage.py test api
```

---

## Appendix: Third-Party Integrations

As part of the application's development, two external services were integrated to handle static asset delivery and transactional communications, ensuring a more scalable and professional architecture.

### 1. Cloudinary (Asset Hosting & CDN)
**Purpose:** To manage and deliver optimized images for the various workspace resources (Desks, Focus Pods, Boardrooms) displayed on the frontend.

**Implementation:**
* Rather than storing heavy static image files directly within the local repository or the Django database, workspace assets are hosted remotely on Cloudinary.
* The React frontend features a utility function that dynamically maps the `resource_type` of each workspace payload to its corresponding Cloudinary URL.
* **Technical Benefit:** This approach offloads bandwidth from the Django backend, leverages a global Content Delivery Network (CDN) for faster image rendering in the UI, and keeps the database lightweight.

### 2. Twilio SendGrid (Transactional Email Service)
**Purpose:** To automatically send users a professional booking confirmation receipt the moment their reservation is successfully saved to the database.

**Implementation:**
* Integrated SendGrid as the primary SMTP backend within Django's `settings.py`, authenticated via a secure API Key and a verified Single Sender Identity.
* Upgraded Django's standard `send_mail` utility to deliver a dual-format payload: a plain-text fallback (for maximum compatibility) and a responsive HTML template.
* The HTML template utilizes inline CSS to match the application's frontend design system, including brand colors (e.g., `#1976d2`) and layout structures.
* **Error Handling & Security:** Wrapped the SMTP dispatch in a `try/except` block. This ensures that if the third-party email server times out or fails, the core booking transaction still succeeds without crashing the user's frontend experience.
* **Development Challenges Overcome:** Successfully resolved local environment SSL/TLS certificate verification failures (common in macOS Python environments) by integrating the `certifi` package to securely validate the connection to SendGrid's SMTP servers.

## Appendix: Generative AI Acknowledgement (Yellow Category)

In accordance with the module's "Yellow" category classification for Generative AI usage, AI tools (specifically Google Gemini) were utilized to support planning, debugging, and the refinement of technical features during the development of this enterprise application.

**Critical Evaluation of AI Usage:**
* **Debugging & Environment Configuration:** Gemini was used to diagnose and resolve a macOS-specific SSL/TLS certificate verification failure (`[SSL: CERTIFICATE_VERIFY_FAILED]`) during the SendGrid SMTP integration. It suggested implementing the `certifi` package to securely validate the connection to SendGrid's servers.
* **Component Generation & Styling:** AI was leveraged to generate boilerplate React functional components (using Material UI) for the Registration and Password Reset flows. The generated code was then manually reviewed, tested, and integrated into the existing routing architecture to ensure it matched the application's unified design system.
* **Content Generation:** AI assisted in drafting the responsive inline-CSS HTML templates used for the transactional emails (Welcome and Booking Confirmations) sent via SendGrid.

All AI-assisted code was thoroughly tested, verified for accuracy, and fully understood before being integrated into the final deployment.