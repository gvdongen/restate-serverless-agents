import restate

from agents import Agent, RunConfig, Runner, function_tool, RunContextWrapper
from pydantic import BaseModel

from utils.middleware import DurableModelCalls
from utils.utils import (
    query_user_db, fetch_service_status, create_support_ticket_in_crm, SupportTicket,
)

# PROMPT

# Example customer support request
example_prompt = "My API calls are failing, what's wrong with my account?"
"""
Other examples:
    "What's my current subscription plan and usage limits?",
    "Is there an outage affecting the payment service?",
    "I need to report a bug with the dashboard, please create a ticket"
"""


class Prompt(BaseModel):
    user_id: str = "user_12345"
    message: str = example_prompt


# TOOLS


@function_tool
async def query_user_database(
    wrapper: RunContextWrapper[restate.Context], user_id: str
) -> str:
    """Get the current weather for a given city."""
    # Do durable steps using the Restate context
    restate_context = wrapper.context
    return await restate_context.run_typed(
        "Query user DB", query_user_db, user_id=user_id
    )


@function_tool
async def get_service_status(
    wrapper: RunContextWrapper[restate.Context]
) -> str:
    """Get the current weather for a given city."""
    # Do durable steps using the Restate context
    restate_context = wrapper.context
    return await restate_context.run_typed(
        "Get service status", fetch_service_status
    )


@function_tool
async def create_support_ticket(
    wrapper: RunContextWrapper[restate.Context], ticket: SupportTicket
) -> str:
    """Get the current weather for a given city."""
    # Do durable steps using the Restate context
    restate_context = wrapper.context
    return await restate_context.run_typed(
        "create support ticket",
        create_support_ticket_in_crm,
        ticket=ticket,
    )

# AGENT

customer_support_agent = Agent[restate.Context](
    name="CustomerSupportAgent",
    instructions="You are a helpful agent for customer support. Use the tools to assist with user account, billing, service status, and issue reporting.",
    tools=[query_user_database, get_service_status, create_support_ticket],
)


customer_support_service = restate.Service("agent")


@customer_support_service.handler()
async def route(restate_context: restate.Context, prompt: Prompt) -> str:
    """Customer support for questions about account, billing, service status, and issues"""
    result = await Runner.run(
        customer_support_agent,
        input=prompt.message,
        # Pass the Restate context to tools to make tool execution steps durable
        context=restate_context,
        # Choose any model and let Restate persist your calls
        run_config=RunConfig(
            model="gpt-4o", model_provider=DurableModelCalls(restate_context)
        ),
    )
    return result.final_output