# 🎟️ mTicket - Smart Ticket Booking System

![mTicket](https://mticket.pythonanywhere.com/static/images/logo.png =200x200)

mTicket is a **smart ticket booking system** designed for seamless **event management and booking**. It allows event managers to create events, sell tickets, and provides users with an easy and secure way to book tickets online.  

🔗 **Live Website:** [mTicket](https://your-mticket-website.com)  

---

## ✨ Features

- 🎫 **Event Creation & Management** (For Managers)
- 🌂 **Dynamic Ticket Pricing & Stock Updates**
- 🛒 **Secure Razorpay Payment Integration**
- 🗓️ **Real-Time Booking System**
- 📊 **Event Dashboard with Insights**
- 🔒 **Authentication & Role-Based Access**
- 📍 **Location-Based Event Discovery**

---

## 🚀 Tech Stack

| Technology  | Description |
|-------------|------------|
| **Django**  | Backend Framework |
| **HTML/CSS/JS** | Frontend Development |
| **Bootstrap/Tailwind** | UI Styling |
| **Razorpay API** | Payment Gateway |
| **Pythonanywhere.com** | Hosting & Deployment |
| **SQLite** | Database |

---

## 🛠️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/mTicket.git
cd mTicket
```

### 2️⃣ Create a Virtual Environment & Activate It
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables
Create a `.env` file and configure your **database, secret key, and API keys**.
```env
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
RAZORPAY_API_KEY=your-razorpay-key
```

### 5️⃣ Run Migrations
```bash
python manage.py migrate
```

### 6️⃣ Create a Superuser (For Admin Access)
```bash
python manage.py createsuperuser
```

### 7️⃣ Run the Development Server
```bash
python manage.py runserver
```
Visit **`http://127.0.0.1:8000/`** in your browser!

---

## 📸 Screenshots  

| Home Page | Event Booking | Payment Gateway |
|-----------|--------------|-----------------|
| ![Home](https://via.placeholder.com/300x200?text=Home) | ![Booking](https://via.placeholder.com/300x200?text=Booking) | ![Payment](https://via.placeholder.com/300x200?text=Payment) |

---

## 🛠️ Contribution Guidelines  

Want to contribute? Awesome! Follow these steps:

1. **Fork** the repository 🍴
2. **Clone** your fork 🔾  
   ```bash
   git clone https://github.com/your-username/mTicket.git
   cd mTicket
   ```
3. **Create a new branch** 🔀  
   ```bash
   git checkout -b feature-branch
   ```
4. **Make your changes & commit** 🛠️  
   ```bash
   git add .
   git commit -m "Added new feature"
   ```
5. **Push and create a Pull Request** 🚀  
   ```bash
   git push origin feature-branch
   ```
6. Wait for your PR to be reviewed and merged! ✅  

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 📢 Contact & Support

For queries, reach out to:

📧 Email: [akhildevreddy207@gmail.com](mailto:akhildevreddy207@gmail.com)  
💼 LinkedIn: [Akhildev Reddy](www.linkedin.com/in/akhildevreddy)  

---

🚀 **mTicket - Your Smart Ticket Booking Solution!** 🎟️  

