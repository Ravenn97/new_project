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
		#cur.fetchall() trả về 1 tuple, lấy giá trị thứ nhất của tuple
		list_day.append(day[0]) 
		print("add success")
		#lấy 7 ngày gần nhất, sử dụng sorted sắp xếp 7 ngày đến ngày gần nhất dùng slide [-7:] sử dụng set để loaij bỏ các ngày trùng nhau
	seven_days_latest = list(set(sorted(list_day)))[-7:]  
	for day in seven_days_latest:
		cur.execute("SELECT COUNT(cid), SUM(ndelivered), SUM(ndroped), SUM(nclicked), SUM(nopened), _date FROM staticweek WHERE _date =  %s GROUP BY _date",(str(day),))
		print("excute success")
		mydb.commit()
		result = cur.fetchall()[0]
		print(len(result), result)
		list_result.append({"day":str(day), "count_id" : int(result[0]), "sum_ndelivered" : int(result[1]), "sum_ndroped": int(result[2]), "sum_nclicked" : int(result[3]), "sum_opened" : int(result[4])})

	cur.close()
	mydb.close()
	return str(list_result)
	





	
if __name__ == '__main__':
	app.run(port = 5000)