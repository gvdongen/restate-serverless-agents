import datetime
import uuid

from pydantic import BaseModel


def fetch_service_status() -> str:
    # Mock service status data (would be real API calls to monitoring systems)
    return str(
        {
            "api": {
                "name": "API Gateway",
                "status": "operational",
                "uptime_24h": 99.8,
                "response_time_avg": "120ms",
                "incidents": 0,
            },
            "database": {
                "name": "Primary Database",
                "status": "operational",
                "uptime_24h": 100.0,
                "response_time_avg": "15ms",
                "incidents": 0,
            },
            "payment": {
                "name": "Payment Service",
                "status": "degraded",
                "uptime_24h": 95.2,
                "response_time_avg": "450ms",
                "incidents": 1,
                "incident_description": "Intermittent timeout issues with payment processor",
            },
            "dashboard": {
                "name": "User Dashboard",
                "status": "operational",
                "uptime_24h": 99.9,
                "response_time_avg": "200ms",
                "incidents": 0,
            },
            "notifications": {
                "name": "Email/SMS Service",
                "status": "maintenance",
                "uptime_24h": 98.5,
                "response_time_avg": "N/A",
                "incidents": 0,
                "incident_description": "Scheduled maintenance until 14:00 UTC",
            },
        }
    )


class SupportTicket(BaseModel):
    user_id: str
    message: str


def create_support_ticket_in_crm(ticket: SupportTicket) -> str:
    # Mock ticket creation (would be real API calls to ticketing systems)
    ticket_id = "TICKET-" + str(uuid.uuid4())
    return str(
        {
            "ticket_id": ticket_id,
            "user_id": ticket.user_id,
            "status": "open",
            "created_at": datetime.datetime.now().isoformat(),
            "details": ticket.message,
        }
    )


# Mock user database with subscription and usage data
users_db = {
    "user_12345": {
        "user_id": "user_12345",
        "email": "john@example.com",
        "subscription": {
            "plan": "Pro",
            "status": "active",
            "billing_cycle": "monthly",
            "price": 49.99,
            "next_billing": "2024-02-15",
        },
        "usage": {
            "api_calls_this_month": 10000,
            "api_limit": 10000,
            "storage_used_gb": 12.5,
            "storage_limit_gb": 50,
        },
        "account_status": "good_standing",
        "created_date": "2023-06-15",
    },
    "user_67890": {
        "user_id": "user_67890",
        "email": "jane@startup.com",
        "subscription": {
            "plan": "Enterprise",
            "status": "active",
            "billing_cycle": "yearly",
            "price": 999.99,
            "next_billing": "2024-06-01",
        },
        "usage": {
            "api_calls_this_month": 45000,
            "api_limit": 100000,
            "storage_used_gb": 180.2,
            "storage_limit_gb": 1000,
        },
        "account_status": "good_standing",
        "created_date": "2022-01-10",
    },
}


def query_user_db(user_id: str) -> str:
    content = users_db.get(user_id, None)
    if content:
        return str(content)
    else:
        return "User not found"