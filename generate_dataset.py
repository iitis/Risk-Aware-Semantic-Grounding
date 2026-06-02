import json

dataset = {
    "dataset": [
    {
        "query": "Go to the gray sofa in the living room.",
        "category": "single_step",
        "decision": "execute",
        "ground_truth": [ "sofa_1"]
    },
    {
        "query": "Move to the refrigerator in the kitchen.",
        "category": "single_step",
        "decision": "execute",
        "ground_truth": ["refrigerator_1"]
    },
    {
        "query": "Navigate to the desk in the office.",
        "category": "single_step",
        "decision": "execute",
        "ground_truth": [ "desk_office_1" ]
    },
    {
        "query": "Go to the bed in Bedroom 1.",
        "category": "single_step",
        "decision": "execute",
        "ground_truth": [ "bed_double_1" ]
    },

  {
    "query": "Go to the sofa in the living room.",
    "category": "single_step",
    "decision": "execute",
    "ground_truth": ["sofa_1"]
  },
  {
    "query": "Go to the armchair in the living room.",
    "category": "single_step",
    "decision": "execute",
    "ground_truth": ["armchair_1"]
  },
  {
    "query": "Go to the television in the living room.",
    "category": "single_step",
    "decision": "execute",
    "ground_truth": ["tv_1"]
  },
  {
    "query": "Visit the coffee table.",
    "category": "single_step",
    "decision": "execute",
    "ground_truth": ["coffee_table_1"]
  },
  {
    "query": "Go to the dining table in the living room.",
    "category": "single_step",
    "decision": "execute",
    "ground_truth": ["dining_table_1"]
  },

  {
    "query": "Check the refrigerator in the kitchen.",
    "category": "single_step",
    "decision": "execute",
    "ground_truth": ["refrigerator_1"]
  },
  {
    "query": "Go to the stove.",
    "category": "single_step",
    "decision": "execute",
    "ground_truth": ["stove_1"]
  },
  {
    "query": "Visit the oven in the kitchen.",
    "category": "single_step",
    "decision": "execute",
    "ground_truth": ["oven_1"]
  },
  {
    "query": "Go to the kitchen sink.",
    "category": "single_step",
    "decision": "execute",
    "ground_truth": ["sink_k_1"]
  },
  {
    "query": "Visit the refrigerator.",
    "category": "single_step",
    "decision": "execute",
    "ground_truth": ["refrigerator_1"]
  },

  {
    "query": "Go to the double bed in Bedroom 1.",
    "category": "single_step",
    "decision": "execute",
    "ground_truth": ["bed_double_1"]
  },
  {
    "query": "Go to the wardrobe in Bedroom 1.",
    "category": "single_step",
    "decision": "execute",
    "ground_truth": ["wardrobe_b1_1"]
  },
  {
    "query": "Visit the desk in Bedroom 1.",
    "category": "single_step",
    "decision": "execute",
    "ground_truth": ["desk_b1_1"]
  },
  {
    "query": "Go to the window in Bedroom 1.",
    "category": "single_step",
    "decision": "execute",
    "ground_truth": ["window_b1_1"]
  },
  {
    "query": "Check the chair in Bedroom 1.",
    "category": "single_step",
    "decision": "execute",
    "ground_truth": ["chair_b1_1"]
  },

  {
    "query": "Go to the single bed in Bedroom 2.",
    "category": "single_step",
    "decision": "execute",
    "ground_truth": ["bed_single_1"]
  },
  {
    "query": "Inspect the wardrobe in Bedroom 2.",
    "category": "single_step",
    "decision": "execute",
    "ground_truth": ["wardrobe_b2_1"]
  },
  {
    "query": "Visit the desk in Bedroom 2.",
    "category": "single_step",
    "decision": "execute",
    "ground_truth": ["desk_b2_1"]
  },
  {
    "query": "Go to the bookshelf in Bedroom 2.",
    "category": "single_step",
    "decision": "execute",
    "ground_truth": ["library_1"]
  },
  {
    "query": "Inspect the window in Bedroom 2.",
    "category": "single_step",
    "decision": "execute",
    "ground_truth": ["window_b2_1"]
  },

  {
    "query": "Visit the office desk.",
    "category": "single_step",
    "decision": "execute",
    "ground_truth": ["desk_office_1"]
  },
  {
    "query": "Go to the office chair.",
    "category": "single_step",
    "decision": "execute",
    "ground_truth": ["chair_office_1"]
  },
  {
    "query": "Inspect the laptop in the office.",
    "category": "single_step",
    "decision": "execute",
    "ground_truth": ["laptop_1"]
  },

  {
    "query": "Go to the bathroom sink.",
    "category": "single_step",
    "decision": "execute",
    "ground_truth": ["sink_bath_1"]
  },
  {
    "query": "Inspect the toilet.",
    "category": "single_step",
    "decision": "execute",
    "ground_truth": ["toilet_1"]
  },
  {
    "query": "Go to the shower.",
    "category": "single_step",
    "decision": "execute",
    "ground_truth": ["shower_1"]
  },

  {
    "query": "Visit the shoe rack near the entrance.",
    "category": "single_step",
    "decision": "execute",
    "ground_truth": ["shoe_rack_1"]
  },
  {
    "query": "Inspect the coat hanger in the entrance hall.",
    "category": "single_step",
    "decision": "execute",
    "ground_truth": ["coat_hanger_1"]
  },

  {
    "query": "Go to the brown armchair.",
    "category": "single_step",
    "decision": "execute",
    "ground_truth": ["armchair_1"]
  },
  {
    "query": "Visit the gray sofa.",
    "category": "single_step",
    "decision": "execute",
    "ground_truth": ["sofa_1"]
  },
        {
        "query": "Walk to the sofa in the living room, then stand beside the coffee table closest to it.",
        "category": "multi_step",
        "decision": "execute",
        "ground_truth": [
            "sofa_1",
            "coffee_table_1"
        ]
    },
    {
        "query": "Go to the kitchen table, then stand next to the chair farthest from the refrigerator.",
        "category": "multi_step",
        "decision": "execute",
        "ground_truth": [
            "kitchen_table_1",
            "chair_b2_1"
        ]
    },
    {
        "query": "Go to the bed in the closest bedroom, then stop near the wardrobe closest to the window.",
        "category": "multi_step",
        "decision": "execute",
        "ground_truth": [
            "bed_double_1",
            "wardrobe_b1_1"
        ]
    },
    {
        "query": "Move to the TV in the living room, then stand next to the armchair closest to it.",
        "category": "multi_step",
        "decision": "execute",
        "ground_truth": [
            "tv_1",
            "armchair_1"
        ]
    },
    {
        "query": "Go to the sink in the kitchen, then stand beside the chair closest to the oven",
        "category": "multi_step",
        "decision": "execute",
        "ground_truth": [
            "sink_k_1",
            "chair_k_3"
        ]
    },
    {
        "query": "Before going to the window in Bedroom 1, make sure the desk and the double bed are visited. Then stop by the wardrobe, and finally go to the chair.",
        "category": "multi_step",
        "decision": "execute",
        "ground_truth": [
            "bed_double_1",
            "desk_b1_1",
            "window_b1_1",
            "wardrobe_b1_1",
            "chair_b1_1"
        ]
    },
    {
        "query": "Go to the kitchen sink, but first visit the stove and the oven. Then move to the refrigerator, and finish at the kitchen table.",
        "category": "multi_step",
        "decision": "execute",
        "ground_truth": [
            "stove_1",
            "oven_1",
            "sink_k_1",
            "refrigerator_1",
            "kitchen_table_1"
        ]
    },
    {
        "query": "Before heading to the coffee table, stop by the armchair, the TV and the sofa in the living room. Then finish at the dining table.",
        "category": "multi_step",
        "decision": "execute",
        "ground_truth": [
            "tv_1",
            "armchair_1",
            "sofa_1",
            "coffee_table_1",
            "dining_table_1"
        ]
    },
    {
        "query": "Visit the office chair and the desk, then go to the laptop, afterward move to the sofa. Finally stop at the TV.",
        "category": "multi_step",
        "decision": "execute",
            "ground_truth": [
            "chair_office_1",
            "desk_office_1",
            "laptop_1",
            "sofa_1",
            "tv_1"
        ]
    },
    {
        "query": "Before going to the shower, make sure the bathroom sink and the toilet are visited. Then move to the wardrobe in Bedroom 2, and finish at the window.",
        "category": "multi_step",
        "decision": "execute",
        "ground_truth": [
            "sink_bath_1",
            "toilet_1",
            "shower_1",
            "wardrobe_b2_1",
            "window_b2_1"
        ]
    },
    {
        "query": "Check desk in the office, wardrope in the bedroom2, oven in the kitchen, coffe table in the living room, and double bed in bedroom 2. Visit whichever is closer first.",
        "category": "multi_step",
        "decision": "execute",
        "ground_truth": [
            "bed_double_1",
            "coffee_table_1",
            "oven_1",
            "wardrobe_b2_1",
            "desk_office_1"
        ]
    },
  {
    "query": "Visit the sofa and then inspect the refrigerator.",
    "category": "multi_step",
    "decision": "execute",
    "ground_truth": ["sofa_1","refrigerator_1"]
  },
  {
    "query": "Go to the office desk and then inspect the laptop.",
    "category": "multi_step",
    "decision": "execute",
    "ground_truth": ["desk_office_1","laptop_1"]
  },
  {
    "query": "Visit the double bed and then inspect the desk in Bedroom 1.",
    "category": "multi_step",
    "decision": "execute",
    "ground_truth": ["bed_double_1","desk_b1_1"]
  },
  {
    "query": "Inspect the refrigerator, then the stove, and finally the oven.",
    "category": "multi_step",
    "decision": "execute",
    "ground_truth": ["refrigerator_1","stove_1","oven_1"]
  },
  {
    "query": "Visit the sofa, then the coffee table, and finally the television.",
    "category": "multi_step",
    "decision": "execute",
    "ground_truth": ["sofa_1","coffee_table_1","tv_1"]
  },

  {
    "query": "Go to the desk in Bedroom 1, then inspect the wardrobe, and finally visit the window.",
    "category": "multi_step",
    "decision": "execute",
    "ground_truth": ["desk_b1_1","wardrobe_b1_1","window_b1_1"]
  },
  {
    "query": "Inspect the desk in Bedroom 2, then the bookshelf, and finally the single bed.",
    "category": "multi_step",
    "decision": "execute",
    "ground_truth": ["desk_b2_1","library_1","bed_single_1"]
  },
  {
    "query": "Visit the office chair, then inspect the laptop, and finally the office desk.",
    "category": "multi_step",
    "decision": "execute",
    "ground_truth": ["chair_office_1","laptop_1","desk_office_1"]
  },
  {
    "query": "Inspect the sink, then the toilet, and finally the shower.",
    "category": "multi_step",
    "decision": "execute",
    "ground_truth": ["sink_bath_1","toilet_1","shower_1"]
  },
  {
    "query": "Visit the shoe rack, then inspect the coat hanger, and finally go to the sofa.",
    "category": "multi_step",
    "decision": "execute",
    "ground_truth": ["shoe_rack_1","coat_hanger_1","sofa_1"]
  },

  {
    "query": "Go to the sofa, then the refrigerator, then the laptop, and finally the shower.",
    "category": "multi_step",
    "decision": "execute",
    "ground_truth": ["sofa_1","refrigerator_1","laptop_1","shower_1"]
  },
  {
    "query": "Inspect the double bed, then the wardrobe, then the desk, and finally the window in Bedroom 1.",
    "category": "multi_step",
    "decision": "execute",
    "ground_truth": ["bed_double_1","wardrobe_b1_1","desk_b1_1","window_b1_1"]
  },
  {
    "query": "Visit the single bed, then the desk, then the bookshelf, and finally the wardrobe in Bedroom 2.",
    "category": "multi_step",
    "decision": "execute",
    "ground_truth": ["bed_single_1","desk_b2_1","library_1","wardrobe_b2_1"]
  },
  {
    "query": "Inspect the refrigerator, then the stove, then the oven, and finally the kitchen sink.",
    "category": "multi_step",
    "decision": "execute",
    "ground_truth": ["refrigerator_1","stove_1","oven_1","sink_k_1"]
  },
  {
    "query": "Visit the coffee table, then the armchair, then the sofa, and finally the television.",
    "category": "multi_step",
    "decision": "execute",
    "ground_truth": ["coffee_table_1","armchair_1","sofa_1","tv_1"]
  },

  {
    "query": "Go to the shoe rack, then the coat hanger, then the refrigerator, then the laptop, and finally the shower.",
    "category": "multi_step",
    "decision": "execute",
    "ground_truth": ["shoe_rack_1","coat_hanger_1","refrigerator_1","laptop_1","shower_1"]
  },
  {
    "query": "Visit the office desk, then the laptop, then the sofa, then the refrigerator, and finally the shower.",
    "category": "multi_step",
    "decision": "execute",
    "ground_truth": ["desk_office_1","laptop_1","sofa_1","refrigerator_1","shower_1"]
  },
  {
    "query": "Inspect the television, then the coffee table, then the sofa, then the refrigerator, and finally the office desk.",
    "category": "multi_step",
    "decision": "execute",
    "ground_truth": ["tv_1","coffee_table_1","sofa_1","refrigerator_1","desk_office_1"]
  },
  {
    "query": "Visit the double bed, then the desk in Bedroom 1, then the bookshelf, then the desk in Bedroom 2, and finally the laptop.",
    "category": "multi_step",
    "decision": "execute",
    "ground_truth": ["bed_double_1","desk_b1_1","library_1","desk_b2_1","laptop_1"]
  },
  {
    "query": "Inspect the refrigerator, then the oven, then the sink, then the sofa, and finally the television.",
    "category": "multi_step",
    "decision": "execute",
    "ground_truth": ["refrigerator_1","oven_1","sink_k_1","sofa_1","tv_1"]
  },

  {
    "query": "Visit the shoe rack, then the coat hanger, then the sofa, then the refrigerator, then the laptop, and finally the shower.",
    "category": "multi_step",
    "decision": "execute",
    "ground_truth": ["shoe_rack_1","coat_hanger_1","sofa_1","refrigerator_1","laptop_1","shower_1"]
  },
  {
    "query": "Inspect the double bed, then the wardrobe, then the desk, then the window, then the refrigerator, and finally the laptop.",
    "category": "multi_step",
    "decision": "execute",
    "ground_truth": ["bed_double_1","wardrobe_b1_1","desk_b1_1","window_b1_1","refrigerator_1","laptop_1"]
  },
  {
    "query": "Visit the single bed, then the bookshelf, then the desk, then the wardrobe, then the office desk, and finally the laptop.",
    "category": "multi_step",
    "decision": "execute",
    "ground_truth": ["bed_single_1","library_1","desk_b2_1","wardrobe_b2_1","desk_office_1","laptop_1"]
  },
  {
    "query": "Inspect the refrigerator, then the stove, then the oven, then the sink, then the sofa, and finally the television.",
    "category": "multi_step",
    "decision": "execute",
    "ground_truth": ["refrigerator_1","stove_1","oven_1","sink_k_1","sofa_1","tv_1"]
  },
  {
    "query": "Visit the coffee table, then the dining table, then the armchair, then the sofa, then the television, and finally the office desk.",
    "category": "multi_step",
    "decision": "execute",
    "ground_truth": ["coffee_table_1","dining_table_1","armchair_1","sofa_1","tv_1","desk_office_1"]
  },

  {
    "query": "Go to the sofa before visiting the refrigerator and then inspect the laptop.",
    "category": "multi_step",
    "decision": "execute",
    "ground_truth": ["sofa_1","refrigerator_1","laptop_1"]
  },
  {
    "query": "Visit the double bed first, then the desk in Bedroom 1, and finally the office desk.",
    "category": "multi_step",
    "decision": "execute",
    "ground_truth": ["bed_double_1","desk_b1_1","desk_office_1"]
  },
  {
    "query": "Inspect the bookshelf before visiting the laptop and then the shower.",
    "category": "multi_step",
    "decision": "execute",
    "ground_truth": ["library_1","laptop_1","shower_1"]
  },
  {
    "query": "Go to the television, then the sofa, then the refrigerator, then the laptop, then the shower, and finally the office desk.",
    "category": "multi_step",
    "decision": "execute",
    "ground_truth": ["tv_1","sofa_1","refrigerator_1","laptop_1","shower_1","desk_office_1"]
  },
  {
    "query": "Visit the shoe rack, then the coat hanger, then the dining table, then the refrigerator, then the laptop, and finally the shower.",
    "category": "multi_step",
    "decision": "execute",
    "ground_truth": ["shoe_rack_1","coat_hanger_1","dining_table_1","refrigerator_1","laptop_1","shower_1"]
  },

  {
    "query": "Go to the chair.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },
  {
    "query": "Inspect the chair.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },
  {
    "query": "Visit the chair next to the window.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },
  {
    "query": "Go to a chair.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },
  {
    "query": "Check the wooden chair.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },

  {
    "query": "Visit the desk.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },
  {
    "query": "Inspect the desk.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },
  {
    "query": "Go to the wooden desk.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },
  {
    "query": "Visit the work desk.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },
  {
    "query": "Check the desk near the chair.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },

  {
    "query": "Go to the window.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },
  {
    "query": "Go to the window.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },
  {
    "query": "Visit the white window.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },
  {
    "query": "Go to the desk near the window.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },
  {
    "query": "Close the large window.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },

  {
    "query": "Visit the wardrobe.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },
  {
    "query": "Inspect the wardrobe.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },
  {
    "query": "Go to the wooden wardrobe.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },
  {
    "query": "Check the wardrobe near the bed.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },
  {
    "query": "Visit the closet.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },

  {
    "query": "Inspect the sink.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },
  {
    "query": "Go to the sink.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },
  {
    "query": "Visit the ceramic sink.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },
  {
    "query": "Check the sink near the wall.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },
  {
    "query": "Inspect the wash basin.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },

  {
    "query": "Go to the dining table.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },
  {
    "query": "Inspect the table.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },
  {
    "query": "Visit the wooden table.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },

  {
    "query": "Go to the bed.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },
  {
    "query": "Inspect the bed.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },
  {
    "query": "Visit the sleeping area.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },

  {
    "query": "Visit the chair and then inspect the desk.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },
  {
    "query": "Go to the window and then the chair.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },
  {
    "query": "Inspect the desk and then the window.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },
  {
    "query": "Visit the chair near the desk.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },
  {
    "query": "Go to the desk and then inspect the chair next to it.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },

  {
    "query": "Inspect the wardrobe and then visit the bed.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },
  {
    "query": "Visit the sink and then inspect the window.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },
  {
    "query": "Go to the chair, then the window, and finally the desk.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },
  {
    "query": "Inspect the bed and then the wardrobe near it.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },
  {
    "query": "Visit the table and then the chair closest to it.",
    "category": "ambiguous",
    "decision": "clarify",
    "ground_truth": []
  },

  {
    "query": "Go to the piano.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Inspect the piano.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Visit the printer.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Go to the microwave.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Inspect the dishwasher.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },

  {
    "query": "Visit the aquarium.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Go to the fireplace.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Inspect the washing machine.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Visit the projector.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Go to the coffee machine.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },

  {
    "query": "Inspect the air conditioner.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Visit the treadmill.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Go to the guitar.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Inspect the drum set.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Visit the speaker system.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },

  {
    "query": "Go to the vacuum robot.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Inspect the gaming console.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Visit the scanner.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Go to the fax machine.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Inspect the server rack.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },

  {
    "query": "Visit the water dispenser.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Go to the fish tank.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Inspect the microscope.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Visit the telescope.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Go to the sewing machine.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },

  {
    "query": "Inspect the 3D printer.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Visit the photocopier.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Go to the smart speaker.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Inspect the radiator.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Visit the humidifier.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },

  {
    "query": "Visit the refrigerator and then inspect the piano.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Go to the sofa and then the aquarium.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Inspect the laptop and then the printer.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Visit the shower and then the microwave.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Go to the television and then inspect the fireplace.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },

  {
    "query": "Visit the office desk and then the projector.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Inspect the bookshelf and then the washing machine.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Go to the refrigerator, then the stove, and finally the dishwasher.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Visit the laptop, then the office chair, and finally the scanner.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Inspect the double bed and then the guitar.",
    "category": "hallucination",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Go to the refrigerator in Bedroom 1.",
    "category": "semantic_conflict",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Inspect the refrigerator in Bedroom 2.",
    "category": "semantic_conflict",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Visit the laptop in the bathroom.",
    "category": "semantic_conflict",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Go to the shower in the office.",
    "category": "semantic_conflict",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Inspect the sofa in the bathroom.",
    "category": "semantic_conflict",
    "decision": "reject",
    "ground_truth": []
  },

  {
    "query": "Visit the television in Bedroom 1.",
    "category": "semantic_conflict",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Go to the office desk in the kitchen.",
    "category": "semantic_conflict",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Inspect the stove in Bedroom 2.",
    "category": "semantic_conflict",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Visit the oven in the bathroom.",
    "category": "semantic_conflict",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Go to the bookshelf in the kitchen.",
    "category": "semantic_conflict",
    "decision": "reject",
    "ground_truth": []
  },

  {
    "query": "Inspect the toilet in the office.",
    "category": "semantic_conflict",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Visit the double bed in the living room.",
    "category": "semantic_conflict",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Go to the single bed in the kitchen.",
    "category": "semantic_conflict",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Inspect the refrigerator in the office.",
    "category": "semantic_conflict",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Visit the shower in Bedroom 1.",
    "category": "semantic_conflict",
    "decision": "reject",
    "ground_truth": []
  },

  {
    "query": "Go to the laptop in Bedroom 2.",
    "category": "semantic_conflict",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Inspect the office chair in the bathroom.",
    "category": "semantic_conflict",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Visit the dining table in the bathroom.",
    "category": "semantic_conflict",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Go to the coffee table in Bedroom 2.",
    "category": "semantic_conflict",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Inspect the sofa in the office.",
    "category": "semantic_conflict",
    "decision": "reject",
    "ground_truth": []
  },

  {
    "query": "Visit the wardrobe in the kitchen.",
    "category": "semantic_conflict",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Go to the wardrobe in the bathroom.",
    "category": "semantic_conflict",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Inspect the television in Bedroom 2.",
    "category": "semantic_conflict",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Visit the laptop in the corridor.",
    "category": "semantic_conflict",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Go to the office desk in Bedroom 1.",
    "category": "semantic_conflict",
    "decision": "reject",
    "ground_truth": []
  },

  {
    "query": "Inspect the kitchen sink in the office.",
    "category": "semantic_conflict",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Visit the bathroom sink in the kitchen.",
    "category": "semantic_conflict",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Go to the bookshelf in the bathroom.",
    "category": "semantic_conflict",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Inspect the refrigerator in the entrance hall.",
    "category": "semantic_conflict",
    "decision": "reject",
    "ground_truth": []
  },
  {
    "query": "Visit the toilet in Bedroom 2.",
    "category": "semantic_conflict",
    "decision": "reject",
    "ground_truth": []
  },



]
}

with open("dataset/dataset_query_decision_gt.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=4)