source = """
0900 0912	english
0926 1047	machine learning
1216 1251	electromagnetism L
1306 1335
1345 1358
1415 1530	machine learning L
1558 1604	optimization
1621 1734
1841 1850
"""

totalMinutes = 0

for line in source.strip().split("\n"):
  try:
    line = line.split("\t")[0].split(" ")
    t1 = int(line[0])
    t2 = int(line[1])
    dHrs = t2 // 100 - t1 // 100
    dMins = t2 % 100 - t1 % 100
    dt = 60 * dHrs + dMins

    if dt < 0:
      print("Negative time interval:", t1, t2)

    totalMinutes += dt
  except:
    pass

print(totalMinutes // 60, str(totalMinutes % 60).zfill(2), sep=":")

def create_csv(file_in, file_out):
	weekdays = ("ma", "ti", "ke", "to", "pe", "la", "su")
	current_day = "UNDEFINED_DAY"
	current_activity = "UNDEFINED_ACTIVITY"

	f_out.write("viikonpäivä,päivämäärä,aloitus,lopetus,toiminta,lisämääre\n")
	for idx, line in enumerate(file_in):
		if (idx % 100 == 0):
			print(f"Processing line {idx}.")

		line = line.strip(" \n\t")

		output_line = ""

		if line.startswith(weekdays):
			# Output day in the format {weekday},{day}.{month}
			current_day = ",".join(line.split(" "))
			continue
		elif line == "":
			# Skip empty lines
			continue
		elif line.startswith("yht"):
			# Skip lines summarizing total minutes
			continue
		elif line[0].isnumeric():
			# Here the first character in the line is a number

			# The line should separate its numeric and tex parts by a tab
			splits = line.split("\t")
			
			# The numbers are separated by a space
			numerics = splits[0].strip().split(" ")
			# There should be exactly two numeric parts before the tab
			if len(numerics) != 2:
				print("Erroneous line:", line, end="")
				continue
			# The numeric parts should be given in the format hhmm 
			if len(numerics[0]) != 4 or len(numerics[1]) != 4:
				print("Erroneous line", line, end="")
				continue

			# Change the time format to hh:mm 
			numerics = [ns[0:2] + ":" + ns[2:4] for ns in numerics]
			
			num = ",".join(numerics)
			
			if len(splits) > 2:
				# There should be no more than one tab in the line
				print("Erroneous line:", line, end="")
				continue
			elif len(splits) == 2:
				# The part after the tab describes the activity
				text = splits[1]
				# Extract the rightmost word of the text
				text_spl = text.rsplit(" ", 1)
				
				glue = " "
				# Check if the text has at least two parts and that the last one is a single letter (specifying the activity) 
				if len(text_spl) > 1 and len(text_spl[1]) == 1:
					glue = ","
			
				# Update the current activity
				current_activity = glue.join(text_spl)
			if len(splits) == 1:
				# The line only contains a numeric part
				pass

			output_line = f"{num},{current_activity}"
		
		else:
			# In case of unkwnown line format, print error message
			print("Erroneous line:", line)
			continue

		file_out.write(f"{current_day},{output_line}")
		file_out.write("\n")

	f_in.close()
	f_out.close()

f_in = open("./data/ajkoja eletty2023.txt", "r", encoding="utf8")
f_out = open("./data/ajat2023.csv", "w", encoding="utf8")

create_csv(f_in, f_out)