"""FastAPI demo application."""

from fastapi import FastAPI

from services.order_service import process_orders
from services.user_service import list_users, user_display

app = FastAPI(title="Demo Python Service")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/users")
def get_users():
    users = list_users(5)
    return [{"id": u.id, "name": u.name, "email": u.email} for u in users]


@app.get("/users/{user_id}")
def get_user_endpoint(user_id: int):
    return {"display": user_display(user_id)}


@app.post("/orders")
def create_orders():
    summaries = process_orders([1, 2, 3])
    return {"orders": summaries}
