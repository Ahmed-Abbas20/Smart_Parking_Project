# 🚗 Smart Parking (SPOTIT) – Mobile Application

**SPOTIT** is a mobile application designed to simplify the parking experience through a smart system that allows users to view available parking slots, reserve in real time, and navigate easily. It also integrates a machine learning model (using Keras) to predict parking demand and improve user experience.

## 📱 Features

- **Live Parking Availability Updates**
- **Secure Slot Reservation System**
- **Navigation to Reserved Slots**
- **Clean and Intuitive UI/UX**
- **Booking Reminders and Notifications**
- **Machine Learning-based Predictions using Keras**
- **Backend APIs powered by FastAPI**

## 🛠️ Tech Stack

### 📲 Frontend
- **Flutter** (Dart): Cross-platform mobile application
- **Adobe XD**: UI/UX design and prototyping

### ⚙️ Backend
- **FastAPI** (Python): High-performance API framework
- **SQLAlchemy + PyMySQL**: ORM and MySQL connector
- **MySQL**: Relational database
- **Keras**: Lightweight neural networks library for prediction and classification tasks

### 🧪 Tools & Support
- **Postman**: API development and testing
- **Visual Studio Code**: Development IDE
- **XAMPP**: Local server environment
- **Software Ideas Modeler**: UML diagrams and system modeling

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- Flutter SDK
- MySQL Server (local or remote)
- Git

### Clone the Project

```bash
git clone https://github.com/Ahmed-Abbas20/Smart_Parking_Project.git
cd Smart_Parking_Project
```

### Setup Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Setup Frontend (Flutter)

```bash
cd ../frontend
flutter pub get
flutter run
```

### Machine Learning Setup

- Install Keras:
```bash
pip install keras
```

- ML model training & prediction logic is located in:
```
backend/ml/keras_model.py
```

## 🧠 UML Diagrams

Designed with **Software Ideas Modeler** and include:
- Use Case Diagram
- Class Diagram
- Sequence Diagram

## 🤝 Contributors

- [Ahmed Abbas](https://github.com/Ahmed-Abbas20)
- [Ahmed Nasser Mohamed](https://github.com/AHMED-NASSER-Mohmaed)

## 📄 Licenses

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

> 📢 For suggestions, improvements, or bug reports — please open an issue or pull request on GitHub.
