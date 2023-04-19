## My solution for this Google interview: https://www.youtube.com/watch?v=qz9tKlF431k

Resume:
```python
# These are the exisiting airport connection
[
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

# Add 3 connections ["LGA", some_other_airport] to be able to fly to every destination starting from "LGA".
# The correct result is the most economic solution (less connections between flights). 
```

```python
# Output
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
```
