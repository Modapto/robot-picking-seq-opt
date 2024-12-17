# Containers dictionary
from scipy.spatial import distance_matrix
#random positioning of containers
containers = {
    "Container_1": {"gr_position": "1.1","contents" : [{"position":"1.1.1","type":"Component_1"},
                                                       {"position":"1.1.2","type":"Component_1"},
                                                       {"position":"1.1.3","type":"Component_1"},
                                                       {"position":"1.1.4","type":"Component_1"}]},
    "Container_2": {"gr_position": "1.2","contents" : [{"position":"1.2.1","type":"Component_2"},
                                                       {"position":"1.2.2","type":"Component_2"},
                                                       {"position":"1.2.3","type":"Component_2"},
                                                       {"position":"1.2.4","type":"Component_2"}]},
    "Container_3": {"gr_position": "1.3", "contents": [{"position": "1.3.1", "type": "Component_3"},
                                                       {"position": "1.3.2", "type": "Component_3"},
                                                       {"position": "1.3.3", "type": "Component_3"},
                                                       {"position": "1.3.4", "type": "Component_3"}]},
    "Container_4": {"gr_position": "1.4", "contents": [{"position": "1.4.1", "type": "Component_4"},
                                                       {"position": "1.4.2", "type": "Component_4"},
                                                       {"position": "1.4.3", "type": "Component_4"},
                                                       {"position": "1.4.4", "type": "Component_4"}]},
    "Container_5": {"gr_position": "1.5", "contents": [{"position": "1.5.1", "type": "Component_5"},
                                                       {"position": "1.5.2", "type": "Component_5"},
                                                       {"position": "1.5.3", "type": "Component_5"},
                                                       {"position": "1.5.4", "type": "Component_5"}]},
    "Container_6": {"gr_position": "1.6", "contents": [{"position": "1.6.1", "type": "Component_7"},
                                                       {"position": "1.6.2", "type": "Component_7"},
                                                       {"position": "1.6.3", "type": "Component_7"},
                                                       {"position": "1.6.4", "type": "Component_7"}]},
    "Container_7": {"gr_position": "1.7", "contents": [{"position": "1.7.1", "type": "Component_9"},
                                                       {"position": "1.7.2", "type": "Component_9"},
                                                       {"position": "1.7.3", "type": "Component_9"},
                                                       {"position": "1.7.4", "type": "Component_9"}]},
    "Container_8": {"gr_position": "1.8", "contents": [{"position": "2.1.1", "type": "Component_10"},
                                                       {"position": "2.1.2", "type": "Component_10"},
                                                       {"position": "2.1.3", "type": "Component_10"},
                                                       {"position": "2.1.4", "type": "Component_10"}]},
    "Container_9": {"gr_position": "1.9", "contents": [{"position": "2.2.1", "type": "Component_11"},
                                                       {"position": "2.2.2", "type": "Component_11"},
                                                       {"position": "2.2.3", "type": "Component_11"},
                                                       {"position": "2.2.4", "type": "Component_11"}]},
    "Container_10": {"gr_position": "1.10", "contents": [{"position": "2.3.1", "type": "Component_12"},
                                                       {"position": "2.3.2", "type": "Component_12"},
                                                       {"position": "2.3.3", "type": "Component_12"},
                                                       {"position": "2.3.4", "type": "Component_12"}]},
    "Container_11": {"gr_position": "1.11", "contents": [{"position": "2.4.1", "type": "Component_13"},
                                                       {"position": "2.4.2", "type": "Component_13"},
                                                       {"position": "2.4.3", "type": "Component_13"},
                                                       {"position": "2.4.4", "type": "Component_13"}]},
    "Container_12": {"gr_position": "1.12", "contents": [{"position": "2.5.1", "type": "Component_14"},
                                                       {"position": "2.5.2", "type": "Component_14"},
                                                       {"position": "2.5.3", "type": "Component_14"},
                                                       {"position": "2.5.4", "type": "Component_14"}]},
    "Container_13": {"gr_position": "1.13", "contents": [{"position": "2.6.1", "type": "Component_15"},
                                                       {"position": "2.6.2", "type": "Component_15"},
                                                       {"position": "2.6.3", "type": "Component_15"},
                                                       {"position": "2.6.4", "type": "Component_15"}]},
    "Container_14": {"gr_position": "1.14", "contents": [{"position": "2.7.1", "type": "Component_16"},
                                                       {"position": "2.7.2", "type": "Component_16"},
                                                       {"position": "2.7.3", "type": "Component_16"},
                                                       {"position": "2.7.4", "type": "Component_16"}]}
}
#random selection and positioning of kitholders
# Kit Holders dictionary
kit_holders = {
    "KH001": {"kh_position": "1",
              "contents": [{"position": "1.1", "type": "Component_5"},
                           {"position": "1.2", "type": "Component_15"},
                           {"position": "1.3", "type": "Component_3"},
                           {"position": "1.4", "type": "Component_16"},
                           {"position": "1.5", "type": "Component_14"},
                           {"position": "1.6", "type": "Component_11"}]},
    "KH002": {"kh_position": "2",
              "contents": [{"position": "2.1", "type": "Component_4"},
                           {"position": "2.2", "type": "Component_2"},
                           {"position": "2.3", "type": "Component_12"},
                           {"position": "2.4", "type": "Component_10"}]},
    "KH003": {"kh_position": "3",
              "contents": [{"position": "3.1", "type": "Component_9"},
                           {"position": "3.2", "type": "Component_13"},
                           {"position": "3.3", "type": "Component_1"},
                           {"position": "3.4", "type": "Component_7"},
                           {"position": "3.5", "type": "Component_10"}]},
    "KH004": {"kh_position": "4",
              "contents": [{"position": "4.1", "type": "Component_5"},
                           {"position": "4.2", "type": "Component_15"},
                           {"position": "4.3", "type": "Component_3"},
                           {"position": "4.4", "type": "Component_16"},
                           {"position": "4.5", "type": "Component_14"},
                           {"position": "4.6", "type": "Component_11"}]},
}


distance_matrix = {
    "0.0": [
        {
            "1.1": [
                {
                    "node": "1.1.1",
                    "distance": 16776
                },
                {
                    "node": "1.1.2",
                    "distance": 16776
                },
                {
                    "node": "1.1.3",
                    "distance": 16776
                },
                {
                    "node": "1.1.4",
                    "distance": 16776
                },
                {
                    "node": "1.2.1",
                    "distance": 16776
                },
                {
                    "node": "1.2.2",
                    "distance": 16776
                },
                {
                    "node": "1.2.3",
                    "distance": 16776
                },
                {
                    "node": "1.2.4",
                    "distance": 16776
                },
                {
                    "node": "1.3.1",
                    "distance": 16776
                },
                {
                    "node": "1.3.2",
                    "distance": 16776
                },
                {
                    "node": "1.3.3",
                    "distance": 16776
                },
                {
                    "node": "1.3.4",
                    "distance": 16776
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 27230
                },
                {
                    "node": "1.5.2",
                    "distance": 27230
                },
                {
                    "node": "1.5.3",
                    "distance": 27230
                },
                {
                    "node": "1.5.4",
                    "distance": 27230
                },
                {
                    "node": "1.6.1",
                    "distance": 33628
                },
                {
                    "node": "1.6.2",
                    "distance": 33628
                },
                {
                    "node": "1.6.3",
                    "distance": 33628
                },
                {
                    "node": "1.6.4",
                    "distance": 33628
                },
                {
                    "node": "1.7.1",
                    "distance": 40110
                },
                {
                    "node": "1.7.2",
                    "distance": 40110
                },
                {
                    "node": "1.7.3",
                    "distance": 40110
                },
                {
                    "node": "1.7.4",
                    "distance": 40110
                },
                {
                    "node": "2.1.1",
                    "distance": 16752
                },
                {
                    "node": "2.1.2",
                    "distance": 16752
                },
                {
                    "node": "2.1.3",
                    "distance": 16752
                },
                {
                    "node": "2.1.4",
                    "distance": 16752
                },
                {
                    "node": "2.2.1",
                    "distance": 16752
                },
                {
                    "node": "2.2.2",
                    "distance": 16752
                },
                {
                    "node": "2.2.3",
                    "distance": 16752
                },
                {
                    "node": "2.2.4",
                    "distance": 16752
                },
                {
                    "node": "2.3.1",
                    "distance": 16752
                },
                {
                    "node": "2.3.2",
                    "distance": 16752
                },
                {
                    "node": "2.3.3",
                    "distance": 16752
                },
                {
                    "node": "2.3.4",
                    "distance": 16752
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 27230
                },
                {
                    "node": "2.5.2",
                    "distance": 27230
                },
                {
                    "node": "2.5.3",
                    "distance": 27230
                },
                {
                    "node": "2.5.4",
                    "distance": 27230
                },
                {
                    "node": "2.6.1",
                    "distance": 33628
                },
                {
                    "node": "2.6.2",
                    "distance": 33628
                },
                {
                    "node": "2.6.3",
                    "distance": 33628
                },
                {
                    "node": "2.6.4",
                    "distance": 33628
                },
                {
                    "node": "2.7.1",
                    "distance": 40110
                },
                {
                    "node": "2.7.2",
                    "distance": 40110
                },
                {
                    "node": "2.7.3",
                    "distance": 40110
                },
                {
                    "node": "2.7.4",
                    "distance": 40110
                }
            ]
        },
        {
            "1.2": [
                {
                    "node": "1.1.1",
                    "distance": 16776
                },
                {
                    "node": "1.1.2",
                    "distance": 16776
                },
                {
                    "node": "1.1.3",
                    "distance": 16776
                },
                {
                    "node": "1.1.4",
                    "distance": 16776
                },
                {
                    "node": "1.2.1",
                    "distance": 16776
                },
                {
                    "node": "1.2.2",
                    "distance": 16776
                },
                {
                    "node": "1.2.3",
                    "distance": 16776
                },
                {
                    "node": "1.2.4",
                    "distance": 16776
                },
                {
                    "node": "1.3.1",
                    "distance": 16776
                },
                {
                    "node": "1.3.2",
                    "distance": 16776
                },
                {
                    "node": "1.3.3",
                    "distance": 16776
                },
                {
                    "node": "1.3.4",
                    "distance": 16776
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 27230
                },
                {
                    "node": "1.5.2",
                    "distance": 27230
                },
                {
                    "node": "1.5.3",
                    "distance": 27230
                },
                {
                    "node": "1.5.4",
                    "distance": 27230
                },
                {
                    "node": "1.6.1",
                    "distance": 33628
                },
                {
                    "node": "1.6.2",
                    "distance": 33628
                },
                {
                    "node": "1.6.3",
                    "distance": 33628
                },
                {
                    "node": "1.6.4",
                    "distance": 33628
                },
                {
                    "node": "1.7.1",
                    "distance": 40110
                },
                {
                    "node": "1.7.2",
                    "distance": 40110
                },
                {
                    "node": "1.7.3",
                    "distance": 40110
                },
                {
                    "node": "1.7.4",
                    "distance": 40110
                },
                {
                    "node": "2.1.1",
                    "distance": 16752
                },
                {
                    "node": "2.1.2",
                    "distance": 16752
                },
                {
                    "node": "2.1.3",
                    "distance": 16752
                },
                {
                    "node": "2.1.4",
                    "distance": 16752
                },
                {
                    "node": "2.2.1",
                    "distance": 16752
                },
                {
                    "node": "2.2.2",
                    "distance": 16752
                },
                {
                    "node": "2.2.3",
                    "distance": 16752
                },
                {
                    "node": "2.2.4",
                    "distance": 16752
                },
                {
                    "node": "2.3.1",
                    "distance": 16752
                },
                {
                    "node": "2.3.2",
                    "distance": 16752
                },
                {
                    "node": "2.3.3",
                    "distance": 16752
                },
                {
                    "node": "2.3.4",
                    "distance": 16752
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 27230
                },
                {
                    "node": "2.5.2",
                    "distance": 27230
                },
                {
                    "node": "2.5.3",
                    "distance": 27230
                },
                {
                    "node": "2.5.4",
                    "distance": 27230
                },
                {
                    "node": "2.6.1",
                    "distance": 33628
                },
                {
                    "node": "2.6.2",
                    "distance": 33628
                },
                {
                    "node": "2.6.3",
                    "distance": 33628
                },
                {
                    "node": "2.6.4",
                    "distance": 33628
                },
                {
                    "node": "2.7.1",
                    "distance": 40110
                },
                {
                    "node": "2.7.2",
                    "distance": 40110
                },
                {
                    "node": "2.7.3",
                    "distance": 40110
                },
                {
                    "node": "2.7.4",
                    "distance": 40110
                }
            ]
        },
        {
            "1.3": [
                {
                    "node": "1.1.1",
                    "distance": 16776
                },
                {
                    "node": "1.1.2",
                    "distance": 16776
                },
                {
                    "node": "1.1.3",
                    "distance": 16776
                },
                {
                    "node": "1.1.4",
                    "distance": 16776
                },
                {
                    "node": "1.2.1",
                    "distance": 16776
                },
                {
                    "node": "1.2.2",
                    "distance": 16776
                },
                {
                    "node": "1.2.3",
                    "distance": 16776
                },
                {
                    "node": "1.2.4",
                    "distance": 16776
                },
                {
                    "node": "1.3.1",
                    "distance": 16776
                },
                {
                    "node": "1.3.2",
                    "distance": 16776
                },
                {
                    "node": "1.3.3",
                    "distance": 16776
                },
                {
                    "node": "1.3.4",
                    "distance": 16776
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 27230
                },
                {
                    "node": "1.5.2",
                    "distance": 27230
                },
                {
                    "node": "1.5.3",
                    "distance": 27230
                },
                {
                    "node": "1.5.4",
                    "distance": 27230
                },
                {
                    "node": "1.6.1",
                    "distance": 33628
                },
                {
                    "node": "1.6.2",
                    "distance": 33628
                },
                {
                    "node": "1.6.3",
                    "distance": 33628
                },
                {
                    "node": "1.6.4",
                    "distance": 33628
                },
                {
                    "node": "1.7.1",
                    "distance": 40110
                },
                {
                    "node": "1.7.2",
                    "distance": 40110
                },
                {
                    "node": "1.7.3",
                    "distance": 40110
                },
                {
                    "node": "1.7.4",
                    "distance": 40110
                },
                {
                    "node": "2.1.1",
                    "distance": 16752
                },
                {
                    "node": "2.1.2",
                    "distance": 16752
                },
                {
                    "node": "2.1.3",
                    "distance": 16752
                },
                {
                    "node": "2.1.4",
                    "distance": 16752
                },
                {
                    "node": "2.2.1",
                    "distance": 16752
                },
                {
                    "node": "2.2.2",
                    "distance": 16752
                },
                {
                    "node": "2.2.3",
                    "distance": 16752
                },
                {
                    "node": "2.2.4",
                    "distance": 16752
                },
                {
                    "node": "2.3.1",
                    "distance": 16752
                },
                {
                    "node": "2.3.2",
                    "distance": 16752
                },
                {
                    "node": "2.3.3",
                    "distance": 16752
                },
                {
                    "node": "2.3.4",
                    "distance": 16752
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 27230
                },
                {
                    "node": "2.5.2",
                    "distance": 27230
                },
                {
                    "node": "2.5.3",
                    "distance": 27230
                },
                {
                    "node": "2.5.4",
                    "distance": 27230
                },
                {
                    "node": "2.6.1",
                    "distance": 33628
                },
                {
                    "node": "2.6.2",
                    "distance": 33628
                },
                {
                    "node": "2.6.3",
                    "distance": 33628
                },
                {
                    "node": "2.6.4",
                    "distance": 33628
                },
                {
                    "node": "2.7.1",
                    "distance": 40110
                },
                {
                    "node": "2.7.2",
                    "distance": 40110
                },
                {
                    "node": "2.7.3",
                    "distance": 40110
                },
                {
                    "node": "2.7.4",
                    "distance": 40110
                }
            ]
        },
        {
            "1.4": [
                {
                    "node": "1.1.1",
                    "distance": 16776
                },
                {
                    "node": "1.1.2",
                    "distance": 16776
                },
                {
                    "node": "1.1.3",
                    "distance": 16776
                },
                {
                    "node": "1.1.4",
                    "distance": 16776
                },
                {
                    "node": "1.2.1",
                    "distance": 16776
                },
                {
                    "node": "1.2.2",
                    "distance": 16776
                },
                {
                    "node": "1.2.3",
                    "distance": 16776
                },
                {
                    "node": "1.2.4",
                    "distance": 16776
                },
                {
                    "node": "1.3.1",
                    "distance": 16776
                },
                {
                    "node": "1.3.2",
                    "distance": 16776
                },
                {
                    "node": "1.3.3",
                    "distance": 16776
                },
                {
                    "node": "1.3.4",
                    "distance": 16776
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 27230
                },
                {
                    "node": "1.5.2",
                    "distance": 27230
                },
                {
                    "node": "1.5.3",
                    "distance": 27230
                },
                {
                    "node": "1.5.4",
                    "distance": 27230
                },
                {
                    "node": "1.6.1",
                    "distance": 33628
                },
                {
                    "node": "1.6.2",
                    "distance": 33628
                },
                {
                    "node": "1.6.3",
                    "distance": 33628
                },
                {
                    "node": "1.6.4",
                    "distance": 33628
                },
                {
                    "node": "1.7.1",
                    "distance": 40110
                },
                {
                    "node": "1.7.2",
                    "distance": 40110
                },
                {
                    "node": "1.7.3",
                    "distance": 40110
                },
                {
                    "node": "1.7.4",
                    "distance": 40110
                },
                {
                    "node": "2.1.1",
                    "distance": 16752
                },
                {
                    "node": "2.1.2",
                    "distance": 16752
                },
                {
                    "node": "2.1.3",
                    "distance": 16752
                },
                {
                    "node": "2.1.4",
                    "distance": 16752
                },
                {
                    "node": "2.2.1",
                    "distance": 16752
                },
                {
                    "node": "2.2.2",
                    "distance": 16752
                },
                {
                    "node": "2.2.3",
                    "distance": 16752
                },
                {
                    "node": "2.2.4",
                    "distance": 16752
                },
                {
                    "node": "2.3.1",
                    "distance": 16752
                },
                {
                    "node": "2.3.2",
                    "distance": 16752
                },
                {
                    "node": "2.3.3",
                    "distance": 16752
                },
                {
                    "node": "2.3.4",
                    "distance": 16752
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 27230
                },
                {
                    "node": "2.5.2",
                    "distance": 27230
                },
                {
                    "node": "2.5.3",
                    "distance": 27230
                },
                {
                    "node": "2.5.4",
                    "distance": 27230
                },
                {
                    "node": "2.6.1",
                    "distance": 33628
                },
                {
                    "node": "2.6.2",
                    "distance": 33628
                },
                {
                    "node": "2.6.3",
                    "distance": 33628
                },
                {
                    "node": "2.6.4",
                    "distance": 33628
                },
                {
                    "node": "2.7.1",
                    "distance": 40110
                },
                {
                    "node": "2.7.2",
                    "distance": 40110
                },
                {
                    "node": "2.7.3",
                    "distance": 40110
                },
                {
                    "node": "2.7.4",
                    "distance": 40110
                }
            ]
        },
        {
            "1.5": [
                {
                    "node": "1.1.1",
                    "distance": 16776
                },
                {
                    "node": "1.1.2",
                    "distance": 16776
                },
                {
                    "node": "1.1.3",
                    "distance": 16776
                },
                {
                    "node": "1.1.4",
                    "distance": 16776
                },
                {
                    "node": "1.2.1",
                    "distance": 16776
                },
                {
                    "node": "1.2.2",
                    "distance": 16776
                },
                {
                    "node": "1.2.3",
                    "distance": 16776
                },
                {
                    "node": "1.2.4",
                    "distance": 16776
                },
                {
                    "node": "1.3.1",
                    "distance": 16776
                },
                {
                    "node": "1.3.2",
                    "distance": 16776
                },
                {
                    "node": "1.3.3",
                    "distance": 16776
                },
                {
                    "node": "1.3.4",
                    "distance": 16776
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 27230
                },
                {
                    "node": "1.5.2",
                    "distance": 27230
                },
                {
                    "node": "1.5.3",
                    "distance": 27230
                },
                {
                    "node": "1.5.4",
                    "distance": 27230
                },
                {
                    "node": "1.6.1",
                    "distance": 33628
                },
                {
                    "node": "1.6.2",
                    "distance": 33628
                },
                {
                    "node": "1.6.3",
                    "distance": 33628
                },
                {
                    "node": "1.6.4",
                    "distance": 33628
                },
                {
                    "node": "1.7.1",
                    "distance": 40110
                },
                {
                    "node": "1.7.2",
                    "distance": 40110
                },
                {
                    "node": "1.7.3",
                    "distance": 40110
                },
                {
                    "node": "1.7.4",
                    "distance": 40110
                },
                {
                    "node": "2.1.1",
                    "distance": 16752
                },
                {
                    "node": "2.1.2",
                    "distance": 16752
                },
                {
                    "node": "2.1.3",
                    "distance": 16752
                },
                {
                    "node": "2.1.4",
                    "distance": 16752
                },
                {
                    "node": "2.2.1",
                    "distance": 16752
                },
                {
                    "node": "2.2.2",
                    "distance": 16752
                },
                {
                    "node": "2.2.3",
                    "distance": 16752
                },
                {
                    "node": "2.2.4",
                    "distance": 16752
                },
                {
                    "node": "2.3.1",
                    "distance": 16752
                },
                {
                    "node": "2.3.2",
                    "distance": 16752
                },
                {
                    "node": "2.3.3",
                    "distance": 16752
                },
                {
                    "node": "2.3.4",
                    "distance": 16752
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 27230
                },
                {
                    "node": "2.5.2",
                    "distance": 27230
                },
                {
                    "node": "2.5.3",
                    "distance": 27230
                },
                {
                    "node": "2.5.4",
                    "distance": 27230
                },
                {
                    "node": "2.6.1",
                    "distance": 33628
                },
                {
                    "node": "2.6.2",
                    "distance": 33628
                },
                {
                    "node": "2.6.3",
                    "distance": 33628
                },
                {
                    "node": "2.6.4",
                    "distance": 33628
                },
                {
                    "node": "2.7.1",
                    "distance": 40110
                },
                {
                    "node": "2.7.2",
                    "distance": 40110
                },
                {
                    "node": "2.7.3",
                    "distance": 40110
                },
                {
                    "node": "2.7.4",
                    "distance": 40110
                }
            ]
        },
        {
            "1.6": [
                {
                    "node": "1.1.1",
                    "distance": 16776
                },
                {
                    "node": "1.1.2",
                    "distance": 16776
                },
                {
                    "node": "1.1.3",
                    "distance": 16776
                },
                {
                    "node": "1.1.4",
                    "distance": 16776
                },
                {
                    "node": "1.2.1",
                    "distance": 16776
                },
                {
                    "node": "1.2.2",
                    "distance": 16776
                },
                {
                    "node": "1.2.3",
                    "distance": 16776
                },
                {
                    "node": "1.2.4",
                    "distance": 16776
                },
                {
                    "node": "1.3.1",
                    "distance": 16776
                },
                {
                    "node": "1.3.2",
                    "distance": 16776
                },
                {
                    "node": "1.3.3",
                    "distance": 16776
                },
                {
                    "node": "1.3.4",
                    "distance": 16776
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 27230
                },
                {
                    "node": "1.5.2",
                    "distance": 27230
                },
                {
                    "node": "1.5.3",
                    "distance": 27230
                },
                {
                    "node": "1.5.4",
                    "distance": 27230
                },
                {
                    "node": "1.6.1",
                    "distance": 33628
                },
                {
                    "node": "1.6.2",
                    "distance": 33628
                },
                {
                    "node": "1.6.3",
                    "distance": 33628
                },
                {
                    "node": "1.6.4",
                    "distance": 33628
                },
                {
                    "node": "1.7.1",
                    "distance": 40110
                },
                {
                    "node": "1.7.2",
                    "distance": 40110
                },
                {
                    "node": "1.7.3",
                    "distance": 40110
                },
                {
                    "node": "1.7.4",
                    "distance": 40110
                },
                {
                    "node": "2.1.1",
                    "distance": 16752
                },
                {
                    "node": "2.1.2",
                    "distance": 16752
                },
                {
                    "node": "2.1.3",
                    "distance": 16752
                },
                {
                    "node": "2.1.4",
                    "distance": 16752
                },
                {
                    "node": "2.2.1",
                    "distance": 16752
                },
                {
                    "node": "2.2.2",
                    "distance": 16752
                },
                {
                    "node": "2.2.3",
                    "distance": 16752
                },
                {
                    "node": "2.2.4",
                    "distance": 16752
                },
                {
                    "node": "2.3.1",
                    "distance": 16752
                },
                {
                    "node": "2.3.2",
                    "distance": 16752
                },
                {
                    "node": "2.3.3",
                    "distance": 16752
                },
                {
                    "node": "2.3.4",
                    "distance": 16752
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 27230
                },
                {
                    "node": "2.5.2",
                    "distance": 27230
                },
                {
                    "node": "2.5.3",
                    "distance": 27230
                },
                {
                    "node": "2.5.4",
                    "distance": 27230
                },
                {
                    "node": "2.6.1",
                    "distance": 33628
                },
                {
                    "node": "2.6.2",
                    "distance": 33628
                },
                {
                    "node": "2.6.3",
                    "distance": 33628
                },
                {
                    "node": "2.6.4",
                    "distance": 33628
                },
                {
                    "node": "2.7.1",
                    "distance": 40110
                },
                {
                    "node": "2.7.2",
                    "distance": 40110
                },
                {
                    "node": "2.7.3",
                    "distance": 40110
                },
                {
                    "node": "2.7.4",
                    "distance": 40110
                }
            ]
        },
        {
            "2.1": [
                {
                    "node": "1.1.1",
                    "distance": 16776
                },
                {
                    "node": "1.1.2",
                    "distance": 16776
                },
                {
                    "node": "1.1.3",
                    "distance": 16776
                },
                {
                    "node": "1.1.4",
                    "distance": 16776
                },
                {
                    "node": "1.2.1",
                    "distance": 16776
                },
                {
                    "node": "1.2.2",
                    "distance": 16776
                },
                {
                    "node": "1.2.3",
                    "distance": 16776
                },
                {
                    "node": "1.2.4",
                    "distance": 16776
                },
                {
                    "node": "1.3.1",
                    "distance": 16776
                },
                {
                    "node": "1.3.2",
                    "distance": 16776
                },
                {
                    "node": "1.3.3",
                    "distance": 16776
                },
                {
                    "node": "1.3.4",
                    "distance": 16776
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 27257
                },
                {
                    "node": "1.6.2",
                    "distance": 27257
                },
                {
                    "node": "1.6.3",
                    "distance": 27257
                },
                {
                    "node": "1.6.4",
                    "distance": 27257
                },
                {
                    "node": "1.7.1",
                    "distance": 33670
                },
                {
                    "node": "1.7.2",
                    "distance": 33670
                },
                {
                    "node": "1.7.3",
                    "distance": 33670
                },
                {
                    "node": "1.7.4",
                    "distance": 33670
                },
                {
                    "node": "2.1.1",
                    "distance": 16752
                },
                {
                    "node": "2.1.2",
                    "distance": 16752
                },
                {
                    "node": "2.1.3",
                    "distance": 16752
                },
                {
                    "node": "2.1.4",
                    "distance": 16752
                },
                {
                    "node": "2.2.1",
                    "distance": 16752
                },
                {
                    "node": "2.2.2",
                    "distance": 16752
                },
                {
                    "node": "2.2.3",
                    "distance": 16752
                },
                {
                    "node": "2.2.4",
                    "distance": 16752
                },
                {
                    "node": "2.3.1",
                    "distance": 16752
                },
                {
                    "node": "2.3.2",
                    "distance": 16752
                },
                {
                    "node": "2.3.3",
                    "distance": 16752
                },
                {
                    "node": "2.3.4",
                    "distance": 16752
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 27257
                },
                {
                    "node": "2.6.2",
                    "distance": 27257
                },
                {
                    "node": "2.6.3",
                    "distance": 27257
                },
                {
                    "node": "2.6.4",
                    "distance": 27257
                },
                {
                    "node": "2.7.1",
                    "distance": 33670
                },
                {
                    "node": "2.7.2",
                    "distance": 33670
                },
                {
                    "node": "2.7.3",
                    "distance": 33670
                },
                {
                    "node": "2.7.4",
                    "distance": 33670
                }
            ]
        },
        {
            "2.2": [
                {
                    "node": "1.1.1",
                    "distance": 16776
                },
                {
                    "node": "1.1.2",
                    "distance": 16776
                },
                {
                    "node": "1.1.3",
                    "distance": 16776
                },
                {
                    "node": "1.1.4",
                    "distance": 16776
                },
                {
                    "node": "1.2.1",
                    "distance": 16776
                },
                {
                    "node": "1.2.2",
                    "distance": 16776
                },
                {
                    "node": "1.2.3",
                    "distance": 16776
                },
                {
                    "node": "1.2.4",
                    "distance": 16776
                },
                {
                    "node": "1.3.1",
                    "distance": 16776
                },
                {
                    "node": "1.3.2",
                    "distance": 16776
                },
                {
                    "node": "1.3.3",
                    "distance": 16776
                },
                {
                    "node": "1.3.4",
                    "distance": 16776
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 27257
                },
                {
                    "node": "1.6.2",
                    "distance": 27257
                },
                {
                    "node": "1.6.3",
                    "distance": 27257
                },
                {
                    "node": "1.6.4",
                    "distance": 27257
                },
                {
                    "node": "1.7.1",
                    "distance": 33670
                },
                {
                    "node": "1.7.2",
                    "distance": 33670
                },
                {
                    "node": "1.7.3",
                    "distance": 33670
                },
                {
                    "node": "1.7.4",
                    "distance": 33670
                },
                {
                    "node": "2.1.1",
                    "distance": 16752
                },
                {
                    "node": "2.1.2",
                    "distance": 16752
                },
                {
                    "node": "2.1.3",
                    "distance": 16752
                },
                {
                    "node": "2.1.4",
                    "distance": 16752
                },
                {
                    "node": "2.2.1",
                    "distance": 16752
                },
                {
                    "node": "2.2.2",
                    "distance": 16752
                },
                {
                    "node": "2.2.3",
                    "distance": 16752
                },
                {
                    "node": "2.2.4",
                    "distance": 16752
                },
                {
                    "node": "2.3.1",
                    "distance": 16752
                },
                {
                    "node": "2.3.2",
                    "distance": 16752
                },
                {
                    "node": "2.3.3",
                    "distance": 16752
                },
                {
                    "node": "2.3.4",
                    "distance": 16752
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 27257
                },
                {
                    "node": "2.6.2",
                    "distance": 27257
                },
                {
                    "node": "2.6.3",
                    "distance": 27257
                },
                {
                    "node": "2.6.4",
                    "distance": 27257
                },
                {
                    "node": "2.7.1",
                    "distance": 33670
                },
                {
                    "node": "2.7.2",
                    "distance": 33670
                },
                {
                    "node": "2.7.3",
                    "distance": 33670
                },
                {
                    "node": "2.7.4",
                    "distance": 33670
                }
            ]
        },
        {
            "2.3": [
                {
                    "node": "1.1.1",
                    "distance": 16776
                },
                {
                    "node": "1.1.2",
                    "distance": 16776
                },
                {
                    "node": "1.1.3",
                    "distance": 16776
                },
                {
                    "node": "1.1.4",
                    "distance": 16776
                },
                {
                    "node": "1.2.1",
                    "distance": 16776
                },
                {
                    "node": "1.2.2",
                    "distance": 16776
                },
                {
                    "node": "1.2.3",
                    "distance": 16776
                },
                {
                    "node": "1.2.4",
                    "distance": 16776
                },
                {
                    "node": "1.3.1",
                    "distance": 16776
                },
                {
                    "node": "1.3.2",
                    "distance": 16776
                },
                {
                    "node": "1.3.3",
                    "distance": 16776
                },
                {
                    "node": "1.3.4",
                    "distance": 16776
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 27257
                },
                {
                    "node": "1.6.2",
                    "distance": 27257
                },
                {
                    "node": "1.6.3",
                    "distance": 27257
                },
                {
                    "node": "1.6.4",
                    "distance": 27257
                },
                {
                    "node": "1.7.1",
                    "distance": 33670
                },
                {
                    "node": "1.7.2",
                    "distance": 33670
                },
                {
                    "node": "1.7.3",
                    "distance": 33670
                },
                {
                    "node": "1.7.4",
                    "distance": 33670
                },
                {
                    "node": "2.1.1",
                    "distance": 16752
                },
                {
                    "node": "2.1.2",
                    "distance": 16752
                },
                {
                    "node": "2.1.3",
                    "distance": 16752
                },
                {
                    "node": "2.1.4",
                    "distance": 16752
                },
                {
                    "node": "2.2.1",
                    "distance": 16752
                },
                {
                    "node": "2.2.2",
                    "distance": 16752
                },
                {
                    "node": "2.2.3",
                    "distance": 16752
                },
                {
                    "node": "2.2.4",
                    "distance": 16752
                },
                {
                    "node": "2.3.1",
                    "distance": 16752
                },
                {
                    "node": "2.3.2",
                    "distance": 16752
                },
                {
                    "node": "2.3.3",
                    "distance": 16752
                },
                {
                    "node": "2.3.4",
                    "distance": 16752
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 27257
                },
                {
                    "node": "2.6.2",
                    "distance": 27257
                },
                {
                    "node": "2.6.3",
                    "distance": 27257
                },
                {
                    "node": "2.6.4",
                    "distance": 27257
                },
                {
                    "node": "2.7.1",
                    "distance": 33670
                },
                {
                    "node": "2.7.2",
                    "distance": 33670
                },
                {
                    "node": "2.7.3",
                    "distance": 33670
                },
                {
                    "node": "2.7.4",
                    "distance": 33670
                }
            ]
        },
        {
            "2.4": [
                {
                    "node": "1.1.1",
                    "distance": 16776
                },
                {
                    "node": "1.1.2",
                    "distance": 16776
                },
                {
                    "node": "1.1.3",
                    "distance": 16776
                },
                {
                    "node": "1.1.4",
                    "distance": 16776
                },
                {
                    "node": "1.2.1",
                    "distance": 16776
                },
                {
                    "node": "1.2.2",
                    "distance": 16776
                },
                {
                    "node": "1.2.3",
                    "distance": 16776
                },
                {
                    "node": "1.2.4",
                    "distance": 16776
                },
                {
                    "node": "1.3.1",
                    "distance": 16776
                },
                {
                    "node": "1.3.2",
                    "distance": 16776
                },
                {
                    "node": "1.3.3",
                    "distance": 16776
                },
                {
                    "node": "1.3.4",
                    "distance": 16776
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 27257
                },
                {
                    "node": "1.6.2",
                    "distance": 27257
                },
                {
                    "node": "1.6.3",
                    "distance": 27257
                },
                {
                    "node": "1.6.4",
                    "distance": 27257
                },
                {
                    "node": "1.7.1",
                    "distance": 33670
                },
                {
                    "node": "1.7.2",
                    "distance": 33670
                },
                {
                    "node": "1.7.3",
                    "distance": 33670
                },
                {
                    "node": "1.7.4",
                    "distance": 33670
                },
                {
                    "node": "2.1.1",
                    "distance": 16752
                },
                {
                    "node": "2.1.2",
                    "distance": 16752
                },
                {
                    "node": "2.1.3",
                    "distance": 16752
                },
                {
                    "node": "2.1.4",
                    "distance": 16752
                },
                {
                    "node": "2.2.1",
                    "distance": 16752
                },
                {
                    "node": "2.2.2",
                    "distance": 16752
                },
                {
                    "node": "2.2.3",
                    "distance": 16752
                },
                {
                    "node": "2.2.4",
                    "distance": 16752
                },
                {
                    "node": "2.3.1",
                    "distance": 16752
                },
                {
                    "node": "2.3.2",
                    "distance": 16752
                },
                {
                    "node": "2.3.3",
                    "distance": 16752
                },
                {
                    "node": "2.3.4",
                    "distance": 16752
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 27257
                },
                {
                    "node": "2.6.2",
                    "distance": 27257
                },
                {
                    "node": "2.6.3",
                    "distance": 27257
                },
                {
                    "node": "2.6.4",
                    "distance": 27257
                },
                {
                    "node": "2.7.1",
                    "distance": 33670
                },
                {
                    "node": "2.7.2",
                    "distance": 33670
                },
                {
                    "node": "2.7.3",
                    "distance": 33670
                },
                {
                    "node": "2.7.4",
                    "distance": 33670
                }
            ]
        },
        {
            "3.1": [
                {
                    "node": "1.1.1",
                    "distance": 21130
                },
                {
                    "node": "1.1.2",
                    "distance": 21130
                },
                {
                    "node": "1.1.3",
                    "distance": 21130
                },
                {
                    "node": "1.1.4",
                    "distance": 21130
                },
                {
                    "node": "1.2.1",
                    "distance": 17958
                },
                {
                    "node": "1.2.2",
                    "distance": 17958
                },
                {
                    "node": "1.2.3",
                    "distance": 17958
                },
                {
                    "node": "1.2.4",
                    "distance": 17958
                },
                {
                    "node": "1.3.1",
                    "distance": 16776
                },
                {
                    "node": "1.3.2",
                    "distance": 16776
                },
                {
                    "node": "1.3.3",
                    "distance": 16776
                },
                {
                    "node": "1.3.4",
                    "distance": 16776
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 21394
                },
                {
                    "node": "2.1.2",
                    "distance": 21394
                },
                {
                    "node": "2.1.3",
                    "distance": 21394
                },
                {
                    "node": "2.1.4",
                    "distance": 21394
                },
                {
                    "node": "2.2.1",
                    "distance": 18222
                },
                {
                    "node": "2.2.2",
                    "distance": 18222
                },
                {
                    "node": "2.2.3",
                    "distance": 18222
                },
                {
                    "node": "2.2.4",
                    "distance": 18222
                },
                {
                    "node": "2.3.1",
                    "distance": 16752
                },
                {
                    "node": "2.3.2",
                    "distance": 16752
                },
                {
                    "node": "2.3.3",
                    "distance": 16752
                },
                {
                    "node": "2.3.4",
                    "distance": 16752
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "3.2": [
                {
                    "node": "1.1.1",
                    "distance": 21130
                },
                {
                    "node": "1.1.2",
                    "distance": 21130
                },
                {
                    "node": "1.1.3",
                    "distance": 21130
                },
                {
                    "node": "1.1.4",
                    "distance": 21130
                },
                {
                    "node": "1.2.1",
                    "distance": 17958
                },
                {
                    "node": "1.2.2",
                    "distance": 17958
                },
                {
                    "node": "1.2.3",
                    "distance": 17958
                },
                {
                    "node": "1.2.4",
                    "distance": 17958
                },
                {
                    "node": "1.3.1",
                    "distance": 16776
                },
                {
                    "node": "1.3.2",
                    "distance": 16776
                },
                {
                    "node": "1.3.3",
                    "distance": 16776
                },
                {
                    "node": "1.3.4",
                    "distance": 16776
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 21394
                },
                {
                    "node": "2.1.2",
                    "distance": 21394
                },
                {
                    "node": "2.1.3",
                    "distance": 21394
                },
                {
                    "node": "2.1.4",
                    "distance": 21394
                },
                {
                    "node": "2.2.1",
                    "distance": 18222
                },
                {
                    "node": "2.2.2",
                    "distance": 18222
                },
                {
                    "node": "2.2.3",
                    "distance": 18222
                },
                {
                    "node": "2.2.4",
                    "distance": 18222
                },
                {
                    "node": "2.3.1",
                    "distance": 16752
                },
                {
                    "node": "2.3.2",
                    "distance": 16752
                },
                {
                    "node": "2.3.3",
                    "distance": 16752
                },
                {
                    "node": "2.3.4",
                    "distance": 16752
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "3.3": [
                {
                    "node": "1.1.1",
                    "distance": 21130
                },
                {
                    "node": "1.1.2",
                    "distance": 21130
                },
                {
                    "node": "1.1.3",
                    "distance": 21130
                },
                {
                    "node": "1.1.4",
                    "distance": 21130
                },
                {
                    "node": "1.2.1",
                    "distance": 17958
                },
                {
                    "node": "1.2.2",
                    "distance": 17958
                },
                {
                    "node": "1.2.3",
                    "distance": 17958
                },
                {
                    "node": "1.2.4",
                    "distance": 17958
                },
                {
                    "node": "1.3.1",
                    "distance": 16776
                },
                {
                    "node": "1.3.2",
                    "distance": 16776
                },
                {
                    "node": "1.3.3",
                    "distance": 16776
                },
                {
                    "node": "1.3.4",
                    "distance": 16776
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 21394
                },
                {
                    "node": "2.1.2",
                    "distance": 21394
                },
                {
                    "node": "2.1.3",
                    "distance": 21394
                },
                {
                    "node": "2.1.4",
                    "distance": 21394
                },
                {
                    "node": "2.2.1",
                    "distance": 18222
                },
                {
                    "node": "2.2.2",
                    "distance": 18222
                },
                {
                    "node": "2.2.3",
                    "distance": 18222
                },
                {
                    "node": "2.2.4",
                    "distance": 18222
                },
                {
                    "node": "2.3.1",
                    "distance": 16752
                },
                {
                    "node": "2.3.2",
                    "distance": 16752
                },
                {
                    "node": "2.3.3",
                    "distance": 16752
                },
                {
                    "node": "2.3.4",
                    "distance": 16752
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "3.4": [
                {
                    "node": "1.1.1",
                    "distance": 21130
                },
                {
                    "node": "1.1.2",
                    "distance": 21130
                },
                {
                    "node": "1.1.3",
                    "distance": 21130
                },
                {
                    "node": "1.1.4",
                    "distance": 21130
                },
                {
                    "node": "1.2.1",
                    "distance": 17958
                },
                {
                    "node": "1.2.2",
                    "distance": 17958
                },
                {
                    "node": "1.2.3",
                    "distance": 17958
                },
                {
                    "node": "1.2.4",
                    "distance": 17958
                },
                {
                    "node": "1.3.1",
                    "distance": 16776
                },
                {
                    "node": "1.3.2",
                    "distance": 16776
                },
                {
                    "node": "1.3.3",
                    "distance": 16776
                },
                {
                    "node": "1.3.4",
                    "distance": 16776
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 21394
                },
                {
                    "node": "2.1.2",
                    "distance": 21394
                },
                {
                    "node": "2.1.3",
                    "distance": 21394
                },
                {
                    "node": "2.1.4",
                    "distance": 21394
                },
                {
                    "node": "2.2.1",
                    "distance": 18222
                },
                {
                    "node": "2.2.2",
                    "distance": 18222
                },
                {
                    "node": "2.2.3",
                    "distance": 18222
                },
                {
                    "node": "2.2.4",
                    "distance": 18222
                },
                {
                    "node": "2.3.1",
                    "distance": 16752
                },
                {
                    "node": "2.3.2",
                    "distance": 16752
                },
                {
                    "node": "2.3.3",
                    "distance": 16752
                },
                {
                    "node": "2.3.4",
                    "distance": 16752
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "3.5": [
                {
                    "node": "1.1.1",
                    "distance": 21130
                },
                {
                    "node": "1.1.2",
                    "distance": 21130
                },
                {
                    "node": "1.1.3",
                    "distance": 21130
                },
                {
                    "node": "1.1.4",
                    "distance": 21130
                },
                {
                    "node": "1.2.1",
                    "distance": 17958
                },
                {
                    "node": "1.2.2",
                    "distance": 17958
                },
                {
                    "node": "1.2.3",
                    "distance": 17958
                },
                {
                    "node": "1.2.4",
                    "distance": 17958
                },
                {
                    "node": "1.3.1",
                    "distance": 16776
                },
                {
                    "node": "1.3.2",
                    "distance": 16776
                },
                {
                    "node": "1.3.3",
                    "distance": 16776
                },
                {
                    "node": "1.3.4",
                    "distance": 16776
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 21394
                },
                {
                    "node": "2.1.2",
                    "distance": 21394
                },
                {
                    "node": "2.1.3",
                    "distance": 21394
                },
                {
                    "node": "2.1.4",
                    "distance": 21394
                },
                {
                    "node": "2.2.1",
                    "distance": 18222
                },
                {
                    "node": "2.2.2",
                    "distance": 18222
                },
                {
                    "node": "2.2.3",
                    "distance": 18222
                },
                {
                    "node": "2.2.4",
                    "distance": 18222
                },
                {
                    "node": "2.3.1",
                    "distance": 16752
                },
                {
                    "node": "2.3.2",
                    "distance": 16752
                },
                {
                    "node": "2.3.3",
                    "distance": 16752
                },
                {
                    "node": "2.3.4",
                    "distance": 16752
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "4.1": [
                {
                    "node": "1.1.1",
                    "distance": 27570
                },
                {
                    "node": "1.1.2",
                    "distance": 27570
                },
                {
                    "node": "1.1.3",
                    "distance": 27570
                },
                {
                    "node": "1.1.4",
                    "distance": 27570
                },
                {
                    "node": "1.2.1",
                    "distance": 24329
                },
                {
                    "node": "1.2.2",
                    "distance": 24329
                },
                {
                    "node": "1.2.3",
                    "distance": 24329
                },
                {
                    "node": "1.2.4",
                    "distance": 24329
                },
                {
                    "node": "1.3.1",
                    "distance": 21130
                },
                {
                    "node": "1.3.2",
                    "distance": 21130
                },
                {
                    "node": "1.3.3",
                    "distance": 21130
                },
                {
                    "node": "1.3.4",
                    "distance": 21130
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 27834
                },
                {
                    "node": "2.1.2",
                    "distance": 27834
                },
                {
                    "node": "2.1.3",
                    "distance": 27834
                },
                {
                    "node": "2.1.4",
                    "distance": 27834
                },
                {
                    "node": "2.2.1",
                    "distance": 24593
                },
                {
                    "node": "2.2.2",
                    "distance": 24593
                },
                {
                    "node": "2.2.3",
                    "distance": 24593
                },
                {
                    "node": "2.2.4",
                    "distance": 24593
                },
                {
                    "node": "2.3.1",
                    "distance": 21394
                },
                {
                    "node": "2.3.2",
                    "distance": 21394
                },
                {
                    "node": "2.3.3",
                    "distance": 21394
                },
                {
                    "node": "2.3.4",
                    "distance": 21394
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "4.2": [
                {
                    "node": "1.1.1",
                    "distance": 27570
                },
                {
                    "node": "1.1.2",
                    "distance": 27570
                },
                {
                    "node": "1.1.3",
                    "distance": 27570
                },
                {
                    "node": "1.1.4",
                    "distance": 27570
                },
                {
                    "node": "1.2.1",
                    "distance": 24329
                },
                {
                    "node": "1.2.2",
                    "distance": 24329
                },
                {
                    "node": "1.2.3",
                    "distance": 24329
                },
                {
                    "node": "1.2.4",
                    "distance": 24329
                },
                {
                    "node": "1.3.1",
                    "distance": 21130
                },
                {
                    "node": "1.3.2",
                    "distance": 21130
                },
                {
                    "node": "1.3.3",
                    "distance": 21130
                },
                {
                    "node": "1.3.4",
                    "distance": 21130
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 27834
                },
                {
                    "node": "2.1.2",
                    "distance": 27834
                },
                {
                    "node": "2.1.3",
                    "distance": 27834
                },
                {
                    "node": "2.1.4",
                    "distance": 27834
                },
                {
                    "node": "2.2.1",
                    "distance": 24593
                },
                {
                    "node": "2.2.2",
                    "distance": 24593
                },
                {
                    "node": "2.2.3",
                    "distance": 24593
                },
                {
                    "node": "2.2.4",
                    "distance": 24593
                },
                {
                    "node": "2.3.1",
                    "distance": 21394
                },
                {
                    "node": "2.3.2",
                    "distance": 21394
                },
                {
                    "node": "2.3.3",
                    "distance": 21394
                },
                {
                    "node": "2.3.4",
                    "distance": 21394
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "4.3": [
                {
                    "node": "1.1.1",
                    "distance": 27570
                },
                {
                    "node": "1.1.2",
                    "distance": 27570
                },
                {
                    "node": "1.1.3",
                    "distance": 27570
                },
                {
                    "node": "1.1.4",
                    "distance": 27570
                },
                {
                    "node": "1.2.1",
                    "distance": 24329
                },
                {
                    "node": "1.2.2",
                    "distance": 24329
                },
                {
                    "node": "1.2.3",
                    "distance": 24329
                },
                {
                    "node": "1.2.4",
                    "distance": 24329
                },
                {
                    "node": "1.3.1",
                    "distance": 21130
                },
                {
                    "node": "1.3.2",
                    "distance": 21130
                },
                {
                    "node": "1.3.3",
                    "distance": 21130
                },
                {
                    "node": "1.3.4",
                    "distance": 21130
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 27834
                },
                {
                    "node": "2.1.2",
                    "distance": 27834
                },
                {
                    "node": "2.1.3",
                    "distance": 27834
                },
                {
                    "node": "2.1.4",
                    "distance": 27834
                },
                {
                    "node": "2.2.1",
                    "distance": 24593
                },
                {
                    "node": "2.2.2",
                    "distance": 24593
                },
                {
                    "node": "2.2.3",
                    "distance": 24593
                },
                {
                    "node": "2.2.4",
                    "distance": 24593
                },
                {
                    "node": "2.3.1",
                    "distance": 21394
                },
                {
                    "node": "2.3.2",
                    "distance": 21394
                },
                {
                    "node": "2.3.3",
                    "distance": 21394
                },
                {
                    "node": "2.3.4",
                    "distance": 21394
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "4.4": [
                {
                    "node": "1.1.1",
                    "distance": 27570
                },
                {
                    "node": "1.1.2",
                    "distance": 27570
                },
                {
                    "node": "1.1.3",
                    "distance": 27570
                },
                {
                    "node": "1.1.4",
                    "distance": 27570
                },
                {
                    "node": "1.2.1",
                    "distance": 24329
                },
                {
                    "node": "1.2.2",
                    "distance": 24329
                },
                {
                    "node": "1.2.3",
                    "distance": 24329
                },
                {
                    "node": "1.2.4",
                    "distance": 24329
                },
                {
                    "node": "1.3.1",
                    "distance": 21130
                },
                {
                    "node": "1.3.2",
                    "distance": 21130
                },
                {
                    "node": "1.3.3",
                    "distance": 21130
                },
                {
                    "node": "1.3.4",
                    "distance": 21130
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 27834
                },
                {
                    "node": "2.1.2",
                    "distance": 27834
                },
                {
                    "node": "2.1.3",
                    "distance": 27834
                },
                {
                    "node": "2.1.4",
                    "distance": 27834
                },
                {
                    "node": "2.2.1",
                    "distance": 24593
                },
                {
                    "node": "2.2.2",
                    "distance": 24593
                },
                {
                    "node": "2.2.3",
                    "distance": 24593
                },
                {
                    "node": "2.2.4",
                    "distance": 24593
                },
                {
                    "node": "2.3.1",
                    "distance": 21394
                },
                {
                    "node": "2.3.2",
                    "distance": 21394
                },
                {
                    "node": "2.3.3",
                    "distance": 21394
                },
                {
                    "node": "2.3.4",
                    "distance": 21394
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "4.5": [
                {
                    "node": "1.1.1",
                    "distance": 27570
                },
                {
                    "node": "1.1.2",
                    "distance": 27570
                },
                {
                    "node": "1.1.3",
                    "distance": 27570
                },
                {
                    "node": "1.1.4",
                    "distance": 27570
                },
                {
                    "node": "1.2.1",
                    "distance": 24329
                },
                {
                    "node": "1.2.2",
                    "distance": 24329
                },
                {
                    "node": "1.2.3",
                    "distance": 24329
                },
                {
                    "node": "1.2.4",
                    "distance": 24329
                },
                {
                    "node": "1.3.1",
                    "distance": 21130
                },
                {
                    "node": "1.3.2",
                    "distance": 21130
                },
                {
                    "node": "1.3.3",
                    "distance": 21130
                },
                {
                    "node": "1.3.4",
                    "distance": 21130
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 27834
                },
                {
                    "node": "2.1.2",
                    "distance": 27834
                },
                {
                    "node": "2.1.3",
                    "distance": 27834
                },
                {
                    "node": "2.1.4",
                    "distance": 27834
                },
                {
                    "node": "2.2.1",
                    "distance": 24593
                },
                {
                    "node": "2.2.2",
                    "distance": 24593
                },
                {
                    "node": "2.2.3",
                    "distance": 24593
                },
                {
                    "node": "2.2.4",
                    "distance": 24593
                },
                {
                    "node": "2.3.1",
                    "distance": 21394
                },
                {
                    "node": "2.3.2",
                    "distance": 21394
                },
                {
                    "node": "2.3.3",
                    "distance": 21394
                },
                {
                    "node": "2.3.4",
                    "distance": 21394
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "4.6": [
                {
                    "node": "1.1.1",
                    "distance": 27570
                },
                {
                    "node": "1.1.2",
                    "distance": 27570
                },
                {
                    "node": "1.1.3",
                    "distance": 27570
                },
                {
                    "node": "1.1.4",
                    "distance": 27570
                },
                {
                    "node": "1.2.1",
                    "distance": 24329
                },
                {
                    "node": "1.2.2",
                    "distance": 24329
                },
                {
                    "node": "1.2.3",
                    "distance": 24329
                },
                {
                    "node": "1.2.4",
                    "distance": 24329
                },
                {
                    "node": "1.3.1",
                    "distance": 21130
                },
                {
                    "node": "1.3.2",
                    "distance": 21130
                },
                {
                    "node": "1.3.3",
                    "distance": 21130
                },
                {
                    "node": "1.3.4",
                    "distance": 21130
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 27834
                },
                {
                    "node": "2.1.2",
                    "distance": 27834
                },
                {
                    "node": "2.1.3",
                    "distance": 27834
                },
                {
                    "node": "2.1.4",
                    "distance": 27834
                },
                {
                    "node": "2.2.1",
                    "distance": 24593
                },
                {
                    "node": "2.2.2",
                    "distance": 24593
                },
                {
                    "node": "2.2.3",
                    "distance": 24593
                },
                {
                    "node": "2.2.4",
                    "distance": 24593
                },
                {
                    "node": "2.3.1",
                    "distance": 21394
                },
                {
                    "node": "2.3.2",
                    "distance": 21394
                },
                {
                    "node": "2.3.3",
                    "distance": 21394
                },
                {
                    "node": "2.3.4",
                    "distance": 21394
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        }
    ],
    "1.1": [
        {
            "1.1": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 27230
                },
                {
                    "node": "1.5.2",
                    "distance": 27230
                },
                {
                    "node": "1.5.3",
                    "distance": 27230
                },
                {
                    "node": "1.5.4",
                    "distance": 27230
                },
                {
                    "node": "1.6.1",
                    "distance": 33628
                },
                {
                    "node": "1.6.2",
                    "distance": 33628
                },
                {
                    "node": "1.6.3",
                    "distance": 33628
                },
                {
                    "node": "1.6.4",
                    "distance": 33628
                },
                {
                    "node": "1.7.1",
                    "distance": 40110
                },
                {
                    "node": "1.7.2",
                    "distance": 40110
                },
                {
                    "node": "1.7.3",
                    "distance": 40110
                },
                {
                    "node": "1.7.4",
                    "distance": 40110
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 27230
                },
                {
                    "node": "2.5.2",
                    "distance": 27230
                },
                {
                    "node": "2.5.3",
                    "distance": 27230
                },
                {
                    "node": "2.5.4",
                    "distance": 27230
                },
                {
                    "node": "2.6.1",
                    "distance": 33628
                },
                {
                    "node": "2.6.2",
                    "distance": 33628
                },
                {
                    "node": "2.6.3",
                    "distance": 33628
                },
                {
                    "node": "2.6.4",
                    "distance": 33628
                },
                {
                    "node": "2.7.1",
                    "distance": 40110
                },
                {
                    "node": "2.7.2",
                    "distance": 40110
                },
                {
                    "node": "2.7.3",
                    "distance": 40110
                },
                {
                    "node": "2.7.4",
                    "distance": 40110
                }
            ]
        },
        {
            "1.2": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 27230
                },
                {
                    "node": "1.5.2",
                    "distance": 27230
                },
                {
                    "node": "1.5.3",
                    "distance": 27230
                },
                {
                    "node": "1.5.4",
                    "distance": 27230
                },
                {
                    "node": "1.6.1",
                    "distance": 33628
                },
                {
                    "node": "1.6.2",
                    "distance": 33628
                },
                {
                    "node": "1.6.3",
                    "distance": 33628
                },
                {
                    "node": "1.6.4",
                    "distance": 33628
                },
                {
                    "node": "1.7.1",
                    "distance": 40110
                },
                {
                    "node": "1.7.2",
                    "distance": 40110
                },
                {
                    "node": "1.7.3",
                    "distance": 40110
                },
                {
                    "node": "1.7.4",
                    "distance": 40110
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 27230
                },
                {
                    "node": "2.5.2",
                    "distance": 27230
                },
                {
                    "node": "2.5.3",
                    "distance": 27230
                },
                {
                    "node": "2.5.4",
                    "distance": 27230
                },
                {
                    "node": "2.6.1",
                    "distance": 33628
                },
                {
                    "node": "2.6.2",
                    "distance": 33628
                },
                {
                    "node": "2.6.3",
                    "distance": 33628
                },
                {
                    "node": "2.6.4",
                    "distance": 33628
                },
                {
                    "node": "2.7.1",
                    "distance": 40110
                },
                {
                    "node": "2.7.2",
                    "distance": 40110
                },
                {
                    "node": "2.7.3",
                    "distance": 40110
                },
                {
                    "node": "2.7.4",
                    "distance": 40110
                }
            ]
        },
        {
            "1.3": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 27230
                },
                {
                    "node": "1.5.2",
                    "distance": 27230
                },
                {
                    "node": "1.5.3",
                    "distance": 27230
                },
                {
                    "node": "1.5.4",
                    "distance": 27230
                },
                {
                    "node": "1.6.1",
                    "distance": 33628
                },
                {
                    "node": "1.6.2",
                    "distance": 33628
                },
                {
                    "node": "1.6.3",
                    "distance": 33628
                },
                {
                    "node": "1.6.4",
                    "distance": 33628
                },
                {
                    "node": "1.7.1",
                    "distance": 40110
                },
                {
                    "node": "1.7.2",
                    "distance": 40110
                },
                {
                    "node": "1.7.3",
                    "distance": 40110
                },
                {
                    "node": "1.7.4",
                    "distance": 40110
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 27230
                },
                {
                    "node": "2.5.2",
                    "distance": 27230
                },
                {
                    "node": "2.5.3",
                    "distance": 27230
                },
                {
                    "node": "2.5.4",
                    "distance": 27230
                },
                {
                    "node": "2.6.1",
                    "distance": 33628
                },
                {
                    "node": "2.6.2",
                    "distance": 33628
                },
                {
                    "node": "2.6.3",
                    "distance": 33628
                },
                {
                    "node": "2.6.4",
                    "distance": 33628
                },
                {
                    "node": "2.7.1",
                    "distance": 40110
                },
                {
                    "node": "2.7.2",
                    "distance": 40110
                },
                {
                    "node": "2.7.3",
                    "distance": 40110
                },
                {
                    "node": "2.7.4",
                    "distance": 40110
                }
            ]
        },
        {
            "1.4": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 27230
                },
                {
                    "node": "1.5.2",
                    "distance": 27230
                },
                {
                    "node": "1.5.3",
                    "distance": 27230
                },
                {
                    "node": "1.5.4",
                    "distance": 27230
                },
                {
                    "node": "1.6.1",
                    "distance": 33628
                },
                {
                    "node": "1.6.2",
                    "distance": 33628
                },
                {
                    "node": "1.6.3",
                    "distance": 33628
                },
                {
                    "node": "1.6.4",
                    "distance": 33628
                },
                {
                    "node": "1.7.1",
                    "distance": 40110
                },
                {
                    "node": "1.7.2",
                    "distance": 40110
                },
                {
                    "node": "1.7.3",
                    "distance": 40110
                },
                {
                    "node": "1.7.4",
                    "distance": 40110
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 27230
                },
                {
                    "node": "2.5.2",
                    "distance": 27230
                },
                {
                    "node": "2.5.3",
                    "distance": 27230
                },
                {
                    "node": "2.5.4",
                    "distance": 27230
                },
                {
                    "node": "2.6.1",
                    "distance": 33628
                },
                {
                    "node": "2.6.2",
                    "distance": 33628
                },
                {
                    "node": "2.6.3",
                    "distance": 33628
                },
                {
                    "node": "2.6.4",
                    "distance": 33628
                },
                {
                    "node": "2.7.1",
                    "distance": 40110
                },
                {
                    "node": "2.7.2",
                    "distance": 40110
                },
                {
                    "node": "2.7.3",
                    "distance": 40110
                },
                {
                    "node": "2.7.4",
                    "distance": 40110
                }
            ]
        },
        {
            "1.5": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 27230
                },
                {
                    "node": "1.5.2",
                    "distance": 27230
                },
                {
                    "node": "1.5.3",
                    "distance": 27230
                },
                {
                    "node": "1.5.4",
                    "distance": 27230
                },
                {
                    "node": "1.6.1",
                    "distance": 33628
                },
                {
                    "node": "1.6.2",
                    "distance": 33628
                },
                {
                    "node": "1.6.3",
                    "distance": 33628
                },
                {
                    "node": "1.6.4",
                    "distance": 33628
                },
                {
                    "node": "1.7.1",
                    "distance": 40110
                },
                {
                    "node": "1.7.2",
                    "distance": 40110
                },
                {
                    "node": "1.7.3",
                    "distance": 40110
                },
                {
                    "node": "1.7.4",
                    "distance": 40110
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 27230
                },
                {
                    "node": "2.5.2",
                    "distance": 27230
                },
                {
                    "node": "2.5.3",
                    "distance": 27230
                },
                {
                    "node": "2.5.4",
                    "distance": 27230
                },
                {
                    "node": "2.6.1",
                    "distance": 33628
                },
                {
                    "node": "2.6.2",
                    "distance": 33628
                },
                {
                    "node": "2.6.3",
                    "distance": 33628
                },
                {
                    "node": "2.6.4",
                    "distance": 33628
                },
                {
                    "node": "2.7.1",
                    "distance": 40110
                },
                {
                    "node": "2.7.2",
                    "distance": 40110
                },
                {
                    "node": "2.7.3",
                    "distance": 40110
                },
                {
                    "node": "2.7.4",
                    "distance": 40110
                }
            ]
        },
        {
            "1.6": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 27230
                },
                {
                    "node": "1.5.2",
                    "distance": 27230
                },
                {
                    "node": "1.5.3",
                    "distance": 27230
                },
                {
                    "node": "1.5.4",
                    "distance": 27230
                },
                {
                    "node": "1.6.1",
                    "distance": 33628
                },
                {
                    "node": "1.6.2",
                    "distance": 33628
                },
                {
                    "node": "1.6.3",
                    "distance": 33628
                },
                {
                    "node": "1.6.4",
                    "distance": 33628
                },
                {
                    "node": "1.7.1",
                    "distance": 40110
                },
                {
                    "node": "1.7.2",
                    "distance": 40110
                },
                {
                    "node": "1.7.3",
                    "distance": 40110
                },
                {
                    "node": "1.7.4",
                    "distance": 40110
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 27230
                },
                {
                    "node": "2.5.2",
                    "distance": 27230
                },
                {
                    "node": "2.5.3",
                    "distance": 27230
                },
                {
                    "node": "2.5.4",
                    "distance": 27230
                },
                {
                    "node": "2.6.1",
                    "distance": 33628
                },
                {
                    "node": "2.6.2",
                    "distance": 33628
                },
                {
                    "node": "2.6.3",
                    "distance": 33628
                },
                {
                    "node": "2.6.4",
                    "distance": 33628
                },
                {
                    "node": "2.7.1",
                    "distance": 40110
                },
                {
                    "node": "2.7.2",
                    "distance": 40110
                },
                {
                    "node": "2.7.3",
                    "distance": 40110
                },
                {
                    "node": "2.7.4",
                    "distance": 40110
                }
            ]
        },
        {
            "2.1": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 27257
                },
                {
                    "node": "1.6.2",
                    "distance": 27257
                },
                {
                    "node": "1.6.3",
                    "distance": 27257
                },
                {
                    "node": "1.6.4",
                    "distance": 27257
                },
                {
                    "node": "1.7.1",
                    "distance": 33670
                },
                {
                    "node": "1.7.2",
                    "distance": 33670
                },
                {
                    "node": "1.7.3",
                    "distance": 33670
                },
                {
                    "node": "1.7.4",
                    "distance": 33670
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 27257
                },
                {
                    "node": "2.6.2",
                    "distance": 27257
                },
                {
                    "node": "2.6.3",
                    "distance": 27257
                },
                {
                    "node": "2.6.4",
                    "distance": 27257
                },
                {
                    "node": "2.7.1",
                    "distance": 33670
                },
                {
                    "node": "2.7.2",
                    "distance": 33670
                },
                {
                    "node": "2.7.3",
                    "distance": 33670
                },
                {
                    "node": "2.7.4",
                    "distance": 33670
                }
            ]
        },
        {
            "2.2": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 27257
                },
                {
                    "node": "1.6.2",
                    "distance": 27257
                },
                {
                    "node": "1.6.3",
                    "distance": 27257
                },
                {
                    "node": "1.6.4",
                    "distance": 27257
                },
                {
                    "node": "1.7.1",
                    "distance": 33670
                },
                {
                    "node": "1.7.2",
                    "distance": 33670
                },
                {
                    "node": "1.7.3",
                    "distance": 33670
                },
                {
                    "node": "1.7.4",
                    "distance": 33670
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 27257
                },
                {
                    "node": "2.6.2",
                    "distance": 27257
                },
                {
                    "node": "2.6.3",
                    "distance": 27257
                },
                {
                    "node": "2.6.4",
                    "distance": 27257
                },
                {
                    "node": "2.7.1",
                    "distance": 33670
                },
                {
                    "node": "2.7.2",
                    "distance": 33670
                },
                {
                    "node": "2.7.3",
                    "distance": 33670
                },
                {
                    "node": "2.7.4",
                    "distance": 33670
                }
            ]
        },
        {
            "2.3": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 27257
                },
                {
                    "node": "1.6.2",
                    "distance": 27257
                },
                {
                    "node": "1.6.3",
                    "distance": 27257
                },
                {
                    "node": "1.6.4",
                    "distance": 27257
                },
                {
                    "node": "1.7.1",
                    "distance": 33670
                },
                {
                    "node": "1.7.2",
                    "distance": 33670
                },
                {
                    "node": "1.7.3",
                    "distance": 33670
                },
                {
                    "node": "1.7.4",
                    "distance": 33670
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 27257
                },
                {
                    "node": "2.6.2",
                    "distance": 27257
                },
                {
                    "node": "2.6.3",
                    "distance": 27257
                },
                {
                    "node": "2.6.4",
                    "distance": 27257
                },
                {
                    "node": "2.7.1",
                    "distance": 33670
                },
                {
                    "node": "2.7.2",
                    "distance": 33670
                },
                {
                    "node": "2.7.3",
                    "distance": 33670
                },
                {
                    "node": "2.7.4",
                    "distance": 33670
                }
            ]
        },
        {
            "2.4": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 27257
                },
                {
                    "node": "1.6.2",
                    "distance": 27257
                },
                {
                    "node": "1.6.3",
                    "distance": 27257
                },
                {
                    "node": "1.6.4",
                    "distance": 27257
                },
                {
                    "node": "1.7.1",
                    "distance": 33670
                },
                {
                    "node": "1.7.2",
                    "distance": 33670
                },
                {
                    "node": "1.7.3",
                    "distance": 33670
                },
                {
                    "node": "1.7.4",
                    "distance": 33670
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 27257
                },
                {
                    "node": "2.6.2",
                    "distance": 27257
                },
                {
                    "node": "2.6.3",
                    "distance": 27257
                },
                {
                    "node": "2.6.4",
                    "distance": 27257
                },
                {
                    "node": "2.7.1",
                    "distance": 33670
                },
                {
                    "node": "2.7.2",
                    "distance": 33670
                },
                {
                    "node": "2.7.3",
                    "distance": 33670
                },
                {
                    "node": "2.7.4",
                    "distance": 33670
                }
            ]
        },
        {
            "3.1": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "3.2": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "3.3": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "3.4": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "3.5": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "4.1": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "4.2": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "4.3": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "4.4": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "4.5": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "4.6": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        }
    ],
    "2.1": [
        {
            "1.1": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 27257
                },
                {
                    "node": "1.6.2",
                    "distance": 27257
                },
                {
                    "node": "1.6.3",
                    "distance": 27257
                },
                {
                    "node": "1.6.4",
                    "distance": 27257
                },
                {
                    "node": "1.7.1",
                    "distance": 33670
                },
                {
                    "node": "1.7.2",
                    "distance": 33670
                },
                {
                    "node": "1.7.3",
                    "distance": 33670
                },
                {
                    "node": "1.7.4",
                    "distance": 33670
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 27257
                },
                {
                    "node": "2.6.2",
                    "distance": 27257
                },
                {
                    "node": "2.6.3",
                    "distance": 27257
                },
                {
                    "node": "2.6.4",
                    "distance": 27257
                },
                {
                    "node": "2.7.1",
                    "distance": 33670
                },
                {
                    "node": "2.7.2",
                    "distance": 33670
                },
                {
                    "node": "2.7.3",
                    "distance": 33670
                },
                {
                    "node": "2.7.4",
                    "distance": 33670
                }
            ]
        },
        {
            "1.2": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 27257
                },
                {
                    "node": "1.6.2",
                    "distance": 27257
                },
                {
                    "node": "1.6.3",
                    "distance": 27257
                },
                {
                    "node": "1.6.4",
                    "distance": 27257
                },
                {
                    "node": "1.7.1",
                    "distance": 33670
                },
                {
                    "node": "1.7.2",
                    "distance": 33670
                },
                {
                    "node": "1.7.3",
                    "distance": 33670
                },
                {
                    "node": "1.7.4",
                    "distance": 33670
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 27257
                },
                {
                    "node": "2.6.2",
                    "distance": 27257
                },
                {
                    "node": "2.6.3",
                    "distance": 27257
                },
                {
                    "node": "2.6.4",
                    "distance": 27257
                },
                {
                    "node": "2.7.1",
                    "distance": 33670
                },
                {
                    "node": "2.7.2",
                    "distance": 33670
                },
                {
                    "node": "2.7.3",
                    "distance": 33670
                },
                {
                    "node": "2.7.4",
                    "distance": 33670
                }
            ]
        },
        {
            "1.3": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 27257
                },
                {
                    "node": "1.6.2",
                    "distance": 27257
                },
                {
                    "node": "1.6.3",
                    "distance": 27257
                },
                {
                    "node": "1.6.4",
                    "distance": 27257
                },
                {
                    "node": "1.7.1",
                    "distance": 33670
                },
                {
                    "node": "1.7.2",
                    "distance": 33670
                },
                {
                    "node": "1.7.3",
                    "distance": 33670
                },
                {
                    "node": "1.7.4",
                    "distance": 33670
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 27257
                },
                {
                    "node": "2.6.2",
                    "distance": 27257
                },
                {
                    "node": "2.6.3",
                    "distance": 27257
                },
                {
                    "node": "2.6.4",
                    "distance": 27257
                },
                {
                    "node": "2.7.1",
                    "distance": 33670
                },
                {
                    "node": "2.7.2",
                    "distance": 33670
                },
                {
                    "node": "2.7.3",
                    "distance": 33670
                },
                {
                    "node": "2.7.4",
                    "distance": 33670
                }
            ]
        },
        {
            "1.4": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 27257
                },
                {
                    "node": "1.6.2",
                    "distance": 27257
                },
                {
                    "node": "1.6.3",
                    "distance": 27257
                },
                {
                    "node": "1.6.4",
                    "distance": 27257
                },
                {
                    "node": "1.7.1",
                    "distance": 33670
                },
                {
                    "node": "1.7.2",
                    "distance": 33670
                },
                {
                    "node": "1.7.3",
                    "distance": 33670
                },
                {
                    "node": "1.7.4",
                    "distance": 33670
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 27257
                },
                {
                    "node": "2.6.2",
                    "distance": 27257
                },
                {
                    "node": "2.6.3",
                    "distance": 27257
                },
                {
                    "node": "2.6.4",
                    "distance": 27257
                },
                {
                    "node": "2.7.1",
                    "distance": 33670
                },
                {
                    "node": "2.7.2",
                    "distance": 33670
                },
                {
                    "node": "2.7.3",
                    "distance": 33670
                },
                {
                    "node": "2.7.4",
                    "distance": 33670
                }
            ]
        },
        {
            "1.5": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 27257
                },
                {
                    "node": "1.6.2",
                    "distance": 27257
                },
                {
                    "node": "1.6.3",
                    "distance": 27257
                },
                {
                    "node": "1.6.4",
                    "distance": 27257
                },
                {
                    "node": "1.7.1",
                    "distance": 33670
                },
                {
                    "node": "1.7.2",
                    "distance": 33670
                },
                {
                    "node": "1.7.3",
                    "distance": 33670
                },
                {
                    "node": "1.7.4",
                    "distance": 33670
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 27257
                },
                {
                    "node": "2.6.2",
                    "distance": 27257
                },
                {
                    "node": "2.6.3",
                    "distance": 27257
                },
                {
                    "node": "2.6.4",
                    "distance": 27257
                },
                {
                    "node": "2.7.1",
                    "distance": 33670
                },
                {
                    "node": "2.7.2",
                    "distance": 33670
                },
                {
                    "node": "2.7.3",
                    "distance": 33670
                },
                {
                    "node": "2.7.4",
                    "distance": 33670
                }
            ]
        },
        {
            "1.6": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 27257
                },
                {
                    "node": "1.6.2",
                    "distance": 27257
                },
                {
                    "node": "1.6.3",
                    "distance": 27257
                },
                {
                    "node": "1.6.4",
                    "distance": 27257
                },
                {
                    "node": "1.7.1",
                    "distance": 33670
                },
                {
                    "node": "1.7.2",
                    "distance": 33670
                },
                {
                    "node": "1.7.3",
                    "distance": 33670
                },
                {
                    "node": "1.7.4",
                    "distance": 33670
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 27257
                },
                {
                    "node": "2.6.2",
                    "distance": 27257
                },
                {
                    "node": "2.6.3",
                    "distance": 27257
                },
                {
                    "node": "2.6.4",
                    "distance": 27257
                },
                {
                    "node": "2.7.1",
                    "distance": 33670
                },
                {
                    "node": "2.7.2",
                    "distance": 33670
                },
                {
                    "node": "2.7.3",
                    "distance": 33670
                },
                {
                    "node": "2.7.4",
                    "distance": 33670
                }
            ]
        },
        {
            "2.1": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 20886
                },
                {
                    "node": "1.6.2",
                    "distance": 20886
                },
                {
                    "node": "1.6.3",
                    "distance": 20886
                },
                {
                    "node": "1.6.4",
                    "distance": 20886
                },
                {
                    "node": "1.7.1",
                    "distance": 27230
                },
                {
                    "node": "1.7.2",
                    "distance": 27230
                },
                {
                    "node": "1.7.3",
                    "distance": 27230
                },
                {
                    "node": "1.7.4",
                    "distance": 27230
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 20886
                },
                {
                    "node": "2.6.2",
                    "distance": 20886
                },
                {
                    "node": "2.6.3",
                    "distance": 20886
                },
                {
                    "node": "2.6.4",
                    "distance": 20886
                },
                {
                    "node": "2.7.1",
                    "distance": 27230
                },
                {
                    "node": "2.7.2",
                    "distance": 27230
                },
                {
                    "node": "2.7.3",
                    "distance": 27230
                },
                {
                    "node": "2.7.4",
                    "distance": 27230
                }
            ]
        },
        {
            "2.2": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 20886
                },
                {
                    "node": "1.6.2",
                    "distance": 20886
                },
                {
                    "node": "1.6.3",
                    "distance": 20886
                },
                {
                    "node": "1.6.4",
                    "distance": 20886
                },
                {
                    "node": "1.7.1",
                    "distance": 27230
                },
                {
                    "node": "1.7.2",
                    "distance": 27230
                },
                {
                    "node": "1.7.3",
                    "distance": 27230
                },
                {
                    "node": "1.7.4",
                    "distance": 27230
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 20886
                },
                {
                    "node": "2.6.2",
                    "distance": 20886
                },
                {
                    "node": "2.6.3",
                    "distance": 20886
                },
                {
                    "node": "2.6.4",
                    "distance": 20886
                },
                {
                    "node": "2.7.1",
                    "distance": 27230
                },
                {
                    "node": "2.7.2",
                    "distance": 27230
                },
                {
                    "node": "2.7.3",
                    "distance": 27230
                },
                {
                    "node": "2.7.4",
                    "distance": 27230
                }
            ]
        },
        {
            "2.3": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 20886
                },
                {
                    "node": "1.6.2",
                    "distance": 20886
                },
                {
                    "node": "1.6.3",
                    "distance": 20886
                },
                {
                    "node": "1.6.4",
                    "distance": 20886
                },
                {
                    "node": "1.7.1",
                    "distance": 27230
                },
                {
                    "node": "1.7.2",
                    "distance": 27230
                },
                {
                    "node": "1.7.3",
                    "distance": 27230
                },
                {
                    "node": "1.7.4",
                    "distance": 27230
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 20886
                },
                {
                    "node": "2.6.2",
                    "distance": 20886
                },
                {
                    "node": "2.6.3",
                    "distance": 20886
                },
                {
                    "node": "2.6.4",
                    "distance": 20886
                },
                {
                    "node": "2.7.1",
                    "distance": 27230
                },
                {
                    "node": "2.7.2",
                    "distance": 27230
                },
                {
                    "node": "2.7.3",
                    "distance": 27230
                },
                {
                    "node": "2.7.4",
                    "distance": 27230
                }
            ]
        },
        {
            "2.4": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 20886
                },
                {
                    "node": "1.6.2",
                    "distance": 20886
                },
                {
                    "node": "1.6.3",
                    "distance": 20886
                },
                {
                    "node": "1.6.4",
                    "distance": 20886
                },
                {
                    "node": "1.7.1",
                    "distance": 27230
                },
                {
                    "node": "1.7.2",
                    "distance": 27230
                },
                {
                    "node": "1.7.3",
                    "distance": 27230
                },
                {
                    "node": "1.7.4",
                    "distance": 27230
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 20886
                },
                {
                    "node": "2.6.2",
                    "distance": 20886
                },
                {
                    "node": "2.6.3",
                    "distance": 20886
                },
                {
                    "node": "2.6.4",
                    "distance": 20886
                },
                {
                    "node": "2.7.1",
                    "distance": 27230
                },
                {
                    "node": "2.7.2",
                    "distance": 27230
                },
                {
                    "node": "2.7.3",
                    "distance": 27230
                },
                {
                    "node": "2.7.4",
                    "distance": 27230
                }
            ]
        },
        {
            "3.1": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "3.2": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "3.3": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "3.4": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "3.5": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "4.1": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "4.2": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "4.3": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "4.4": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "4.5": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "4.6": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        }
    ],
    "3.1": [
        {
            "1.1": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "1.2": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "1.3": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "1.4": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "1.5": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "1.6": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "2.1": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "2.2": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "2.3": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "2.4": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "3.1": [
                {
                    "node": "1.1.1",
                    "distance": 27230
                },
                {
                    "node": "1.1.2",
                    "distance": 27230
                },
                {
                    "node": "1.1.3",
                    "distance": 27230
                },
                {
                    "node": "1.1.4",
                    "distance": 27230
                },
                {
                    "node": "1.2.1",
                    "distance": 20886
                },
                {
                    "node": "1.2.2",
                    "distance": 20886
                },
                {
                    "node": "1.2.3",
                    "distance": 20886
                },
                {
                    "node": "1.2.4",
                    "distance": 20886
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 27230
                },
                {
                    "node": "2.1.2",
                    "distance": 27230
                },
                {
                    "node": "2.1.3",
                    "distance": 27230
                },
                {
                    "node": "2.1.4",
                    "distance": 27230
                },
                {
                    "node": "2.2.1",
                    "distance": 20886
                },
                {
                    "node": "2.2.2",
                    "distance": 20886
                },
                {
                    "node": "2.2.3",
                    "distance": 20886
                },
                {
                    "node": "2.2.4",
                    "distance": 20886
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "3.2": [
                {
                    "node": "1.1.1",
                    "distance": 27230
                },
                {
                    "node": "1.1.2",
                    "distance": 27230
                },
                {
                    "node": "1.1.3",
                    "distance": 27230
                },
                {
                    "node": "1.1.4",
                    "distance": 27230
                },
                {
                    "node": "1.2.1",
                    "distance": 20886
                },
                {
                    "node": "1.2.2",
                    "distance": 20886
                },
                {
                    "node": "1.2.3",
                    "distance": 20886
                },
                {
                    "node": "1.2.4",
                    "distance": 20886
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 27230
                },
                {
                    "node": "2.1.2",
                    "distance": 27230
                },
                {
                    "node": "2.1.3",
                    "distance": 27230
                },
                {
                    "node": "2.1.4",
                    "distance": 27230
                },
                {
                    "node": "2.2.1",
                    "distance": 20886
                },
                {
                    "node": "2.2.2",
                    "distance": 20886
                },
                {
                    "node": "2.2.3",
                    "distance": 20886
                },
                {
                    "node": "2.2.4",
                    "distance": 20886
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "3.3": [
                {
                    "node": "1.1.1",
                    "distance": 27230
                },
                {
                    "node": "1.1.2",
                    "distance": 27230
                },
                {
                    "node": "1.1.3",
                    "distance": 27230
                },
                {
                    "node": "1.1.4",
                    "distance": 27230
                },
                {
                    "node": "1.2.1",
                    "distance": 20886
                },
                {
                    "node": "1.2.2",
                    "distance": 20886
                },
                {
                    "node": "1.2.3",
                    "distance": 20886
                },
                {
                    "node": "1.2.4",
                    "distance": 20886
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 27230
                },
                {
                    "node": "2.1.2",
                    "distance": 27230
                },
                {
                    "node": "2.1.3",
                    "distance": 27230
                },
                {
                    "node": "2.1.4",
                    "distance": 27230
                },
                {
                    "node": "2.2.1",
                    "distance": 20886
                },
                {
                    "node": "2.2.2",
                    "distance": 20886
                },
                {
                    "node": "2.2.3",
                    "distance": 20886
                },
                {
                    "node": "2.2.4",
                    "distance": 20886
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "3.4": [
                {
                    "node": "1.1.1",
                    "distance": 27230
                },
                {
                    "node": "1.1.2",
                    "distance": 27230
                },
                {
                    "node": "1.1.3",
                    "distance": 27230
                },
                {
                    "node": "1.1.4",
                    "distance": 27230
                },
                {
                    "node": "1.2.1",
                    "distance": 20886
                },
                {
                    "node": "1.2.2",
                    "distance": 20886
                },
                {
                    "node": "1.2.3",
                    "distance": 20886
                },
                {
                    "node": "1.2.4",
                    "distance": 20886
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 27230
                },
                {
                    "node": "2.1.2",
                    "distance": 27230
                },
                {
                    "node": "2.1.3",
                    "distance": 27230
                },
                {
                    "node": "2.1.4",
                    "distance": 27230
                },
                {
                    "node": "2.2.1",
                    "distance": 20886
                },
                {
                    "node": "2.2.2",
                    "distance": 20886
                },
                {
                    "node": "2.2.3",
                    "distance": 20886
                },
                {
                    "node": "2.2.4",
                    "distance": 20886
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "3.5": [
                {
                    "node": "1.1.1",
                    "distance": 27230
                },
                {
                    "node": "1.1.2",
                    "distance": 27230
                },
                {
                    "node": "1.1.3",
                    "distance": 27230
                },
                {
                    "node": "1.1.4",
                    "distance": 27230
                },
                {
                    "node": "1.2.1",
                    "distance": 20886
                },
                {
                    "node": "1.2.2",
                    "distance": 20886
                },
                {
                    "node": "1.2.3",
                    "distance": 20886
                },
                {
                    "node": "1.2.4",
                    "distance": 20886
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 27230
                },
                {
                    "node": "2.1.2",
                    "distance": 27230
                },
                {
                    "node": "2.1.3",
                    "distance": 27230
                },
                {
                    "node": "2.1.4",
                    "distance": 27230
                },
                {
                    "node": "2.2.1",
                    "distance": 20886
                },
                {
                    "node": "2.2.2",
                    "distance": 20886
                },
                {
                    "node": "2.2.3",
                    "distance": 20886
                },
                {
                    "node": "2.2.4",
                    "distance": 20886
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "4.1": [
                {
                    "node": "1.1.1",
                    "distance": 33670
                },
                {
                    "node": "1.1.2",
                    "distance": 33670
                },
                {
                    "node": "1.1.3",
                    "distance": 33670
                },
                {
                    "node": "1.1.4",
                    "distance": 33670
                },
                {
                    "node": "1.2.1",
                    "distance": 27257
                },
                {
                    "node": "1.2.2",
                    "distance": 27257
                },
                {
                    "node": "1.2.3",
                    "distance": 27257
                },
                {
                    "node": "1.2.4",
                    "distance": 27257
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 33670
                },
                {
                    "node": "2.1.2",
                    "distance": 33670
                },
                {
                    "node": "2.1.3",
                    "distance": 33670
                },
                {
                    "node": "2.1.4",
                    "distance": 33670
                },
                {
                    "node": "2.2.1",
                    "distance": 27257
                },
                {
                    "node": "2.2.2",
                    "distance": 27257
                },
                {
                    "node": "2.2.3",
                    "distance": 27257
                },
                {
                    "node": "2.2.4",
                    "distance": 27257
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "4.2": [
                {
                    "node": "1.1.1",
                    "distance": 33670
                },
                {
                    "node": "1.1.2",
                    "distance": 33670
                },
                {
                    "node": "1.1.3",
                    "distance": 33670
                },
                {
                    "node": "1.1.4",
                    "distance": 33670
                },
                {
                    "node": "1.2.1",
                    "distance": 27257
                },
                {
                    "node": "1.2.2",
                    "distance": 27257
                },
                {
                    "node": "1.2.3",
                    "distance": 27257
                },
                {
                    "node": "1.2.4",
                    "distance": 27257
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 33670
                },
                {
                    "node": "2.1.2",
                    "distance": 33670
                },
                {
                    "node": "2.1.3",
                    "distance": 33670
                },
                {
                    "node": "2.1.4",
                    "distance": 33670
                },
                {
                    "node": "2.2.1",
                    "distance": 27257
                },
                {
                    "node": "2.2.2",
                    "distance": 27257
                },
                {
                    "node": "2.2.3",
                    "distance": 27257
                },
                {
                    "node": "2.2.4",
                    "distance": 27257
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "4.3": [
                {
                    "node": "1.1.1",
                    "distance": 33670
                },
                {
                    "node": "1.1.2",
                    "distance": 33670
                },
                {
                    "node": "1.1.3",
                    "distance": 33670
                },
                {
                    "node": "1.1.4",
                    "distance": 33670
                },
                {
                    "node": "1.2.1",
                    "distance": 27257
                },
                {
                    "node": "1.2.2",
                    "distance": 27257
                },
                {
                    "node": "1.2.3",
                    "distance": 27257
                },
                {
                    "node": "1.2.4",
                    "distance": 27257
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 33670
                },
                {
                    "node": "2.1.2",
                    "distance": 33670
                },
                {
                    "node": "2.1.3",
                    "distance": 33670
                },
                {
                    "node": "2.1.4",
                    "distance": 33670
                },
                {
                    "node": "2.2.1",
                    "distance": 27257
                },
                {
                    "node": "2.2.2",
                    "distance": 27257
                },
                {
                    "node": "2.2.3",
                    "distance": 27257
                },
                {
                    "node": "2.2.4",
                    "distance": 27257
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "4.4": [
                {
                    "node": "1.1.1",
                    "distance": 33670
                },
                {
                    "node": "1.1.2",
                    "distance": 33670
                },
                {
                    "node": "1.1.3",
                    "distance": 33670
                },
                {
                    "node": "1.1.4",
                    "distance": 33670
                },
                {
                    "node": "1.2.1",
                    "distance": 27257
                },
                {
                    "node": "1.2.2",
                    "distance": 27257
                },
                {
                    "node": "1.2.3",
                    "distance": 27257
                },
                {
                    "node": "1.2.4",
                    "distance": 27257
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 33670
                },
                {
                    "node": "2.1.2",
                    "distance": 33670
                },
                {
                    "node": "2.1.3",
                    "distance": 33670
                },
                {
                    "node": "2.1.4",
                    "distance": 33670
                },
                {
                    "node": "2.2.1",
                    "distance": 27257
                },
                {
                    "node": "2.2.2",
                    "distance": 27257
                },
                {
                    "node": "2.2.3",
                    "distance": 27257
                },
                {
                    "node": "2.2.4",
                    "distance": 27257
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "4.5": [
                {
                    "node": "1.1.1",
                    "distance": 33670
                },
                {
                    "node": "1.1.2",
                    "distance": 33670
                },
                {
                    "node": "1.1.3",
                    "distance": 33670
                },
                {
                    "node": "1.1.4",
                    "distance": 33670
                },
                {
                    "node": "1.2.1",
                    "distance": 27257
                },
                {
                    "node": "1.2.2",
                    "distance": 27257
                },
                {
                    "node": "1.2.3",
                    "distance": 27257
                },
                {
                    "node": "1.2.4",
                    "distance": 27257
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 33670
                },
                {
                    "node": "2.1.2",
                    "distance": 33670
                },
                {
                    "node": "2.1.3",
                    "distance": 33670
                },
                {
                    "node": "2.1.4",
                    "distance": 33670
                },
                {
                    "node": "2.2.1",
                    "distance": 27257
                },
                {
                    "node": "2.2.2",
                    "distance": 27257
                },
                {
                    "node": "2.2.3",
                    "distance": 27257
                },
                {
                    "node": "2.2.4",
                    "distance": 27257
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "4.6": [
                {
                    "node": "1.1.1",
                    "distance": 33670
                },
                {
                    "node": "1.1.2",
                    "distance": 33670
                },
                {
                    "node": "1.1.3",
                    "distance": 33670
                },
                {
                    "node": "1.1.4",
                    "distance": 33670
                },
                {
                    "node": "1.2.1",
                    "distance": 27257
                },
                {
                    "node": "1.2.2",
                    "distance": 27257
                },
                {
                    "node": "1.2.3",
                    "distance": 27257
                },
                {
                    "node": "1.2.4",
                    "distance": 27257
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 33670
                },
                {
                    "node": "2.1.2",
                    "distance": 33670
                },
                {
                    "node": "2.1.3",
                    "distance": 33670
                },
                {
                    "node": "2.1.4",
                    "distance": 33670
                },
                {
                    "node": "2.2.1",
                    "distance": 27257
                },
                {
                    "node": "2.2.2",
                    "distance": 27257
                },
                {
                    "node": "2.2.3",
                    "distance": 27257
                },
                {
                    "node": "2.2.4",
                    "distance": 27257
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        }
    ],
    "4.1": [
        {
            "1.1": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "1.2": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "1.3": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "1.4": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "1.5": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "1.6": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "2.1": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "2.2": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "2.3": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "2.4": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "3.1": [
                {
                    "node": "1.1.1",
                    "distance": 33670
                },
                {
                    "node": "1.1.2",
                    "distance": 33670
                },
                {
                    "node": "1.1.3",
                    "distance": 33670
                },
                {
                    "node": "1.1.4",
                    "distance": 33670
                },
                {
                    "node": "1.2.1",
                    "distance": 27257
                },
                {
                    "node": "1.2.2",
                    "distance": 27257
                },
                {
                    "node": "1.2.3",
                    "distance": 27257
                },
                {
                    "node": "1.2.4",
                    "distance": 27257
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 33670
                },
                {
                    "node": "2.1.2",
                    "distance": 33670
                },
                {
                    "node": "2.1.3",
                    "distance": 33670
                },
                {
                    "node": "2.1.4",
                    "distance": 33670
                },
                {
                    "node": "2.2.1",
                    "distance": 27257
                },
                {
                    "node": "2.2.2",
                    "distance": 27257
                },
                {
                    "node": "2.2.3",
                    "distance": 27257
                },
                {
                    "node": "2.2.4",
                    "distance": 27257
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "3.2": [
                {
                    "node": "1.1.1",
                    "distance": 33670
                },
                {
                    "node": "1.1.2",
                    "distance": 33670
                },
                {
                    "node": "1.1.3",
                    "distance": 33670
                },
                {
                    "node": "1.1.4",
                    "distance": 33670
                },
                {
                    "node": "1.2.1",
                    "distance": 27257
                },
                {
                    "node": "1.2.2",
                    "distance": 27257
                },
                {
                    "node": "1.2.3",
                    "distance": 27257
                },
                {
                    "node": "1.2.4",
                    "distance": 27257
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 33670
                },
                {
                    "node": "2.1.2",
                    "distance": 33670
                },
                {
                    "node": "2.1.3",
                    "distance": 33670
                },
                {
                    "node": "2.1.4",
                    "distance": 33670
                },
                {
                    "node": "2.2.1",
                    "distance": 27257
                },
                {
                    "node": "2.2.2",
                    "distance": 27257
                },
                {
                    "node": "2.2.3",
                    "distance": 27257
                },
                {
                    "node": "2.2.4",
                    "distance": 27257
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "3.3": [
                {
                    "node": "1.1.1",
                    "distance": 33670
                },
                {
                    "node": "1.1.2",
                    "distance": 33670
                },
                {
                    "node": "1.1.3",
                    "distance": 33670
                },
                {
                    "node": "1.1.4",
                    "distance": 33670
                },
                {
                    "node": "1.2.1",
                    "distance": 27257
                },
                {
                    "node": "1.2.2",
                    "distance": 27257
                },
                {
                    "node": "1.2.3",
                    "distance": 27257
                },
                {
                    "node": "1.2.4",
                    "distance": 27257
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 33670
                },
                {
                    "node": "2.1.2",
                    "distance": 33670
                },
                {
                    "node": "2.1.3",
                    "distance": 33670
                },
                {
                    "node": "2.1.4",
                    "distance": 33670
                },
                {
                    "node": "2.2.1",
                    "distance": 27257
                },
                {
                    "node": "2.2.2",
                    "distance": 27257
                },
                {
                    "node": "2.2.3",
                    "distance": 27257
                },
                {
                    "node": "2.2.4",
                    "distance": 27257
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "3.4": [
                {
                    "node": "1.1.1",
                    "distance": 33670
                },
                {
                    "node": "1.1.2",
                    "distance": 33670
                },
                {
                    "node": "1.1.3",
                    "distance": 33670
                },
                {
                    "node": "1.1.4",
                    "distance": 33670
                },
                {
                    "node": "1.2.1",
                    "distance": 27257
                },
                {
                    "node": "1.2.2",
                    "distance": 27257
                },
                {
                    "node": "1.2.3",
                    "distance": 27257
                },
                {
                    "node": "1.2.4",
                    "distance": 27257
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 33670
                },
                {
                    "node": "2.1.2",
                    "distance": 33670
                },
                {
                    "node": "2.1.3",
                    "distance": 33670
                },
                {
                    "node": "2.1.4",
                    "distance": 33670
                },
                {
                    "node": "2.2.1",
                    "distance": 27257
                },
                {
                    "node": "2.2.2",
                    "distance": 27257
                },
                {
                    "node": "2.2.3",
                    "distance": 27257
                },
                {
                    "node": "2.2.4",
                    "distance": 27257
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "3.5": [
                {
                    "node": "1.1.1",
                    "distance": 33670
                },
                {
                    "node": "1.1.2",
                    "distance": 33670
                },
                {
                    "node": "1.1.3",
                    "distance": 33670
                },
                {
                    "node": "1.1.4",
                    "distance": 33670
                },
                {
                    "node": "1.2.1",
                    "distance": 27257
                },
                {
                    "node": "1.2.2",
                    "distance": 27257
                },
                {
                    "node": "1.2.3",
                    "distance": 27257
                },
                {
                    "node": "1.2.4",
                    "distance": 27257
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 33670
                },
                {
                    "node": "2.1.2",
                    "distance": 33670
                },
                {
                    "node": "2.1.3",
                    "distance": 33670
                },
                {
                    "node": "2.1.4",
                    "distance": 33670
                },
                {
                    "node": "2.2.1",
                    "distance": 27257
                },
                {
                    "node": "2.2.2",
                    "distance": 27257
                },
                {
                    "node": "2.2.3",
                    "distance": 27257
                },
                {
                    "node": "2.2.4",
                    "distance": 27257
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "4.1": [
                {
                    "node": "1.1.1",
                    "distance": 40110
                },
                {
                    "node": "1.1.2",
                    "distance": 40110
                },
                {
                    "node": "1.1.3",
                    "distance": 40110
                },
                {
                    "node": "1.1.4",
                    "distance": 40110
                },
                {
                    "node": "1.2.1",
                    "distance": 33628
                },
                {
                    "node": "1.2.2",
                    "distance": 33628
                },
                {
                    "node": "1.2.3",
                    "distance": 33628
                },
                {
                    "node": "1.2.4",
                    "distance": 33628
                },
                {
                    "node": "1.3.1",
                    "distance": 27230
                },
                {
                    "node": "1.3.2",
                    "distance": 27230
                },
                {
                    "node": "1.3.3",
                    "distance": 27230
                },
                {
                    "node": "1.3.4",
                    "distance": 27230
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 40110
                },
                {
                    "node": "2.1.2",
                    "distance": 40110
                },
                {
                    "node": "2.1.3",
                    "distance": 40110
                },
                {
                    "node": "2.1.4",
                    "distance": 40110
                },
                {
                    "node": "2.2.1",
                    "distance": 33628
                },
                {
                    "node": "2.2.2",
                    "distance": 33628
                },
                {
                    "node": "2.2.3",
                    "distance": 33628
                },
                {
                    "node": "2.2.4",
                    "distance": 33628
                },
                {
                    "node": "2.3.1",
                    "distance": 27230
                },
                {
                    "node": "2.3.2",
                    "distance": 27230
                },
                {
                    "node": "2.3.3",
                    "distance": 27230
                },
                {
                    "node": "2.3.4",
                    "distance": 27230
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "4.2": [
                {
                    "node": "1.1.1",
                    "distance": 40110
                },
                {
                    "node": "1.1.2",
                    "distance": 40110
                },
                {
                    "node": "1.1.3",
                    "distance": 40110
                },
                {
                    "node": "1.1.4",
                    "distance": 40110
                },
                {
                    "node": "1.2.1",
                    "distance": 33628
                },
                {
                    "node": "1.2.2",
                    "distance": 33628
                },
                {
                    "node": "1.2.3",
                    "distance": 33628
                },
                {
                    "node": "1.2.4",
                    "distance": 33628
                },
                {
                    "node": "1.3.1",
                    "distance": 27230
                },
                {
                    "node": "1.3.2",
                    "distance": 27230
                },
                {
                    "node": "1.3.3",
                    "distance": 27230
                },
                {
                    "node": "1.3.4",
                    "distance": 27230
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 40110
                },
                {
                    "node": "2.1.2",
                    "distance": 40110
                },
                {
                    "node": "2.1.3",
                    "distance": 40110
                },
                {
                    "node": "2.1.4",
                    "distance": 40110
                },
                {
                    "node": "2.2.1",
                    "distance": 33628
                },
                {
                    "node": "2.2.2",
                    "distance": 33628
                },
                {
                    "node": "2.2.3",
                    "distance": 33628
                },
                {
                    "node": "2.2.4",
                    "distance": 33628
                },
                {
                    "node": "2.3.1",
                    "distance": 27230
                },
                {
                    "node": "2.3.2",
                    "distance": 27230
                },
                {
                    "node": "2.3.3",
                    "distance": 27230
                },
                {
                    "node": "2.3.4",
                    "distance": 27230
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "4.3": [
                {
                    "node": "1.1.1",
                    "distance": 40110
                },
                {
                    "node": "1.1.2",
                    "distance": 40110
                },
                {
                    "node": "1.1.3",
                    "distance": 40110
                },
                {
                    "node": "1.1.4",
                    "distance": 40110
                },
                {
                    "node": "1.2.1",
                    "distance": 33628
                },
                {
                    "node": "1.2.2",
                    "distance": 33628
                },
                {
                    "node": "1.2.3",
                    "distance": 33628
                },
                {
                    "node": "1.2.4",
                    "distance": 33628
                },
                {
                    "node": "1.3.1",
                    "distance": 27230
                },
                {
                    "node": "1.3.2",
                    "distance": 27230
                },
                {
                    "node": "1.3.3",
                    "distance": 27230
                },
                {
                    "node": "1.3.4",
                    "distance": 27230
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 40110
                },
                {
                    "node": "2.1.2",
                    "distance": 40110
                },
                {
                    "node": "2.1.3",
                    "distance": 40110
                },
                {
                    "node": "2.1.4",
                    "distance": 40110
                },
                {
                    "node": "2.2.1",
                    "distance": 33628
                },
                {
                    "node": "2.2.2",
                    "distance": 33628
                },
                {
                    "node": "2.2.3",
                    "distance": 33628
                },
                {
                    "node": "2.2.4",
                    "distance": 33628
                },
                {
                    "node": "2.3.1",
                    "distance": 27230
                },
                {
                    "node": "2.3.2",
                    "distance": 27230
                },
                {
                    "node": "2.3.3",
                    "distance": 27230
                },
                {
                    "node": "2.3.4",
                    "distance": 27230
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "4.4": [
                {
                    "node": "1.1.1",
                    "distance": 40110
                },
                {
                    "node": "1.1.2",
                    "distance": 40110
                },
                {
                    "node": "1.1.3",
                    "distance": 40110
                },
                {
                    "node": "1.1.4",
                    "distance": 40110
                },
                {
                    "node": "1.2.1",
                    "distance": 33628
                },
                {
                    "node": "1.2.2",
                    "distance": 33628
                },
                {
                    "node": "1.2.3",
                    "distance": 33628
                },
                {
                    "node": "1.2.4",
                    "distance": 33628
                },
                {
                    "node": "1.3.1",
                    "distance": 27230
                },
                {
                    "node": "1.3.2",
                    "distance": 27230
                },
                {
                    "node": "1.3.3",
                    "distance": 27230
                },
                {
                    "node": "1.3.4",
                    "distance": 27230
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 40110
                },
                {
                    "node": "2.1.2",
                    "distance": 40110
                },
                {
                    "node": "2.1.3",
                    "distance": 40110
                },
                {
                    "node": "2.1.4",
                    "distance": 40110
                },
                {
                    "node": "2.2.1",
                    "distance": 33628
                },
                {
                    "node": "2.2.2",
                    "distance": 33628
                },
                {
                    "node": "2.2.3",
                    "distance": 33628
                },
                {
                    "node": "2.2.4",
                    "distance": 33628
                },
                {
                    "node": "2.3.1",
                    "distance": 27230
                },
                {
                    "node": "2.3.2",
                    "distance": 27230
                },
                {
                    "node": "2.3.3",
                    "distance": 27230
                },
                {
                    "node": "2.3.4",
                    "distance": 27230
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "4.5": [
                {
                    "node": "1.1.1",
                    "distance": 40110
                },
                {
                    "node": "1.1.2",
                    "distance": 40110
                },
                {
                    "node": "1.1.3",
                    "distance": 40110
                },
                {
                    "node": "1.1.4",
                    "distance": 40110
                },
                {
                    "node": "1.2.1",
                    "distance": 33628
                },
                {
                    "node": "1.2.2",
                    "distance": 33628
                },
                {
                    "node": "1.2.3",
                    "distance": 33628
                },
                {
                    "node": "1.2.4",
                    "distance": 33628
                },
                {
                    "node": "1.3.1",
                    "distance": 27230
                },
                {
                    "node": "1.3.2",
                    "distance": 27230
                },
                {
                    "node": "1.3.3",
                    "distance": 27230
                },
                {
                    "node": "1.3.4",
                    "distance": 27230
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 40110
                },
                {
                    "node": "2.1.2",
                    "distance": 40110
                },
                {
                    "node": "2.1.3",
                    "distance": 40110
                },
                {
                    "node": "2.1.4",
                    "distance": 40110
                },
                {
                    "node": "2.2.1",
                    "distance": 33628
                },
                {
                    "node": "2.2.2",
                    "distance": 33628
                },
                {
                    "node": "2.2.3",
                    "distance": 33628
                },
                {
                    "node": "2.2.4",
                    "distance": 33628
                },
                {
                    "node": "2.3.1",
                    "distance": 27230
                },
                {
                    "node": "2.3.2",
                    "distance": 27230
                },
                {
                    "node": "2.3.3",
                    "distance": 27230
                },
                {
                    "node": "2.3.4",
                    "distance": 27230
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "4.6": [
                {
                    "node": "1.1.1",
                    "distance": 40110
                },
                {
                    "node": "1.1.2",
                    "distance": 40110
                },
                {
                    "node": "1.1.3",
                    "distance": 40110
                },
                {
                    "node": "1.1.4",
                    "distance": 40110
                },
                {
                    "node": "1.2.1",
                    "distance": 33628
                },
                {
                    "node": "1.2.2",
                    "distance": 33628
                },
                {
                    "node": "1.2.3",
                    "distance": 33628
                },
                {
                    "node": "1.2.4",
                    "distance": 33628
                },
                {
                    "node": "1.3.1",
                    "distance": 27230
                },
                {
                    "node": "1.3.2",
                    "distance": 27230
                },
                {
                    "node": "1.3.3",
                    "distance": 27230
                },
                {
                    "node": "1.3.4",
                    "distance": 27230
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 40110
                },
                {
                    "node": "2.1.2",
                    "distance": 40110
                },
                {
                    "node": "2.1.3",
                    "distance": 40110
                },
                {
                    "node": "2.1.4",
                    "distance": 40110
                },
                {
                    "node": "2.2.1",
                    "distance": 33628
                },
                {
                    "node": "2.2.2",
                    "distance": 33628
                },
                {
                    "node": "2.2.3",
                    "distance": 33628
                },
                {
                    "node": "2.2.4",
                    "distance": 33628
                },
                {
                    "node": "2.3.1",
                    "distance": 27230
                },
                {
                    "node": "2.3.2",
                    "distance": 27230
                },
                {
                    "node": "2.3.3",
                    "distance": 27230
                },
                {
                    "node": "2.3.4",
                    "distance": 27230
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        }
    ]
}



def filter_distance_matrix(matrix, containers, kit_holders):
    filtered_matrix = {"0.0": []}  # starting node

    for kh_key, kh_value in kit_holders.items():
        kh_position = kh_value["kh_position"]  # e.g. "1"

        for kh_content in kh_value["contents"]:
            kit_position = kh_content["position"]  # e.g. "1.1"
            kit_component = kh_content["type"]  # e.g. "Component_5"

            valid_nodes = []

            for container_key, container_value in containers.items():
                for cont_content in container_value["contents"]:
                    cont_position = cont_content["position"]  # e.g. "1.5.1"
                    cont_component = cont_content["type"]  # e.g. "Component_5"

                    # add the connection only if the components match
                    if kit_component == cont_component:
                        distance = get_distance_from_matrix(matrix, kit_position, cont_position)
                        if distance is not None:  # include valid distances
                            valid_nodes.append({"node": cont_position, "distance": distance})

            # skip duplicate entries for container nodes
            unique_nodes = list({node['node']: node for node in valid_nodes}.values())

            # append to the filtered matrix only if valid connections
            if unique_nodes:
                filtered_matrix["0.0"].append({
                    kit_position: unique_nodes
                })

    return filtered_matrix


def get_distance_from_matrix(matrix, kh_position, container_position):
    for kh_entry in matrix.get("0.0", []):
        if kh_position in kh_entry:
            for container in kh_entry[kh_position]:
                if container["node"] == container_position:
                    return container["distance"]
    return 0

filtered_matrix = filter_distance_matrix(distance_matrix, containers, kit_holders)

import json
with open("filtered_distance_matrix.json", "w") as f:
    json.dump(filtered_matrix, f, indent=4)

print("Filtered distance matrix saved successfully.")

