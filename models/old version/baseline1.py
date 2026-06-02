from map_manager import load_map_data
from base_planner import BasePlanner
from point import Point

class SingleNearestGoalSemanticPlanner(BasePlanner):
    def __init__(self, map_data):
        self.map_data = map_data

    def plan(self, start: Point, instruction: str):
        goal_type = self._extract_goal_type(instruction)

        if goal_type:
            print(f"Extracted type of goal: {goal_type}")
            goal = self._find_nearest_goal(start, goal_type)
            if goal:
                print(f"Found nearest goal: {goal}")
                return [goal['id']]
            else:
                print("No valid goal found.")
                return None
        else:
            print("No goal type extracted from instruction.")

    def _extract_goal_type(self, instruction: str) -> str:
        words = instruction.split()
        for word in words:
            for obj in self.map_data['objects']:
                if word.lower() == obj['type'].lower():
                    return word.lower()
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
    map_data = load_map_data("test_map.json")

    if map_data:
        print("Map data loaded successfully!")
        print(f"Number of objects: {len(map_data['objects'])}")
        print()
    else:
        print("Failed to load map data.")
        exit(1)

    # instruction = input("Enter your instruction for planner: ")
    instruction = "Go to the wooden table in the kitchen, next take a look on a sofa, then stop near the black cabinet."

    planner = SingleNearestGoalSemanticPlanner(map_data)
    plan = planner.plan(Point(x=0.2, y=4.0), instruction)

    print(f"Generated plan: {plan}")
