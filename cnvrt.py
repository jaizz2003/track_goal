import gpxpy 
import gpxpy.gpx 
import pandas as pd
import gmplot
from geopy.distance import geodesic 
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time as tm
import numpy as np
# import mysql.connector

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   passwd="pass"
# )
trck_latitude = [[]]
trck_longitude = [[]]
trck_elevation = [[]]
trck_Time = [[]]
trck_Total_elevation = []
trck_Total_distance = []
trck_Total_time = []
trck_max_altitude = []
trck_min_altitude = []

points = ['#FF0000','#008000','#0000FF','#800080','#FF00FF']

def segment(lati1,longi1,lati2,longi2):
	no_of_trck = len(trck_latitude)
	Total_seg_time = []
	Total_seg_dist = []
	Total_seg_speed = []
	Total_seg_ele = []
	max_seg_alt = []
	min_seg_alt = []
	lati = []
	longi = []
	ele = []
	tim = []
	j=0
	while j < no_of_trck:
		near_lat1 = 1
		near_lon1 = 1
		near_lat2 = 1
		near_lon2 = 1
		p = len(trck_latitude[j])
		i = 0
		near_dist1 = 10000000
		near_dist2 = 10000000
		point1 = 0
		point2 = 0
		#print(trck_longitude[1][1])
		while i<p:
			a = (lati1, longi1)
			b = (lati2,longi2) 
			c = (trck_latitude[j][i],trck_longitude[j][i])
			dist1 = (geodesic(a,c).km)
			dist2 = (geodesic(b,c).km)
			if near_dist1>dist1:
				near_dist1 = dist1
				near_lat1 = trck_latitude[j][i]
				near_lon1 = trck_longitude[j][i]
				point1 = i
			if near_dist2>dist2:
				near_dist2 = dist2
				near_lat2 = trck_latitude[j][i]
				near_lon2 = trck_longitude[j][i]
				point2 = i
			i = i+1
		p1 = min(point1,point2)
		p2 = max(point1,point2)
		p = len(trck_latitude[j])
		print(p1)
		print(p2)
		print(p) 
		i = 0
		k=p1
		latitude = []
		longitude = []
		elevation = []
		Time = []
		while k <= p2:
			latitude.append(trck_latitude[j][k])
			longitude.append(trck_longitude[j][k])
			elevation.append(trck_elevation[j][k])
			Time.append(trck_Time[j][k])
			k=k+1
		
		lati = latitude
		longi = longitude
		ele = elevation
		tim = Time

		n = len(Time)
		td = Time[n-1] - Time[0]
		Total_time = int(round(td.total_seconds()))

		alt_max = max(elevation)
		alt_min = min(elevation)
		ele = alt_max - alt_min
	   
		total_dist=0
		p = len(latitude)
		w = 0
		while w<p-1:
			a = (latitude[w], longitude[w]) 
			b = (latitude[w+1],longitude[w+1])
			total_dist += (geodesic(a,b).km)
			w = w+1
		Total_seg_ele.append(ele)
		max_seg_alt.append(alt_max)
		min_seg_alt.append(alt_min)
		Total_seg_time.append(Total_time)
		Total_seg_dist.append(total_dist)
		Total_seg_speed.append((total_dist/Total_time)*60)
		j = j+1
	data = gmplot.GoogleMapPlotter(lati[0],longi[0],17)
	data.scatter(lati,longi,'#FF0000',size = 1, marker = False)
	data.plot(lati,longi, 'cornflowerblue', edge_width = 3.0)
	data.draw("templates/part.html")
	i = 0
	ride = []
	while i < len(Total_seg_time):
		ride.append(i)
		i=i+1

	print(Total_seg_dist)
	print(Total_seg_time)
	index = np.arange(len(ride))
	plt.bar(index,Total_seg_time)
	plt.xlabel('Ride number', fontsize=5)
	plt.ylabel('Time Taken', fontsize=5)
	plt.xticks(index, ride, fontsize=5, rotation=30)
	plt.title('Comparison between different rides for the given segment')
	graph_name = "graph" + str(tm.time()) + ".png"
	for filename in os.listdir('static/'):
		if filename.startswith('graph'):  # not to remove other images
			os.remove('static/' + filename)
	plt.savefig('static/'+ graph_name,bbox_inches='tight')
	plt.close()
	name = "static/"+graph_name
	return Total_seg_dist[0],max_seg_alt[0],min_seg_alt[0]

# def plottin(Total_time,alt_max,alt_min,Ele,new_dist):

def trck(file_name):
	del trck_latitude[:]
	del trck_longitude[:]
	del trck_elevation[:]
	del trck_Time[:]
	for file in os.listdir('gps_data/'):
		latitude = []
		longitude = []
		elevation = []
		Time = []
		name = "gps_data/" + file
		gpx_file = open(name,'r')
		gpx = gpxpy.parse(gpx_file)
		for track in gpx.tracks:
			for segment in track.segments:
				for point in segment.points:
					for ex in point.extensions:
						latitude.append(point.latitude)
						longitude.append(point.longitude)
						elevation.append(point.elevation)
						Time.append(point.time)
		trck_latitude.append(latitude)
		trck_longitude.append(longitude)
		trck_elevation.append(elevation)
		trck_Time.append(Time)
	for file in os.listdir('gps_data/'):
		name = "gps_data/"+file
		os.remove(name)
	# plot = {'Latitude':latitude,'Longitude':longitude,'Elevation':elevation,'Time':Time}
	# df = pd.DataFrame(plot)
	# df.to_csv('file1.csv')
	no_of_trck = len(trck_latitude)
	print("hii")
	print(no_of_trck)
	print("hii")
	i = 0
	data = gmplot.GoogleMapPlotter(latitude[0],longitude[0],17)
	while i < no_of_trck:
		latitude = trck_latitude[i]
		longitude = trck_longitude[i]
		elevation = trck_elevation[i]
		Time = trck_Time[i]
		data.scatter(latitude,longitude,'#000000',size = 1, marker = False)
		data.plot(latitude,longitude, '%s'%points[i], edge_width = 3.0)
		i = i+1
		if i==no_of_trck:
			data.draw("%s"%file_name)
	j = 0
	print(no_of_trck)
	del trck_Total_elevation[:]
	del trck_Total_distance[:]
	del trck_Total_time[:]
	del trck_max_altitude[:]
	del trck_min_altitude[:]
	while j < no_of_trck:
		latitude = trck_latitude[j]
		longitude = trck_longitude[j]
		elevation = trck_elevation[j]
		Time = trck_Time[j]

		n = len(Time)
		td = Time[n-1] - Time[0]
		Total_time = int(round(td.total_seconds()/60))

		alt_max = max(elevation)
		alt_min = min(elevation)
		ele = alt_max - alt_min
	   
		total_dist=0
		p = len(latitude)
		i = 0
		while i<p-1:
			a = (latitude[i], longitude[i]) 
			b = (latitude[i+1],longitude[i+1])
			total_dist += (geodesic(a,b).km)
			i = i+1
		trck_min_altitude.append(alt_min)
		trck_max_altitude.append(alt_max)
		trck_Total_time.append(Total_time)
		trck_Total_distance.append(total_dist)
		trck_Total_elevation.append(ele)
		#print(total_dist)
		j = j+1
		# return trck_Total_elevation,trck_min_altitude,trck_max_altitude,trck_Total_distance,trck_Total_time

def trckdetails(no):
	p = len(trck_Total_time)
	print(p)
	return trck_Total_time[no],trck_min_altitude[no],trck_max_altitude[no],trck_Total_elevation[no],trck_Total_distance[no]

def graphanalysis(tracks,attribute):
	total_trck = len(tracks)
	i=0
	while i<total_trck:
		j = tracks[i]
		elevation = trck_elevation[j]
		Time = trck_Time[j]
		latitude = trck_latitude[j]
		longitude = trck_longitude[j]
		distance = []
		time = []
		p = len(elevation)
		k = 0
		while k<=p-1:
			a = (latitude[0], longitude[0])
			b = (latitude[k],longitude[k])
			c = (geodesic(a,b).km)
			distance.append(c)
			k = k+1
		i = i+1
		if attribute=="Elevation":
			plt.plot(distance,elevation,label='Track %d'%j)
		elif attribute=="Time":
			u = len(Time)
			t = 0
			while t<=u-1:
				td = Time[t] - Time[0]
				td = int(round(td.total_seconds()/60))
				time.append(td)
				t = t+1
			plt.plot(distance,time,label='Track %d'%j)
	plt.xlabel('Distance(in km)')
	if attribute=="Elevation":
		plt.ylabel('Elevation(in metre)')
		plt.title('Distance Vs Elevation')
	elif attribute=="Time":
		plt.ylabel('Time(in minutes)')
		plt.title('Distance Vs Time')
	
	plt.grid(True)
	plt.legend()
	# plt.show()
	graph_name = "graph" + str(tm.time()) + ".png"
	for filename in os.listdir('static/'):
		if filename.startswith('graph'):  # not to remove other images
			os.remove('static/' + filename)
	plt.savefig('static/'+ graph_name,bbox_inches='tight')
	plt.close()
	name = "static/"+graph_name
	return name

