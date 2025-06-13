from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner
from env_loader import client  
from pydantic import BaseModel
import asyncio

class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail Check",
    instructions="Check if the user is asking about homework.",
    output_type=HomeworkOutput,
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning step-by-step with examples.",
)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for history questions",
    instructions="You explain historical events clearly and concisely.",
)

async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )

triage_agent = Agent(
    name="Triage Agent",
    instructions="You decide which tutor to hand the question to.",
    handoffs=[math_tutor_agent, history_tutor_agent],
    input_guardrails=[
        InputGuardrail(guardrail_function=homework_guardrail),
    ],
)
async def main():
    questions = [
        "who was the first president of the united states?",
        "what is the integral of x squared?",
    ]

    for question in questions:
        result = await Runner.run(triage_agent, question)
        print(f"\n User: {question}")
        print(f"Agent Response: {result.final_output}\n")

if __name__ == "__main__":
    asyncio.run(main())
