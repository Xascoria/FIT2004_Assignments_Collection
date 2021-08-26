## Name:       Pang Siang Cheng
## ID:         30857708
## Assignment: FIT2004 Assignment 2

"""
weekly_income is a list of non-negative integers, where weekly_income[i] is the amount of
money you will earn working as a personal trainer in week i.

competitions is a list of tuples, each representing a sporting competition. Each tuple contains
3 non-negative integers, (start_time, end_time, winnings).

start_time is the is the week that you will need to begin preparing for this competition.

end_time is the last week that you will need to spend recovering from this competition.

winnings is the amount of money you will win if you compete in this competition.

returns an integer, which is the maximum amount of money that can be earned.

High level description: The function sort the competitions with the start date, then, create a memorization array
that store the highest amount of money that can be made up to week[i]. Loop through both the competitions and the
weekly income and put the higher amount in week[i], then return week[-1] which would be the highest.

Complexities:
N: total number of elements in weekly_income and competitions combined.
Best-case Time Complexity:  O(N)
Worst-case Time Complexity: O(N)
Space Complexity:           O(N)
Auxiliary Space complexity: O(N)
"""
def best_schedule(weekly_income, competitions):
	# Edge case
	if len(weekly_income) == 0:
		return 0

	# Half counting sort the competitions according to their start time
	# Since the columns of num = length of weekly_income = a, and the length of columns = length of competitions = b
	# And a + b = N
	# Thus this has a constant Time and Space complexity of O(N) and Aux Space of O(N) for the counting columns

	# Start by setting the columns
	competition_sort = []
	for i in range(len(weekly_income)):
		competition_sort.append([])

	# Fill columns with tuples
	for i in competitions:
		competition_sort[i[0]].append(i)

	# Dynamic Programming
	# Replace previous memory in memorization if new actions make more money
	# Time complexity is constant O(N) = O(a+b) since its O(a) for the incomes and O(b) for the inner loop

	# Highest income after that day in the week
	# Aux-space complexity increased by O(N)
	memorization = [0] * (len(weekly_income) + 1)

	# For every week
	for i in range(1, len(memorization)):
		# Calculate income for this week
		income_today = weekly_income[i-1]
		# If working today will have a higher income, then work
		if income_today + memorization[i-1] > memorization[i]:
			memorization[i] = income_today + memorization[i-1]

		# Check all the competitions that starts today
		for event in competition_sort[i-1]:
			starting_week = event[0]
			ending_week = event[1]
			# starting_week doesn't need to -1 because we want to add the week before the contest start
			# and the real starting_week in memo is starting_week + 1, which is offsetted
			if starting_week < len(memorization) and ending_week+1 < len(memorization) and event[2] + memorization[starting_week] > memorization[ending_week+1]:
				memorization[ending_week+1] = event[2] + memorization[starting_week]

	# Return the end, which will be the highest amount of money earned
	return memorization[-1]


"""
profit is a list of lists. All interior lists are length n. Each interior list represents a different day. 
profit[d][c] is the profit that the salesperson will make by working in city c on day d.

quarantine_time is a list of non-negative integers. quarantine_time[i] is the number of
days city i requires visitors to quarantine before they can work there.

home is an integer between 0 and n-1 inclusive, which represents the city that the salesperson
starts in. They can start working in this city without needing to quarantine on the first day.
If they leave and come back later, they will need to quarantine

High level description: Create two memorization table to store maximum amount of money that the salesperson can make
at that point before and after quarantine, start from the bottom (so after quarantine have to stay and before quarantine
makes no money) then, for each day at each city, calculate which paths (left, stay, right) earns the most money.
Return the result after reaching the first day.

Complexities:
N: the number of cities
D: the number of days
Best-case Time Complexity:  O(ND)
Worst-case Time Complexity: O(ND)
Space Complexity:           O(ND)
Auxiliary Space complexity: O(ND)
"""
def best_itinerary(profit, quarantine_time, home):
	# Edge case
	if len(profit) == 0 or len(quarantine_time) == 0:
		return 0

	# Memorizations:
	# Store the highest amount of money that you can possibly make in a particular day and city
	# Before you start quarantine (just arrive) and after you finish quarantine
	# Time/Space complexity is O(2ND) = O(ND)
	after_quar_memo = []
	before_quar_memo = []

	# Put a list of city and set all their default values to 1 every day
	for i in range(len(profit)):
		after_quar_memo.append([-1] * len(quarantine_time))
		before_quar_memo.append([-1] * len(quarantine_time))

	# Dynamic Programming
	# Start by setting up the base case for the last days, which is usually
	# Time/Space Complexity is O(2ND) = O(ND) as it checks for every city every day, twice

	# Starting from the last day to the first one
	for day in range(len(profit) - 1, -1, -1):
		# For each city
		for city in range(len(quarantine_time)):
			# Setting up bases cases in the last day
			if day == len(profit) - 1:
				# It's the last day so you can only make money if you stay
				after_quar_memo[day][city] = profit[day][city]
				# Same with before quarantining, if somehow the city doesn't need quarantine
				before_quar_memo[day][city] = profit[day][city] if (quarantine_time[city] == 0) else 0
			else:
				# Consider all 3 directions:

				# Staying at the city
				# After quarantine - money today = income + money made after tmr
				if after_quar_memo[day+1][city] + profit[day][city] > after_quar_memo[day][city]:
					after_quar_memo[day][city] = after_quar_memo[day+1][city] + profit[day][city]
				# Before quarantine - if quarantine last till the end, no money made
				if len(profit) - day <= quarantine_time[city]:
					before_quar_memo[day][city] = 0
				else:
					# If quarantine end before the end, then made the amount stored in after quarantine on the day quar end
					if before_quar_memo[day][city] < after_quar_memo[day + quarantine_time[city]][city]:
						before_quar_memo[day][city] = after_quar_memo[day + quarantine_time[city]][city]

				# Move to the city on the left
				# Can't be already the leftest city
				if city != 0:
					# If city on the left makes money, go to the left for both before and after quar
					if before_quar_memo[day + 1][city - 1] > after_quar_memo[day][city]:
						after_quar_memo[day][city] = before_quar_memo[day + 1][city - 1]
					if before_quar_memo[day + 1][city - 1] > before_quar_memo[day][city]:
						before_quar_memo[day][city] = before_quar_memo[day + 1][city - 1]

				# Move to the city on the left
				# Can't be already the rightest city
				if city != len(quarantine_time) - 1:
					# If city on the right makes money, go to the left for both before and after quar
					if before_quar_memo[day + 1][city + 1] > after_quar_memo[day][city]:
						after_quar_memo[day][city] = before_quar_memo[day + 1][city + 1]
					if before_quar_memo[day + 1][city + 1] > before_quar_memo[day][city]:
						before_quar_memo[day][city] = before_quar_memo[day + 1][city + 1]

	# Return the result, since it's given that you are quarantined at the start, use the result of day 1 from
	# After quarantine at home city
	return after_quar_memo[0][home]

