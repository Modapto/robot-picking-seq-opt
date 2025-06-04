import json

# (Paste your entire list here. For brevity, only a few items are shown.)
distance_matrix = [
      {
        "edge": "(0.0, 1.1.1)",
        "distance": 7515
      },
      {
        "edge": "(0.0, 1.2.1)",
        "distance": 11520
      },
      {
        "edge": "(0.0, 1.3.1)",
        "distance": 14744
      },
      {
        "edge": "(0.0, 1.4.1)",
        "distance": 17958
      },
      {
        "edge": "(0.0, 1.5.1)",
        "distance": 21130
      },
      {
        "edge": "(0.0, 1.6.1)",
        "distance": 24329
      },
      {
        "edge": "(0.0, 1.7.1)",
        "distance": 27570
      },
      {
        "edge": "(0.0, 2.1.1)",
        "distance": 7779
      },
      {
        "edge": "(0.0, 2.2.1)",
        "distance": 11784
      },
      {
        "edge": "(0.0, 2.3.1)",
        "distance": 15008
      },
      {
        "edge": "(0.0, 2.4.1)",
        "distance": 18222
      },
      {
        "edge": "(0.0, 2.5.1)",
        "distance": 21394
      },
      {
        "edge": "(0.0, 2.6.1)",
        "distance": 24593
      },
      {
        "edge": "(0.0, 2.7.1)",
        "distance": 27834
      },
      {
        "edge": "(0.0.0, 0.0)",
        "distance": 0
      },
      {
        "edge": "(1.1.1, 1.1)",
        "distance": 9261
      },
      {
        "edge": "(1.1.1, 2.1)",
        "distance": 22267
      },
      {
        "edge": "(1.1.1, 3.1)",
        "distance": 28653
      },
      {
        "edge": "(1.1.1, 4.1)",
        "distance": 35093
      },
      {
        "edge": "(1.2.1, 1.1)",
        "distance": 19043
      },
      {
        "edge": "(1.2.1, 2.1)",
        "distance": 19043
      },
      {
        "edge": "(1.2.1, 3.1)",
        "distance": 25481
      },
      {
        "edge": "(1.2.1, 4.1)",
        "distance": 31852
      },
      {
        "edge": "(1.3.1, 1.1)",
        "distance": 22267
      },
      {
        "edge": "(1.3.1, 2.1)",
        "distance": 9261
      },
      {
        "edge": "(1.3.1, 3.1)",
        "distance": 22267
      },
      {
        "edge": "(1.3.1, 4.1)",
        "distance": 28653
      },
      {
        "edge": "(1.4.1, 1.1)",
        "distance": 25481
      },
      {
        "edge": "(1.4.1, 2.1)",
        "distance": 19043
      },
      {
        "edge": "(1.4.1, 3.1)",
        "distance": 19043
      },
      {
        "edge": "(1.4.1, 4.1)",
        "distance": 25481
      },
      {
        "edge": "(1.5.1, 1.1)",
        "distance": 28653
      },
      {
        "edge": "(1.5.1, 2.1)",
        "distance": 22267
      },
      {
        "edge": "(1.5.1, 3.1)",
        "distance": 9261
      },
      {
        "edge": "(1.5.1, 4.1)",
        "distance": 22267
      },
      {
        "edge": "(1.6.1, 1.1)",
        "distance": 31852
      },
      {
        "edge": "(1.6.1, 2.1)",
        "distance": 25481
      },
      {
        "edge": "(1.6.1, 3.1)",
        "distance": 19043
      },
      {
        "edge": "(1.6.1, 4.1)",
        "distance": 19043
      },
      {
        "edge": "(1.7.1, 1.1)",
        "distance": 35093
      },
      {
        "edge": "(1.7.1, 2.1)",
        "distance": 28653
      },
      {
        "edge": "(1.7.1, 3.1)",
        "distance": 22267
      },
      {
        "edge": "(1.7.1, 4.1)",
        "distance": 9261
      },
      {
        "edge": "(2.1.1, 1.1)",
        "distance": 8973
      },
      {
        "edge": "(2.1.1, 2.1)",
        "distance": 22531
      },
      {
        "edge": "(2.1.1, 3.1)",
        "distance": 28917
      },
      {
        "edge": "(2.1.1, 4.1)",
        "distance": 35357
      },
      {
        "edge": "(2.2.1, 1.1)",
        "distance": 19307
      },
      {
        "edge": "(2.2.1, 2.1)",
        "distance": 19307
      },
      {
        "edge": "(2.2.1, 3.1)",
        "distance": 25745
      },
      {
        "edge": "(2.2.1, 4.1)",
        "distance": 32116
      },
      {
        "edge": "(2.3.1, 1.1)",
        "distance": 22531
      },
      {
        "edge": "(2.3.1, 2.1)",
        "distance": 8973
      },
      {
        "edge": "(2.3.1, 3.1)",
        "distance": 22531
      },
      {
        "edge": "(2.3.1, 4.1)",
        "distance": 19307
      },
      {
        "edge": "(2.4.1, 1.1)",
        "distance": 25745
      },
      {
        "edge": "(2.4.1, 2.1)",
        "distance": 19307
      },
      {
        "edge": "(2.4.1, 3.1)",
        "distance": 19307
      },
      {
        "edge": "(2.4.1, 4.1)",
        "distance": 25745
      },
      {
        "edge": "(2.5.1, 1.1)",
        "distance": 28917
      },
      {
        "edge": "(2.5.1, 2.1)",
        "distance": 22531
      },
      {
        "edge": "(2.5.1, 3.1)",
        "distance": 8973
      },
      {
        "edge": "(2.5.1, 4.1)",
        "distance": 22531
      },
      {
        "edge": "(2.6.1, 1.1)",
        "distance": 32116
      },
      {
        "edge": "(2.6.1, 2.1)",
        "distance": 25745
      },
      {
        "edge": "(2.6.1, 3.1)",
        "distance": 19307
      },
      {
        "edge": "(2.6.1, 4.1)",
        "distance": 19307
      },
      {
        "edge": "(2.7.1, 1.1)",
        "distance": 35357
      },
      {
        "edge": "(2.7.1, 2.1)",
        "distance": 28917
      },
      {
        "edge": "(2.7.1, 3.1)",
        "distance": 22531
      },
      {
        "edge": "(2.7.1, 4.1)",
        "distance": 8973
      },
      {
        "edge": "(1.1, 0.0.0)",
        "distance": 7523
      },
      {
        "edge": "(1.1, 1.1.1)",
        "distance": 9293
      },
      {
        "edge": "(1.1, 1.2.1)",
        "distance": 19043
      },
      {
        "edge": "(1.1, 1.3.1)",
        "distance": 22267
      },
      {
        "edge": "(1.1, 1.4.1)",
        "distance": 25481
      },
      {
        "edge": "(1.1, 1.5.1)",
        "distance": 28653
      },
      {
        "edge": "(1.1, 1.6.1)",
        "distance": 31852
      },
      {
        "edge": "(1.1, 1.7.1)",
        "distance": 35093
      },
      {
        "edge": "(1.1, 2.1.1)",
        "distance": 8945
      },
      {
        "edge": "(1.1, 2.2.1)",
        "distance": 19307
      },
      {
        "edge": "(1.1, 2.3.1)",
        "distance": 22531
      },
      {
        "edge": "(1.1, 2.4.1)",
        "distance": 25745
      },
      {
        "edge": "(1.1, 2.5.1)",
        "distance": 28917
      },
      {
        "edge": "(1.1, 2.6.1)",
        "distance": 32116
      },
      {
        "edge": "(1.1, 2.7.1)",
        "distance": 35357
      },
      {
        "edge": "(2.1, 0.0.0)",
        "distance": 14752
      },
      {
        "edge": "(2.1, 1.1.1)",
        "distance": 22267
      },
      {
        "edge": "(2.1, 1.2.1)",
        "distance": 19043
      },
      {
        "edge": "(2.1, 1.3.1)",
        "distance": 9293
      },
      {
        "edge": "(2.1, 1.4.1)",
        "distance": 19043
      },
      {
        "edge": "(2.1, 1.5.1)",
        "distance": 22267
      },
      {
        "edge": "(2.1, 1.6.1)",
        "distance": 25481
      },
      {
        "edge": "(2.1, 1.7.1)",
        "distance": 28653
      },
      {
        "edge": "(2.1, 2.1.1)",
        "distance": 22531
      },
      {
        "edge": "(2.1, 2.2.1)",
        "distance": 19307
      },
      {
        "edge": "(2.1, 2.3.1)",
        "distance": 8945
      },
      {
        "edge": "(2.1, 2.4.1)",
        "distance": 19307
      },
      {
        "edge": "(2.1, 2.5.1)",
        "distance": 22531
      },
      {
        "edge": "(2.1, 2.6.1)",
        "distance": 25745
      },
      {
        "edge": "(2.1, 2.7.1)",
        "distance": 28917
      },
      {
        "edge": "(3.1, 0.0.0)",
        "distance": 21138
      },
      {
        "edge": "(3.1, 1.1.1)",
        "distance": 28653
      },
      {
        "edge": "(3.1, 1.2.1)",
        "distance": 25481
      },
      {
        "edge": "(3.1, 1.3.1)",
        "distance": 22267
      },
      {
        "edge": "(3.1, 1.4.1)",
        "distance": 19043
      },
      {
        "edge": "(3.1, 1.5.1)",
        "distance": 9293
      },
      {
        "edge": "(3.1, 1.6.1)",
        "distance": 19043
      },
      {
        "edge": "(3.1, 1.7.1)",
        "distance": 22267
      },
      {
        "edge": "(3.1, 2.1.1)",
        "distance": 28917
      },
      {
        "edge": "(3.1, 2.2.1)",
        "distance": 25745
      },
      {
        "edge": "(3.1, 2.3.1)",
        "distance": 22531
      },
      {
        "edge": "(3.1, 2.4.1)",
        "distance": 19307
      },
      {
        "edge": "(3.1, 2.5.1)",
        "distance": 8945
      },
      {
        "edge": "(3.1, 2.6.1)",
        "distance": 19307
      },
      {
        "edge": "(3.1, 2.7.1)",
        "distance": 22531
      },
      {
        "edge": "(4.1, 0.0.0)",
        "distance": 27578
      },
      {
        "edge": "(4.1, 1.1.1)",
        "distance": 35093
      },
      {
        "edge": "(4.1, 1.2.1)",
        "distance": 31852
      },
      {
        "edge": "(4.1, 1.3.1)",
        "distance": 28653
      },
      {
        "edge": "(4.1, 1.4.1)",
        "distance": 25481
      },
      {
        "edge": "(4.1, 1.5.1)",
        "distance": 22267
      },
      {
        "edge": "(4.1, 1.6.1)",
        "distance": 19043
      },
      {
        "edge": "(4.1, 1.7.1)",
        "distance": 9293
      },
      {
        "edge": "(4.1, 2.1.1)",
        "distance": 35357
      },
      {
        "edge": "(4.1, 2.2.1)",
        "distance": 32116
      },
      {
        "edge": "(4.1, 2.3.1)",
        "distance": 28917
      },
      {
        "edge": "(4.1, 2.4.1)",
        "distance": 25745
      },
      {
        "edge": "(4.1, 2.5.1)",
        "distance": 22531
      },
      {
        "edge": "(4.1, 2.6.1)",
        "distance": 19307
      },
      {
        "edge": "(4.1, 2.7.1)",
        "distance": 8945
      }
    ]

nested = {}
for entry in distance_matrix:
    # Strip parentheses and split by comma
    node_a, node_b = [s.strip().strip("()") for s in entry["edge"].split(",")]
    dist = entry["distance"]

    # Insert into nested dict
    if node_a not in nested:
        nested[node_a] = {}
    nested[node_a][node_b] = dist

# Print the result
print(json.dumps(nested, indent=4))
