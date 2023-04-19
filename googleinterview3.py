import itertools
import operator
from collections import defaultdict
from functools import reduce
from pprint import pprint

# Some functions i wrote a while ago to handle nested iterables
# https://github.com/hansalemaos/flatten_any_dict_iterable_or_whatsoever
# pip install flatten-any-dict-iterable-or-whatsoever
from flatten_any_dict_iterable_or_whatsoever import fla_tu

# List of airports (including LGA)
airports = [
    "BGI",
    "CDG",
    "DEL",
    "DOH",
    "DSM",
    "EWR",
    "EYW",
    "HND",
    "ICN",
    "JFK",
    "LGA",
    "LHR",
    "ORD",
    "SAN",
    "SFO",
    "SIN",
    "TLV",
    "BUD",
]

# List of flight routes (departure - destination)
routes2 = [
    ["DSM", "ORD"],
    ["ORD", "BGI"],
    ["BGI", "LGA"],
    ["SIN", "CDG"],
    ["CDG", "SIN"],
    ["CDG", "BUD"],
    ["DEL", "DOH"],
    ["DEL", "CDG"],
    ["TLV", "DEL"],
    ["EWR", "HND"],
    ["HND", "ICN"],
    ["HND", "JFK"],
    ["ICN", "JFK"],
    ["JFK", "LGA"],
    ["EYW", "LHR"],
    ["LHR", "SFO"],
    ["SFO", "SAN"],
    ["SFO", "DSM"],
    ["SAN", "EYW"],
]

# Flag indicating if a connection to a disconnected airports is mandatory when
# iterating through all possibilities
# There is no possible solution without a connection to one of these airports:
# {"BUD", "CDG", "DEL", "DOH", "SIN", "TLV"}
# This option is to speed up the code a bit.
disconnected_airport_mandatory = True
disconnected_airports = {"BUD", "CDG", "DEL", "DOH", "SIN", "TLV"}

startairport = "LGA"


# Function to generate all possible flight routes
def get_all_routes():
    # Function to recursively generate all subroutes starting from an airport
    def get_all_subroutes(airportnick):
        if isinstance(airportnick, str):
            airportnick = (airportnick,)

        # Check all possible flights departing from the last airport in the current subroute
        for child in copyofairportdict[airportnick[-1]]:
            all_parsed_flight_routes = tuple(fla_tu(airportvariations))
            for c, parsed_flight_route in all_parsed_flight_routes:
                if airportnick[-1] in parsed_flight_route:
                    ina = parsed_flight_route.index(airportnick[-1])
                    cut_parsed_index = parsed_flight_route[: ina + 1]
                    if cut_parsed_index + (child,) in alreadydone:
                        continue
                    subdict_of_airport = reduce(
                        operator.getitem, cut_parsed_index, airportvariations
                    )
                    if child in subdict_of_airport:
                        subdict_of_airport[child].update(dummydict.copy())
                    else:
                        subdict_of_airport[child] = dummydict.copy()
                    if not cut_parsed_index + (child,) in alreadydone:
                        alreadydone.add(cut_parsed_index + (child,))
                        get_all_subroutes(cut_parsed_index + (child,))

        # Continue with the next subroute starting from a different airport
        for _, parsedairportroute in tuple(fla_tu(airportvariations)):
            if parsedairportroute[:-1] not in alreadydone:
                alreadydone.add(parsedairportroute[:-1])
                get_all_subroutes(parsedairportroute[:-1])

    alreadydone = set()

    # Generate all subroutes starting from all airports in the list
    for sta in airports:
        airportvariations[sta] = dummydict.copy()
        get_all_subroutes(sta)


# A nested dictionary that can create an unlimited number of levels
nested_dict = lambda: defaultdict(nested_dict)

# List of all possible combinations that can be added excluding the starting airport -> (LGA - LGA) is senseless
all_lga_variations = []
for lga_start_airport in airports:
    if lga_start_airport != startairport:
        all_lga_variations.append((startairport, lga_start_airport))

# Empty list to store the final result
result_variation = []

# Create a dummy dictionary to avoid errors if the 'nested_dict' is empty (fla_tu ignores empty dicts)
dummydict = nested_dict()
dummydict[1] = 0

# Find all combinations of 3 airports that are not the starting airport
for each_lga_variation in itertools.combinations(all_lga_variations, 3):
    routes = routes2.copy()

    # Append the three airport connections in the current variation to the list of routes
    for variation_element in each_lga_variation:
        routes.append(list(variation_element))

    # If disconnected airports are mandatory, check if there are any disconnected airports in the routes
    # We continue if there is nothing, because the result is meaningless without having one of
    # the disconnected_airports
    if disconnected_airport_mandatory:
        if (
            not set(([destarp[0] for destarp in fla_tu(routes[-3:])]))
            & disconnected_airports
        ):
            continue

    # Print the last three airports in the current route
    print(routes[-3:], end="\r")

    # Create a dictionary with the first element of each tuple as key and the second element as value for all the routes
    active_parser_dict = defaultdict(list)
    for r in routes:
        active_parser_dict[r[0]].append(r[1])

    # Make a copy of 'active_parser_dict' to have one for each connection combination
    copyofairportdict = active_parser_dict.copy()

    # Create an empty nested dictionary to store the airport variations
    airportvariations = nested_dict()

    # Find all possible routes between each airport
    get_all_routes()

    # Append the active_parser_dict and an empty list to 'result_variation'
    result_variation.append([active_parser_dict.copy(), []])

    # Find all the destinations for each airport (dummydict values are being excluded)
    for ap2check in [x[-1][:-1] for x in tuple(fla_tu(airportvariations))]:
        result_variation[-1][-1].append(ap2check)

# List of indices of valid connections with all airports (must contain all 18 airports)
valid_conections_with_all_airports = [
    wq
    for wq, ra in enumerate(result_variation)
    if len(set([h[0] for h in fla_tu([ro for ro in ra[-1] if ro[0] == startairport])]))
    == len(airports)
]

# Empty list to store all valid combinations (must include all airports)
single_passed_route = []

# Append the single passed routes to the list
for wita in valid_conections_with_all_airports:
    single_passed_route.append(result_variation[wita])

# Sort the final results in descending order based on the length of the route
# The first airport must be LGA, and the last one must not be LGA
final_results_sorted = [
    [rr for rr in r[-1] if rr[0] == startairport and rr[-1] != startairport]
    for r in single_passed_route
]
finalresultdicts = [
    {ux[-1]: ux for ux in kk}
    for kk in [
        list(reversed(sorted(f, key=lambda x: len(x)))) for f in final_results_sorted
    ]
]

# Sort the final results based on the length of the route and the index
# The shorter, the better (less connections between each flight)
final_ind_sorted_all = sorted(
    [(i, max([len(v) for k, v in q.items()])) for i, q in enumerate(finalresultdicts)],
    key=lambda x: x[-1],
)

# Loop through the list of indices in reverse order along with their corresponding positions
# to print all possible combination that would work, starting with the worst one (most connections
# between flights)
for place, indexplace in reversed(
    list(
        zip(
            [q + 1 for q in list(range(len(final_ind_sorted_all)))],
            final_ind_sorted_all,
        )
    )
):
    # Print a banner indicating the current position in the list
    print(f'{"█" * 10} {place}. Place {"█" * 10}')

    # Get the index corresponding to the current position in the list
    final_ind_sorted = final_ind_sorted_all[place - 1][0]
    right_answer = single_passed_route[final_ind_sorted][0][startairport]

    # Get all routes of the valid answer and Pretty-print them
    allright_routes = finalresultdicts[final_ind_sorted]
    pprint(allright_routes)

    # Print a banner indicating the starting airport for the right answer
    print("█ ", end="")
    for goodairport in right_answer:
        print(f"LGA:{goodairport} █ ", end="")
    print(f'\n{"█" * 26}\n{"█" * 26}')

# ██████████ 4. Place ██████████
# {'BGI': ('LGA', 'SAN', 'EYW', 'LHR', 'SFO', 'DSM', 'ORD', 'BGI'),
#  'BUD': ('LGA', 'TLV', 'DEL', 'CDG', 'BUD'),
#  'CDG': ('LGA', 'TLV', 'DEL', 'CDG'),
#  'DEL': ('LGA', 'TLV', 'DEL'),
#  'DOH': ('LGA', 'TLV', 'DEL', 'DOH'),
#  'DSM': ('LGA', 'SAN', 'EYW', 'LHR', 'SFO', 'DSM'),
#  'EWR': ('LGA', 'EWR'),
#  'EYW': ('LGA', 'SAN', 'EYW'),
#  'HND': ('LGA', 'EWR', 'HND'),
#  'ICN': ('LGA', 'EWR', 'HND', 'ICN'),
#  'JFK': ('LGA', 'EWR', 'HND', 'JFK'),
#  'LHR': ('LGA', 'SAN', 'EYW', 'LHR'),
#  'ORD': ('LGA', 'SAN', 'EYW', 'LHR', 'SFO', 'DSM', 'ORD'),
#  'SAN': ('LGA', 'SAN'),
#  'SFO': ('LGA', 'SAN', 'EYW', 'LHR', 'SFO'),
#  'SIN': ('LGA', 'TLV', 'DEL', 'CDG', 'SIN'),
#  'TLV': ('LGA', 'TLV')}
# █ LGA:EWR █ LGA:SAN █ LGA:TLV █
# ██████████████████████████
# ██████████████████████████
# ██████████ 3. Place ██████████
# {'BGI': ('LGA', 'EYW', 'LHR', 'SFO', 'DSM', 'ORD', 'BGI'),
#  'BUD': ('LGA', 'TLV', 'DEL', 'CDG', 'BUD'),
#  'CDG': ('LGA', 'TLV', 'DEL', 'CDG'),
#  'DEL': ('LGA', 'TLV', 'DEL'),
#  'DOH': ('LGA', 'TLV', 'DEL', 'DOH'),
#  'DSM': ('LGA', 'EYW', 'LHR', 'SFO', 'DSM'),
#  'EWR': ('LGA', 'EWR'),
#  'EYW': ('LGA', 'EYW'),
#  'HND': ('LGA', 'EWR', 'HND'),
#  'ICN': ('LGA', 'EWR', 'HND', 'ICN'),
#  'JFK': ('LGA', 'EWR', 'HND', 'JFK'),
#  'LHR': ('LGA', 'EYW', 'LHR'),
#  'ORD': ('LGA', 'EYW', 'LHR', 'SFO', 'DSM', 'ORD'),
#  'SAN': ('LGA', 'EYW', 'LHR', 'SFO', 'SAN'),
#  'SFO': ('LGA', 'EYW', 'LHR', 'SFO'),
#  'SIN': ('LGA', 'TLV', 'DEL', 'CDG', 'SIN'),
#  'TLV': ('LGA', 'TLV')}
# █ LGA:EWR █ LGA:EYW █ LGA:TLV █
# ██████████████████████████
# ██████████████████████████
# ██████████ 2. Place ██████████
# {'BGI': ('LGA', 'LHR', 'SFO', 'DSM', 'ORD', 'BGI'),
#  'BUD': ('LGA', 'TLV', 'DEL', 'CDG', 'BUD'),
#  'CDG': ('LGA', 'TLV', 'DEL', 'CDG'),
#  'DEL': ('LGA', 'TLV', 'DEL'),
#  'DOH': ('LGA', 'TLV', 'DEL', 'DOH'),
#  'DSM': ('LGA', 'LHR', 'SFO', 'DSM'),
#  'EWR': ('LGA', 'EWR'),
#  'EYW': ('LGA', 'LHR', 'SFO', 'SAN', 'EYW'),
#  'HND': ('LGA', 'EWR', 'HND'),
#  'ICN': ('LGA', 'EWR', 'HND', 'ICN'),
#  'JFK': ('LGA', 'EWR', 'HND', 'JFK'),
#  'LHR': ('LGA', 'LHR'),
#  'ORD': ('LGA', 'LHR', 'SFO', 'DSM', 'ORD'),
#  'SAN': ('LGA', 'LHR', 'SFO', 'SAN'),
#  'SFO': ('LGA', 'LHR', 'SFO'),
#  'SIN': ('LGA', 'TLV', 'DEL', 'CDG', 'SIN'),
#  'TLV': ('LGA', 'TLV')}
# █ LGA:EWR █ LGA:LHR █ LGA:TLV █
# ██████████████████████████
# ██████████████████████████
# ██████████ 1. Place ██████████
# {'BGI': ('LGA', 'SFO', 'DSM', 'ORD', 'BGI'),
#  'BUD': ('LGA', 'TLV', 'DEL', 'CDG', 'BUD'),
#  'CDG': ('LGA', 'TLV', 'DEL', 'CDG'),
#  'DEL': ('LGA', 'TLV', 'DEL'),
#  'DOH': ('LGA', 'TLV', 'DEL', 'DOH'),
#  'DSM': ('LGA', 'SFO', 'DSM'),
#  'EWR': ('LGA', 'EWR'),
#  'EYW': ('LGA', 'SFO', 'SAN', 'EYW'),
#  'HND': ('LGA', 'EWR', 'HND'),
#  'ICN': ('LGA', 'EWR', 'HND', 'ICN'),
#  'JFK': ('LGA', 'EWR', 'HND', 'JFK'),
#  'LHR': ('LGA', 'SFO', 'SAN', 'EYW', 'LHR'),
#  'ORD': ('LGA', 'SFO', 'DSM', 'ORD'),
#  'SAN': ('LGA', 'SFO', 'SAN'),
#  'SFO': ('LGA', 'SFO'),
#  'SIN': ('LGA', 'TLV', 'DEL', 'CDG', 'SIN'),
#  'TLV': ('LGA', 'TLV')}
# █ LGA:EWR █ LGA:SFO █ LGA:TLV █
# ██████████████████████████
# ██████████████████████████
