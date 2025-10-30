# Gamers Hub - Ecommerce Shopping Cart

A Django-based ecommerce platform specialized for gaming products with a responsive cart system and secure payment integration.

## Features

- 🛒 Dynamic Shopping Cart with Local Storage
- 🔐 User Authentication System
- 💳 Secure Payment Integration (PayTM)
- 📱 Responsive Design
- 👤 User Profile Management
- 🔍 Product Search & Filtering
- 📦 Order Management System

## Technologies Used

- **Backend:** Django 3.x
- **Frontend:** HTML5, CSS3, JavaScript
- **Database:** SQLite3
- **Payment Gateway:** PayTM
- **UI Framework:** Bootstrap
- **Icons:** Font Awesome
- **Storage:** Local Storage for Cart Management

## Setup Instructions

### Prerequisites

- Python 3.9+
- Git
- pip (Python package manager)

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/ARCEUSOPOP/rospl_group_no21.git
cd ecommerce
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Apply database migrations:
```bash
python manage.py migrate
```

5. Create a superuser (admin):
```bash
python manage.py createsuperuser
```

6. Start the development server:
```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser to access the application.

## Project Structure

```
ecommerce/
├── authcart/              # Authentication app
├── ecommerce/            # Main project settings
├── ecommerceapp/         # Core ecommerce functionality
├── PayTm/                # Payment gateway integration
├── media/                # User uploaded files
├── static/               # Static files (CSS, JS, images)
└── templates/            # HTML templates
```

## Key Features Explained

### Shopping Cart
- Persistent cart storage using browser's localStorage
- Real-time cart updates without page refresh
- Visual feedback on cart operations

### Authentication
- User registration with email verification
- Password reset functionality
- Profile management

### Payment Integration
- Secure payment processing through PayTM
- Order tracking system
- Payment status notifications

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## Environment Variables

Create a `.env` file in the root directory with the following variables:
```
SECRET_KEY=your_django_secret_key
DEBUG=True
PAYTM_MERCHANT_KEY=your_paytm_merchant_key
PAYTM_MERCHANT_ID=your_paytm_merchant_id
```

## Contact

- Website Admin: gamerhub@gmail.com
- Project Link: https://github.com/ARCEUSOPOP/rospl_group_no21

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Django Documentation
- Bootstrap Templates
- Font Awesome Icons
- PayTM Payment Gateway Documentation