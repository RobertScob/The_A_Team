# CAMPUS MARKETPLACE

> **"A Campus Marketplace is an application designed specifically for university students to buy and sell second-hand items within their campus community."**

---

## Project Overview

The Campus Marketplace is a high-performance, responsive web application built with Django. It bridges the gap between students, providing a secure, internal economy for trading textbooks, furniture, and electronics.

#### Key Features

- **Live AJAX Search:** Instant item filtering without page reloads using jQuery.
  
- **Internal Wallet System:** Users can "Top Up" a virtual balance to purchase items.
  
- **Secure Transactions:** Atomic purchase logic ensuring items are marked "Sold" and funds are transferred correctly.
  

---

## Setup & Installation

##### 1. Clone the Repository

Bash

```
git clone https://github.com/your-username/The_A_Team.git
cd The_A_Team
```

##### 2. Install Requirements

Ensure you have Python 3.11+ installed.

Bash

```
pip install -r requirements.txt
```

*(Requires mainly: Django, Pillow)*

##### 3. Initialize & Populate Database

This will create the database schema and inject the Glasgow-themed test data.

Bash

```
python manage.py migrate
python populate_market.py
```

> ⚠️ **IMPORTANT NOTE:** When the population script runs, it generates physical duplicates of images in your `media/` directory. **Do not commit these files back into the repository** to keep the repo size optimized.

##### 4. Launch Application

Bash

```
python manage.py runserver
```

Visit the app at: `http://127.0.0.1:8000/`

---

## Running Tests

Our application maintains a robust **Automated Test Suite** to ensure stability and logic accuracy.

Bash

```
python manage.py test
```

The test suite provides a stylish terminal output detailing:

- **Model Validation** (Prohibited keywords, UUID integrity)
  
- **View Access** (Login/Anonymous redirect logic)
  
- **Business Logic** (Wallet deductions, transaction logs)
  
- **AJAX Integrity** (Search component response checks)
  

---

## Technical Architecture

#### Database Structure (The "A-Team" Schema)

- **User:** Custom UUID-based model with `student_id` and `account_balance`.
  
- **Item:** Supports categorisation, price validation, and a prohibited keyword scanner.
  
- **Transaction:** Logs every `TOPUP` and `PURCHASE` for financial auditing.
  
- **ItemPhoto:** Allows for multiple high-resolution images per listing.
  

#### Application Views

| **View** | **Description** |
| --- | --- |
| **Shop (Home)** | The main grid featuring live AJAX search and category filtering. |
| **Item Detail** | Deep-dive into item specs with seller information. |
| **Dashboard** | User's personal hub showing items they are selling. |
| **Account** | Management of profile details and wallet balance. |
| **Create Listing** | A multi-part form for uploading new campus items. |

---

## Marking Scheme Compliance

| **Requirement** | **Implementation Detail** |
| --- | --- |
| **User Auth** | Custom `AbstractUser` using Email as the primary identifier. |
| **Search/Filter** | Dynamic filtering via jQuery AJAX for a "Single Page App" feel. |
| **Data Population** | `population_script.py` generates 10 users and 20+ UofG items. |
| **Testing** | 10+ detailed unit tests with formatted console output. |
| **Styling** | Custom Bootstrap 5 theme with CSS Grid and glassmorphism cards. |

---

## Authors & Contributors

The following students are the core architects of the Campus Marketplace:

- **Robert Scobie**
  
- **Ore Ajibade**
  
- **Tess Byrne**
  
- **Hayden Gilmour**
  
- **Radiance Adegboyega**
  
- **Parisan Vazirinejad**
  

---

## Frameworks & Libraries

- [Django 4.2+](https://www.djangoproject.com/) - Core Web Interface
  
- [Bootstrap 5](https://getbootstrap.com/) - CSS Styling Framework
  
- [jQuery](https://jquery.com/) - AJAX & UI Interactions
  
- [FontAwesome](https://fontawesome.com/) - Iconography
  

---

## Support the Team

If this marketplace helped you find a cheap textbook or clear out your Hillhead flat, consider buying the team a coffee!

**Donations:** [Donate via PayPal](https://www.paypal.com/paypalme/OreoluwaAjibade932)

---

*Created for the University of Glasgow by The A-Team ©2026*
