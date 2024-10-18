from pulp import *

# Plants
plants = ['P1', 'P2', 'P3']

# Warehouses
warehouses = ['W1', 'W2']

# Distribution Centers
distribution_centers = ['D1', 'D2', 'D3']

# Demand at distribution centers
demand = {'D1': 400, 'D2': 600, 'D3': 800}

# Capacity of each plant
capacity = {'P1': 600, 'P2': 500, 'P3': 700}

# Transportation costs from plants to warehouses and from warehouses to distribution centers
cost_plant_to_warehouse = {
    ('P1', 'W1'): 6, ('P1', 'W2'): 5,
    ('P2', 'W1'): 4, ('P2', 'W2'): 7,
    ('P3', 'W1'): 8, ('P3', 'W2'): 5
}

cost_warehouse_to_dc = {
    ('W1', 'D1'): 6, ('W1', 'D2'): 7, ('W1', 'D3'): 9,
    ('W2', 'D1'): 3, ('W2', 'D2'): 6, ('W2', 'D3'): 12
}

# Problem definition
problem = LpProblem("Minimize_Transportation_Cost", LpMinimize)

# Decision variables for flows from plants to warehouses
x = LpVariable.dicts("Flow_PW", [(p, w) for p in plants for w in warehouses], lowBound=0)

# Decision variables for flows from warehouses to distribution centers
y = LpVariable.dicts("Flow_WD", [(w, d) for w in warehouses for d in distribution_centers], lowBound=0)

# Objective function: Minimize total cost
problem += lpSum(cost_plant_to_warehouse[(p, w)] * x[(p, w)] for p in plants for w in warehouses) + \
           lpSum(cost_warehouse_to_dc[(w, d)] * y[(w, d)] for w in warehouses for d in distribution_centers)

# Constraints: Plant capacities
for p in plants:
    problem += lpSum(x[(p, w)] for w in warehouses) == capacity[p], f"Plant_{p}_Capacity"

# Constraints: Warehouse balance (inflow >= outflow)
for w in warehouses:
    problem += lpSum(x[(p, w)] for p in plants) >= lpSum(y[(w, d)] for d in distribution_centers), f"Warehouse_{w}_Balance"

# Constraints: Demand at distribution centers
for d in distribution_centers:
    problem += lpSum(y[(w, d)] for w in warehouses) == demand[d], f"Demand_{d}"

# Solve the problem
problem.solve()

# Output results
print("Status:", LpStatus[problem.status])
print("Total cost:", value(problem.objective))
print("Plant to Warehouse transportation:")
for p in plants:
    for w in warehouses:
        print(f"From {p} to {w} =", value(x[(p, w)]))

print("Warehouse to Distribution Center transportation:")
for w in warehouses:
    for d in distribution_centers:
        print(f"From {w} to {d} =", value(y[(w, d)]))
