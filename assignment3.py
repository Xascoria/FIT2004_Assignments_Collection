## Name: Pang Siang Cheng
## ID  : 30857708
## FIT2004 S2/2020: Assignment 3 - Tries and Trees


class Q1_Node:
	"""
	The class for a trie node for question 1

	child_ref: Store the references to its child nodes, in order of @(Stop sign), A, B, C, D

	query_res: Store the relevant information that is required to deduce the current query result for the node
	content is (frequency, index_from_parent_node, db_string_index)
	-frequency is how frequent this string is
	-index_from_parent_node store which child node this string comes from within this node's children (for lex order)
	-db_string_index is a ptr to db where it store the real stop node

	stored_string: String stored in this node, only in end nodes

	string_index: The index where the DB has stored a ref to this end node, only in end nodes

	num: Frequency of string, only in end nodes

	index_from_parent_node: The index in which the parent node store the current node
	"""
	def __init__(self, index_from_parent_node: int):
		self.child_ref = [None] * 5
		self.query_res = (0, 0, 0) # frequency, index from parent node, db string index
		self.stored_string = None
		self.string_index = 0
		self.num = 0
		self.index_from_parent_node = index_from_parent_node

class SequenceDatabase:
	"""
	Create the initial Sequence Database with the following data:

	trie_root: The root node of the trie

	list_of_strings: A list of reference to end nodes in the trie, which store the strings

	lex_compare_res: A list of boolean that will always be the same length as the list of strings, all False by default.
	It acts as a cache for a new string to compare to previous added string, which will changed to true if the newer
	string is lower on the lexicographical order.

	lex_com_res_changed: A list of indexes within lex_compare_res that was changed during adding the new string, all
	would be reverted back to False, this ensure the complexity is still within O(len(s)) since maximum amount of comparison
	while adding a new string is len(s).
	"""
	def __init__(self):
		self.trie_root: Q1_Node = Q1_Node(0)
		self.list_of_strings = []
		self.lex_compare_res = []
		self.lex_com_res_changed = []

	"""
	Store s into the instance of SequenceDatabase. 
	s: new string to be stored.
	
	High level description: Transverse down the trie using the given string, create new nodes in the trie if it doesn't
	exist yet. After reaching the bottom, start returning query results to upper layers through recursion. Query result
	contains the minimum info needed to check if a string should replaces the original query result. Do this to every
	nodes until reaching the top of the tree.
	
	Complexities: 
	len(s): Length of the string s
	Best-case Time Complexity:  O(len(s))
	Worst-case Time Complexity: O(len(s))
	Space Complexity:           O(len(s))
	Auxiliary Space complexity: O(len(s))
	"""
	def addSequence(self, s: str):
		# Add stop sign(@) to the end of string, which will be used when inserted into the trie
		# Complexity of O(len(s) + 1) -> O(len(s))
		string_with_stopped = s + "@"

		# Start the recursive auxiliary function with the root note and other arguments
		# Time and Space Complexity of O(len(s)) since the function will recursively call itself len(s) times.
		self.recursive_aux(0, self.trie_root, string_with_stopped, s)

		# Revert all the True in the lex comparison cache to false
		# Worst time and space complexity is O(len(s)), when every single node's query results on the way up is changed.
		while len(self.lex_com_res_changed) != 0:
			x = self.lex_com_res_changed.pop()
			self.lex_compare_res[x] = False

	## Recursive auxiliary helper function for addSequence
	## A complexity of O(len(string_with_stop)) to iterate through a trie to reach the end node
	def recursive_aux(self, current_layer: int, parent_node: Q1_Node, string_with_stop: str, org_string: str):
		# Base case
		# When it's already after the end of the string
		if current_layer == len(string_with_stop):
			# The end node have a num value of 0, which means that it's a new string that have not been in the DB
			if parent_node.num == 0:
				# Record down the string
				# O(len(s)) to duplicate the string
				parent_node.stored_string = org_string
				# Add the node reference to the list of end nodes within the database
				# And also record where this node if within that list
				parent_node.string_index = len(self.list_of_strings)
				self.list_of_strings.append(parent_node)
				# Comparison cache added new False for the current string
				# This slot won't be used until at least adding the next string (Can't compare with yourself)
				self.lex_compare_res.append(False)
			# Increase end node count by 1
			parent_node.num += 1
			# Return the query result to the parent node
			# With (frequency of s, index in parent's node, and s's end node's index in the db references storage)
			parent_node.query_res = (parent_node.num, parent_node.index_from_parent_node, parent_node.string_index)
			return parent_node.query_res
		else:
			# Not base case
			# Find the child index on where the next index(layer) at string s is.
			child_index = ord(string_with_stop[current_layer]) - 64
			# If the Trie current have no child at that position, create one
			if parent_node.child_ref[child_index] is None:
				parent_node.child_ref[child_index] = Q1_Node(child_index)
			# Get the result of recursion for the next layer
			res = self.recursive_aux(current_layer + 1, parent_node.child_ref[child_index], string_with_stop, org_string)
			# If the new string has a higher frequency than the current query result
			if res[0] > parent_node.query_res[0]:
				# The query result is changed
				parent_node.query_res = res
			# Else if they have the same frequency
			elif res[0] == parent_node.query_res[0]:
				# And the cache result says that the string in the query is lexicographically higher than the new string
				if self.lex_compare_res[parent_node.query_res[2]]:
					# Change the query result
					parent_node.query_res = res
				# But the new recursion result comes from a node that is lexicographical lower in order(determined via index)
				# The query result is also changed
				elif res[1] < parent_node.query_res[1]:
					# This ensure that comparison at higher layers of the trie will automatically knows if a comparison
					# already took place between the new string and a specific string stored in the DB
					self.lex_compare_res[parent_node.query_res[2]] = True
					# Added into the list of changed lex (To be reverted efficiently for the next string after this)
					self.lex_com_res_changed.append(parent_node.query_res[2])
					# Change the query result
					parent_node.query_res = res
			# Return query result, however, index_from_parent_node is updated to use the current node's to check
			# lexicographical order compare to its siblings in the layer above
			return (parent_node.query_res[0], parent_node.index_from_parent_node, parent_node.query_res[2])

	"""
	q: String to be queried
	query(q) return a string with the following properties:
	- Have q as a prefix
	- Have a higher frequency in the database than any other string with q as a prefix
	- If two or more strings with prefix q are tied for most frequent, return the lexicographically least of them
	- If no such string exists, query should return None.
	
	High level description: Transverse down the trie using the given string, then get the query result that is already
	stored at the node. If transverse isn't possible (no such string) return None
	
	Complexities: 
	len(q): Length of the string q
	Best-case Time Complexity:  O(1)
	Worst-case Time Complexity: O(len(q))
	Space Complexity:           O(len(q))
	Auxiliary Space complexity: O(1)
	"""
	def query(self, q):
		# Start with the root node
		current_node = self.trie_root
		# For every characters within string q
		for i in range(len(q)):
			# If the current node doesn't have this character as a child root (No prefix in trie), return immediately
			if current_node.child_ref[ord(q[i]) - 64] is None:
				return None
			# Else move to that node
			current_node = current_node.child_ref[ord(q[i]) - 64]

		# After reaching the final char of q
		# If the frequency is 0 (Default, no string in DB), return None
		if current_node.query_res[0] == 0:
			return None
		# Else return the string stored at query result
		return self.list_of_strings[current_node.query_res[2]].stored_string

"""
The class for a trie node for question 2

branches: Store a list of indexes of prefixes where the prefix end at this current node within the trie

child_ref: Store the references to the children nodes, None if none exist
"""
class Q2_Node:
	def __init__(self):
		self.branches = []
		self.child_ref = [None] * 5


class OrfFinder:
	"""
	Create the initial Orf Finder with the inputted string genome

	High level description: Create a suffix trie with the input, and then store where each suffix end at the nodes

	Complexities:
	N: Length of the string genome
	Best-case Time Complexity:  O(N^2)
	Worst-case Time Complexity: O(N^2)
	Space Complexity:           O(N^2)
	Auxiliary Space complexity: O(N^2)
	"""
	def __init__(self, genome: str):
		# Store an instance of the orignal string
		self.org_str = genome
		# Create root node
		self.root_node = Q2_Node()

		# Add stop sign (@) for used in the suffix trie
		# Complexity of O(N)
		stopped = genome + "@"
		# Create the suffix trie
		# For every suffixes, insert suffix into the trie
		# Space/Time Complexity of O(N^2)
		for i in range(len(stopped)):
			self.recursive_aux(i, stopped, self.root_node)

	## Recursion helper method for adding new string into the trie
	## Space/Time Complexity of O(N)
	def recursive_aux(self, current_index: int, genome: str, parent_node: Q2_Node):
		# Base case
		# If it's end of the string, add the previous index into the node's branch, then start returning
		if current_index == len(genome):
			parent_node.branches.append(current_index-1)
			return current_index-1
		else:
		# If it's not the end of the string
			# If the current child slot corresponded to the character is empty
			# Create a new node
			child_index = ord(genome[current_index]) - 64
			if parent_node.child_ref[child_index] is None:
				parent_node.child_ref[child_index] = Q2_Node()
			# Recursively call to add the rest of the string
			res = self.recursive_aux(current_index +1, genome, parent_node.child_ref[child_index])
			# Save new index at the parent
			parent_node.branches.append(res-1)
			# Return the new index
			return res-1

	"""
	find returns a list of strings. This list contains all the substrings of genome which have start
	as a prefix and end as a suffix. start and end must not overlap in the substring.
	
	High level description: Transverse down the suffix trie with both the prefix and the suffix. Compare the indexes
	stored at both place, and if a prefix's index comes before a suffix's index minus len(suffix) to get suffix's start,
	then get the substring from the original string and append it into the output.

	Complexities:
	len(start) = length of prefix
	len(end) = length of suffix
	U = length of output
	N: Length of the string genome
	Best-case Time Complexity:  O(1)
	Worst-case Time Complexity: O(U + len(start) + len(end)) -> (O(N^2)) 
	Space Complexity:           O(U + len(start) + len(end))
	Auxiliary Space complexity: O(U)
	"""
	def find(self, start: str, end: str):
		# First create the output list
		output = []
		# Get the root node
		current_node = self.root_node
		# Traverse down the trie with the prefix
		# Complexity of O(len(start))
		for i in range(len(start)):
			# If the prefix is not even in the trie, just return empty list
			if current_node.child_ref[ord(start[i]) - 64] is None:
				return output
			current_node = current_node.child_ref[ord(start[i]) - 64]
		# Get the list of indexes that the prefix is in
		prefix_branch = current_node.branches
		# Switch back to the root node for the suffix
		current_node = self.root_node
		# Traverse down the trie with the suffix
		# Complexity of O(len(end))
		for i in range(len(end)):
			# If the suffix is not even in the trie, just return empty list
			if current_node.child_ref[ord(end[i]) - 64] is None:
				return output
			current_node = current_node.child_ref[ord(end[i]) - 64]
		# Get the list of indexes that the suffix is in
		suffix_branch = current_node.branches

		# Set suffix end pointer to -1, which is the stopping point to check the suffixes, any indexes before the pointer
		# Is guaranteed to be larger because it is bigger than the previous prefix in the sorted prefix indexes list
		# Time/Space Complexity of O(U)
		suffix_end_ptr = -1
		# For every prefixes
		for i in range(len(prefix_branch)):
			# For every suffix that needed to be checked
			for j in range(len(suffix_branch)-1, suffix_end_ptr, -1):
				# If the suffix is indeed after the prefix
				if prefix_branch[i] < suffix_branch[j] + 1 - len(end):
					# Add the substring to the output
					output.append(self.org_str[prefix_branch[i] - len(start) + 1: suffix_branch[j] + 1])
				# Else that the suffix is now before/within the prefix
				else:
					# Set new stop point
					suffix_end_ptr = j
					break
			# If all suffix is already exhausted by this point, just return the output
			if suffix_end_ptr == len(suffix_branch) - 1:
				return output

		# Return the output after all the substrings are added.
		return output
