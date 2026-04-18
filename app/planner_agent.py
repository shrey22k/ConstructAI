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
    """Generate execution schedule. Input: JSON string list of tasks with task, duration_hours, depends_on fields."""
    try:
        tasks = json.loads(tasks_json)
        schedule = []
        current_hour = 8
        for i, task in enumerate(tasks):
            duration = task.get("duration_hours", 1)
            schedule.append(
                f"Step {i+1}: {task['task']} | "
                f"Start: {current_hour:02d}:00 | "
                f"End: {current_hour + duration:02d}:00 | "
                f"Depends on: {', '.join(task.get('depends_on', [])) or 'None'}"
            )
            current_hour += duration
        return "\n".join(schedule)
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

When given a construction goal you MUST:
1. DECOMPOSE the goal into 4-6 actionable steps
2. USE tools to check workers, materials, and equipment availability
3. VALIDATE site conditions using the validate_site_conditions tool
4. GENERATE a detailed execution schedule using generate_task_schedule tool
5. PRODUCE a final structured construction plan with all findings

Always use tools before writing your final plan. Be professional and thorough."""),
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
            max_iterations=10,
            handle_parsing_errors=True
        )

    def plan(self, goal: str, topic: str, location: str) -> dict:
        query = f"""
Construction goal: {goal}
Topic: {topic}
Site location: {location}
Date: {date.today()}

Please:
1. Decompose this into actionable steps
2. Check availability of relevant workers, materials, and equipment using tools
3. Validate site conditions at {location} using tools
4. Generate an execution schedule using tools
5. Provide a final comprehensive construction plan
"""
        result = self.executor.invoke({"input": query})
        return {
            "goal": goal,
            "topic": topic,
            "location": location,
            "plan": result["output"]
        }