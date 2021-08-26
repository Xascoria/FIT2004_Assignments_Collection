## Name: Pang Siang Cheng
##   ID: 30857708
## FIT2004 - Assignment 4

"""
Return the maximum value that you can obtain after performing at most max_trades trades.

         prices: An array where prices[i] is the value of 1L of the liquid with ID i.
starting_liquid: The ID of the liquid you arrive with. You always start with 1L of this liquid.
     max_trades: Maximum amount of trade you can participate in.
    townspeople: A list of lists. Each interior list corresponds to the trades offered by a particular person.

High level description: Using each liquid as a vertex, and the trades as edges, travel down M iterations
with Bellman-Ford, then get the maximum profit after M amount of trades

Complexities:
N: The number of liquids
T: The total number of trades available
M: Max trades
Best-case Time Complexity:  O(T * M)
Worst-case Time Complexity: O(T * M)
Space Complexity:           O(N + T)
Auxiliary Space complexity: O(N)
"""
def best_trades(prices, starting_liquid, max_trades, townspeople):
	# Create an array of adjacency lists using liquid type as vertex and price as edge
	adj_list = [[] for _ in range(len(prices))]

	# Filling the adjacency lists
	# For every person
	for i in range(len(townspeople)):
		# For every trade offer
		for j in range(len(townspeople[i])):
			trade_detail = townspeople[i][j]
			changed = False
			# If trade offer already exist in graph, use the more profitable one
			# Trade offer are stored in details of (target liquid type, pricing ratio)
			for k in range(len(adj_list[trade_detail[0]])):
				if adj_list[trade_detail[0]][k][0] == trade_detail[1]:
					changed = True
					profit_margin = (prices[trade_detail[0]]*trade_detail[2]) - prices[trade_detail[0]]
					if adj_list[trade_detail[0]][k][1] < trade_detail[2]:
						adj_list[trade_detail[0]][k] = (trade_detail[1], trade_detail[2])

			# Else add the trade offer in
			if not changed:
				adj_list[trade_detail[0]].append( (trade_detail[1], trade_detail[2]) )

	# Bellman-Ford with 2 arrays
	first_step_arr = []
	# Setup the initial contents
	# Store data (volume, money made)
	for i in range(len(prices)):
		first_step_arr.append((0,float("-inf")))

	# Start with 1 volume of starting liquid
	# Space complexity increase by O(N)
	first_step_arr[starting_liquid] = (1, prices[starting_liquid])
	second_step_arr = first_step_arr.copy()

	# For every iteration
	for i in range(max_trades):
		for j in range(len(first_step_arr)):
			# If the starting position has a known price
			if first_step_arr[j] != float("-inf"):
				# Walk down every path from that position
				for trade_detail in adj_list[j]:
					# Calculate profit through (volume of current liquid * ratio * price of new liquid)
					profit = first_step_arr[j][0] * trade_detail[1] * prices[trade_detail[0]]
					# If profit is larger then its replaced
					if second_step_arr[trade_detail[0]][1] < profit:
						second_step_arr[trade_detail[0]] = (first_step_arr[j][0] * trade_detail[1], profit)
		# Store result of this iteration to the first arr
		first_step_arr = second_step_arr.copy()

	# Return the highest profit stored in first_step_arr
	output = float("-inf")
	for i in first_step_arr:
		if i[1] > output:
			output = i[1]

	return output

## Heap implementations
# A node within the heap
class HeapNode:
	def __init__(self, value: int, heap_index: int, city_num: int, previous_city: int):
		self.value = value                       # Cost of going to this city
		self.heap_index = heap_index             # Where this node is located on the heap
		self.city_num = city_num                 # The city the current node refers to
		self.previous_node: int = previous_city  # -1 for starting city

# Min Heap
class MinHeap:
	# Initialization of a min heap
	def __init__(self):
		self.heap = [None]
		self.back_index = 0

	# Reset the heap
	def reset_heap(self):
		self.heap = [None]
		self.back_index = 0

	# Swap two nodes inside the heap
	def swap_nodes(self, index_1: int, index_2: int):
		self.heap[index_1].heap_index = index_2
		self.heap[index_2].heap_index = index_1

		self.heap[index_1], self.heap[index_2] = self.heap[index_2], self.heap[index_1]

	# Insert a new node into the heap with the given arguments
	# Return heap node reference
	def insert(self, new_value: int, city_num: int, previous_city: int) -> HeapNode:
		new_node : HeapNode = HeapNode(new_value, len(self.heap), city_num, previous_city)
		self.heap.append(new_node)
		self.back_index = len(self.heap) - 1

		while new_node.heap_index != 1 and new_node.value < self.heap[new_node.heap_index//2].value:
			self.swap_nodes(new_node.heap_index, new_node.heap_index//2)

		return new_node

	# Return the minimum heap node
	def get_min(self) -> HeapNode:
		return self.heap[1]

	# Extract minimum node and rearrange the heap
	def extract_min(self):
		head = self.heap[1]
		self.heap[1] = self.heap[self.back_index]
		self.heap[1].heap_index = 1
		new_top = self.heap[1]
		self.heap.pop()

		child_info = self.has_children(new_top.heap_index)
		while child_info[0] or child_info[1]:
			swapped = False
			if child_info[0] and child_info[1]:
				left = self.heap[new_top.heap_index * 2].value
				right = self.heap[(new_top.heap_index * 2) + 1].value
				smaller = min(left, right)
				if smaller < new_top.value:
					swapped = True
					if smaller == left:
						self.swap_nodes(new_top.heap_index, new_top.heap_index * 2)
					else:
						self.swap_nodes(new_top.heap_index, (new_top.heap_index * 2) + 1)
			elif child_info[0] and self.heap[new_top.heap_index * 2].value < new_top.value:
				self.swap_nodes(new_top.heap_index, new_top.heap_index * 2)
				swapped = True
			elif child_info[1] and self.heap[(new_top.heap_index * 2) + 1].value < new_top.value:
				self.swap_nodes(new_top.heap_index, (new_top.heap_index * 2)+1)
				swapped = True
			if not swapped:
				break
			child_info = self.has_children(new_top.heap_index)

		self.back_index -= 1
		return head

	# Lower the value of a given heap node then readjust the tree
	# Return new heap index
	def lower_value(self, heap_index, new_val: int, previous_city: int) -> int:
		target_node :HeapNode = self.heap[heap_index]
		target_node.value = new_val
		target_node.previous_node = previous_city

		while target_node.heap_index != 1 and target_node.value < self.heap[target_node.heap_index // 2].value:
			self.swap_nodes(target_node.heap_index, target_node.heap_index // 2)

		return target_node.heap_index

	# Return a pair of bool indicating if this node have a child on its left or right
	def has_children(self, index):
		left_child_exist = index * 2 < len(self.heap)
		right_child_exist = (index * 2) + 1 < len(self.heap)
		return (left_child_exist, right_child_exist)

"""
Returns a tuple containing the cost of travelling from the start city to the end city and 
the cities we need to travel to in order to achieve the cheapest cost

n       : The number of cities. The cities are numbered [0..n-1].
roads   : A list of tuples. Each tuple is of the form (u,v,w). Each tuple represents an road between 
          cities u and v. w is the cost of traveling along that road, which is always non-negative
start   : The number of the city you start at
end     : The number of the city you ended at
delivery: A tuple, containing the pick up city, drop of city, and profit from making the delivery

High level description: Perform a dijkstra from start to end and start to delivery pick up city, then, perform second
dijkstra from delivery end city to end and delivery start city, compare the cost between start-end and 
start-dev_pick_up-dev_drop_off-end minus delivery profit, and choose the shorter route.

Complexities:
R is the total number of roads
N is the total number of cities
Best-case Time Complexity:  O(R * log(N))
Worst-case Time Complexity: O(R * log(N))
Space Complexity:           O(R + log(N))
Auxiliary Space complexity: O(R + log(N))
"""
def opt_delivery(n, roads, start, end, delivery):
	# Store a references to all the nodes
	# Size of N (Bounded by R)
	graph_nodes = [None] * n
	# Bool if the city is discovered
	cities_discovered = [False] * n
	# Bool if the city is visited
	cities_visited = [False] * n
	# Create an array of adjacency lists using city as vertex and road as edge
	adj_list = [[] for _ in range(n)]
	# Create min heap to be used for the question
	min_heap : MinHeap = MinHeap()

	# Populate the adjacency lists with roads
	# Format: (target city, cost)
	for i in roads:
		adj_list[i[0]].append( (i[1], i[2]) )
		adj_list[i[1]].append( (i[0], i[2]) )

	# Bool if the end is visited
	end_visited = False
	# Bool if the delivery picked up point is visited
	delivery_visited = False
	# Dijkstra from start to the above two nodes
	graph_nodes[start] = min_heap.insert(0, start, -1)
	cities_discovered[start] = True

	# Terminate if both targets are reached
	while not end_visited or not delivery_visited:
		# Get the closest city
		closest_city: HeapNode = min_heap.get_min()
		# For every path in that city
		for path in adj_list[closest_city.city_num]:
			# If city has not been discovered
			if not cities_discovered[path[0]]:
				# Add it to the heap
				graph_nodes[path[0]] = min_heap.insert(path[1] + closest_city.value, path[0], closest_city.city_num)
				cities_discovered[path[0]] = True
			# Else if city is not been visited, and also found a closer path
			elif not cities_visited[path[0]] and graph_nodes[path[0]].value > path[1] + closest_city.value:
				# Replace the city's distance in the heap
				min_heap.lower_value(graph_nodes[path[0]].heap_index, path[1] + closest_city.value, closest_city.city_num)
		# Current city has now been visit
		cities_visited[closest_city.city_num] = True

		# Tag the target if current city is target
		if closest_city.city_num == end:
			end_visited = True
		if closest_city.city_num == delivery[0]:
			delivery_visited = True

		# Remove it from min heap
		min_heap.extract_min()

	# Backtrack to get a path from start to end
	# Start with end, add previous city to node, till reaches -1
	current_node = end
	straight_cost = graph_nodes[end].value
	straight_path_to_end = []
	while graph_nodes[current_node].previous_node != -1:
		straight_path_to_end.append(current_node)
		current_node = graph_nodes[current_node].previous_node
	straight_path_to_end.append(start)
	straight_path_to_end.reverse()

	# If the path to the delivery start point is more expensive than just going to end even with delivery
	if graph_nodes[end].value < graph_nodes[delivery[0]].value - delivery[2]:
		# Go straight to the end
		return straight_cost, straight_path_to_end

	delivery_start_cost = graph_nodes[delivery[0]].value
	# Backtrack to get a path from start to delivery pick up point
	# Start with delivery pick up point, add previous city to node, till reaches -1
	current_node = delivery[0]
	path_to_dev_start = []
	while graph_nodes[current_node].previous_node != -1:
		path_to_dev_start.append(current_node)
		current_node = graph_nodes[current_node].previous_node
	path_to_dev_start.append(start)
	path_to_dev_start.reverse()

	# Prepare for second dijkstra
	# adj_list can be reused
	graph_nodes = [None] * n
	cities_discovered = [False] * n
	cities_visited = [False] * n
	min_heap.reset_heap()

	# Same as above, use to check if end and delivery start has been visited
	end_visited = False
	delivery_visited = False

	# Second dijkstra
	# From delivery drop point to delivery start point and end
	graph_nodes[delivery[1]] = min_heap.insert(0, delivery[1], -1)
	cities_discovered[delivery[1]] = True
	# The same process as the dijkstra above
	while not end_visited or not delivery_visited:
		closest_city: HeapNode = min_heap.get_min()
		for path in adj_list[closest_city.city_num]:
			if not cities_discovered[path[0]]:
				graph_nodes[path[0]] = min_heap.insert(path[1] + closest_city.value, path[0], closest_city.city_num)
				cities_discovered[path[0]] = True
			elif not cities_visited[path[0]] and graph_nodes[path[0]].value > path[1] + closest_city.value:
				min_heap.lower_value(graph_nodes[path[0]].heap_index, path[1] + closest_city.value, closest_city.city_num)
		cities_visited[closest_city.city_num] = True
		if closest_city.city_num == end:
			end_visited = True
		if closest_city.city_num == delivery[0]:
			delivery_visited = True
		min_heap.extract_min()

	# Calculate delivery cost by shortest path to dev start, dev start to dev end and dev and to end, minus profit
	delivery_cost = delivery_start_cost + graph_nodes[delivery[0]].value + graph_nodes[end].value - delivery[2]
	# If doing the delivery cost more than just going there
	if delivery_cost > straight_cost:
		# Go directly to the end
		return straight_cost, straight_path_to_end

	# Backtrack to get the path from delivery start to delivery end
	# For this specific one, there's no reverse because we did Dijkstra from delivery end to delivery start
	# Backtrack will reverse it
	delivery_path = path_to_dev_start
	# Remove the original end point (delivery start) which will be readded during backtrack
	delivery_path.pop()
	current_node = delivery[0]
	while graph_nodes[current_node].previous_node != -1:
		delivery_path.append(current_node)
		current_node = graph_nodes[current_node].previous_node
	delivery_path.append(delivery[1])

	# Backtrack to get the path from delivery end to end
	current_node = end
	drop_off_to_end = []
	while graph_nodes[current_node].previous_node != -1:
		drop_off_to_end.append(current_node)
		current_node = graph_nodes[current_node].previous_node
	drop_off_to_end.reverse()

	# Return the cost (or profit) of delivery and the path from start to delivery end + delivery to end
	return delivery_cost, delivery_path + drop_off_to_end
