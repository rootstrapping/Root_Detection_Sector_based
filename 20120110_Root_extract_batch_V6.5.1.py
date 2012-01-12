###################by Wolfgang Busch May2011##############################
#This tool extracts root lengths measurements
#Principles
#1. Scan rows for completly empty space (partitions roots)
#2. Scan segments for last 55 value that is follwed by 10 55 values (beginning of root) [55 values are indicative of root color]
#3. Fills gaps up to a certain limit
#4. Counts total pixels and filled in gaps for total length
#5. Calculate euclidian distance of start and end of the root
#6. Gets the Angle of the root relative
#7. Gets width of the root (i.e. distance map value)
# creates output suitable for diagnostic images
#problems: if two shots overlap partition of regions don't work; need to do repartitioning ;

import sys
import os
import time
import datetime

#specify path to directory with XY coordinates of roots from plates (Extract_XY_from_plate_data_V4.ijm output)

path='/net/gmi.oeaw.ac.at/busch/lab/20120111_MAGIC_Santosh_reprocessing/'

max_allowed_gap=70

#start output
today = datetime.date.today()
outfilename=path+str(today)+"_XY_width_coord_no_shoot_Quantification_REB_V6.5.txt"

#filehandling

outfile=open(outfilename, 'w')
outfile.write("Analyzed_File\troot_number\tsanity_flag\troot_start_x\troot_start_y\troot_end_x\troot_end_y\tshort_root_length\troot_angle\tcounted_root_pixels\taverage width\n")

dirList=os.listdir(path)
for files in range(0,len(dirList)):
	final_fill_table_roots=[]
	true_root_no=0
	if dirList[files].startswith('XY_width_coord_no_shoot_'):
		file = dirList[files]
		xml_content=open(path+file, 'r')
		xml=xml_content.readlines()
		xml_content.close()
		
		width_file = file.replace('no_shoot_','')
		width_content=open(path+width_file, 'r')
		width=width_content.readlines()
		width_content.close()
		
		x_coord=[]
		y_coord=[]
		intensity=[]
		width_xy_hash=[]
		width_value=[]
		objectintervals=[]
		
		for line in xml:
			x_coord.append(int(line.split('\t')[0]))
			y_coord.append(int(line.split('\t')[1]))
			intensity.append(int(line.split('\t')[2]))
		
		for line in width:
			width_xy_hash.append(str(line.split('\t')[0])+"_"+(line.split('\t')[1]))
			width_temp=255-(int(line.split('\t')[2]))
			width_value.append(width_temp)
		
		
		x_y_int = zip(x_coord,y_coord,intensity)
		x_y = zip(x_coord,y_coord)
		x_y_int_y_key=sorted(x_y_int, key=lambda student: x_y_int[1])
		
		x_trigger=0
		object_range=0
		# right root issue solved by extending the right range of object detection
		for value in range(min(x_coord),max(x_coord)+50):
			if value in x_coord:
				if x_trigger==0:
					if value not in objectintervals:
						objectintervals.append(value)
						x_trigger=1
			else:
				if x_trigger==1:
					if value not in objectintervals:
						objectintervals.append(value-1)
						x_trigger=0
		
		no_object=len(objectintervals)/2
		
		#check if objects have a shoot and determine botom of hypocotyl and bottom of root
		
		#get position in values
		#objectintervals_pos=[]
		last_records=[]
		
		#for coord in range(0,len(x_coord)):
		#	if x_coord[coord] in objectintervals:
		#		if x_coord[coord] not in last_records:
		#			objectintervals_pos.append(coord)
		#			last_records.append(x_coord[coord])
		
		object_range=0
		true_roots=[]
		lowest_shoot_xcoord_table=[]
		lowest_root_xcoord_table=[]
		lowest_shoot_ycoord_table=[]
		lowest_root_ycoord_table=[]
		
		
		for object in range(0,no_object):
			true_root=0
			lowest_shoot_coord=100000000
			lowest_root_coord=100000000
			lowest_shoot_xcoord=100000000
			lowest_root_xcoord=100000000
			lowest_shoot_ycoord=100000000
			lowest_root_ycoord=100000000
			shoot_counter=0
			for intensities in range(0,len(x_y_int_y_key)):
				if x_y_int_y_key[intensities][0] in range(objectintervals[object_range],objectintervals[object_range+1]):
					if lowest_root_ycoord > x_y_int_y_key[intensities][1]:
						lowest_root_xcoord =x_y_int_y_key[intensities][0]
						lowest_root_ycoord =x_y_int_y_key[intensities][1]
					if x_y_int_y_key[intensities][2]<100 and x_y_int_y_key[intensities][2] > 10:
						shoot_counter=shoot_counter+1
					elif x_y_int_y_key[intensities][2]>100 and x_y_int_y_key[intensities][2] < 10:
						shoot_counter=0
					if shoot_counter==50:
						true_root=1
						lowest_shoot_xcoord=x_y_int_y_key[intensities-50][0]
						lowest_shoot_ycoord=x_y_int_y_key[intensities-50][1]
			true_roots.append(true_root)
			lowest_shoot_xcoord_table.append(lowest_shoot_xcoord)
			lowest_root_xcoord_table.append(lowest_root_xcoord)
			lowest_shoot_ycoord_table.append(lowest_shoot_ycoord)
			lowest_root_ycoord_table.append(lowest_root_ycoord)
			object_range=object_range+2
		
		#determine if objects have shoot and root
		root_objects=[]
		lowest_true_shoot_xcoord_table=[]
		lowest_true_root_xcoord_table=[]
		lowest_true_shoot_ycoord_table=[]
		lowest_true_root_ycoord_table=[]
		obj_no=0
		
		for object in range(0,len(true_roots)):
			if true_roots[object] == 1:
				root_objects.append(objectintervals[obj_no])
				root_objects.append(objectintervals[obj_no+1])
				lowest_true_shoot_xcoord_table.append(lowest_shoot_xcoord_table[object])
				lowest_true_root_xcoord_table.append(lowest_root_xcoord_table[object])
				lowest_true_shoot_ycoord_table.append(lowest_shoot_ycoord_table[object])
				lowest_true_root_ycoord_table.append(lowest_root_ycoord_table[object])
			obj_no=obj_no+2
		
		true_root_no=len(root_objects)/2
		
		
		# determine intersection of root at deepest shoot point (used as a staring point for measurement)
		
		object_range=0
		lowest_shoot_xcoord_table_temp=[]
		lowest_shoot_ycoord_table_temp=[]
		total_root_skel_pixel=[]
		
		for object in range(0,true_root_no):
			root_pixels=[]
			filetered_rpx=[]
			for intensities in range(0,len(x_y_int)):
				if x_y_int[intensities][0] in range(root_objects[object_range],root_objects[object_range+1]):
					if x_y_int[intensities][2]>100:
						root_pixels.append(x_y_int[intensities][1])
						if lowest_true_shoot_ycoord_table[object] == x_y_int[intensities][1]:
							lowest_shoot_xcoord=x_y_int[intensities][0]
							lowest_shoot_ycoord=x_y_int[intensities][1]
			lowest_shoot_xcoord_table_temp.append(lowest_shoot_xcoord)
			lowest_shoot_ycoord_table_temp.append(lowest_shoot_ycoord)
			for pixels in range(0,len(root_pixels)):
				if root_pixels[pixels] <= lowest_shoot_ycoord:
					filetered_rpx.append(root_pixels[pixels])
			total_root_skel_pixel.append(len(filetered_rpx))
			object_range=object_range+2
		
		lowest_true_shoot_xcoord_table=lowest_shoot_xcoord_table_temp
		lowest_true_shoot_ycoord_table=lowest_shoot_ycoord_table_temp
		
		
		#measurements lengths and angle
		import math
		import numpy
		
		rootlength_short_table=[]
		root_angle_table=[]
		fill_start=[]
		fill_end=[]
		root_fill=[]
		fill_pixels_y=[]
		fill_pixels_x=[]
		width_table=[]
		final_width_table=[]
		final_root_end_table_x=[]
		final_root_end_table_y=[]
		final_root_eucl_length_table=[]
		final_root_total_length_table=[]
		final_root_angle_table=[]
		final_fill_table=[]
		final_fill_table_roots=[]
		object_range=0
		sanity_flag_table=[]
		extracted_roots=0
		
		#fill gaps and correct ends of root; remember that coordiante system is not intuitive (shoots are at hight y-values)
		for root in range(0,true_root_no):
			filled_segments=0
			total_root_pixel=0
			total_fill=0
			current_rootx=[]
			current_rooty=[]
			last_y_pixelroot_pixels=[]
			fill_dist=0
			last_ycoord=lowest_true_shoot_ycoord_table[root]
			last_xcoord=lowest_true_shoot_xcoord_table[root]
			final_root_end_y=lowest_true_root_ycoord_table[root]
			final_root_end_x=lowest_true_root_xcoord_table[root]
			shoot_np=numpy.array((lowest_true_shoot_xcoord_table[root],lowest_true_shoot_ycoord_table[root]))
			root_np=numpy.array((lowest_true_root_xcoord_table[root],lowest_true_root_ycoord_table[root]))
			for intensities in range(0,len(x_y_int)):
				if x_y_int[intensities][0] in range(root_objects[object_range],root_objects[object_range+1]):
					current_rootx.append(x_y_int[intensities][0])
					current_rooty.append(x_y_int[intensities][1])
			curr_root_x_y = zip(current_rootx,current_rooty)
			curr_root_y_key=sorted(curr_root_x_y, key=lambda student: curr_root_x_y[1])
			last_y=curr_root_y_key[0][1]
			last_x=curr_root_y_key[0][0]
			for y_coords in range(1,len(curr_root_y_key)):
				#look for subsequent pixels
				if (curr_root_y_key[y_coords][1]-last_y)<=1:
					last_y=curr_root_y_key[y_coords][1]
					last_x=curr_root_y_key[y_coords][0]
				#if there is are disjoint components, look for next component along vector of gravity
				elif (curr_root_y_key[y_coords][1]-last_y)>1 and ((curr_root_y_key[y_coords][1]-last_y)) < max_allowed_gap and ((curr_root_y_key[y_coords][1])) < lowest_true_shoot_ycoord_table[root]:
					fill_start.append(last_y+1)
					current_x=curr_root_y_key[y_coords][0]
					current_y=curr_root_y_key[y_coords][1]
					fill_line_point_1= numpy.array((last_x,last_y))
					fill_line_point_2= numpy.array((current_x,current_y))
					fill_dist = numpy.linalg.norm(fill_line_point_2-fill_line_point_1)
					if fill_dist < 2*(current_y-last_y):
						#print(last_x)
						#print(current_x)
						final_fill_table_roots.append(root)
						final_fill_table.append(last_x)
						final_fill_table_roots.append(root)
						final_fill_table.append(last_y)
						final_fill_table_roots.append(root)
						final_fill_table.append(current_x)
						final_fill_table_roots.append(root)
						final_fill_table.append(current_y)
						final_fill_table_roots.append(root)
						final_fill_table.append((abs(last_y-curr_root_y_key[y_coords][1])-2))
						final_fill_table_roots.append(root)
						final_fill_table.append(fill_dist)
						filled_segments=filled_segments+1
						last_y=curr_root_y_key[y_coords][1]
					else:
						continue
				#if components are more distant than threshhold, don't consider; since the algorythm goes from bottom to top, disjoint pieces that were already picked up, will be thrown out
				elif (curr_root_y_key[y_coords][1]-last_y)>1 and ((curr_root_y_key[y_coords][1]-last_y)) > max_allowed_gap and ((curr_root_y_key[y_coords][1])) < lowest_true_shoot_ycoord_table[root]:
					final_root_end_y=curr_root_y_key[y_coords][1]
					final_root_end_x=curr_root_y_key[y_coords][0]
					last_y=curr_root_y_key[y_coords][1]
					last_x=curr_root_y_key[y_coords][0]
					root_np=numpy.array((final_root_end_x,final_root_end_y))
					if filled_segments > 0:
						for filled_seg in range (0,filled_segments*6):
							final_fill_table.pop()
							final_fill_table_roots.pop()
							filled_segments=filled_segments-1
			#get sum of filled segments
			#print (root)
			#print len(final_fill_table)
			#print len(final_fill_table_roots)
			for fill in range(1,(len(final_fill_table)/6)+1):
				if (fill>extracted_roots):
					total_fill=total_fill+final_fill_table[(6*fill)-1]
			extracted_roots=len(final_fill_table)/6
			# get number of pixels in range of root
			#last_hit prevents segments with several unidentified roots to score multiple times;
			last_hit=[]
			for rows in range(1,len(current_rooty)):
				if current_rooty[rows] < lowest_true_shoot_ycoord_table[root] and current_rooty[rows] > final_root_end_y:
					if current_rooty[rows] not in last_hit:
						total_root_pixel=total_root_pixel+1
						last_hit.append(current_rooty[rows])
						xy_pos_hash=str(current_rootx[rows])+"_"+str(current_rooty[rows])
						for hashes in range(0,len(width_xy_hash)):
							if width_xy_hash[hashes] == xy_pos_hash:
								width_table.append(int(width_value[hashes]))
								break
					else:
						if abs(current_rootx[rows] - current_rootx[rows-1]) < 2:
							total_root_pixel=total_root_pixel+1
							last_hit.append(current_rooty[rows])
							xy_pos_hash=str(current_rootx[rows])+"_"+str(current_rooty[rows])
							for hashes in range(0,len(width_xy_hash)):
								if width_xy_hash[hashes] == xy_pos_hash:
									width_table.append(int(width_value[hashes]))
									break
			dist = numpy.linalg.norm(shoot_np-root_np)
			angle = math.atan2(lowest_true_shoot_xcoord_table[root]-final_root_end_x, lowest_true_shoot_ycoord_table[root]-final_root_end_y)
			degrees=math.degrees(angle)
			final_width_table.append(numpy.mean(width_table))
			final_root_end_table_x.append(final_root_end_x)
			final_root_end_table_y.append(final_root_end_y)
			final_root_eucl_length_table.append(dist)
			final_root_total_length_table.append(total_root_pixel+total_fill)
			final_root_angle_table.append(degrees)
			sanity_flag=1
			if ((abs(final_root_total_length_table[root]-numpy.mean(final_root_total_length_table))/numpy.std(final_root_total_length_table)) > 1.0):
				if ((abs(lowest_true_shoot_ycoord_table[root]-numpy.mean(lowest_true_shoot_ycoord_table))/numpy.std(lowest_true_shoot_ycoord_table)) > 1.0):
					sanity_flag=0
			sanity_flag_table.append(sanity_flag)
			object_range=object_range+2
	if (true_root_no > 0):
		fillings_table=zip(final_fill_table_roots,final_fill_table)
		for root in range(0,true_root_no):
			outfile.write(str(file)+"\t"+str(root+1)+"\t"+str(sanity_flag_table[root])+"\t"+str(lowest_true_shoot_xcoord_table[root])+"\t"+str(lowest_true_shoot_ycoord_table[root])+"\t"+str(final_root_end_table_x[root])+"\t"+str(final_root_end_table_y[root])+"\t"+str(final_root_eucl_length_table[root])+"\t"+str(final_root_angle_table[root])+"\t"+str(final_root_total_length_table[root])+"\t"+str(final_width_table[root])+"\t")
			for segment in range(0,len(fillings_table)):
				if (fillings_table[segment][0] == root):
					outfile.write(str(fillings_table[segment][1])+",")
			outfile.write("\n")


outfile.close()


