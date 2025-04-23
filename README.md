# Hospital Management System

[![Hospital Management System YouTube Video](https://img.youtube.com/vi/UxrR2jmaVbA/0.jpg)](https://youtu.be/UxrR2jmaVbA)

This is a RESTful API server for a Hospital Management System, built using Python and the Flask framework. The system is designed to manage hospital admissions and monitor blood bank resources efficiently. It supports multiple clients interacting with a central server using standard HTTP methods.

---

## Features

The server provides two primary services:

1. [Hospital Admission System](#admission-system-api)
2. [Hospital Blood Bank System](#blood-bank-api)

---

## Admission System API

### 1. `POST /beds-num`

- **Description**: Set the total number of beds in the hospital.
- **Input**: `int` – Number of beds.
- **Output**: `bool` – `true` if initialized successfully.
- **Note**: Runs only once when the server starts.

### 2. `POST /new-patient`

- **Description**: Admit a new patient.
- **Input**: `string` – Patient name.
- **Output**: `bool` – `true` if a bed is available and admission is successful; `false` otherwise.

### 3. `GET /empty-beds`

- **Description**: Get the number of available (empty) beds.
- **Output**: `int` – Count of empty beds.

### 4. `DELETE /discharge`

- **Description**: Discharge a patient.
- **Input**: `string` – Patient name.
- **Output**: `bool` – `true` if patient was discharged successfully; `false` if patient was not found.

---

## Blood Bank API

### 1. `POST /blood-bank`

- **Description**: Initialize the quantity of each blood type.
- **Input**: `string` (Blood Type: A, B, AB, O), `int` (Quantity).
- **Output**: `bool` – `true` if initialized successfully.
- **Note**: Can only be called once per blood type when the server starts.

### 2. `PUT /blood-bank`

- **Description**: Update the quantity of a blood type.
- **Input**: `string` (Blood Type), `int` (Amount – can be positive or negative).
- **Output**: `bool` – `true` if updated successfully.

### 3. `POST /new-patient`

- **Description**: Admit a patient who needs blood.
- **Input**:
  - `string` – Patient name
  - `string` – Blood type
  - `int` – Daily required amount
  - `int` – Number of hospitalization days
- **Logic**:
  - If the blood bank can cover the full blood requirements, patient is admitted.
  - If only one day's worth blood is available, patient is admitted but server enters **Critical Mode**.
  - Otherwise, admission fails.
- **Output**: `bool` – `true` if admitted; `false` otherwise.

### 4. `GET /critical-mode`

- **Description**: Check if the blood bank is in **Critical Mode**.
- **Output**: `bool` – `true` if in critical mode, else `false`.

---

## Technologies Used

- Python
- Flask
- REST API design
- HTTP Protocol

---

## Installation

```bash
git clone https://github.com/negarK2000/Hospital-Management-System.git
cd Hospital-Management-System
pip install -r requirements.txt
python admission.py
python bloodbank.py
```

---

## API Testing

Use tools like [Postman](https://www.postman.com/) or `curl` to interact with the endpoints.
