import csv

def create_cvs_file():
	records = [
	{ 'id' : '1' , 'firstname' : 'fathi' , 'lastname' : 'altoom' },
	{ 'id' : '2' , 'firstname' : 'omer' , 'lastname' : 'ali' },
	]
	csv_writer = csv.writer(open('record.csv' , 'w') , delimiter=',')
	csv_writer.writerow(['Id' , 'Firstname' , 'Lastname'])
	for record in records:
		csv_writer.writerow([record['id'] , record['firstname'] , record['lastname']])

def read_csv_file():
	for row in csv.reader(open('record.csv' , 'r') , delimiter=','):
		if len(row) > 0 :
			print(row[0]+' '+row[1]+' '+row[2])
def update_csv_file():
	csv_writer = csv.writer(open('record.csv' , 'a') , delimiter=',')
	csv_writer.writerow(['5', 'ols' ,'altoom' ])



if __name__ == "__main__":
	# create_cvs_file()
	# read_csv_file()
	update_csv_file()
