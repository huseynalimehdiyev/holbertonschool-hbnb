# HBnB – High-Level Architecture Diagram

## 📌 Overview
This document presents a high-level package diagram of the HBnB application. The diagram illustrates a **three-layer architecture** and demonstrates how these layers communicate using the **Facade design pattern**.

The goal is to provide a clear and structured view of how the system is organized and how its components interact.

---

## 🏗️ Architecture Overview
The HBnB application follows a **layered architecture** composed of three main layers:

1. **Presentation Layer**
2. **Business Logic Layer**
3. **Persistence Layer**

Each layer has a specific responsibility and communicates with others in a controlled and organized manner.

---

## 📊 Package Diagram

```mermaid
classDiagram

class PresentationLayer {
    <<Layer>>
    +API Endpoints
    +Services
}

class Facade {
    <<Facade>>
    +createUser()
    +getPlaces()
    +addReview()
    +addAmenity()
}

class BusinessLogicLayer {
    <<Layer>>
    +User
    +Place
    +Review
    +Amenity
}

class PersistenceLayer {
    <<Layer>>
    +UserRepository
    +PlaceRepository
    +ReviewRepository
    +AmenityRepository
}

PresentationLayer --> Facade : Uses
Facade --> BusinessLogicLayer : Handles business logic
BusinessLogicLayer --> PersistenceLayer : Database operations
