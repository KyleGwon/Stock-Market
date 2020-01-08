import math
from time import sleep as wait
import csv
#------------------------------
def reverseSort(lsts):
	newLsts = []
	for lst in lsts:
		tempLst = []
		for i in range(len(lst)):
			inverse = (i * -1) - 1
			tempLst.append(lst[inverse])
		newLsts.append(tempLst)
	return newLsts
#------------------------------
def compare(data1, data2, minPercent):
	dates = [] #dates: strings
	outperformed = [] #value outperformed growth: boolean
	allPercents = [] #percent of value outperforming growth
	market = []
	for i in range(len(data1[1])):
		if data1[1][i] != 0 and data1[1][i] != 0:
			percentGreater = (100*data1[1][i]) - (100*data2[1][i])
			if data1[1][i] > data2[1][i] and percentGreater > minPercent:
				allPercents.append(percentGreater)
				outperformed.append(True)
			else:
				allPercents.append("N/A")
				outperformed.append(False)
			if data1[2][i] == "UP" and data2[2][i] == "UP":
				market.append("UP")
			else:
				market.append("DOWN")
			dates.append(data1[0][i])
		else:
			pass
			#print(data1[1][i], " ", data2[1][i])
	return [dates, outperformed, allPercents, market]
#------------------------------
def returns(data, minPercent):
	data1 = data[0]
	data2 = data[1]
	newData1 = [[],[],[]]
	newData2 = [[],[],[]]
	try:
		amountOfDays = int(input("How many trading days (weekdays) would you like to see returns compounded?\n> "))
		end = False
		for i in range(len(data[0][1])):
			try:
				data[0][1][i] = float(data[0][1][i])
			except:
				pass
		for i in range(len(data1[1])):
			if not end:
				if isinstance(data[0][1][i], float) or isinstance(data[0][1][i], int):
					if data1[1][i+amountOfDays] == data1[1][-1]:
						end = True
					if data1[1][i] - data1[1][i+amountOfDays] > 0:
						marketVal = "UP"
					else:
						marketVal = "DOWN"
					percent = (data1[1][i] - data1[1][i+amountOfDays]) / data1[1][i+amountOfDays]
					# percent = (data1[1][i+amountOfDays] / data1[1][i]) - 1
					newData1[0].append(data1[0][i])
					newData1[1].append(percent)
					newData1[2].append(marketVal)
			else:
				break


		end = False
		for i in range(len(data[1][1])):
			try:
				data[1][1][i] = float(data[1][1][i])
			except:
				pass
		for i in range(len(data2[1])):
			if not end:
				if isinstance(data[1][1][i], float) or isinstance(data[1][1][i], int):
					if data2[1][i+amountOfDays] == data2[1][-1]:
						end = True
					if data2[1][i] - data2[1][i+amountOfDays] > 0:
						marketGro = "UP"
					else:
						marketGro = "DOWN"
					percent = (data2[1][i] - data2[1][i+amountOfDays]) / data2[1][i+amountOfDays]
					# percent = (data2[1][i+amountOfDays] / data2[1][i]) - 1
					newData2[0].append(data2[0][i])
					newData2[1].append(percent)
					newData2[2].append(marketGro)
			else:
				break
		info = compare(newData1, newData2, minPercent)
		return info
	except:
		return "fail"
#------------------------------
def main():
	fileName = "percents.csv"
	data = [[[],[]],[[],[]]]
	#data[0][0] is a list of the dates in file 1
	#data[0][1] is a list of the NAV, or prices, in file 1
	#data[1][0] is a list of the dates in file 2
	#data[1][1] is a list of the NAV, or prices, in file 2
	dataFile1 = "value-2.csv"
	dataFile2 = "growth-2.csv"
	run = False
	start1 = False
	start2 = False
	csvData1 = open(dataFile1, "r")
	csvData2 = open(dataFile2, "r")
	linesData1 = csvData1.readlines()
	linesData2 = csvData2.readlines()
	try:
		minPercent = float(input("What should be the minimum percent? (Please only input a number)\n> "))
		run = True
	except:
		print("Not valid. Stopping program.")
		wait(1)
	if run:
		for i in range(len(linesData1)):
			line = linesData1[i].split(",")
			if line[0] == "Date":
				start1 = True
			elif start1:
				date, NAV = line[0], line[7]
				data[0][0].append(date)
				data[0][1].append(NAV)
		for i in range(len(linesData2)):
			line = linesData2[i].split(",")
			if line[0] == "Date":
				start2 = True
			elif start2:
				date, NAV = line[0], line[7]
				data[1][0].append(date)
				data[1][1].append(NAV)
		rawInfo = returns(data, minPercent)
		if rawInfo == "fail":
			print("Failure")
		else:
			info = reverseSort(rawInfo)
			dates = info[0]
			outperformed = info[1]
			allPercents = info[2]
			market = info[3]
			with open(fileName, "w") as csv_file:
				writer = csv.writer(csv_file, lineterminator="\n")
				writer.writerow(["Minimum Percent: ", str(minPercent) + "%"])
				writer.writerow([])
				writer.writerow(["Date","Outperformed","Percent Difference", "Market"])
				for i in range(len(dates)):
					writer.writerow([dates[i], outperformed[i], allPercents[i], market[i]])
			print("Success!", "\n" + "%s was either created or updated!" % (fileName))
main()