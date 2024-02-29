import sched
import comedian
import demographic
import ReaderWriter
import timetable
import random
import math

class Scheduler:

	days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

	def __init__(self,comedian_List, demographic_List):
		self.comedian_List = comedian_List
		self.demographic_List = demographic_List

	#Using the comedian_List and demographic_List, the this class will create a timetable of slots for each of the 5 work days of the week.
	#The slots are labelled 1-5, and so when creating the timetable, they can be assigned as such:
	#	timetableObj.addSession("Monday", 1, comedian_Obj, demographic_Obj, "main")
	#This line will set the session slot '1' on Monday to a main show with comedian_obj, which is being marketed to demographic_obj.
	#Note here that the comedian and demographic are represented by objects, not strings.
	#The day (1st argument) can be assigned the following values: "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
	#The slot (2nd argument) can be assigned the following values: 1, 2, 3, 4, 5 in Task 1 and 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 in Tasks 2 and 3.
	#Comedian (3rd argument) and Demographic (4th argument) can be assigned any value, but if the comedian or demographic are not in the original lists,
	#	your solution will be marked incorrectly.
	#The final, 5th argument, is the show type. For Task 1, all shows should be "main". For Tasks 2 and 3, you should assign either "main" or "test" as the show type.
	#In Tasks 2 and 3, all shows will either be a 'main' show or a 'test' show

	#demographic_List is a list of Demographic objects. A Demographic object, 'd' has the following attributes:
	# d.reference  - the reference code of the demographic
	# d.topics - a list of strings, describing the topics that the demographic like to see in their comedy shows e.g. ["Politics", "Family"]

	#comedian_List is a list of Comedian objects. A Comedian object, 'c', has the following attributes:
	# c.name - the name of the Comedian
	# c.themes - a list of strings, describing the themes that the comedian uses in their comedy shows e.g. ["Politics", "Family"]

	#For Task 1:
	#Keep in mind that a comedian can only have their show marketed to a demographic
	#	if the comedian's themes contain every topic the demographic likes to see in their comedy shows.
	#Furthermore, a comedian can only perform one main show a day, and a maximum of two main shows over the course of the week.
	#There will always be 25 demographics, one for each slot in the week, but the number of comedians will vary.
	#In some problems, demographics will have 2 topics and in others 3 topics.
	#A comedian will have between 3-8 different themes.

	#For Tasks 2 and 3:
	#A comedian can only have their test show marketed to a demographic if the comedian's themes contain at least one topic
	#	that the demographic likes to see in their comedy shows.
	#Comedians can only manage 4 hours of stage time a week, where main shows are 2 hours and test shows are 1 hour.
	#A Comedian cannot be on stage for more than 2 hours a day.

	#You should not use any other methods and/or properties from the classes, these five calls are the only methods you should need.
	#Furthermore, you should not import anything else beyond what has been imported above.
	#To reiterate, the five calls are timetableObj.addSession, d.reference, d.topics, c.name, c.themes

#------------------------------------------------- TASK 1 ---------------------------------------------------------------------------------------------

	# TASK 1 PREAMBLE:
	#	This solution to task 1 uses the Backtracking Search algorithm to assign (comedian, demographic) pair values to the slot variables
	# satisfying the constraints of the task. The algorithm makes use of Least Constraining Value heuristics when choosing the order of
	# values to try for each variable, this reduces the runtime of the algorithm significantly. As the constraints per day are simply the total
	# shows each comedian performs per day and the total overall, by assigning slots in chronological order, this is actually MRV or "Fail-First"
	# and so simply taking each slot in order is the most efficient way to choose variables to assign. It stores all the remaining demoTypePairs, 
	# as a complete solution will always contain exactly one of each, and also the number of shows each comedian is performing in each day and 
	# in total over the week. These avoid recalculating the same information over and over again and instead simply requires the lists to
	# be updated in constant time every time an assignment is made or fails.

	demosRemaining = list()
	comedianShows = dict()

#	This method should return a timetable object with a schedule that is legal according to all constraints of Task 1.
	def createSchedule(self):
	#	Do not change this line
		timetableObj = timetable.Timetable(1)

	#	Here is where you schedule your timetable
		self.demosRemaining = list()
		self.comedianShows = dict()

	#	Sort the comedians by the number oof themes they cover, this should help find a solution faster.
		self.comedian_List.sort(key=self.countThemes, reverse = True)
	#	Store all remaining demos so that we don't have to calculate them each time.
		self.demosRemaining = [a for a in self.demographic_List]
	#	Store all current comedian shows per day and week total so that we don't have to keep calculating them.
		self.comedianShows = {c : {"Monday":0,"Tuesday":0,"Wednesday":0,"Thursday":0,"Friday":0,"Total":0} for c in self.comedian_List}

	#	Find a working schedule using a Backtracking algorithm
		schedule = self.recursiveBacktrack1 ({	"Monday" 	: [[], [], [], [], []],
									 			"Tuesday" 	: [[], [], [], [], []],
									  			"Wednesday" : [[], [], [], [], []],
									   			"Thursday" 	: [[], [], [], [], []],
									    		"Friday" 	: [[], [], [], [], []]
											})
	#	If the schedule = False then the algorithm exhaustively proved the task was not possible
		if schedule == False:
			print ("No valid assignment exists")
			return timetableObj

	#	Take the schedule produced by the backtrackSearch and add it to the timetableObj
		for day in self.days:
			for slot in range (0, 5):
				timetableObj.addSession (day, slot+1, schedule[day][slot][0], schedule[day][slot][1], "main")

	#	Do not change this line
		return timetableObj

	def recursiveBacktrack1 (self, schedule):
		if self.assignmentComplete1 (schedule):
			return schedule

	#	Find the next variable to assign: the next empty slot
		(day, slot) = self.selectUnassignedVariable1 (schedule)

		for (comedian, demographic) in self.orderDomainValues1 ():
			if self.consistent1 (day, comedian):
			#	Update the comedianHours and remaining demoTypePairs
			#	Add the value to the schedule slot.
				self.comedianShows[comedian][day] += 1
				self.comedianShows[comedian]["Total"] += 1
				self.demosRemaining.remove(demographic)
				schedule[day][slot] = [comedian, demographic]

			# 	If successful, return the schedule all the way back up to the initial call
				if self.recursiveBacktrack1 (schedule) != False:
					return schedule

			#	If the assignment failed, undo the changes to the comedianHours and demoTypePairs
			#	Also remove the value assignment from the schedule.
				self.comedianShows[comedian][day] -= 1
				self.comedianShows[comedian]["Total"] -= 1
				self.demosRemaining.append(demographic)
				schedule[day][slot] = []

			#	Now try the next value in the domain

	#	If all values in the domain fail, return False to indicate 
	#	the previous assignment was not possible
		return False

	def assignmentComplete1 (self, schedule):
	#	Check all slots are non-empty
		for day in self.days:
			for slot in range(0, 5):
				if schedule[day][slot] == []:
					return False
		return True

#	Choose variables in chronological order, no heuristics used.
	def selectUnassignedVariable1 (self, schedule):
	#	Check the slots in order and return the first one found to be empty
		for day in self.days:
			for slot in range(0, 5):
				if schedule[day][slot] == []:
					return (day, slot)
		raise ValueError ("No free variables in CSP to assign, this method shouldn't have been called.")

#	Use LCV to order by the least constraining value for this variable
	def orderDomainValues1 (self):
	#	Create the cartesian product of comedians and demographics, but only the pairs which are compatible
	#	Give each an index equal to the number of shows the comedian is already performing this week; massive if already this day
		possiblePairs = [((a,b),self.comedianShows[a]["Total"]) for a in self.comedian_List for b in self.demosRemaining if self.canMarket (a, b, False)]

	#	Sort by the showsThisWeek index
		possiblePairs.sort(key=self.takeSecond)

	#	Take just the (comedian, demo) pairs from the list and return it.
		domain, h = zip(*possiblePairs)
		return domain

	def countComedianShows1 (self, day, slot, comedian, schedule):
	#	Count the number of shows the comedian is already performing this week
	#	If the comedian is already performing on this day or twice in the week,
	# they cannot again, so return a large number
		showsThisWeek = 0
		for d in self.days:
			for s in range (0, 5):
				if schedule[d][s] != [] and schedule[d][s][0] == comedian:
					if d == day and s != slot: return 255

					if showsThisWeek == 1: return 255
					else: showsThisWeek = 1

		return showsThisWeek

	def consistent1 (self, day, comedian):
	#	Check the comedian shows for the current comedian + 1
	#   remain <= 1 per day and 2 per week
		showsToday = self.comedianShows[comedian][day]
		showsThisWeek = self.comedianShows[comedian]["Total"]

		if showsToday > 0: return False
		if showsThisWeek > 1: return False

		return True

#---------------------------------------------------- TASK 2 --------------------------------------------------------------------------------------------------------------

	# TASK 2 PREAMBLE:
	#	Very similar solution to task 1, using the Backtracking Search algorithm and assigning (Comedian, Demo, Type)
	# triples to each slot in chronological order. This solution however makes use of a different heuristic (still LCV), simply the 
	# number of hours the comedian is already performing this week - the length of the show (1 hour for Test and 2 for Main), this  
	# prioritises main shows by comedians who are not already performing many shows. As in task 1 it stores all the remaining 
	# demoTypePairs, as a complete solution will always contain exactly one of each, and also the number of hours each comedian is 
	# performing in each day and in total over the week.

	demoTypePairs = list()
	comedianHours = dict()

	#Now, for Task 2 we introduce test shows. Each day now has ten sessions, and we want to market one main show and one test show
	#	to each demographic.
	#All slots must be either a main or a test show, and each show requires a comedian and a demographic.
	#A comedian can have their test show marketed to a demographic if the comedian's themes include at least one topic the demographic likes.
	#We are also concerned with stage hours. A comedian can be on stage for a maximum of four hours a week.
	#Main shows are 2 hours long, test shows are 1 hour long.
	#A comedian cannot be on stage for more than 2 hours a day.

	def createTestShowSchedule(self):
	#	Do not change this line
		timetableObj = timetable.Timetable(2)

	#	Here is where you schedule your timetable
		self.demoTypePairs = list()
		self.comedianHours = dict()

	#	Sort the comedians by the number oof themes they cover, this should help find a solution faster.
		self.comedian_List.sort(key=self.countThemes, reverse = True)
	#	Store all remaining (demo, showType) pairs so that we don't have to calculate them each time.
		self.demoTypePairs = [(a,b) for a in self.demographic_List for b in [2, 1]]
	#	Store all current comedian hours per day and week total so that we don't have to keep calculating them.
		self.comedianHours = {c : {"Monday":0,"Tuesday":0,"Wednesday":0,"Thursday":0,"Friday":0,"Total":0} for c in self.comedian_List}

	#	Find a working schedule using a Backtracking algorithm
		schedule = self.recursiveBacktrack2 ({	"Monday" 	: [[], [], [], [], [], [], [], [], [], []],
												"Tuesday" 	: [[], [], [], [], [], [], [], [], [], []],
												"Wednesday" : [[], [], [], [], [], [], [], [], [], []],
												"Thursday" 	: [[], [], [], [], [], [], [], [], [], []],
												"Friday" 	: [[], [], [], [], [], [], [], [], [], []]
											})

	#	If the schedule = False then the algorithm exhaustively proved the task was not possible
		if schedule == False:
			print ("No valid assignment exists")
			return timetableObj

	#	Take the schedule produced by the backtrackSearch and add it to the timetableObj
		for day in self.days:
			for slot in range (0, 10):
				if schedule[day][slot] != []:
					timetableObj.addSession (day, slot+1, schedule[day][slot][0], schedule[day][slot][1], "main" if schedule[day][slot][2] == 2 else "test")

	#	Do not change this line
		return timetableObj

	def recursiveBacktrack2 (self, schedule):
		if self.assignmentComplete2 (schedule):
			return schedule

	#	Find the next variable to assign: the next empty slot
		(day, slot) = self.selectUnassignedVariable2 (schedule)

		for (comedian, demographic, type) in self.orderDomainValues2 ():
			if self.consistent2 (day, comedian, type):

			#	Update the comedianHours and remaining demoTypePairs
			#	Add the value to the schedule slot.
				self.comedianHours[comedian][day] += type
				self.comedianHours[comedian]["Total"] += type
				self.demoTypePairs.remove ((demographic, type))
				schedule[day][slot] = [comedian, demographic, type]

			#	If successful, return the schedule all the way back up to the initial call
				if self.recursiveBacktrack2 (schedule) != False:
					return schedule

			#	If the assignment failed, undo the changes to the comedianHours and demoTypePairs
			#	Also remove the value assignment from the schedule.
				self.comedianHours[comedian][day] -= type
				self.comedianHours[comedian]["Total"] -= type
				self.demoTypePairs.append ((demographic, type))
				schedule[day][slot] = []

			#	Now try the next value in the domain
	
	#	If all values in the domain fail, return False to indicate 
	#	the previous assignment was not possible
		return False

	def assignmentComplete2 (self, schedule):
	#	Check all slots are non-empty
		for day in self.days:
			for slot in range(0, 10):
				if schedule[day][slot] == []:
					return False
		return True

#	Choose variables in chronological order, no heuristics used.
	def selectUnassignedVariable2 (self, schedule):
	#	Check the slots in order and return the first one found to be empty
		for day in self.days:
			for slot in range(0, 10):
				if schedule[day][slot] == []:
					return (day, slot)
		raise ValueError ("No free variables in CSP to assign, this method shouldn't have been called.")

#	Use comedianHours - showLength heuristic to order the domain of values.
	def orderDomainValues2 (self):
	#	Create the cartesian product of comedians and (demographic, type), but only the pairs which are compatible
	#	Give each an index equal to the comedianHours this week - length of the show (Test - 1 hour or Main - 2 hours)
		possibleTriples = [((a,p[0],p[1]),self.comedianHours[a]["Total"] - p[1]) for a in self.comedian_List for p in self.demoTypePairs if self.canMarket (a, p[0], p[1] == 1)]

	#	Sort by the showLength index, we want to prioritise Main shows first and comedians with fewer total hours
		possibleTriples.sort(key=self.takeSecond)

	#	Take just the (comedian, demo, type) pairs from the list and return it.
		domain, h = zip(*possibleTriples)
		return domain

	def consistent2 (self, day, comedian, type):
	#	Check the comedian hours for the current comedian + the length of the new show to be added
	#   remain <= 2 per day and 4 per week
		hoursToday = self.comedianHours[comedian][day]
		hoursThisWeek = self.comedianHours[comedian]["Total"]

		if hoursToday + type > 2: return False
		if hoursThisWeek + type > 4: return False

		return True
	#--------------------------------------------------- TASK 3 -------------------------------------------------------------------------------------------------------------


	# TASK 3 PREAMBLE: 
	# 	I was unable to reach an optimal solution for this task however the algorithm produces somewhat close to optimal solutions.
	# Again I made use of the Backtracking Search algorithm and used heuristics and orderings of the comedianList to ensure the solution
	# was found quickly and the cost of the schedule was small. Specifically, the domain is ordered by the showLength such that main shows 
	# are assigned first and then once they have been assigned, or none are available e.g the only remaining comedians for the main shows 
	# are already performing one on this day, the test shows are then assigned. The subordering of the comedians is also based on the 
	# number of valid values they appear in: if a comedian would in theory be able to perform 4 main shows for different demographics it
	# would appear before one who only matches 2 when we are considering main show assignments and with test shows we look at the number
	# of demographics we could market a test show by this comedian to.

	# In practise, this algorithm proovides the following cost solution for the 8 example problems:
	#	Problem 1: £11225
	#	Problem 2: £11325
	#	Problem 3: £12875
	#	Problem 4: £11925
	#	Problem 5: £12075
	#	Problem 6: £12675
	#	Problem 7: £11375
	#	Problem 8: £11325

	# The optimal solutions for the problems have a cost of £10050 and so while there is still much room for improvement I believe
	# this approach is on the right tracks to an optimal algorithm.

	demoTypePairs = list()
	comedianShows = dict()
	showLength = {"test" : 1, "main" : 2}
	comediansMainOrder = []
	comediansTestOrder = []

	#Theoretical Lower Bound: £10,050

	#Now, in Task 3 it costs £500 to hire a comedian for a single main show.
	#If we hire a comedian for a second show, it only costs £300. (meaning 2 shows cost £800 compared to £1000)
	#If those two shows are run on consecutive days, the second show only costs £100. (meaning 2 shows cost £600 compared to £1000)

	#It costs £250 to hire a comedian for a test show, and then £50 less for each extra test show (£200, £150 and £100)
	#If a test shows occur on the same day as anything else a comedian is in, then its cost is halved.

	#Using this method, return a timetable object that produces a schedule that is close, or equal, to the optimal solution.
	#You are not expected to always find the optimal solution, but you should be as close as possible.
	#You should consider the lecture material, particular the discussions on heuristics, and how you might develop a heuristic to help you here.

	def createMinCostSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(3)

		#Here is where you schedule your timetable
		self.demoTypePairs = list()
		self.comedianShows = dict()
		self.showLength = {"test" : 1, "main" : 2}
		self.comediansMainOrder = []
		self.comediansTestOrder = []
		
	#	Store all remaining (demo, showType) pairs so that we don't have to calculate them each time.
		self.demoTypePairs = [(a,b) for b in ["main", "test"] for a in self.demographic_List]

	#	Sort the comedians by the number of demographics they are compatible with in both Main and Test shows
		for c in self.comedian_List:
			self.comediansMainOrder.append(c)
			self.comediansTestOrder.append(c)
		self.comediansTestOrder.sort(key=self.countMainDemos, reverse = True)
		self.comediansTestOrder.sort(key=self.countTestDemos, reverse = True)
		self.comediansMainOrder.sort(key=self.countMainDemos, reverse = True)

	#	Store all current comedian shows per day and week total so that we don't have to keep calculating them. 
	# 	Comedian c is doing comedianShows[c][d][0] Test shows and comedianShows[c][d][1] Main shows on day d.
		self.comedianShows = {c : {"Monday":(0,0),"Tuesday":(0,0),"Wednesday":(0,0),"Thursday":(0,0),"Friday":(0,0),"Total":(0,0)} for c in self.comedian_List}
	
	#	Find a working schedule using a Backtracking algorithm
		schedule = self.recursiveBacktrack3 ({	"Monday" 	: [[], [], [], [], [], [], [], [], [], []],
												"Tuesday" 	: [[], [], [], [], [], [], [], [], [], []],
												"Wednesday" : [[], [], [], [], [], [], [], [], [], []],
												"Thursday" 	: [[], [], [], [], [], [], [], [], [], []],
												"Friday" 	: [[], [], [], [], [], [], [], [], [], []]
											})

	#	If the schedule = False then the algorithm exhaustively proved the task was not possible
		if schedule == False:
			print ("No valid assignment exists")
			return timetableObj

	#	Take the schedule produced by the backtrackSearch and add it to the timetableObj
		for day in self.days:
			for slot in range (0, 10):
				if schedule[day][slot] != []:
					timetableObj.addSession (day, slot+1, schedule[day][slot][0], schedule[day][slot][1], schedule[day][slot][2])

	#	Do not change this line
		return timetableObj

	def recursiveBacktrack3 (self, schedule):
		if self.assignmentComplete3 (schedule):
			return schedule

	#	Find the next variable to assign: the next empty slot
		(day, slot) = self.selectUnassignedVariable3 (schedule)

		for (comedian, demographic, type) in self.orderDomainValues3 ():
			if self.consistent3 (day, comedian, type):

			#	Update the comedianHours and remaining demoTypePairs
			#	Add the value to the schedule slot.
				self.comedianShows[comedian][day] 	  = (self.comedianShows[comedian][day][0] + 1    , self.comedianShows[comedian][day][1]) 	 if type=="test" else (self.comedianShows[comedian][day][0]    , self.comedianShows[comedian][day][1] + 1)
				self.comedianShows[comedian]["Total"] = (self.comedianShows[comedian]["Total"][0] + 1, self.comedianShows[comedian]["Total"][1]) if type=="test" else (self.comedianShows[comedian]["Total"][0], self.comedianShows[comedian]["Total"][1] + 1)
				i = self.demoTypePairs.index((demographic, type))
				self.demoTypePairs.remove ((demographic, type))
				schedule[day][slot] = [comedian, demographic, type]

			#	If successful, return the schedule all the way back up to the initial call
				if self.recursiveBacktrack3 (schedule) != False:
					return schedule

			#	If the assignment failed, undo the changes to the comedianHours and demoTypePairs
			#	Also remove the value assignment from the schedule.
				self.comedianShows[comedian][day]	  = (self.comedianShows[comedian][day][0] - 1	 , self.comedianShows[comedian][day][1]) 	 if type=="test" else (self.comedianShows[comedian][day][0]	   , self.comedianShows[comedian][day][1] - 1)
				self.comedianShows[comedian]["Total"] = (self.comedianShows[comedian]["Total"][0] - 1, self.comedianShows[comedian]["Total"][1]) if type=="test" else (self.comedianShows[comedian]["Total"][0], self.comedianShows[comedian]["Total"][1] - 1)
				self.demoTypePairs.insert (i, (demographic, type))
				schedule[day][slot] = []

			#	Now try the next value in the domain
	
	#	If all values in the domain fail, return False to indicate 
	#	the previous assignment was not possible
		return False

	def assignmentComplete3 (self, schedule):
	#	Check all slots are non-empty
		for day in self.days:
			for slot in range(0, 10):
				if schedule[day][slot] == []:
					return False
		return True

#	Choose variables in chronological order, no heuristics used.
	def selectUnassignedVariable3 (self, schedule):
	#	Check the slots in order and return the first one found to be empty
		for day in self.days:
			for slot in range(0, 10):
				if schedule[day][slot] == []:
					return (day, slot)

		print(schedule)
		raise ValueError ("No free variables in CSP to assign, this method shouldn't have been called.")

#	Use comedianHours - showLength heuristic to order the domain of values.
	def orderDomainValues3 (self):
	#	Create the cartesian product of comedians and remaining (demographic, type), but only the pairs which are compatible
	#	Give each an index equal to the showLength (Test - 1 hour or Main - 2 hours)
		possibleTriples = [((a,p[0],p[1]),self.showLength[p[1]]) for a in self.comediansMainOrder for p in self.demoTypePairs if p[1] == "main" and self.canMarket (a, p[0], False)]
		possibleTriples.extend ([((a,p[0],p[1]),self.showLength[p[1]]) for a in self.comediansTestOrder for p in self.demoTypePairs if p[1] == "test" and self.canMarket (a, p[0], True)])
		
	#	Sort by the index, we want to prioritise Main shows first and comedians who are compatible with the
	#	most of the type of show in concern.
		possibleTriples.sort(key=self.takeSecond, reverse = True)

	#	Take just the (comedian, demo, type) pairs from the list and return it.
		domain, h = zip(*possibleTriples)
		return domain

	def consistent3 (self, day, comedian, type):
	#	Check the comedian hours for the current comedian + the length of the new show to be added
	#   remain <= 2 per day and 4 per week
		hoursToday 	  = self.comedianShows[comedian][day][0] 	 + 2*self.comedianShows[comedian][day][1]
		hoursThisWeek = self.comedianShows[comedian]["Total"][0] + 2*self.comedianShows[comedian]["Total"][1]

		if hoursToday 	 + self.showLength[type] > 2: return False
		if hoursThisWeek + self.showLength[type] > 4: return False

		return True
	#------------------------------------------------------------------------------------------------------------------------------------------------------------------------- v

	#This simplistic approach merely assigns each demographic and comedian to a random slot, iterating through the timetable.
	def randomMainSchedule(self,timetableObj):

		sessionNumber = 1
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
		dayNumber = 0
		for demographic in self.demographic_List:
			comedian = self.comedian_List[random.randrange(0, len(self.comedian_List))]

			timetableObj.addSession(days[dayNumber], sessionNumber, comedian, demographic, "main")

			sessionNumber = sessionNumber + 1

			if sessionNumber == 6:
				sessionNumber = 1
				dayNumber = dayNumber + 1

	#This simplistic approach merely assigns each demographic to a random main and test show, with a random comedian, iterating through the timetable.
	def randomMainAndTestSchedule(self,timetableObj):

		sessionNumber = 1
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
		dayNumber = 0
		for demographic in self.demographic_List:
			comedian = self.comedian_List[random.randrange(0, len(self.comedian_List))]

			timetableObj.addSession(days[dayNumber], sessionNumber, comedian, demographic, "main")

			sessionNumber = sessionNumber + 1

			if sessionNumber == 11:
				sessionNumber = 1
				dayNumber = dayNumber + 1

		for demographic in self.demographic_List:
			comedian = self.comedian_List[random.randrange(0, len(self.comedian_List))]

			timetableObj.addSession(days[dayNumber], sessionNumber, comedian, demographic, "test")

			sessionNumber = sessionNumber + 1

			if sessionNumber == 11:
				sessionNumber = 1
				dayNumber = dayNumber + 1

	#------------------------- COPIED FROM TIMETABLE CLASS TO BE USED EASILY HERE --------------------------------------------------------------

	#Small utility method to check if a comedian can market a show to a demographic
	def canMarket(self, comedian, demographic, isTest):
		#if it is not a test show, we make sure every one of the demographics' topics is matched by the comedian's themes.
		if not isTest:
			topics = demographic.topics

			i = 0
			for t in topics:
				if t not in comedian.themes:
					return False

			return True

		#if it is a test show, we make sure the comedian has at least one theme that matches a topic of the demographic.
		else:
			topics = demographic.topics

			i = 0
			for t in topics:
				if t in comedian.themes:
					return True

			return False


#	Get the xth element. This is used as `key` param for sort().
	def takeSecond (self, e): return e[1]

	def countMainDemos(self, c):
		x=0
		for d in self.demoTypePairs:
			if self.canMarket(c, d[0], False): x+=1
		return x

	def countTestDemos(self, c, r = 1):
		x=0
		for d in self.demoTypePairs:
			if self.canMarket(c, d[0], True): x+=1
		return x

	def countThemes(self, c):
		return len(c.themes)
	#-----------------------------------------------------------------------------------------------------------------------------------------
