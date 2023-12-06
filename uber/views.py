from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render, get_object_or_404
from django.urls import reverse
import cx_Oracle
from datetime import datetime, timedelta

def index(request):
	return render(request, 'uber/index.html')

def userSignUp(request):
	if request.method == 'POST':
		inputLst = []  # contains the received data from sing up form
		inputLst.append(request.POST['firstName'])
		inputLst[len(inputLst) - 1].strip()
		inputLst.append(request.POST['middleName'])
		inputLst[len(inputLst) - 1].strip()
		inputLst.append(request.POST['lastName'])
		inputLst[len(inputLst) - 1].strip()

		inputLst.append(request.POST['userName'])
		inputLst[len(inputLst) - 1].strip()
		inputLst.append(request.POST['passWord'])
		inputLst.append(request.POST['mobileNumber'])
		inputLst[len(inputLst) - 1].strip()

		inputLst.append(request.POST['email'])
		inputLst[len(inputLst) - 1].strip()
		inputLst.append(request.POST['birthDay'])
		inputLst.append(request.POST['street'])

		inputLst[len(inputLst) - 1].strip()
		inputLst.append(request.POST['city'])
		inputLst[len(inputLst) - 1].strip()
		inputLst.append(request.POST['postCode'])
		inputLst[len(inputLst) - 1].strip()

		errorLst = []

		# for first, middle and last name

		for i in range(3):
			inputLst[i] = inputLst[i].strip()
			flag = False
			errorLst.append('')
			name =''

			if i == 0:
				name = "First Name"
			elif i == 1:
				name = "Middle Name"
			else:
				name = "Last Name"

			for ch in inputLst[i]:
				if not ((ch >= 'a' and ch <= 'z') or (ch >= 'A' and ch <= 'Z')):
					flag = True
			if flag:
				errorLst[i] = "Invalid " + name

			if inputLst[i] and len(inputLst[i]) > 40:
				errorLst[i] = name + " too long!"

		#for username - 3      =================================

		errorLst.append('')

		connection = cx_Oracle.connect("SYSTEM/hello@localhost/orcl")
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM APP_USER WHERE USERNAME = :username", username=inputLst[3])
		checkLst=[]
		for line in cursor:
			checkLst.append(line)

		if checkLst:
			errorLst[len(errorLst) - 1] = 'Username already taken!'
		elif len(inputLst[3]) > 40:
			errorLst[len(errorLst) - 1] = 'User Name too long!'

		# ================================== for passowrd - 4

		errorLst.append('')
		if len(inputLst[4]) > 40:
			errorLst[len(errorLst) - 1] = 'Password too long!'
		elif len(inputLst[4]) < 3:
			errorLst[len(errorLst) - 1] = 'Password too short!'

		#=================================== for mobile number - 5
		mobNumOk = True
		mobNumExist = False

		if len(inputLst[5]) != 11:
			errorLst.append("Invalide mobile number")
			mobNumOk = False
		elif inputLst[5][0] != '0' or inputLst[5][1] != '1':
			errorLst.append("Invalid mobile number")
			mobNumOk = False
		else:
			flag = True
			for i in range(2, 11):
				if not(inputLst[5][i] >= '0' and inputLst[5][i] <= '9'):
					flag = False

			if not flag:
				errorLst.append("Invalide mobile number")
				mobNumOk = False

		if mobNumOk:
			cursor.execute("SELECT * FROM MOBILE_NUMBERS WHERE MOBILE_NUMBER = :mob_num", mob_num=inputLst[5])
			checkLst = []
			for line in cursor:
				checkLst.append(line)

			if not checkLst or not checkLst[0][1]:
				if checkLst:
					mobNumExist = True
			else:
				errorLst.append("Mobile number already taken!")

		#=================================for email - 6 - not verified


		#=================================for birthday - 7 - not verified

		#=================================for location: street - 8, city - 9, postCode - 10
		#query with only street and city
		inputLst.append('')#for location ID

		errorLst.append('')
		errorLst.append('')
		errorLst.append('')
		if inputLst[8] and len(inputLst[8]) > 40:
			errorLst[len(errorLst) - 3] = 'Street name too long!'
		elif len(inputLst[9]) > 40:
			errorLst[len(errorLst) - 2] = 'City name too long!'
		elif inputLst[10] and len(inputLst[10]) > 10:
			errorLst[len(errorLst) - 1] = 'Postal Code too long!'

		isOK = True
		for val in errorLst:
			if val:
				isOK = False

		if not isOK:
			return render(request, 'uber/userSignUp.html', {
				'inputLst': inputLst,
				'errorLst': errorLst,
			})



		if inputLst[8]:
			cursor.execute("SELECT * FROM LOCATION WHERE CITY = :city AND STREET = :street", city=inputLst[9], street = inputLst[8])
			checkLst = []
			for line in cursor:
				checkLst.append(line)

			if checkLst:
				inputLst[len(inputLst) - 1] = checkLst[0][0]
			else:
				cursor.execute("INSERT INTO LOCATION(STREET, CITY) VALUES( :street, :city)", [inputLst[8], inputLst[9]])
				connection.commit()

				cursor.execute("SELECT * FROM LOCATION WHERE CITY = :city AND STREET = :street", city=inputLst[9],
							   street=inputLst[8])
				checkLst = []
				for line in cursor:
					checkLst.append(line)

				if checkLst:
					inputLst[len(inputLst) - 1] = checkLst[0][0]

		else:
			cursor.execute("SELECT * FROM LOCATION WHERE CITY = :city", city=inputLst[9])
			checkLst = []
			for line in cursor:
				checkLst.append(line)

			if checkLst:
				inputLst[len(inputLst) - 1] = checkLst[0][0]
			else:
				cursor.execute("INSERT INTO LOCATION(CITY) VALUES( :city)", city=inputLst[9])
				connection.commit()

				cursor.execute("SELECT * FROM LOCATION WHERE CITY = :city", city=inputLst[9])
				checkLst = []
				for line in cursor:
					checkLst.append(line)

				if checkLst:
					inputLst[len(inputLst) - 1] = checkLst[0][0]

		cursor.execute("INSERT INTO APP_USER(FIRST_NAME, MIDDLE_NAME, LAST_NAME, USERNAME, PASSWORD, EMAIL, DATE_OF_BIRTH, LOCATION_ID ) VALUES(:firstName, :middleName, :lastName, :userName, :passWord, :email, TO_DATE(:date_of_birth, 'YYYY-MM-DD'), :location_id)", [inputLst[0], inputLst[1], inputLst[2], inputLst[3], inputLst[4], inputLst[6], inputLst[7], inputLst[11]])


		connection.commit()

		cursor.execute("SELECT * FROM APP_USER WHERE USERNAME = :userName", userName=inputLst[3])

		checkLst = []
		for line in cursor:
			checkLst.append(line)

		userId = checkLst[0][0]

		if mobNumExist:
			cursor.execute("UPDATE MOBILE_NUMBERS SET USER_ID = :user_id WHERE MOBILE_NUMBER = : mobNum", [userId, inputLst[5]])
			connection.commit()
		else:
			cursor.execute("INSERT INTO MOBILE_NUMBERS(MOBILE_NUMBER, USER_ID) VALUES (:mobNum, :user_id)", [inputLst[5], userId])
			connection.commit()

		cursor.close()
		connection.close()
		return HttpResponseRedirect(reverse('uber:userLogin'))


	else:
		return render(request, 'uber/userSignUp.html')


def driverSignUp(request):
	if request.method == 'POST':
		inputLst = []  # contains the received data from sing up form
		inputLst.append(request.POST['firstName'])
		inputLst[len(inputLst) - 1].strip()
		inputLst.append(request.POST['middleName'])
		inputLst[len(inputLst) - 1].strip()
		inputLst.append(request.POST['lastName'])
		inputLst[len(inputLst) - 1].strip()

		inputLst.append(request.POST['userName'])
		inputLst[len(inputLst) - 1].strip()
		inputLst.append(request.POST['passWord'])
		inputLst.append(request.POST['mobileNumber'])
		inputLst[len(inputLst) - 1].strip()

		inputLst.append(request.POST['email'])
		inputLst[len(inputLst) - 1].strip()
		inputLst.append(request.POST['birthDay'])
		inputLst.append(request.POST['street'])

		inputLst[len(inputLst) - 1].strip()
		inputLst.append(request.POST['city'])
		inputLst[len(inputLst) - 1].strip()
		inputLst.append(request.POST['postCode'])
		inputLst[len(inputLst) - 1].strip()

		errorLst = []

		# for first, middle and last name

		for i in range(3):
			inputLst[i] = inputLst[i].strip()
			flag = False
			errorLst.append('')
			name =''

			if i == 0:
				name = "First Name"
			elif i == 1:
				name = "Middle Name"
			else:
				name = "Last Name"

			for ch in inputLst[i]:
				if not ((ch >= 'a' and ch <= 'z') or (ch >= 'A' and ch <= 'Z')):
					flag = True
			if flag:
				errorLst[i] = "Invalid " + name

			if inputLst[i] and len(inputLst[i]) > 40:
				errorLst[i] = name + " too long!"

		#for username - 3      =================================

		errorLst.append('')

		connection = cx_Oracle.connect("SYSTEM/hello@localhost/orcl")
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM DRIVER WHERE USERNAME = :username", username=inputLst[3])
		checkLst=[]
		for line in cursor:
			checkLst.append(line)

		if checkLst:
			errorLst[len(errorLst) - 1] = 'Username already taken!'
		elif len(inputLst[3]) > 40:
			errorLst[len(errorLst) - 1] = 'User Name too long!'

		# ================================== for passowrd - 4

		errorLst.append('')
		if len(inputLst[4]) > 40:
			errorLst[len(errorLst) - 1] = 'Password too long!'
		elif len(inputLst[4]) < 3:
			errorLst[len(errorLst) - 1] = 'Password too short!'

		#=================================== for mobile number - 5
		mobNumOk = True
		mobNumExist = False

		if len(inputLst[5]) != 11:
			errorLst.append("Invalide mobile number")
			mobNumOk = False
		elif inputLst[5][0] != '0' or inputLst[5][1] != '1':
			errorLst.append("Invalid mobile number")
			mobNumOk = False
		else:
			flag = True
			for i in range(2, 11):
				if not(inputLst[5][i] >= '0' and inputLst[5][i] <= '9'):
					flag = False

			if not flag:
				errorLst.append("Invalide mobile number")
				mobNumOk = False

		if mobNumOk:
			cursor.execute("SELECT * FROM MOBILE_NUMBERS WHERE MOBILE_NUMBER = :mob_num", mob_num=inputLst[5])
			checkLst = []
			for line in cursor:
				checkLst.append(line)

			if not checkLst or not checkLst[0][2]:
				if checkLst:
					mobNumExist = True
			else:
				errorLst.append("Mobile number already taken!")

		#=================================for email - 6 - not verified


		#=================================for birthday - 7 - not verified

		#=================================for location: street - 8, city - 9, postCode - 10
		#query with only street and city
		inputLst.append('')#for location ID

		errorLst.append('')
		errorLst.append('')
		errorLst.append('')
		if inputLst[8] and len(inputLst[8]) > 40:
			errorLst[len(errorLst) - 3] = 'Street name too long!'
		elif len(inputLst[9]) > 40:
			errorLst[len(errorLst) - 2] = 'City name too long!'
		elif inputLst[10] and len(inputLst[10]) > 10:
			errorLst[len(errorLst) - 1] = 'Postal Code too long!'

		isOK = True
		for val in errorLst:
			if val:
				isOK = False

		if not isOK:
			return render(request, 'uber/driverSignUp.html', {
				'inputLst': inputLst,
				'errorLst': errorLst,
			})



		if inputLst[8]:
			cursor.execute("SELECT * FROM LOCATION WHERE CITY = :city AND STREET = :street", city=inputLst[9], street = inputLst[8])
			checkLst = []
			for line in cursor:
				checkLst.append(line)

			if checkLst:
				inputLst[len(inputLst) - 1] = checkLst[0][0]
			else:
				cursor.execute("INSERT INTO LOCATION(STREET, CITY) VALUES( :street, :city)", [inputLst[8], inputLst[9]])
				connection.commit()

				cursor.execute("SELECT * FROM LOCATION WHERE CITY = :city AND STREET = :street", city=inputLst[9],
							   street=inputLst[8])
				checkLst = []
				for line in cursor:
					checkLst.append(line)

				if checkLst:
					inputLst[len(inputLst) - 1] = checkLst[0][0]

		else:
			cursor.execute("SELECT * FROM LOCATION WHERE CITY = :city", city=inputLst[9])
			checkLst = []
			for line in cursor:
				checkLst.append(line)

			if checkLst:
				inputLst[len(inputLst) - 1] = checkLst[0][0]
			else:
				cursor.execute("INSERT INTO LOCATION(CITY) VALUES( :city)", city=inputLst[9])
				connection.commit()

				cursor.execute("SELECT * FROM LOCATION WHERE CITY = :city", city=inputLst[9])
				checkLst = []
				for line in cursor:
					checkLst.append(line)

				if checkLst:
					inputLst[len(inputLst) - 1] = checkLst[0][0]

		cursor.execute("INSERT INTO DRIVER(FIRST_NAME, MIDDLE_NAME, LAST_NAME, USERNAME, PASSWORD, EMAIL, DATE_OF_BIRTH, LOCATION_ID ) VALUES(:firstName, :middleName, :lastName, :userName, :passWord, :email, TO_DATE(:date_of_birth, 'YYYY-MM-DD'), :location_id)", [inputLst[0], inputLst[1], inputLst[2], inputLst[3], inputLst[4], inputLst[6], inputLst[7], inputLst[11]])


		connection.commit()

		cursor.execute("SELECT * FROM DRIVER WHERE USERNAME = :userName", userName=inputLst[3])

		checkLst = []
		for line in cursor:
			checkLst.append(line)

		driverId = checkLst[0][0]

		if mobNumExist:
			cursor.execute("UPDATE MOBILE_NUMBERS SET DRIVER_ID = :driver_id WHERE MOBILE_NUMBER = : mobNum", [driverId, inputLst[5]])
			connection.commit()
		else:
			cursor.execute("INSERT INTO MOBILE_NUMBERS(MOBILE_NUMBER, DRIVER_ID) VALUES (:mobNum, :driver_id)", [inputLst[5], driverId])
			connection.commit()

		cursor.close()
		connection.close()
		return HttpResponseRedirect(reverse('uber:driverLogin'))


	else:
		return render(request, 'uber/driverSignUp.html')

def userLogin(request):
	if request.method == 'POST':
		inputLst = []
		asUser = "userName"

		if 'userName' in request.POST:
			inputLst.append(request.POST['userName'])
		else:
			inputLst.append(request.POST['mobileNumber'])
			asUser = "mobileNumber"

		inputLst.append(request.POST['passWord'])

		errorLst = []

		connection = cx_Oracle.connect("SYSTEM/hello@localhost/orcl")
		cursor = connection.cursor()

		if 'userName' in request.POST:
			cursor.execute("SELECT * FROM APP_USER WHERE USERNAME = :userName", userName = inputLst[0])
			checkLst = []

			for line in cursor:
				checkLst.append(line)

			if checkLst:
				if checkLst[0][5] == inputLst[1]:
					return HttpResponseRedirect(reverse('uber:userHomePage', args=(checkLst[0][0],)))
				else:
					errorLst.append("Invalid password")
			else:
				errorLst.append("Invalid username")
		else:
			cursor.execute("SELECT USER_ID FROM MOBILE_NUMBERS WHERE MOBILE_NUMBER = :mobNum", mobNum = inputLst[0])
			checkLst = []
			for line in cursor:
				checkLst.append(line)

			if checkLst and checkLst[0][0]:
				cursor.execute("SELECT * FROM APP_USER WHERE USER_ID = :userId", userId = checkLst[0][0])
				checkLst = []
				for line in cursor:
					checkLst.append(line)

				if checkLst[0][5] == inputLst[1]:
					return HttpResponseRedirect(reverse('uber:userHomePage', args=(checkLst[0][0],)))
				else:
					errorLst.append("Invalid password")

			else:
				errorLst.append("Invalid mobile number")

		cursor.close()
		connection.close()


		return render(request, 'uber/userLogin.html', {
			'inputLst': inputLst,
			'errorLst': errorLst,
			'asUser': asUser,
		})

	else:
		return render(request, 'uber/userLogin.html')

def driverLogin(request):
	if request.method == 'POST':
		inputLst = []
		asUser = "userName"

		if 'userName' in request.POST:
			inputLst.append(request.POST['userName'])
		else:
			inputLst.append(request.POST['mobileNumber'])
			asUser = "mobileNumber"

		inputLst.append(request.POST['passWord'])

		errorLst = []

		connection = cx_Oracle.connect("SYSTEM/hello@localhost/orcl")
		cursor = connection.cursor()

		if 'userName' in request.POST:
			cursor.execute("SELECT * FROM DRIVER WHERE USERNAME = :userName", userName = inputLst[0])
			checkLst = []

			for line in cursor:
				checkLst.append(line)

			if checkLst:
				if checkLst[0][5] == inputLst[1]:
					return HttpResponseRedirect(reverse('uber:driverHomePage', args=(checkLst[0][0],)))
				else:
					errorLst.append("Invalid password")
			else:
				errorLst.append("Invalid username")
		else:
			cursor.execute("SELECT DRIVER_ID FROM MOBILE_NUMBERS WHERE MOBILE_NUMBER = :mobNum", mobNum = inputLst[0])
			checkLst = []
			for line in cursor:
				checkLst.append(line)

			if checkLst and checkLst[0][0]:
				cursor.execute("SELECT * FROM DRIVER WHERE DRIVER_ID = :driverId", driverId = checkLst[0][0])
				checkLst = []
				for line in cursor:
					checkLst.append(line)

				if checkLst[0][5] == inputLst[1]:
					return HttpResponseRedirect(reverse('uber:driverHomePage', args=(checkLst[0][0],)))
				else:
					errorLst.append("Invalid password")

			else:
				errorLst.append("Invalid mobile number")

		cursor.close()
		connection.close()


		return render(request, 'uber/driverLogin.html', {
			'inputLst': inputLst,
			'errorLst': errorLst,
			'asUser': asUser,
		})

	else:
		return render(request, 'uber/driverLogin.html')


def userHomePage(request, user_id):
	connection = cx_Oracle.connect("SYSTEM/hello@localhost/orcl")
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM APP_USER WHERE USER_ID = :userId", userId=user_id)

	checkLst = []

	for line in cursor:
		checkLst.append(line)

	#Checking if there is a new request for this user

	cursor.execute("SELECT * FROM REQUEST WHERE USER_ID = :userId  AND END_TIME >= :end_time", userId = user_id, end_time=datetime.now())
	requestData = cursor.fetchall()
	riderInfo = []


	if requestData:
		requestData = list(requestData[0])
		if requestData[8]:#if there is a rider found
			cursor.execute("SELECT * FROM DRIVER WHERE DRIVER_ID = :driver_id", driver_id = requestData[8])

			for line in cursor:
				riderInfo = list(line)

			cursor.execute("SELECT MOBILE_NUMBER FROM MOBILE_NUMBERS WHERE DRIVER_ID = :driver_id", driver_id = requestData[8])
			#from index 12 in riderInfo

			nums = []
			for line in cursor:
				nums.append(line[0])

			riderInfo.append(nums)


		cursor.execute("SELECT STREET, CITY FROM LOCATION WHERE LOCATION_ID = :loc_id", loc_id = requestData[3])
		for line in cursor:
			requestData.append(list(line))

		cursor.execute("SELECT STREET, CITY FROM LOCATION WHERE LOCATION_ID = :loc_id", loc_id = requestData[4])
		for line in cursor:
			requestData.append(list(line))




	cursor.close()
	connection.close()

	return render(request, 'uber/userHomePage.html', {
		'userInfo': checkLst[0],
		'requestData': requestData,
		'riderInfo' : riderInfo,
	})

def driverHomePage(request, driver_id):
	connection = cx_Oracle.connect("SYSTEM/hello@localhost/orcl")
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM DRIVER WHERE DRIVER_ID = :driverId", driverId=driver_id)

	checkLst = []

	for line in cursor:
		checkLst.append(line)

	cursor.execute("SELECT * FROM REQUEST WHERE END_TIME >= :end_time AND DRIVER_ID = :driverId", end_time=datetime.now(), driverId = driver_id)
	checkLst1 = cursor.fetchall()

	if checkLst1:
		requestData = []
		for data in checkLst1:
			requestData = list(data)

		cursor.execute("SELECT * FROM APP_USER WHERE USER_ID = :userId", userId=requestData[7])

		tempData = []  # USER Data
		for line in cursor:
			tempData = (list(line))

		cursor.execute("SELECT MOBILE_NUMBER FROM MOBILE_NUMBERS WHERE USER_ID = :userId", userId=requestData[7])
		nums = []
		for line in cursor:
			nums.append(line[0])  # adding mobile number to userData

		tempData.append(nums)

		requestData.append(tempData)  # keeping user Info in request Data
		# at index 9 userInfo and from index 12 of requestData[9] user phone numbers present

		# for pickUP location at index 10 and 11 and destination location

		cursor.execute("SELECT STREET, CITY FROM LOCATION WHERE LOCATION_ID = :loc_id",
					   loc_id=requestData[3])
		for line in cursor:
			requestData.append(list(line))

		cursor.execute("SELECT STREET, CITY FROM LOCATION WHERE LOCATION_ID = :loc_id",
					   loc_id=requestData[4])
		for line in cursor:
			requestData.append(list(line))

		cursor.close()
		connection.close()

		return render(request, 'uber/driverHomePage.html', {
		'driverInfo': checkLst[0],
		'data': requestData,
		})

	else:
		# checking for request

		cursor.execute("SELECT * FROM REQUEST WHERE END_TIME >= :end_time AND DRIVER_ID IS NULL",
					   end_time=datetime.now())
		requestDataTemp = cursor.fetchall()
		requestData = []

		if requestDataTemp:  # requests that are not approved yet
			for data in requestDataTemp:
				requestData.append(list(data))

			i = 0
			for data in requestData:
				cursor.execute("SELECT * FROM APP_USER WHERE USER_ID = :userId", userId=data[7])

				tempData = []  # USER Data
				for line in cursor:
					tempData = (list(line))

				cursor.execute("SELECT MOBILE_NUMBER FROM MOBILE_NUMBERS WHERE USER_ID = :userId", userId=data[7])
				nums = []
				for line in cursor:
					nums.append(line[0])  # adding mobile number to userData

				tempData.append(nums)

				requestData[i].append(tempData)  # keeping user Info in request Data
				# at index 9 userInfo and from index 12 of requestData[9] user phone numbers present
				i = i + 1

				# for pickUP location at index 10 and 11 and destination location

				cursor.execute("SELECT STREET, CITY FROM LOCATION WHERE LOCATION_ID = :loc_id",
							   loc_id=requestData[i - 1][3])
				for line in cursor:
					requestData[i - 1].append(list(line))

				cursor.execute("SELECT STREET, CITY FROM LOCATION WHERE LOCATION_ID = :loc_id",
							   loc_id=requestData[i - 1][4])
				for line in cursor:
					requestData[i - 1].append(list(line))

		cursor.close()
		connection.close()

		return render(request, 'uber/driverHomePage.html', {
			'driverInfo': checkLst[0],
			'requestData': requestData,
		})


def newRequest(request, user_id):
	connection = cx_Oracle.connect("SYSTEM/hello@localhost/orcl")
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM APP_USER WHERE USER_ID = :userId", userId=user_id)

	checkLst = cursor.fetchall()

	pickupLoc = []
	destLoc = []
	pickupLoc.append(request.POST['street1'])
	pickupLoc[len(pickupLoc) - 1].strip()
	pickupLoc.append(request.POST['city1'])
	pickupLoc[len(pickupLoc) - 1].strip()

	destLoc.append(request.POST['street2'])
	destLoc[len(destLoc) - 1].strip()
	destLoc.append(request.POST['city2'])
	destLoc[len(destLoc) - 1].strip()

	errorLst = []

	if len(pickupLoc[0]) > 40:
		errorLst.append("Invalid pickup street name")
	if len(pickupLoc[1]) > 40:
		errorLst.append("Invalid pickup city name")

	if len(destLoc[0]) > 40:
		errorLst.append("Invalid destination street name")
	if len(destLoc[1]) > 40:
		errorLst.append("Invalid destination city name")

	for error in errorLst:
		if error:
			return render(request, 'uber/userHomePage.html', {
				'userInfo': checkLst[0],
				'errorLst': errorLst,
				'pickupLoc': pickupLoc,
				'destLoc': destLoc,
			})


	#search pickup location

	if pickupLoc[0]:
		cursor.execute("SELECT * FROM LOCATION WHERE LOWER(STREET) = :street and LOWER(CITY) = :city", street = pickupLoc[0].lower(), city=pickupLoc[1].lower())
		lst = cursor.fetchall()
		if lst:
			pass
		else:
			cursor.execute("INSERT INTO LOCATION(STREET, CITY) VALUES (:street, :city)", pickupLoc)
			connection.commit()

		cursor.execute("SELECT * FROM LOCATION WHERE LOWER(STREET) = :street AND LOWER(CITY) = :city",
					   street=pickupLoc[0].lower(), city=pickupLoc[1].lower())
		lst = cursor.fetchall()
		pickupLoc.append(lst[0][0])
	else:
		cursor.execute("SELECT * FROM LOCATION WHERE LOWER(CITY) = :city", city=pickupLoc[1].lower())
		lst = cursor.fetchall()
		if lst:
			pass
		else:
			cursor.execute("INSERT INTO LOCATION(CITY) VALUES (:city)", city = pickupLoc[1])
			connection.commit()

		cursor.execute("SELECT * FROM LOCATION WHERE LOWER(CITY) = :city", city=pickupLoc[1].lower())
		lst = cursor.fetchall()
		pickupLoc.append(lst[0][0])


	#search destLoc

	if destLoc[0]:
		cursor.execute("SELECT * FROM LOCATION WHERE LOWER(STREET) = :street and LOWER(CITY) = :city", street = destLoc[0].lower(), city=destLoc[1].lower())
		lst = cursor.fetchall()
		if lst:
			pass
		else:
			cursor.execute("INSERT INTO LOCATION(STREET, CITY) VALUES (:street, :city)", destLoc)
			connection.commit()

		cursor.execute("SELECT * FROM LOCATION WHERE LOWER(STREET) = :street AND LOWER(CITY) = :city",
					   street=destLoc[0].lower(), city=destLoc[1].lower())
		lst = cursor.fetchall()
		destLoc.append(lst[0][0])
	else:
		cursor.execute("SELECT * FROM LOCATION WHERE LOWER(CITY) = :city", city=destLoc[1].lower())
		lst = cursor.fetchall()
		if lst:
			pass
		else:
			cursor.execute("INSERT INTO LOCATION(CITY) VALUES (:city)", city = destLoc[1])
			connection.commit()

		cursor.execute("SELECT * FROM LOCATION WHERE LOWER(CITY) = :city", city=destLoc[1].lower())
		lst = cursor.fetchall()
		destLoc.append(lst[0][0])

	# now add a request

	cursor.execute("INSERT INTO REQUEST (START_TIME, END_TIME, PICK_UP_LOCATION_ID, DESTINATION_LOCATION_ID, APPROX_FARE, USER_ID) VALUES (:start_time, :end_time, :pickup_loc_id, :dest_loc_id, :approx_fare, :user_id)", [datetime.now(), datetime.now() + timedelta(minutes = 10), pickupLoc[2], destLoc[2], 100, checkLst[0][0]])

	connection.commit()

	return HttpResponseRedirect(reverse('uber:userHomePage', args=(checkLst[0][0],)))


def acceptRequest(request, request_id, driver_id):
	connection = cx_Oracle.connect("SYSTEM/hello@localhost/orcl")
	cursor = connection.cursor()

	cursor.execute("SELECT * FROM REQUEST WHERE REQUEST_ID = :req_id AND END_TIME >= :end_time", req_id = request_id, end_time=datetime.now())

	checkLst = cursor.fetchall()

	if checkLst:
		cursor.execute("UPDATE REQUEST SET DRIVER_ID = :driverId WHERE REQUEST_ID = :req_id", driverId=driver_id, req_id = request_id)
		connection.commit()
		return HttpResponseRedirect(reverse('uber:driverHomePage', args=(driver_id,)))
	else:#in case request timeout or cancelled request
		return HttpResponseRedirect(reverse('uber:driverHomePage', args=(driver_id,)))




