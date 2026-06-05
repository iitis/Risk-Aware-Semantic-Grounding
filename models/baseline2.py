from pathlib import Path
import sys
import json

if __package__ is None or __package__ == "":
    # Allow running this file directly from the models directory.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from map_manager import load_map_data
from base_planner import BasePlanner
from point import Point

class RuleBasedSequentialPlanner(BasePlanner):
    def __init__(self, map_data):
        self.map_data = map_data
        self.object_types = set({obj['type'].lower() for obj in self.map_data['objects']})
        self.types_with_properties = self._extract_types_and_properties_from_map()
        self.keywords_to_split = ["then", "after", "next", "and", ",", ";", "."]

    def plan(self, start: Point, instruction: str):
        # Split the instruction into sub-instructions based on keywords
        sub_instructions = []
        for sub_instruction in self._split_instruction(instruction):
            if len(sub_instruction.strip()) == 0:
                continue
            sub_instructions.append(sub_instruction.lower().strip())
        print(f"Sub-instructions: {sub_instructions}")

        plan = []

        for sub_instruction in sub_instructions:
            goal_type = self._extract_goal_type(sub_instruction)

            if goal_type:
                print(f"Extracted type of goal: {goal_type}")
                goal = self._find_goal_with_property(goal_type, sub_instruction)
                if goal:
                    print(f"Found goal with matching properties: {goal}")
                    plan.append(goal['id'])
                else:
                    goal = self._find_nearest_goal(start, goal_type)
                    if goal:
                        print(f"Found nearest goal: {goal}")
                        plan.append(goal['id'])
                    else:
                        print("No valid goal found.")

        if len(plan) > 0:
            return {
                "decision": "execute",
                "plan": plan,
                "answer": "I understood your instruction and I am going to execute it."
            }
        else:
            return {
                "decision": "reject",
                "plan": [],
                "answer": "I am sorry, but I cannot execute this instruction because no valid goals were found."
            }

    def _extract_types_and_properties_from_map(self):
        types_with_properties = dict()

        for type in self.object_types:
            types_with_properties[type] = set()
            for obj in self.map_data['objects']:
                if obj['type'].lower() == type:
                    for prop in obj.get('properties', []):
                        value = prop['value'].lower() if isinstance(prop['value'], str) else prop['value']
                        types_with_properties[type].add(value)

        return types_with_properties

    def _split_instruction(self, instruction: str) -> list:
        for keyword in self.keywords_to_split:
            instruction = instruction.replace(keyword, "|")
        return instruction.split("|")
    
    def _extract_goal_type(self, instruction: str) -> str:
        for word in instruction.lower().split():
            if word in self.object_types:
                return word

        return None

    def _find_goal_with_property(self, goal_type: str, instruction: str) -> dict:
        """Finds an object of the specified type with a property mentioned in the instruction."""
        for obj in self.map_data['objects']:
            if obj['type'].lower() == goal_type.lower():
                # Check if any property value is mentioned in the instruction
                for prop in obj.get('properties', []):
                    prop_value = prop['value']
                    if isinstance(prop_value, str):
                        if prop_value.lower() in instruction.lower():
                            return obj
        return None

    def _find_nearest_goal(self, start: Point, goal_type: str) -> dict:
        """Finds the nearest object of the specified type to the start position."""
        nearest_goal = None
        nearest_distance = float('inf')

        for obj in self.map_data['objects']:
            if obj['type'].lower() == goal_type.lower():
                goal_position = Point.from_dict(obj['position'])
                distance = start.distance_to(goal_position)
                
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_goal = obj

        return nearest_goal

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

    instruction = "Go to the wooden table in the kitchen, next take a look on a sofa, then stop near the black cabinet."
    instruction = "Go to the window in the living room, but before that, make sure the laptop is in the office."

    planner = RuleBasedSequentialPlanner(map_data)
    plan = planner.plan(Point(x=0.2, y=4.0), instruction)

    print(f"Generated plan: {plan}")
