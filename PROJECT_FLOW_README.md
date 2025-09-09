# 🎟️ mTicket - Smart Ticket Booking System

mTicket is a **Django-based smart ticket booking system** designed for seamless **event management and booking**.  
This README explains the **flow of the application** so that both developers and users can understand how the project works.

---

## 🚀 Project Flow

### 1. Homepage & About
- The **About app** provides a simple introduction page (`about/`).
- It renders static content (`about.html`) with project details.

### 2. Events Module (Core of the System)
The **Events app** handles the complete event lifecycle:

#### (a) Event Creation (For Managers)
- Event Managers can log in and **create events** by providing:
  - Title, Description, Type, Location, Image
  - Start and End Dates
  - Ticket details (type, quantity, price, min/max purchase, sale start/end)
- Events are saved to the database with associated tickets.

#### (b) Event Listing & Details
- Users can browse all events (`/events/`).
- Selecting an event (`/events/event/<id>/`) shows:
  - Event details (name, description, location, image, dates)
  - Ticket options

#### (c) Ticket Selection
- On an event page, users choose tickets (`/events/select_tickets/<id>/`).
- Ticket rules enforced:
  - Min/Max per booking
  - Availability window (sale start & end dates)
  - Quantity must not exceed remaining stock

#### (d) Attendee Details & Confirmation
- Users enter attendee information for each ticket.
- Booking preview is shown before checkout.

#### (e) Payment
- Payment page (`/events/payment/<id>/`) integrates with Razorpay (or other gateways).
- Flow:
  1. Tickets are temporarily reserved.
  2. Payment is initiated.
  3. If successful → Booking is confirmed.
  4. If failed or timeout (200s) → Tickets are restored back to stock.

#### (f) Booking Management
- Users can view all their bookings at `/events/bookings/`.
- They can **cancel bookings** if allowed.
- Event Managers can also view/manage bookings.

---

## 🛠️ Tech Stack
- **Backend**: Django (Python)
- **Database**: SQLite (for dev) → Recommend PostgreSQL for production
- **Frontend**: Django templates, HTML, CSS
- **Payment**: Razorpay integration
- **Other Tools**:
  - Django Messages for alerts
  - Django ORM for database handling
  - Threading (for timeout handling)

---

## 📂 Project Structure
```
Ticket-app-main/
│── manage.py
│── db.sqlite3
│── README.md
│
├── about/                # About page app
│   ├── views.py          # About page rendering
│   ├── urls.py           # Routes
│   └── templates/about.html
│
├── events/               # Core ticket booking app
│   ├── models.py         # Event, Ticket, Booking models
│   ├── views.py          # Event & ticket logic
│   ├── urls.py           # Routes for events flow
│   ├── migrations/       # Database migrations
│   └── templates/        # Event pages (listing, detail, booking, payment)
│
└── static/               # CSS, JS, Images
```

---

## 🔑 Key Features
- Event creation with flexible ticketing
- Ticket selection with stock control
- Attendee details capture
- Payment integration with timeout handling
- Booking management & cancellation
- Event manager-specific controls

---

## 📝 How to Run the Project
1. Clone the repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run migrations:
   ```bash
   python manage.py migrate
   ```
3. Start the server:
   ```bash
   python manage.py runserver
   ```
4. Access the site at `http://127.0.0.1:8000/`

---

## 🔮 Future Improvements
- Switch SQLite → PostgreSQL
- Replace threading with Celery for background tasks
- Add seat selection (for auditorium-style events)
- Improved UI with modern frontend (React/Vue)
- Add QR code for tickets

---
