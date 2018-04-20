from flask import Flask , request
import csv
import json
import MySQLdb
from datetime import datetime
app = Flask(__name__)


		
@app.route("/api/statics")
def take_data():
	day = request.args.get("day",default = None)
	csvfile = open("/home/van-xa/Downloads/static_week_2018_04_12_14_04_22.csv", 'r')
	reader = csv.DictReader( csvfile)
	
	for row in reader:
		if day in row["date"]:
			result.append(row)
	csvfile.close()
	return str(result)


@app.route("/api/statics/week")
def sum_of_week():
	list_day = []
	list_result = []

	mydb = MySQLdb.connect(host='localhost',user='root',passwd='dotung',db='loginDB')
	cur = mydb.cursor()
	csvfile = open("/home/van-xa/Downloads/static_week_2018_04_12_14_04_22.csv", 'r')
	reader = csv.reader(csvfile)
	for row in reader:
		try:
			cur.execute('INSERT INTO staticweek (_date, cid, ndelivered, ndroped, nclicked, nopened) VALUES (%s, %s, %s, %s, %s, %s )', row)
			mydb.commit()
		except Exception as e:
			print(e)
			pass
	cur.execute("SELECT _date from staticweek")
	mydb.commit()
	for day in cur.fetchall():
		list_day.append(day[0])
		print("them thanh cong")
	seven_days_latest = list(set(sorted(list_day)))[-7:]
	for day in seven_days_latest:
		cur.execute("SELECT COUNT(cid), SUM(ndelivered), SUM(ndroped), SUM(nclicked), SUM(nopened), _date FROM staticweek WHERE _date =  %s GROUP BY _date",(str(day),))
		print("ex thanh cong")
		mydb.commit()
		result = cur.fetchall()[0]
		print(len(result), result)
		list_result.append({"day":day, "count_id" : result[0], "sum_ndelivered" : result[1], "sum_ndroped": result[2], "sum_nclicked" : result[3], "sum_opened" : result[4]})

	cur.close()
	mydb.close()
	return str(list_result)
	





	
if __name__ == '__main__':
	app.run(port = 5000)