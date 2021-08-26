# Name: Pang Siang Cheng
# Student ID: 30857708
# Content: FIT2004 S1/2021: Assignment 1

import math
from typing import Tuple, List

"""
transactions: unsorted list of integers
t: non-negative int, representing time
return Tuple(best_t, count) where the interval of best_t + t has the most elements and count is the number of elements in the interval

High level description: The function takes the inputs, first calculate the highest number of digits in the list, then,
radix sort the list, then it starts by putting 2 pointers on the sorted list, since we know that the current interval must 
end after the previous interval's ending, we can move both pointers at the same time until one of them reach the end first.

n is the number of elements in transactions
k is the greatest number of digits in any element in transactions
Worst-case Time Complexity is O(kn)
Best-case Time Complexity is also O(kn)
case Space complexity is O(n)
Auxiliary space complexity is O(n), the function is not in place
"""
def best_interval(transactions: List[int], t: int) -> Tuple[int, int]:
	# Handling edge case that would cause an error down the line
	# Probably not necessary but just in case
	if len(transactions) == 0:
		return (0, 0)

	# Calculate number with the most digits within the array, which is used as upper limit for the digits in the radix sort
	# Time Complexity is O(n)
	# Space Complexity is O(1)
	largest_num = 0
	for i in range(0, len(transactions)):
		if transactions[i] > largest_num:
			largest_num = transactions[i]
	# Note: this is also the value of k
	# Complexity is O(k)
	if (largest_num) == 0:
		digits = 1
	else:
		digits = int(math.log10(largest_num)) + 1

	# Create an array of arrays of length 10 to be used as the columns for the radix sort
	# TIme Complexity is O(10) -> O(1)
	# Since the columns are going to include all the indexes later on, space complexity is O(n)
	radix_sort_columns = []
	for i in range(10):
		radix_sort_columns.append([])

	# Implementation of radix sort
	# Total complexity of this part is O(kn)

	# Create a temporary array with size n that is going to be used to transcript sorting result from indexes
	# Space Complexity is O(n)
	temporary_arr = [0] * len(transactions)

	# Since everything inside the loop is repeated for each digit
	# And the total complexity inside the loop is O(n)
	# This part has a time complexity of O(kn)
	for i in range(digits):
		# Calculate the current digit for each item in the list
		# And add to the appropriate radix sort columns
		# Complexity is O(n)
		for j in range(len(transactions)):
			current_digit_value = (transactions[j] // (10**i)) % 10
			radix_sort_columns[current_digit_value].append(j)

		# Put all the elements inside an index-mapping array
		# The reason of reversing the list here before popping is because pop(0) is O(length_of_column) but pop() is O(1),
		# Therefore reversing all the lists, which add up to O(n) and the pop() within the loop will also add up to O(n)
		# Complexity is O(2n) -> O(n)
		index_arr = []
		for j in range(10):
			radix_sort_columns[j].reverse()
			while len(radix_sort_columns[j]) != 0:
				index_arr.append(radix_sort_columns[j].pop())

		# Using the mapped indexes, put the items from the original list into the temporary array
		# Then make a copy of it and overwrites transactions
		# Complexity is O(2n) -> O(n)
		for j in range(len(index_arr)):
			temporary_arr[j] = transactions[index_arr[j]]
		transactions = temporary_arr.copy()

	# Finding the best interval in the sorted list
	# Complexity is O(n)

	# Setup variables inside loops
	# Constants so space complexity is O(1)
	current_start_index = 0
	current_end_index = 0
	best_start = 0
	count = 0

	# This part has a complexity of O(n) because it will loop both current_start_index and current_end_index till one of them reach the
	# end of the array, which is n-sized, even if both reach at the same time its max O(2n) -> O(n)
	# While we haven't reach the end of transactions
	while True:
		# Get the maximum value within this interval
		max_value = transactions[current_start_index] + t
		# Within the range of the start value to the end, find the interval by finding the last number than is
		# Smaller or equal to max_value
		for i in range(current_start_index, len(transactions)):
			if transactions[i] > max_value:
				break
			else:
				current_end_index = i
		# If the new interval has more items than the previous highest
		# Update its value and also record down the best start
		if current_end_index - current_start_index + 1 > count:
			count = current_end_index - current_start_index + 1
			# This took me hours to figure it out
			# If the current start time is higher than the lowest possible start time, pick the lowest start time
			if (transactions[current_end_index] - t < transactions[current_start_index]):
				# But it still can't be negative
				if (transactions[current_end_index] - t <= 0):
					best_start = 0
				else:
					best_start = transactions[current_end_index] - t
			else:
				best_start = transactions[current_start_index]
		# End index reached the end of array
		# Every other consideration from this point onward can only be shorter
		if current_end_index == len(transactions) - 1:
			break
		current_start_index += 1
		# Start index reached the end of the array after added 1
		# Maximum of length 1, which is definitely already considered by previous items inside the array
		if current_start_index == len(transactions) - 1:
			break
		# If the starting item is same as the previous, it shouldn't be considered at all given that the previous as start
		# Will definitely be longer than the current
		while transactions[current_start_index] == transactions[current_start_index - 1]:
			current_start_index += 1

	return (best_start, count)

"""
list1: List of strings
list2: List of strings
return: A list of strings from list1 that have anagrams inside list2

High level description: start by creating a copy and sort both list in lexicographic order with their letters using counting sort,
then, counting sort on the list of the strings and DON'T reform the list, using the buckets, we radix sort each buckets, then
go through the each buckets with the 2 pointers method like question 1, add any words that have anagram to output and return it

L1: length of list1
L2: length of list2
M1: length of the longest string in list1
M2: length of the longest string in list2
Worst-case Time Complexity is O((L1 + L2) * min(M1, M2))
Best-case Time Complexity is O(L1 + L2)  if no strings from either side are the same length
Space complexity is O((L1 + L2) * min(M1, M2))
Auxiliary space complexity is O((L1 + L2) * min(M1, M2)), the function is not in place
"""
def words_with_anagrams(list1: List[str], list2: List[str]) -> List[str]:
	# These will be used to store the sorted words later
	list1_letter_sorted = [""] * len(list1)
	list2_letter_sorted = [""] * len(list2)
	list1_longest_str = 0
	list2_longest_str = 0

	# Find the longest string in both list
	# Time complexity of O(L1 + L2)
	for i in range(len(list1)):
		if len(list1[i]) > list1_longest_str:
			list1_longest_str = len(list1[i])

	for i in range(len(list2)):
		if len(list2[i]) > list2_longest_str:
			list2_longest_str = len(list2[i])

	# Here's since we know we only need to compare strings with the same length,
	# We can safely ignore any strings that have a longer length than the max length from the other list
	max_len_considered = min(list1_longest_str, list2_longest_str)

	# Sort the letters of list 1 and list 2 then put them into their new arrays respectively
	# Complexity of O(M1*L1) and O(M2*L2) to loop through every letters
	# Auxiliary Space Complexity of O((L1 + L2) * min(M1, M2))
	letter_counting = [0] * 26
	full_word = []
	for i in range(len(list1)):
		# Use counting sort to form the sorted word
		# Complexity of O(L1*min(M1, M2))
		# No need to even sort if its higher than maximum length needed to considered
		if len(list1[i]) <= max_len_considered:
			for j in range(len(list1[i])):
				letter_counting[ord(list1[i][j]) - 97] += 1

			for j in range(26):
				while letter_counting[j] > 0:
					full_word.append(chr(j + 97))
					letter_counting[j] -= 1
			list1_letter_sorted[i] = "".join(full_word)
			full_word = []

	for i in range(len(list2)):
		# Use counting sort to form the sorted word
		# Complexity of O(L2*min(M1, M2))
		# No need to even sort if its higher than maximum length needed to considered
		if len(list2[i]) <= max_len_considered:
			for j in range(len(list2[i])):
				letter_counting[ord(list2[i][j]) - 97] += 1
			for j in range(26):
				while letter_counting[j] > 0:
					full_word.append(chr(j + 97))
					letter_counting[j] -= 1
			list2_letter_sorted[i] = "".join(full_word)
			full_word = []

	# Using counting sort, sort both list inside buckets with their length using indexes
	# The buckets have aux space complexity of O(min(M1, M2)*L1) and O(min(M1, M2)*L2) respectively
	# Complexity is O(L1 + L2) to go through every strings and put their indexes inside the buckets
	list1_len_buckets = []
	list2_len_buckets = []
	# Here's since we know we only need to compare strings with the same length,
	# We can safely ignore any strings that have a longer length than the max length from the other list
	max_len_considered = min(list1_longest_str, list2_longest_str)

	# Add 1 here because we want to use the index directly to be more convenient
	for i in range(max_len_considered + 1):
		list1_len_buckets.append([])
	for i in range(max_len_considered + 1):
		list2_len_buckets.append([])

	for i in range(len(list1_letter_sorted)):
		if len(list1_letter_sorted[i]) <= max_len_considered:
			list1_len_buckets[ len(list1_letter_sorted[i]) ].append(i)
	for i in range(len(list2_letter_sorted)):
		if len(list2_letter_sorted[i]) <= max_len_considered:
			list2_len_buckets[ len(list2_letter_sorted[i]) ].append(i)

	# Radix sort every buckets since we don't really need to reform the list anyway
	# Time complexity worst case is O(L1 * min(M1,M2)) if every strings is the same length
	# Space complexity worst case is O(L1) to recreate every index buckets

	# Switch from storing number above to sort string to storing indexes (references) because of radix sort
	for i in range(26):
		letter_counting[i] = []

	# For every buckets within list 1
	for i in range(1, len(list1_len_buckets)):
		# Only sort if the bucket have more than 1 item
		if len(list1_len_buckets[i]) > 1:
			# Loop from the right to the left, since i = length of strings inside the buckets
			for j in range(i - 1, -1, -1):
				# For every item inside the bucket
				for k in range(len(list1_len_buckets[i])):
					# Get the word from sorted letters by referencing inside the bucket that's currently being looped through
					word = list1_letter_sorted[list1_len_buckets[i][k]]
					# Store the new order
					letter_counting[ord(word[j]) - 97].append(k)
				index_array = []
				# Recreate the order that the new list is supposed to be in
				for k in range(26):
					if len(letter_counting[k]) > 0:
						# Same as question 1, doing this to avoid getting to O(n) every loop instead of O(1)
						letter_counting[k].reverse()
						while len(letter_counting[k]) > 0:
							index_array.append(letter_counting[k].pop())
				# Put the indexes into their new places
				new_arr = []
				for k in range(len(index_array)):
					new_arr.append(list1_len_buckets[i][index_array[k]])
				# Replace the old list
				list1_len_buckets[i] = new_arr

	# Do the same thing with list 2
	# Time complexity: O( min(M1,M2) * L2), Space complexity: O(L2) (See explanation above)
	for i in range(1, len(list2_len_buckets)):
		if len(list2_len_buckets[i]) > 1:
			for j in range(i-1, -1, -1):
				for k in range(len(list2_len_buckets[i])):
					word = list2_letter_sorted[list2_len_buckets[i][k]]
					letter_counting[ord(word[j]) - 97].append(k)
				index_array = []
				for k in range(26):
					if len(letter_counting[k]) > 0:
						letter_counting[k].reverse()
						while len(letter_counting[k]) > 0:
							index_array.append(letter_counting[k].pop())
				new_arr = []
				for k in range(len(index_array)):
					new_arr.append(list2_len_buckets[i][index_array[k]])
				list2_len_buckets[i] = new_arr

	# Create the output
	# Time Complexity is O((L1  + L2) * min(M1, M2))
	# Additional aux space are worst case O(L1 * M1)
	output = []

	# Loop through every buckets
	for i in range(max_len_considered + 1):
		# Both buckets have to have something for the comparisons to start
		if len(list1_len_buckets[i]) != 0 and len(list2_len_buckets[i]) != 0:
			# These are used to store where the comparison are at the moment
			# This ensure that the maximum amount of comparison would be O((L1 * L2) + min(M1+M2))
			list1_ptr = 0
			list2_ptr = 0
			# If neither had reached the end yet
			while list1_ptr != len(list1_len_buckets[i]) and list2_ptr != len(list2_len_buckets[i]):
				# If they are equal, that means they are anagrams
				if list1_letter_sorted[list1_len_buckets[i][list1_ptr]] == list2_letter_sorted[list2_len_buckets[i][list2_ptr]]:
					output.append(list1[list1_len_buckets[i][list1_ptr]])
					list1_ptr += 1
				# Else if one of them are bigger advance the other ptr
				elif list1_letter_sorted[list1_len_buckets[i][list1_ptr]] > list2_letter_sorted[list2_len_buckets[i][list2_ptr]]:
					list2_ptr += 1
				else:
					list1_ptr += 1

	# Return output, duh
	# Space complexity worst case is O(L1 * M1)
	return output
