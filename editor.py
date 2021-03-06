import sqlite3


connection = None
c= None

def AddMovie(database):
	#---------------------------------------------------------------
	# Argument 	- database
	#
	# Work Done - This function gives editor the provision to add a 
	#			  movie.He/She can add a new movie to the database. 
	#			  And also add a new cast member. Also is able to assign
	#			  role or reject it by shifting to other function.	 
	#
	# Returns 	- Nothing
	#	
	#---------------------------------------------------------------

	# Connecting the database using cursor 
	global connection,c
	connection = sqlite3.connect(database)
	c = connection.cursor()

	#starting a while loop which prompts the editor 
	while True:
		m_mid = input("Please type the unique movie id :  ")
		c.execute("SELECT COUNT(*) FROM movies WHERE mid=:mid",{'mid':m_mid})
		counts = c.fetchall()
		# this tells us the count of movies with same mid
		count = counts[0][0]
		if count == 0:
			break

	# Taking more inputs		
	m_title = input("Please type the movie title :   ")
	m_year = input("Please type the year of realease :  ")
	m_runtime = input("Please type the runtime :  ")
	
	# making a string to then insert it
	movie_to_add =  (m_mid, m_title, m_year, m_runtime)	
	c.execute("INSERT INTO movies VALUES (?,?,?,?)", movie_to_add)
	
	to_add_cast = input("Do you want to check a cast member?   ")

	# asking and then differentiating according to the choice one wants to do it
	if to_add_cast.lower() != "yes":
		check = "False"
	else:
		check = "True"

	if check == "True":
		# shift to add member when he said yes
		AddCastMember(m_mid)
			
def AddCastMember(mid):
	#---------------------------------------------------------------
	# Argument 	- mid
	#
	# Work Done - This function gives editor the provision to add a 
	#			  cast member. or check with the existing one.
	#			  He/She can add a new cast member and also dedide
	#			  to give role or reject it. 	 
	#
	# Returns 	- Nothing
	#	
	#---------------------------------------------------------------
	global connection,c

	# first while loop to take inputs from the user
	while True:
		c_pid = input("Please enter the id of the cast member you want to check for : ")
		c.execute("SELECT COUNT(*) FROM casts WHERE pid=:pid",{'pid':c_pid})
		count = c.fetchall()[0][0]
		if count != 0:
			# if it exist then print the information of the memeber
			c.execute('''SELECT mp.name, mp.birthYear
						FROM casts c, moviePeople mp
						WHERE c.pid=:pid COLLATE NOCASE and c.pid = mp.pid 
						''',{'pid':c_pid})
			casts_members = c.fetchall()
			print("Member in casts.")
			print(str(casts_members[0][0]) + " | " + str(casts_members[0][1]))

		else:
			# if it does not exist and ask more stuff	
			c_pid = input("Please enter the id of the cast member you want to enter :  ")
			mp_name = input("Please type in the name of the new cast member :  ")
			mp_birthYear = input("Please type in the birth year of the new cast member :  ")
			cast_to_add = (c_pid, mp_name, mp_birthYear)
			c.execute("INSERT INTO moviePeople VALUES (?,?,?)", cast_to_add)
			print("Cast member added.")
		
		# asking if want to give role or reject	
		choice = input("Do you want to give role to the cast member?  ")	
		if choice.lower() == "yes":
			c_role = input("What role do you want to assign him/her?   ")
			# if yes then make a new strimng and insert it into the data
			new_cast = (mid, c_pid, c_role)
			c.execute("INSERT INTO casts VALUES (?,?,?)", new_cast)
			print("Role Given")

		break

	connection.commit()






def Update(database):
	#---------------------------------------------------------------
	# Argument 	- database
	#
	# Work Done - This function gives editor the provision to update 
	#			  the recommendations table.
	#
	# Returns 	- Nothing	
	#---------------------------------------------------------------
	
	# Connecting the database using cursor 
	global connection,c
	connection = sqlite3.connect(database)
	c = connection.cursor()
	
	# Taking the input from the user if he/she wants a monthly annual or all time report
	print('''Please select a term from the following:
		  1.) Monthly
		  2.) Annual
		  3.) All-time Report''')
	term = input()
	if term.lower() == "1":
		till = "-30 days"
	else:
		till = "-365 days"
	
	# the main query running the program.
	c.execute('''
				SELECT m1.mid, m2.mid, count(distinct w1.cid)
				FROM movies m1, movies m2, watch w1, watch w2, sessions s
				WHERE s.sdate > datetime('now', :till)
					and ((w1.sid = s.sid and w1.cid = s.cid) or (w2.sid = s.sid and w2.cid = s.cid))
  					and m1.mid = w1.mid and w1.duration * 2 >= m1.runtime and m2.mid = w2.mid and w2.duration * 2 >= m1.runtime
  					and w1.cid = w2.cid and m1.mid != m2.mid
				GROUP BY m1.mid, m2.mid
				ORDER BY count(distinct w1.cid) DESC	
				''',{'till':till})
	final = c.fetchall()
	
	# making a query to get all the recommended so that we can sacn it later
	c.execute('''
				SELECT watched, recommended
				FROM recommendations 
				''')
	reccomended = c.fetchall()

	# initializing 2 tables to keep record of indicators and score
	score_table = []
	indicator_LIST = []


	for i in range(len(final)):
		if final[i][0:2] in reccomended:
			indicator_LIST.append("YES")
			f_score = getScore(final[i][0:2])
			score_table.append(f_score[0][0])	
		else:
			indicator_LIST.append("NO")
			score_table.append("-")

	# if there is no report print a string		
	if len(final) == 0:
		print("NO REPORT AVAILABLE")
		return
	# if there is a report then print in a specific way.
	else:	
		print("-----------------------------------------------------------------------------")
		print("  S No. " + "|" + "    Watched    " + "|" + "   Reccomended " + "|" + "    Indicator " + " | " + "  Score")	
		print("-----------------------------------------------------------------------------")
		for i in range(0, len(final)):
			print(str(i+1) + "\t|\t " + str(final[i][0]) + "\t|\t" + str(final[i][1]) + "\t|\t" + str(indicator_LIST[i]) + "\t|\t" + str(score_table[i]))	
	
	#getting the input for the movies editor wants
	while True:
		pair_num = int(input("Please select a pair from the table.   "))

	# Agin initializing a print statement to get the input of the user for Add, Delete or Update
		if indicator_LIST[pair_num-1] == "YES":
			print('''Select one from the following:
						1.) Delete
						2.) Update Score
						3.) Go Back
						4.) Exit''')
		elif indicator_LIST[pair_num-1] == "NO":
			print('''Select one from the following:
						1.) Add
						2.) Go Back
						3.) Exit''')

		# Seperating accoprdingly so that we can see what exactly user wants	
		option = int(input())	
		if (option == 3 and indicator_LIST[pair_num-1] == "YES") or (indicator_LIST[pair_num-1] == "NO" and option == 2):
			continue
		elif (option == 4 and indicator_LIST[pair_num-1] == "YES") or (indicator_LIST[pair_num-1] == "NO" and option == 3):
			return	
		elif indicator_LIST[pair_num-1] == "YES" and option == 1:
			Delete_R(final[pair_num-1][0:2])
			print("Successfully Delected")
			return
		elif indicator_LIST[pair_num-1] == "YES" and option == 2:
			Update_R(final[pair_num-1][0:2])
			print("Successfully Updated")
			return
		elif indicator_LIST[pair_num-1] == "NO" and option == 1:
			Add_R(final[pair_num-1][0], final[pair_num-1][1])
			print("New reccomended added to recommendation")
			return
	
	connection.commit()



def Delete_R(recomend):
	# A function to delete the recommended
	global connection,c	
	c.execute('''DELETE from recommendations 
				WHERE watched = :rec1 or recommended = :rec2''',{'rec1':recomend[0],'rec2':recomend[1]})
	connection.commit()


def Add_R(watched,recomend):
	# A function to add the recommended
	global connection,c
	new_score = input("What score do you want to assign?   ")
	recommendation_to_add = [watched, recomend, new_score]
	c.execute("INSERT INTO recommendations VALUES (?,?,?)", recommendation_to_add)
	connection.commit()



def Update_R(recomend):
	# A function to Update the recommended
	global connection,c
	new_score = input("What score do you want to update with ? 	 ")
	c.execute('''UPDATE recommendations 
				SET score = :new_score
				WHERE watched = :rec1 and recommended = :rec2''',{'new_score':new_score, 'rec1':recomend[0],'rec2':recomend[1]})

	connection.commit()


def getScore(got):
	# A function to get score of the given recommended
	global connection,c

	c.execute('''SELECT score	
				FROM recommendations
				WHERE recommended = :rec2 and watched = :rec1''', {'rec2':got[1], 'rec1':got[0]})

	f_score = c.fetchall()
	return f_score


	c.execute("SELECT COUNT(recommended) FROM recommendations WHERE pid=:pid",{'pid':c_pid})
	count = c.fetchall()[0][0]
	if count != 0:
		c.execute('''SELECT mp.name, mp.birthYear
					FROM casts c, moviePeople mp
					WHERE c.pid=:pid COLLATE NOCASE and c.pid = mp.pid 
					''',{'pid':c_pid})
 
	connection.commit()

if __name__=="__main__":
	Update("mini-proj.db")


