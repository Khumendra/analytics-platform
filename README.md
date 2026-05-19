# Real-Time Multi-Tenant Analytics & Reporting Platform

A production-grade, highly optimized SaaS analytics and telemetry ingestion platform built using Python (Django REST Framework) and Next.js 14. The system is designed around strict multi-tenant data isolation layers at the database layer and handles high-throughput event ingestion via asynchronous worker execution.

---

## 🔗 Deployed Application URLs

- **Frontend Dashboard UI (Vercel):** [https://analytics-platform-o2s409dbr-khumendras-projects.vercel.app/login](https://analytics-platform-o2s409dbr-khumendras-projects.vercel.app/login)
  Username: `admin` and Password: `securepassword123`
- **Backend Core REST API Server (Render):** [https://analytics-backend-api.onrender.com/api/dashboard/metrics/](https://analytics-backend-api.onrender.com)
- **Production GitHub Repository:** [https://github.com/Khumendra/analytics-platform](https://github.com/Khumendra/analytics-platform)

---

## 🏛️ Architectural Design & Multi-Tenancy Isolation

The application follows clean coding patterns separating API routes, operational services, serialization schemas, and structural database query hooks.

### Data Ingestion Framework

To avoid event loops blockage during bulk telemetry streams, the endpoint performs structural parsing checks via typed configurations, writes an abstract payload signature, pushes metadata into a **Redis Cluster Queue**, and immediately delivers a `202 Accepted` network frame back to the client.

### Tenant Isolation Mechanics

- Multi-tenancy is structured around a single shared database engine separating tables contextually via automated Foreign Key models (`organization_id`).
- JWT custom access tokens encapsulate user authentication metadata along with the direct operational tenant context (`org_id`) and explicit role-based access tokens (`role`).
- High-throughput query pipelines over millions of database entries are guarded against memory overruns using specialized relational structural indexing on combined indices: `['organization', 'timestamp', 'event_name']`.

---

## 🛠️ API Reference Guide & Endpoints Documentation

All requests targeting private administrative endpoint parameters must include a valid Bearer token signature inside the headers: `Authorization: Bearer <JWT_ACCESS_TOKEN>`.

### 1. User Authentication (Fetch JWT Token Pair)

- **Endpoint:** `POST /api/auth/token/`
- **Postman:** `POST`- `https://analytics-backend-api.onrender.com/api/auth/token/`
- **Access Control:** Public
- **Payload Structure:**

  ```json
  {
    "username": "admin",
    "password": "securepassword123"
  }
  ```

- **Response Structure:**
  ```json
  {
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```
