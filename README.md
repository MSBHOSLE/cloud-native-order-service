# ⚡ Cloud-Native Order Service

[![CI Pipeline](https://github.com/MSBHOSLE/cloud-native-order-service/actions/workflows/ci.yml/badge.svg)](https://github.com/MSBHOSLE/cloud-native-order-service/actions)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A resilient, cloud-native **Order Processing Microservice** engineered with domain state machine lifecycle invariants, guaranteed **HTTP idempotency controls**, and comprehensive automated test coverage.

---

## 🏗️ Order Lifecycle State Machine

```mermaid
stateDiagram-v2
    [*] --> PENDING: Order Placed
    PENDING --> VALIDATED: Inventory & Payment Approved
    PENDING --> CANCELLED: Cancelled by User / Out of Stock
    VALIDATED --> PROCESSING: Dispatched to Fulfillment
    VALIDATED --> CANCELLED: Cancelled
    PROCESSING --> COMPLETED: Delivered & Settled
    PROCESSING --> CANCELLED: Return / Reversal
    COMPLETED --> [*]
    CANCELLED --> [*]
```

---

## ⚡ Core Engineering Highlights

1. **Guaranteed Idempotency Key Processing**:
   - Accepts client-supplied `Idempotency-Key` headers on order creation.
   - Prevents duplicate order placements and double-charging during network retries or transient connection timeouts.

2. **Domain-Driven Invariant Enforcement**:
   - Mathematical precision on unit totals, tax rates, and aggregate calculations.
   - Enforces strict unidirectional state machine transitions; attempts to perform invalid jumps (e.g. `PENDING` -> `COMPLETED`) raise 409 Conflict.

3. **Cloud-Native & Kubernetes Ready**:
   - Built-in `/health/live` and `/health/ready` probe endpoints for container orchestration.
   - Clean separation of domain, service, and transport layers.

---

## 📡 API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/orders` | Create new order (supports `Idempotency-Key` header) |
| `GET` | `/api/v1/orders/{order_id}` | Retrieve order details & state |
| `PATCH` | `/api/v1/orders/{order_id}/status` | Transition order status |
| `POST` | `/api/v1/orders/{order_id}/cancel` | Cancel order |
| `GET` | `/api/v1/orders` | List customer orders |
| `GET` | `/health/live` | Kubernetes Liveness probe |
| `GET` | `/health/ready` | Kubernetes Readiness probe |

---

## 🚀 Quickstart

```bash
git clone https://github.com/MSBHOSLE/cloud-native-order-service.git
cd cloud-native-order-service

# Start with Docker Compose
docker compose up -d --build
```

---

## 🧪 Testing

```bash
python -m unittest discover tests
```

---

## 👤 Author

**Mahesh Sanjayrao Bhosle**
- **GitHub:** [@MSBHOSLE](https://github.com/MSBHOSLE)
- **LinkedIn:** [Mahesh Bhosle](https://linkedin.com/in/mahesh-bhosle-916991198)
- **Email:** msbhosle.2@gmail.com
- **Education:** M.Sc. Data & Computer Science, Heidelberg University

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
