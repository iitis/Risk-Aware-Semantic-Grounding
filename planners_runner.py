import json
from base_planner import BasePlanner
from models.baseline1 import SingleNearestGoalSemanticPlanner
from models.baseline2 import RuleBasedSequentialPlanner
from models.baseline3 import SimpleLlmPlanner
from models.planner_agent import PlannerAgent
from map_manager import load_map_data, display_objects
from point import Point
from typing import List
import time

if __name__ == "__main__":
    # Load data
    map_data = load_map_data("dataset/smart_home_map.json")

    if map_data:
        print("Map data loaded successfully!")
        print(f"Number of objects: {len(map_data['objects'])}")
        print()
    else:
        print("Failed to load map data.")
        exit(1)

    dataset = load_map_data("dataset/dataset_query_decision_gt.json")

    if dataset:
        print("Dataset loaded successfully!")
        print(f"Number of dataset entries: {len(dataset['dataset'])}")
        print()
    else:
        print("Failed to load dataset.")
        exit(1)

    planners : List[BasePlanner] = [
        SingleNearestGoalSemanticPlanner(map_data),
        RuleBasedSequentialPlanner(map_data),
        SimpleLlmPlanner(map_data),
        PlannerAgent(map_data)
    ]

    results = { "results": [] }
    start_time = time.time()
    total_entries = len(dataset['dataset'])
    
    for index, entry in enumerate(dataset['dataset'], 1):
        entry_start = time.time()
        print(f"\n[{index}/{total_entries}] Processing: {entry['query']}")
        
        planner_results = []
        for planner in planners:
            plan = planner.plan(Point(x=0.2, y=4.0), entry['query'])
            print(f"[{planner.__class__.__name__}] Generated plan for {entry['query']}: {plan}")
            planner_results.append({
                "planner": planner.__class__.__name__,
                "result": plan
            })
        
        entry_elapsed = time.time() - entry_start
        elapsed_time = time.time() - start_time
        avg_time = elapsed_time / index
        remaining = (total_entries - index) * avg_time
        
        print(f"Entry completed in {entry_elapsed:.2f}s | Total elapsed: {elapsed_time:.2f}s | ETA: {remaining:.2f}s")
        
        results["results"].append({
            "query": entry['query'],
            "category": entry['category'],
            "decision": entry['decision'],
            "ground_truth": entry['ground_truth'],
            "result": planner_results
        })
    
    total_time = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"All entries processed in {total_time:.2f} seconds ({total_time/60:.2f} minutes)")
    print(f"Average time per entry: {total_time/total_entries:.2f} seconds")
    print(f"{'='*60}\n")

    # Save results to a file
    with open("results/new_dataset_results.json", "w") as f:
        json.dump(results, f, indent=4)

    print("Results saved to results/new_dataset_results.json")
