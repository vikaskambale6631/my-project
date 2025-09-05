# MediShop — Online Medicine Ordering System (Django)

Two modules: **User** and **Admin**. Users can browse/search medicines, add to cart, checkout (COD), upload prescription for RX items, manage addresses, and view orders. Admins (staff users) can manage medicines and update order status via a lightweight dashboard (plus Django Admin).

## Tech
- Django 5 (works with Django 5.0–5.1)
- SQLite (default)
- Pillow for image uploads
- No external CSS frameworks (pure CSS included)

## Quick Start (Step-by-Step)

1. **Create virtual env & install deps**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Migrate & create superuser**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

3. **Load sample data**
   ```bash
   python manage.py loaddata store/fixtures/initial_data.json
   ```

4. **Run server**
   ```bash
   python manage.py runserver
   ```

5. **Login as Admin**
   - Visit `/admin/` for Django Admin (full CRUD).
   - Visit `/dashboard/` for the custom lightweight dashboard.

## Default URLs (User Module)
- `/` — Home (search + latest medicines)
- `/products/` — All medicines; filter by `?q=`
- `/category/<slug>/` — Category view
- `/product/<slug>/` — Product detail
- `/cart/` — View cart
- `/checkout/` — Place order (COD). If cart contains RX items, upload prescription.
- `/my/orders/` — Your orders
- `/profile/` — Addresses
- `/signup/`, `/accounts/login/`, `/accounts/logout/`

## Admin Module
- `/dashboard/` — KPIs
- `/dashboard/medicines/` — Manage medicines (create/update/delete)
- `/dashboard/orders/` — Manage orders (update order status)
- **Plus:** Django Admin at `/admin/`

## Project Structure
```text
medishop/
├─ manage.py
├─ medishop/
│  ├─ settings.py
│  ├─ urls.py
│  ├─ asgi.py
│  └─ wsgi.py
├─ store/
│  ├─ admin.py, apps.py, models.py, forms.py, urls.py, views.py
│  ├─ templates/store/*.html
│  ├─ static/css/styles.css, static/js/app.js
│  └─ fixtures/initial_data.json
├─ static/  # global static (optional)
└─ media/   # uploaded files at runtime
```

## Notes
- **Images:** product images are optional; upload via admin or dashboard.
- **Payments:** simulated as **COD**. Integrate Razorpay/Stripe later if needed.
- **Security:** This is a learning starter. Before production, add permissions hardening, CSRF, rate limiting, proper email verification, etc.

---

## How to Expand
- Add coupon/discounts
- Add wishlists and product reviews
- Add delivery slots, invoice PDFs, and payment gateways
- API (Django REST Framework) + React frontend