#Wolfgang Busch October 2011
# script summarizes the day to day growth rate and other traits
# is streamlined for the sector based plate splitting and QC
#works for 5 days of monitoring


import sys
import os
import time
import datetime
import numpy
from math import *
from numpy import *

# specify input file - the rest should then go automatically
single_root_quant_file="/Volumes/busch/lab/20120111_MAGIC_Santosh_reprocessing/2012-01-12MAGIC_curated_Quantification_REB_V7.5_processed.txt"

outfilename_GR=single_root_quant_file+"_indiv_GR_V7.5_V1.txt"
outfilename_GR_avg=single_root_quant_file+"_avg_GR_V7.5_V1.txt"
outfilename_GR_avg=single_root_quant_file+"_avg_GR_V7.5_V1.txt"


outfile_GR=open(outfilename_GR, 'w')

outfile_GR.write("ACC_ID\tset\tplate\tsector\tindividual\tGRd12\tGRd23\tGRd34\tGRd45\tangle_var\tTL_d1\tTL_d2\tTL_d3\tTL_d4\tTL_d5\tEL_d1\tEL_d2\tEL_d3\tEL_d4\tEL_d5\tTR_d1\tTR_d2\tTR_d3\tTR_d4\tTR_d5\tRW_d1\tRW_d2\tRW_d3\tRW_d4\tRW_d5\n")


xml_content=open(single_root_quant_file, 'r')
seedling_data=xml_content.readlines()[1:]
xml_content.close()

acc_id=[]
set=[]
sector=[]
plate=[]
day_id=[]
root_width=[]
individual=[]
x_root_start=[]
euclid_length=[]
angle=[]
total_length=[]
topology_ratio=[]
hash_id=[]
unique_hash_id=[]
GR_table_plate=[]
GR_table_pos=[]
GR_table_acc_id=[]
GR_table_set=[]
GRd12_table=[]
GRd23_table=[]
GRd34_table=[]
GRd45_table=[]
d1_TL_table=[]
d2_TL_table=[]
d3_TL_table=[]
d4_TL_table=[]
d5_TL_table=[]
d1_RW_table=[]
d2_RW_table=[]
d3_RW_table=[]
d4_RW_table=[]
d5_RW_table=[]
d1_EL_table=[]
d2_EL_table=[]
d3_EL_table=[]
d4_EL_table=[]
d5_EL_table=[]
d1_TR_table=[]
d2_TR_table=[]
d3_TR_table=[]
d4_TR_table=[]
d5_TR_table=[]
angle_var_table=[]
root_width_table=[]

for line in seedling_data:
	line=line.strip("\n")
	line=line.strip("\r")
	acc_id.append(line.split("\t")[0])
	set.append(line.split("\t")[1])
	sector.append(line.split("\t")[2])
	plate.append(line.split("\t")[3])
	day_id.append(int(line.split("\t")[4]))
	individual.append(int(line.split("\t")[5]))
	x_root_start.append(line.split("\t")[6])
	euclid_length.append(float(line.split("\t")[7]))
	angle.append(float(line.split("\t")[8]))
	total_length.append(float(line.split("\t")[9]))
	topology_ratio.append(float(line.split("\t")[10]))
	root_width.append(float(line.split("\t")[11]))
	
	#hash=acc+set+plate+sector+indiv
	hash_id.append(str(line.split("\t")[0])+"_"+(line.split("\t")[1])+"_"+(line.split("\t")[3])+"_"+(line.split("\t")[2])+"_"+(line.split("\t")[5]))

for hi in hash_id:
	if hi not in unique_hash_id:
		unique_hash_id.append(hi)

for U_HI in unique_hash_id:
	TL_day1=(-1)
	TL_day2=(-1)
	TL_day3=(-1)
	TL_day4=(-1)
	TL_day5=(-1)
	RW_day1=(-1)
	RW_day2=(-1)
	RW_day3=(-1)
	RW_day4=(-1)
	RW_day5=(-1)
	EL_day1=(-1)
	EL_day2=(-1)
	EL_day3=(-1)
	EL_day4=(-1)
	EL_day5=(-1)
	TR_day1=(-1)
	TR_day2=(-1)
	TR_day3=(-1)
	TR_day4=(-1)
	TR_day5=(-1)
	GRd12=(-1)
	GRd23=(-1)
	GRd34=(-1)
	GRd45=(-1)
	angle_variation=[]
	
	angle_var=1000
	for root_image in range(0,len(hash_id)):
		if hash_id[root_image]== U_HI:
			if day_id[root_image]==1:
				TL_day1=float(total_length[root_image])
				EL_day1=euclid_length[root_image]
				TR_day1=topology_ratio[root_image]
				ANGLE_day1=angle[root_image]
				angle_variation.append(float(ANGLE_day1))
				RW_day1=float(root_width[root_image])
			if day_id[root_image]==2:
				TL_day2=float(total_length[root_image])
				EL_day2=euclid_length[root_image]
				TR_day2=topology_ratio[root_image]
				ANGLE_day2=angle[root_image]
				angle_variation.append(float(ANGLE_day2))
				RW_day2=float(root_width[root_image])
			if day_id[root_image]==3:
				TL_day3=float(total_length[root_image])
				EL_day3=euclid_length[root_image]
				TR_day3=topology_ratio[root_image]
				ANGLE_day3=angle[root_image]
				angle_variation.append(float(ANGLE_day3))
				RW_day3=float(root_width[root_image])
			if day_id[root_image]==4:
				TL_day4=float(total_length[root_image])
				EL_day4=euclid_length[root_image]
				TR_day4=topology_ratio[root_image]
				ANGLE_day4=angle[root_image]
				angle_variation.append(float(ANGLE_day4))
				RW_day4=float(root_width[root_image])
			if day_id[root_image]==5:
				TL_day5=float(total_length[root_image])
				EL_day5=euclid_length[root_image]
				TR_day5=topology_ratio[root_image]
				ANGLE_day5=angle[root_image]
				angle_variation.append(float(ANGLE_day5))
				RW_day5=float(root_width[root_image])
	if TL_day1 > 0 and TL_day2 > 0:
		GRd12=float(TL_day2)-float(TL_day1)
	if TL_day2 > 0 and TL_day3 > 0:
		GRd23=float(TL_day3)-float(TL_day2)
	if TL_day3 > 0 and TL_day4 > 0:
		GRd34=float(TL_day4)-float(TL_day3)
	if TL_day4 > 0 and TL_day5 > 0:
		GRd45=float(TL_day5)-float(TL_day4)
	if len(angle_variation) > 3:
		angle_var=std(angle_variation)
	GR_table_plate.append(U_HI.split('_')[2])
	GR_table_pos.append(U_HI.split('_')[3])
	GR_table_acc_id.append(U_HI.split('_')[0])
	GR_table_set.append(U_HI.split('_')[1])
	GRd12_table.append(GRd12)
	GRd23_table.append(GRd23)
	GRd34_table.append(GRd34)
	GRd45_table.append(GRd45)
	d1_TL_table.append(TL_day1)
	d2_TL_table.append(TL_day2)
	d3_TL_table.append(TL_day3)
	d4_TL_table.append(TL_day4)
	d5_TL_table.append(TL_day5)
	d1_RW_table.append(RW_day1)
	d2_RW_table.append(RW_day2)
	d3_RW_table.append(RW_day3)
	d4_RW_table.append(RW_day4)
	d5_RW_table.append(RW_day5)
	d1_EL_table.append(EL_day1)
	d2_EL_table.append(EL_day2)
	d3_EL_table.append(EL_day3)
	d4_EL_table.append(EL_day4)
	d5_EL_table.append(EL_day5)
	d1_TR_table.append(TR_day1)
	d2_TR_table.append(TR_day2)
	d3_TR_table.append(TR_day3)
	d4_TR_table.append(TR_day4)
	d5_TR_table.append(TR_day5)
	angle_var_table.append(angle_var)
	outfile_GR.write(str(U_HI.split('_')[0])+"\t"+str(U_HI.split('_')[1])+"\t"+str(U_HI.split('_')[2])+"\t"+str(U_HI.split('_')[3])+"\t"+str(U_HI.split('_')[4])+"\t"+str(GRd12)+"\t"+str(GRd23)+"\t"+str(GRd34)+"\t"+str(GRd45)+"\t"+str(angle_var)+"\t"+str(TL_day1)+"\t"+str(TL_day2)+"\t"+str(TL_day3)+"\t"+str(TL_day4)+str(TL_day5)+"\t"+str(EL_day1)+"\t"+str(EL_day2)+"\t"+str(EL_day3)+"\t"+str(EL_day4)+str(EL_day5)+"\t"+str(TR_day1)+"\t"+str(TR_day2)+"\t"+str(TR_day3)+"\t"+str(TR_day4)+str(TR_day5)+"\t"+str(RW_day1)+"\t"+str(RW_day2)+"\t"+str(RW_day3)+"\t"+str(RW_day4)+str(RW_day5)+"\n")

outfile_GR.close()




outfile_GR_avg=open(outfilename_GR_avg, 'w')

outfile_GR_avg.write("ACC_ID\tGR12_mean\tGR23_mean\tGR34_mean\tGR45_mean\tangle_var\tTL_d1\tTL_d2\tTL_d3\tTL_d4\tTL_d5\tEL_d1\tEL_d2\tEL_d3\tEL_d4\tEL_d5\tTR_d1\tTR_d2\tTR_d3\tTR_d4\tTR_d5\tRW_d1\tRW_d2\tRW_d3\tRW_d4\tRW_d5\n")

unique_acc_id=[]

#get list of unique acc_ids
for si in acc_id:
	if si not in unique_acc_id:
		unique_acc_id.append(si)


for unique_acc in unique_acc_id:
	GRd12_acc_table=[]
	GRd23_acc_table=[]
	GRd34_acc_table=[]
	GRd45_acc_table=[]
	angle_acc_table=[]
	d1_TL_acc_table=[]
	d2_TL_acc_table=[]
	d3_TL_acc_table=[]
	d4_TL_acc_table=[]
	d5_TL_acc_table=[]
	d1_TR_acc_table=[]
	d2_TR_acc_table=[]
	d3_TR_acc_table=[]
	d4_TR_acc_table=[]
	d5_TR_acc_table=[]
	d1_EL_acc_table=[]
	d2_EL_acc_table=[]
	d3_EL_acc_table=[]
	d4_EL_acc_table=[]
	d5_EL_acc_table=[]
	d1_RW_acc_table=[]
	d2_RW_acc_table=[]
	d3_RW_acc_table=[]
	d4_RW_acc_table=[]
	d5_RW_acc_table=[]
	for GR_entry in range(0,len(GR_table_acc_id)):
		if unique_acc == (GR_table_acc_id[GR_entry]):
			if 0 < GRd12_table[GR_entry] < 1000:
				GRd12_acc_table.append(GRd12_table[GR_entry])
			if 0 < GRd23_table[GR_entry] < 1000:
				GRd23_acc_table.append(GRd23_table[GR_entry])
			if 0 < GRd34_table[GR_entry] < 1000:
				GRd34_acc_table.append(GRd34_table[GR_entry])
			if 0 < GRd45_table[GR_entry] < 1000:
				GRd45_acc_table.append(GRd45_table[GR_entry])
			if angle_var_table[GR_entry] < 999:
				angle_acc_table.append(angle_var_table[GR_entry])
			if 0 < d1_TL_table[GR_entry] < 100000:
				d1_TL_acc_table.append(d1_TL_table[GR_entry])
			if 0 < d2_TL_table[GR_entry] < 100000:
				d2_TL_acc_table.append(d2_TL_table[GR_entry])
			if 0 < d3_TL_table[GR_entry] < 100000:
				d3_TL_acc_table.append(d3_TL_table[GR_entry])
			if 0 < d4_TL_table[GR_entry] < 100000:
				d4_TL_acc_table.append(d4_TL_table[GR_entry])
			if 0 < d5_TL_table[GR_entry] < 100000:
				d5_TL_acc_table.append(d5_TL_table[GR_entry])
			if 0 < d1_TR_table[GR_entry] < 100000:
				d1_TR_acc_table.append(d1_TR_table[GR_entry])
			if 0 < d2_TR_table[GR_entry] < 100000:
				d2_TR_acc_table.append(d2_TR_table[GR_entry])
			if 0 < d3_TR_table[GR_entry] < 100000:
				d3_TR_acc_table.append(d3_TR_table[GR_entry])
			if 0 < d4_TR_table[GR_entry] < 100000:
				d4_TR_acc_table.append(d4_TR_table[GR_entry])
			if 0 < d5_TR_table[GR_entry] < 100000:
				d5_TR_acc_table.append(d5_TR_table[GR_entry])
			if 0 < d1_EL_table[GR_entry] < 100000:
				d1_EL_acc_table.append(d1_EL_table[GR_entry])
			if 0 < d2_EL_table[GR_entry] < 100000:
				d2_EL_acc_table.append(d2_EL_table[GR_entry])
			if 0 < d3_EL_table[GR_entry] < 100000:
				d3_EL_acc_table.append(d3_EL_table[GR_entry])
			if 0 < d4_EL_table[GR_entry] < 100000:
				d4_EL_acc_table.append(d4_EL_table[GR_entry])
			if 0 < d5_EL_table[GR_entry] < 100000:
				d5_EL_acc_table.append(d5_EL_table[GR_entry])
			if 0 < d1_RW_table[GR_entry] < 100000:
				d1_RW_acc_table.append(d1_RW_table[GR_entry])
			if 0 < d2_RW_table[GR_entry] < 100000:
				d2_RW_acc_table.append(d2_RW_table[GR_entry])
			if 0 < d3_RW_table[GR_entry] < 100000:
				d3_RW_acc_table.append(d3_RW_table[GR_entry])
			if 0 < d4_RW_table[GR_entry] < 100000:
				d4_RW_acc_table.append(d4_RW_table[GR_entry])
			if 0 < d5_RW_table[GR_entry] < 100000:
				d5_RW_acc_table.append(d5_RW_table[GR_entry])
			print(unique_acc)
	outfile_GR_avg.write(str(unique_acc)+"\t"+str(mean(GRd12_acc_table))+"\t"+str(mean(GRd23_acc_table))+"\t"+str(mean(GRd34_acc_table))+"\t"+str(mean(GRd45_acc_table))+"\t"+str(mean(angle_acc_table))+"\t"+str(mean(d1_TL_acc_table))+"\t"+str(mean(d2_TL_acc_table))+"\t"+str(mean(d3_TL_acc_table))+"\t"+str(mean(d4_TL_acc_table))+"\t"+str(mean(d5_TL_acc_table))+"\t"+str(mean(d1_EL_acc_table))+"\t"+str(mean(d2_EL_acc_table))+"\t"+str(mean(d3_EL_acc_table))+"\t"+str(mean(d4_EL_acc_table))+"\t"+str(mean(d5_EL_acc_table))+"\t"+str(mean(d1_TR_acc_table))+"\t"+str(mean(d2_TR_acc_table))+"\t"+str(mean(d3_TR_acc_table))+"\t"+str(mean(d4_TR_acc_table))+"\t"+str(mean(d5_TR_acc_table))+"\t"+str(mean(d1_RW_acc_table))+"\t"+str(mean(d2_RW_acc_table))+"\t"+str(mean(d3_RW_acc_table))+"\t"+str(mean(d4_RW_acc_table))+"\t"+str(mean(d5_RW_acc_table))+"\n")

outfile_GR_avg.close()

