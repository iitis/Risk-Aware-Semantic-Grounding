from map_manager import load_map_data
from base_planner import BasePlanner
from point import Point
from pydantic import BaseModel
from openai import OpenAI
import copy
import json

class PlanModel(BaseModel):
    decision: str
    steps: list[str]
    answer: str

class SimpleLlmPlanner(BasePlanner):
    def __init__(self, map_data):
        self.map_data = map_data # full map (with positions)

        self.simplified_map_data = copy.deepcopy(map_data)
        for obj in self.simplified_map_data.get("objects", []):
            obj.pop("position", None)  # If the position exists, delete it; otherwise, don't give an error.

        self.client = OpenAI()
        self.system_prompt = \
        f"""
You are an expert planner that generates step-by-step plans based on natural language instructions and a given map of the environment.
You can use the following semantic map data:

{self.simplified_map_data}

You should find about which objects the user is talking about in the instruction, and generate a sequence of object IDs as plan steps. 
Return ONLY object IDs as plan steps.

Add "decision" field: "execute", "clarify" or "reject". 

Add "answer" field in your response with natural answer of robot for the query.

If there are similar objects in the map that can be related to some part of instruction, make decision "clarify" and ask user to clarify which object they mean, for example "Can you clarify which chair you mean?".

if there is no any object in the map that can be related to some part of instruction, just reject the instruction with decision "reject" and answer why it is rejected, for exmaple "I am sorry, but I cannot execute this instruction because there is no refrigerator in the bedroom according to the map data you provided.".

Example outputs as JSON:

- {{"decision": "execute", "plan": ["trash_bin_1", "fridge_1", "table_1"], "answer": "I understood your instruction and I am going to execute it."}}
- {{"decision": "clarify", "plan": [], "answer": "Can you clarify which chair you mean?"}}
- {{"decision": "reject", "plan": [], "answer": "I am sorry, but I cannot execute this instruction because there is no refrigerator in the bedroom according to the map data you provided."}}
        """

    def plan(self, start: Point, instruction: str):
        print(f"Planning with LLM for instruction: {instruction}")

        completion = self.client.chat.completions.parse(
            model="gpt-5.4-mini",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Extract the plan steps from the following instruction: {instruction}"},
            ],
            response_format=PlanModel,
        )

        return json.loads(completion.choices[0].message.parsed.model_dump_json())

if __name__ == "__main__":
    # Load data
    map_data = load_map_data("test_map.json")

    if map_data:
        print("Map data loaded successfully!")
        print(f"Number of objects: {len(map_data['objects'])}")
        print()
    else:
        print("Failed to load map data.")
        exit(1)

    instruction = "Go to the wooden table in the kitchen, next take a look on a sofa, then stop near the black cabinet."

    planner = SimpleLlmPlanner(map_data)
    plan = planner.plan(Point(x=0.2, y=4.0), instruction)

    print(f"Generated plan: {plan}")
