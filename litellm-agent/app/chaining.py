import litellm
import restate
from pydantic import BaseModel

meeting_processing_svc = restate.Service("MeetingProcessingService")

example_transcript = """Meeting: Product Roadmap Planning
Date: October 7, 2025
Attendees: Sarah (PM), Mike (Engineering), Lisa (Design), Tom (Sales)

Sarah: Let's review the Q4 roadmap. We need to prioritize the mobile app redesign.
Mike: I can allocate two engineers to start on that next week. We'll need about 6 weeks.
Lisa: I'll have the wireframes ready by Friday. Can we schedule a design review?
Tom: Our biggest clients are asking for the API integration feature. Can we fast-track that?
Sarah: Good point Tom. Mike, what's the timeline for API integration?
Mike: If we start after the mobile redesign, probably 4 weeks. But if we do them in parallel, we risk delays.
Lisa: I'll coordinate with Mike's team on the design review. Let's schedule it for Monday at 2 PM.
Tom: I'll reach out to the key clients to confirm their requirements for the API feature.
Sarah: Great. Everyone has their action items. Let's reconvene next Friday to check progress."""

class MeetingTranscript(BaseModel):
    transcript: str = example_transcript
    recipient_email: str = "team@company.com"


@meeting_processing_svc.handler()
async def process_meeting(ctx: restate.Context, meeting: MeetingTranscript) -> str:
    """Processes meeting transcript: summarizes, extracts action items, and emails them."""

    # Step 1: Summarize the meeting
    response = await ctx.run_typed(
        "Summarize meeting",
        litellm.acompletion,
        model="gpt-4o",
        messages=[{"role": "user", "content": f"Provide a concise summary of this meeting transcript, including key decisions and outcomes. "
        f"Format as a brief paragraph. Transcript: {meeting.transcript}"}],
    )
    summary = response.choices[0].message

    # Step 2: Extract action items
    response2 = await ctx.run_typed(
        "Extract action items",
        litellm.acompletion,
        model="gpt-4o",
        messages=[{"role": "user", "content": f"Extract all action items from this meeting transcript. Format each action item as "
        f"'- [Person]: [Action] (due: [timeframe if mentioned])'. Transcript: {meeting.transcript}"}],
    )
    action_items = response2.choices[0].message

    # Step 3: Email the summary and action items
    await ctx.run_typed(
        "send email",
        send_email,
        recipient=meeting.recipient_email,
        summary=summary,
        action_items=action_items,
    )



# UTILS
def send_email(summary: str, action_items: str, recipient: str):
    print(
        f"Sending meeting summary and action points to {recipient}. Content: {summary} - {action_items}. "
    )