from map_manager import load_map_data
from base_planner import BasePlanner
from point import Point
from pydantic import BaseModel
from openai import OpenAI
import copy
import os
class PlanModel(BaseModel):
    steps: list[str]

class SimpleLlmPlanner(BasePlanner):
    def __init__(self, map_data):
        self.map_data = map_data # full map (with positions)

        self.simplified_map_data = copy.deepcopy(map_data)
        for obj in self.simplified_map_data.get("objects", []):
            obj.pop("position", None)  # If the position exists, delete it; otherwise, don't give an error.

        self.client = OpenAI(api_key=os.environ["API_KEY_MOBILE_ROBOT"])
        self.system_prompt = \
        f"""
You are an expert planner that generates step-by-step plans based on natural language instructions and a given map of the environment.
You can use the following semantic map data:

{self.simplified_map_data}

You should find about which objects the user is talking about in the instruction, and generate a sequence of object IDs as plan steps. 
Return ONLY object IDs as plan steps.

Example plan steps:

["trash_bin_1", "fridge_1", "table_1"]
        """

    def plan(self, start: Point, instruction: str):
        print(f"Planning with LLM for instruction: {instruction}")

        completion = self.client.chat.completions.parse(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Extract the plan steps from the following instruction: {instruction}"},
            ],
            response_format=PlanModel,
        )

        return completion.choices[0].message.parsed.steps

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
