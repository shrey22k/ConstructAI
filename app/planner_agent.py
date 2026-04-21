from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from datetime import date
import os
import json

load_dotenv()

# ── Mock Tools ──────────────────────────────────────────────

@tool
def check_workers_availability(role: str) -> str:
    """Check if workers of a specific role are available on site."""
    mock_workers = {
        "mason": {"available": 8, "total": 10},
        "electrician": {"available": 3, "total": 5},
        "plumber": {"available": 2, "total": 4},
        "supervisor": {"available": 2, "total": 2},
        "safety officer": {"available": 1, "total": 1},
        "engineer": {"available": 2, "total": 3},
        "laborer": {"available": 20, "total": 25},
    }
    role_lower = role.lower()
    for key in mock_workers:
        if key in role_lower:
            data = mock_workers[key]
            return f"{data['available']} {key}s available out of {data['total']} total."
    return f"5 workers available for role: {role}"

@tool
def check_materials_availability(material: str) -> str:
    """Check if specific construction materials are available."""
    mock_materials = {
        "concrete": {"available": 500, "unit": "cubic meters"},
        "steel": {"available": 200, "unit": "tons"},
        "bricks": {"available": 50000, "unit": "pieces"},
        "cement": {"available": 300, "unit": "bags"},
        "sand": {"available": 100, "unit": "cubic meters"},
        "wood": {"available": 150, "unit": "planks"},
        "wire": {"available": 2000, "unit": "meters"},
        "pipe": {"available": 500, "unit": "meters"},
    }
    material_lower = material.lower()
    for key in mock_materials:
        if key in material_lower:
            data = mock_materials[key]
            return f"{data['available']} {data['unit']} of {key} available."
    return f"Sufficient quantity of {material} available in inventory."

@tool
def check_equipment_availability(equipment: str) -> str:
    """Check if construction equipment is available and operational."""
    mock_equipment = {
        "crane": "1 available, operational",
        "excavator": "2 available, operational",
        "concrete pump": "1 available, operational",
        "scaffolding": "50 units available, operational",
        "generator": "3 available, operational",
        "compactor": "2 available, 1 under maintenance",
    }
    equipment_lower = equipment.lower()
    for key in mock_equipment:
        if key in equipment_lower:
            return f"{key}: {mock_equipment[key]}"
    return f"{equipment}: Available and operational."

@tool
def validate_site_conditions(location: str) -> str:
    """Validate that site conditions are suitable for construction work."""
    return f"""Site validation for {location}:
- Weather: Clear, suitable for work
- Ground conditions: Stable
- Access roads: Open
- Safety perimeter: Established
- Permits: Valid and up to date
- Last inspection: Passed
Status: APPROVED for work"""

@tool
def generate_task_schedule(tasks_json: str) -> str:
    """
    Generate a realistic day-wise execution schedule.
    Input: JSON string list of tasks.
    Each task must have: task (string), duration_hours (1-4 integer).
    Example: [{"task": "Site Inspection", "duration_hours": 2}, ...]
    """
    try:
        tasks = json.loads(tasks_json)
        schedule = []
        current_hour = 8
        current_day = 1
        WORK_START = 8
        WORK_END = 17

        for i, task in enumerate(tasks):
            # Clamp duration between 1 and 4 hours
            duration = max(1, min(4, int(task.get("duration_hours", 1))))

            # If task won't fit in today's work hours, move to next day
            if current_hour + duration > WORK_END:
                current_day += 1
                current_hour = WORK_START

            end_hour = current_hour + duration

            # Determine dependency
            if i == 0:
                depends = "None — Start of sequence"
            else:
                depends = tasks[i - 1]["task"]

            schedule.append(
                f"Step {i + 1}: {task['task']}\n"
                f"   Day:        Day {current_day}\n"
                f"   Start:      {current_hour:02d}:00\n"
                f"   End:        {end_hour:02d}:00\n"
                f"   Duration:   {duration} hour(s)\n"
                f"   Depends on: {depends}"
            )

            current_hour = end_hour

        total_days = current_day
        summary = f"Total Duration: {total_days} work day(s) | Work hours: {WORK_START}:00 - {WORK_END}:00"
        return summary + "\n\n" + "\n\n".join(schedule)

    except Exception as e:
        return f"Schedule generation failed: {str(e)}"


# ── Planner Agent ────────────────────────────────────────────

class PlannerAgent:
    def __init__(self):
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.3-70b-versatile",
            temperature=0.3
        )

        self.tools = [
            check_workers_availability,
            check_materials_availability,
            check_equipment_availability,
            validate_site_conditions,
            generate_task_schedule,
        ]

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a sophisticated Construction Planner Agent built with LangChain and Groq LLM API.
Your job is to orchestrate complex construction tasks through multi-step reasoning.

When given a construction goal you MUST follow these steps in order:
1. DECOMPOSE the goal into 4-6 clear actionable construction steps
2. CHECK worker availability for relevant roles using check_workers_availability tool
3. CHECK materials availability for relevant materials using check_materials_availability tool
4. CHECK equipment availability using check_equipment_availability tool
5. VALIDATE site conditions using validate_site_conditions tool
6. GENERATE execution schedule using generate_task_schedule tool — pass a JSON array where each item has:
   - "task": step name (string)
   - "duration_hours": realistic duration between 1 and 4 (integer only)
   Do NOT include "depends_on" field — dependencies are handled automatically.
7. PRODUCE a final structured construction plan summarizing all findings

STRICT RULES:
- duration_hours must be an integer between 1 and 4 only — never more than 4
- Never pass depends_on in the tasks JSON
- Always call all tools before writing final output
- Be professional and use construction industry terminology"""),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])

        self.agent = create_tool_calling_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )

        self.executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            max_iterations=12,
            handle_parsing_errors=True
        )

    def plan(self, goal: str, topic: str, location: str) -> dict:
        query = f"""
Construction goal: {goal}
Topic: {topic}
Site location: {location}
Date: {date.today()}

Follow all steps: decompose the goal, check workers/materials/equipment availability,
validate site conditions, generate execution schedule, then write the final plan.
"""
        result = self.executor.invoke({"input": query})
        return {
            "goal": goal,
            "topic": topic,
            "location": location,
            "plan": result["output"]
        }