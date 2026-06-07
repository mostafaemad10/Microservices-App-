# Microservices App (DevOps practice project)

Four small, connected Flask microservices in a monorepo layout. The code is
intentionally minimal — the point is the DevOps pipeline around it, not the apps.

```
microservices-app/
├── users-service/      # owns users         (port 5001)
├── products-service/   # owns products      (port 5002)
├── orders-service/     # calls users + products to create orders (port 5003)
├── gateway-service/    # single entry point, aggregates everything (port 5000)
└── docker-compose.yml
```

## How they connect

- `orders-service` calls `users-service` and `products-service` to validate an order.
- `gateway-service` is the front door; it calls all three and exposes a `/summary`.
- Service locations come from environment variables (`USERS_URL`, `PRODUCTS_URL`,
  `ORDERS_URL`) so the same code runs locally, in Docker, and later in Kubernetes.

---

## Option A — Run locally with Python (4 terminals)

```bash
# one-time: a virtualenv per service (or one shared venv works too)
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate

# Terminal 1
cd users-service && pip install -r requirements.txt && python app.py

# Terminal 2
cd products-service && pip install -r requirements.txt && python app.py

# Terminal 3  (point it at the other two)
cd orders-service && pip install -r requirements.txt
export USERS_URL=http://localhost:5001
export PRODUCTS_URL=http://localhost:5002
python app.py

# Terminal 4
cd gateway-service && pip install -r requirements.txt
export USERS_URL=http://localhost:5001
export PRODUCTS_URL=http://localhost:5002
export ORDERS_URL=http://localhost:5003
python app.py
```

## Option B — Run all four with Docker Compose (one command)

```bash
docker compose up --build
```

---

## Test it

```bash
# direct to each service
curl http://localhost:5001/users
curl http://localhost:5002/products
curl http://localhost:5003/orders

# through the gateway
curl http://localhost:5000/
curl http://localhost:5000/users
curl http://localhost:5000/summary

# create an order (orders-service validates user + product across services)
curl -X POST http://localhost:5000/orders \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "product_id": 101}'

# see the created order
curl http://localhost:5000/orders
```

Each service also has a `/health` endpoint, used later for Kubernetes probes.
