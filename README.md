# DRF Stripe API

A Django REST Framework-based backend for managing user registration, JWT authentication, and **recurring Stripe subscriptions**.
---

##  Getting Started
Follow these steps to set up the project locally:

### 1. 🔁 Clone the Repository and Open repository folder
```bash
cd drf-stripe-api
```

### 2.  Set Up Virtual Environment
**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```
**On Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. 🔧 Configure Stripe Settings
Add your Stripe credentials to `settings.py`:
```python
STRIPE_PUBLISHABLE_KEY = '<your-stripe-publishable-key>'
STRIPE_SECRET_KEY = '<your-stripe-secret-key>'
STRIPE_PRICE_ID = '<your-stripe-price-id>'
STRIPE_ENDPOINT_SECRET = '<your-stripe-webhook-endpoint-secret>'
```

### 5. 🛠️ Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Run the Development Server
```bash
python manage.py runserver
```
