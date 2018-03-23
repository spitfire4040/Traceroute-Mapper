# header files
import sys
import os
import geoip2.webservice

def get_route():

	destination = raw_input("Enter a destination IP address to create traceroute map: ")

	# create traceroute and write to file
	cmd = "traceroute " + destination + " > traceroute.txt"
	os.system(cmd)

	# open files
	with open("traceroute.txt", "r") as f:
		with open("ip_list.txt", "w") as output:

			# split lines for parsing
			for line in f:
				line = line.split()

				# if first line, skip it
				if(line[0] == 'traceroute'):
					pass

				else:
					for item in line:

						# find ip address in line and write out
						if(item[0] == '('):
							item = item.strip('(),')

							# filter private IP addresses
							if str(item[0:3]) == '10.' or str(item[0:8]) == '192.168' or str(item[0:8]) == '172.16.':
								pass
							else:
								output.write(item + '\n')

def build_json():
	# open files
	with open("ip_list.txt", "r") as file:
		with open("coordinates.txt", "w") as output:

			# create client object
			client = geoip2.webservice.Client(131747, '8Z4AwF9omrH4')

			# start json string
			json = '{'

			# look up all ip's
			for ip_address in file:
				ip_address = ip_address.strip('\n')

				# get response object
				response = client.insights(ip_address)

				# find latitude and longitude
				lat = str(response.location.latitude)
				lon = str(response.location.longitude)

				# write output to file
				json += '{' + lat + ',' + lon + '},'

			# remove last comma and close json
			json = json[:-1] + '}'

			# write to file
			output.write(json)

def main():

	get_route()

	build_json()



if __name__ == '__main__':
 	main()