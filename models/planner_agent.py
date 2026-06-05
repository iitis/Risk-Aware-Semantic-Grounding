import asyncio
import math
import json
from pathlib import Path
import sys

if __package__ is None or __package__ == "":
    # Allow running this file directly from the models directory.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from map_manager import load_map_data
from base_planner import BasePlanner
from point import Point
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk import runners
from google.genai import types

class PlannerAgent(BasePlanner):
    def __init__(self, map_data):
        self.map_data = map_data
        self.planner_agent = Agent(
            model=LiteLlm(model="openai/gpt-5.4-mini"),
            name="planner_agent",
            description="An agent that creates plans based on natural language instructions and a semantic map accessible by tools.",
            instruction="""
You are an expert planner that generates step-by-step plans based on natural language instructions and a given map of the environment.
You can have access to the following tools to query the semantic map data:

- get_all_types - Returns all types of objects in the map.
- get_all_rooms - Returns all types of rooms in the map.
- get_objects_by_type(object_type: str) - Returns all objects in the map of a given type.
- get_objects_id_in_room(room_type: str) - Returns all objects IDs in the map of a given room type.

Moreover, you can use the following helper function to calculate distances between two points, use it always when instruction contains some spatial dependencies between objects  (e.g. closest window, furthest bed) or robot starting position (e.g. go to an object in the closest room).

- get_distance(x1: float, y1: float, x2: float, y2: float) - Calculates the Euclidean distance between two points.

Based on description of the objects in the instruction and details about the objects in the map, think and understand which objects the user is referring to in the instruction, try to guess (e.g. if there is no exact the same type of object, maybe there is something similar like armchairs/coffee-table or bookshelf/library), and generate a sequence of object IDs as plan steps.

If there are 2 or more objects in the map of the same type and you cannot determine which one is referred in the instruction using properties of the objects, clarify with user by asking a question. Abort plan, DO NOT chose closer one or something like that, just clarify with user by asking a question.

Use received details about the objects in the map to think and understand which objects the user is referring to in the instruction, and generate a sequence of object IDs as plan steps.

Be sure there is a valid order of objects to visit because sometimes it can be not obvious in query, it can be said not in proper order.

Add "decision" field in your response, if you are sure about the plan and there is no need to clarify with user, set decision to "execute", if you think that some part of instruction is not clear and you are not sure about the plan, set decision to "clarify", if instruction is not clear at all and you cannot generate any plan, set decision to "reject".

If you cannot be sure about what objects user is referring to, clarify with user by asking a question, I mean if the object mentioned in the instruction can be related to more than 2 objects in the map, clarify with user by asking a question.

If there is no any object in the map that can be related to some part of instruction, reject the instruction.

if a description of the object in the instruction is misleading and we cannot find the specific object in the map just reject the instruction, for example if user is referring to "the refrigerator in the bedroom" but there is no refrigerator in the bedroom in the map, just reject the instruction.

Add "answer" field in your response, if you are clarifying with user, add your question to the "answer" field.
If there is no need to clarify, just create an answer as a robot that confirms that you understood the instruction and you are going to execute it, for example "I understood your instruction and I am going to execute it".
if there is a rejection, just create an answer as a robot that explains that you cannot execute the instruction, for example "I am sorry, but I cannot execute this instruction because there is no refrigerator in the bedroom according to the map data you provided".

Example plan steps and output format:

- {"decision": "execute", "plan": ["trash_bin_1", "fridge_1", "table_1"], "answer": "I understood your instruction and I am going to execute it."}
- {"decision": "clarify", "plan": [], "answer": "Can you clarify which chair you mean?"}
- {"decision": "reject", "plan": [], "answer": "I am sorry, but I cannot execute this instruction because there is no refrigerator in the bedroom according to the map data you provided."}
            """,
            tools=[
                self.get_distance,
                self.get_all_types,
                self.get_all_rooms,
                self.get_objects_by_type,
                self.get_objects_id_in_room
            ]
        )

    def plan(self, start: Point, instruction: str):
        print(f"Planning with LLM for instruction: {instruction}")

        response = self._run_agent_sync(self.planner_agent, self._get_prompt_for_instruction(start, instruction))
        plan = []
        try:
            plan = json.loads(response)
        except json.JSONDecodeError:
            print(f"Failed to parse JSON response: {response}")
        return plan

    def get_distance(self, x1: float, y1: float, x2: float, y2: float) -> float:
        """Calculates the Euclidean distance between two points."""
        result = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        print(f"Calling get_distance tool by agent! Calculating distance between ({x1}, {y1}) and ({x2}, {y2}). Result: {result}")
        return result

    def get_all_types(self) -> list[str]:
        """Returns all types of objects in the map."""
        result = list({obj['type'].lower() for obj in self.map_data['objects']})
        print(f"Calling get_all_types tool by agent! result: {result}")
        return result

    def get_all_rooms(self) -> list[str]:
        """Returns all types of objects in the map."""
        result = list({obj['type'].lower() for obj in self.map_data['rooms']})
        print(f"Calling get_all_rooms tool by agent! result: {result}")
        return result

    def get_objects_by_type(self, object_type: str) -> list[dict]:
        """Returns all objects in the map of a given type."""
        result = [obj for obj in self.map_data['objects'] if obj['type'].lower() == object_type.lower()]
        print(f"Calling get_objects_by_type tool by agent! Looking for objects of type: {object_type}. Found {len(result)} objects, raw result: {result}")
        return result

    def get_objects_id_in_room(self, room_type: str) -> list[dict]:
        """Returns all objects IDs in the map of a given room type."""
        result = self._flatten([obj['objects'] for obj in self.map_data['rooms'] if obj['type'].lower() == room_type.lower()])
        print(f"Calling get_objects_in_room tool by agent! Looking for objects in room: {room_type}. Found {len(result)} objects, raw result: {result}")
        return result

    def _flatten(self, lst):
        return [item for sub in lst for item in sub]

    def _get_prompt_for_instruction(self, start: Point, instruction: str) -> str:
        return f"Extract the plan steps from the following instruction: {instruction}.\n\nThe starting position is at coordinates x={start.x}, y={start.y}."

    def _run_agent_sync(self, agent: Agent, instruction: str) -> str:
        """Run the agent synchronously and return the final response as a string."""
        async def _run():
            runner = runners.InMemoryRunner(
                agent=agent,
                app_name=f'{agent.name}',
            )
            session = await runner.session_service.create_session(
                app_name=f'{agent.name}', 
                user_id='user'
            )
            initial_message = types.Content(
                role='user', 
                parts=[types.Part(text=instruction)]
            )

            responses = []
            async for event in runner.run_async(
                user_id=session.user_id,
                session_id=session.id,
                new_message=initial_message,
            ):
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            responses.append(part.text)

            return "\n".join(responses) if responses else "No response from agent."
        
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            if loop.is_running():
                import nest_asyncio
                nest_asyncio.apply()
                return loop.run_until_complete(_run())
            else:
                return asyncio.run(_run())
        except RuntimeError:
            return asyncio.run(_run())

if __name__ == "__main__":
    # Load data
    project_root = Path(__file__).resolve().parents[1]
    map_path = project_root / "dataset" / "smart_home_map.json"
    map_data = load_map_data(str(map_path))

    if map_data:
        print("Map data loaded successfully!")
        print(f"Number of objects: {len(map_data['objects'])}")
        print()
    else:
        print("Failed to load map data.")
        exit(1)

    # instruction = "Before heading to the office chair, check the kitchen table and the refrigerator. Finally go to the window in the living room."
    # instruction = "Go to the bookshelf in Bedroom 2, but only after checking the single bed and the desk, and then stop at the window."
    # instruction = "Visit the refrigerator and then inspect the piano."
    instruction = "Inspect the bed and then the wardrobe near it."

    planner = PlannerAgent(map_data)
    plan = planner.plan(Point(x=0.2, y=4.0), instruction)

    print(f"Generated plan: {plan}")
