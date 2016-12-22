import os

class ToDoList:
	"""This is a Python list of entry strings with additional methods for managing a to-do list"""
	
	name = ''
	entry_list = []
	# saves the Notebook directory to stop it being recalculated every time it is needed
	notebook_path = os.path.join(os.path.split(__file__)[0], 'Notebook')

	def __init__(self, list_name=None):
		"""Asks the user for a name unless the name is provided in the declaration"""

		if list_name is None:
			print "Creating new ToDo list..."
			user_input = raw_input("What do you want to call it? ")
			self.name = user_input
		else:
			self.name = list_name

	def __str__(self):
		"""Returns same output as PrintList but as a string"""

		print_string = "<<<<<<<<%s>>>>>>>>\n" % self.name
		for num, entry in enumerate(self.entry_list, start=1):
			print_string += "%i %s\n" % (num, entry)
		print_string += "<<<<<<<<%s>>>>>>>>\n" % ('-' * len(self.name))

		return print_string

	def PrintList(self):
		"""Prints each entry and a decorator"""
		print "<<<<<<<<%s>>>>>>>>" % self.name
		for num, entry in enumerate(self.entry_list, start=1):
			print num, entry
		print "<<<<<<<<%s>>>>>>>>" % ('-' * len(self.name))

		return

############
# IO
############

	def SaveToFile(self, file_name):
		"""Saves the current list's contents to a file"""
		
		# needs to change to the 'notebook' directory first
		os.chdir(self.notebook_path)
		
		list_file = open(file_name, 'w')
		
		for entry in self.entry_list:
			list_file.write(entry + '\n')
			
		list_file.close()

		return
		
	def ReadFile(self, file_name):
		"""Reads list information from a file and replaces the current contents of the ToDoList entry_list."""

		os.chdir(self.notebook_path)

		try:
			list_file = open(file_name, 'r')
		except IOError, msg:
			print msg
			return
		try:
			# clears the list
			self.entry_list = []
			# reads in the text
			for line in list_file:
				self.AddEntryFromFile(line)
		finally:
			list_file.close()

		return

##################
# Adding entries
##################

	def AddEntry(self, entry, *more_entries):
		"""Adds an entry to the To-Do list. Has support for adding multiple entries at once"""

		self.entry_list.append(entry)

		for item in more_entries:
			self.entry_list.append(item)

		return

	def AddEntryFromFile(self, entry):
		"""Same as AddEntry but removes '\n' from the end of the entry string"""

		self.entry_list.append(entry[:-1])

		return

	def InputEntry(self):
		"""Provides the frontend for AddEntry"""

		print "Please enter your entry"
		user_input = raw_input(">> ")

		self.AddEntry(user_input)

		return

#########################
# Deleting entries
#########################

	def RemoveEntry(self, index):
		"""When given an index, will delete the corresponding entry"""

		try:
			del self.entry_list[index]
		except IndexError, msg:
			print msg

		return

	def DeleteEntry(self):
		"""Provides the frontend for Remove entry"""

		user_input = raw_input("Enter the number of the entry you want to delete:  ")
		index = int(user_input)-1

		try:
			self.RemoveEntry(index)
		except IndexError:
			print "'%i' is not a valid index" % index

		return

#####################
# Changing Priority
#####################

	def MakeHighestPriority(self, index):
		"""Moves the entry at the given index to the first slot in the list"""

		self.entry_list.insert(0, self.entry_list.pop(index))

		return

	def MakeLowestPriority(self, index):
		"""Moves the entry at the given index to the last slot in the list"""

		self.entry_list.append(self.entry_list.pop(index))

		return

	def ChangePriority(self):
		"""Lets the user decide between making a entry the highest or lowest priority"""

		user_input = raw_input("Select an entry number: ")
		index = int(user_input)-1
		try:
			print "Moving '%s'..." % self.entry_list[index]
		except IndexError:
			print "'%i' is not a valid index" % index

		else:
			user_input = raw_input("Make highest or lowest priority[h/l]? ")

			if user_input == 'h':
				self.MakeHighestPriority(index)
			if user_input == 'l':
				self.MakeLowestPriority(index)

			return



def DisplayMenu():
	"""Prints out what each command does"""
	
	print """
<<<<<<<<HELP>>>>>>>>
h: displays the help
a: adds an entry to the current list
d: deletes an entry from the list
c: changes an entry's position in the list
p: prints the current list
q: quits RattleList and saves the current list to a file
"""
	return


def main():
	"""Goes through a startup procedure and then runs the main loop of the application"""

	# startup
	# create a list
	working_todo = ToDoList('')

	# create a Notebook directory if it doesn't exist in the current directory
	if "Notebook" not in os.listdir('.'):
		os.mkdir("Notebook")

	lists = os.listdir("Notebook")

	if len(lists) == 0:
		print "There are no lists in the Notebook directory"
	else:
		print "Current lists:", lists

	list_name = raw_input("Please enter the name of a current list or a new list: ")

	# search Notebook directory for matching names
	if list_name in os.listdir("Notebook"):
		# ask if user wants to load the file
		user_choice = raw_input("%s already exists, do you want to overwrite it[y/n]? " % list_name)

		if user_choice == 'n':
			working_todo.ReadFile(list_name)
		elif user_choice == 'y':
			print "Anything you have saved in '%s' will be overwritten" % list_name
			print "To avoid this, don't choose the 'q' option and just close the window"

	DisplayMenu()

	# main loop
	# user options
	OPTIONS_DICT = {'a': 'Add', 'p': 'Print', 'd': 'Delete', 'c': 'Change', 'h': 'Help', 'q': 'Quit'}

	while True:

		working_todo.PrintList()

		user_input = raw_input(working_todo.name+'>> ')
		if user_input in OPTIONS_DICT:
			choice = OPTIONS_DICT[user_input]
			
			if choice == "Add":
				working_todo.InputEntry()
			elif choice == "Print":
				working_todo.PrintList()
			elif choice == "Delete":
				working_todo.DeleteEntry()
			elif choice == "Change":
				working_todo.ChangePriority()
			elif choice == 'Help':
				DisplayMenu()
			elif choice == 'Quit':
				working_todo.SaveToFile(list_name)
				break
		else:
			print "'%s' is not a valid choice, try 'h' for a list of options" % user_input

	return

if __name__ == '__main__':
	main()
