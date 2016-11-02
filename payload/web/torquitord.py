#!/usr/bin/python
import time
import os
import commands
import re
import codecs
import sys
import io



if os.environ.get('TORQUITORHOME') == None :
	os.environ['TORQUITORHOME'] = "/var/www/html/torquitor"


while True:

	###########
	### pbsnodes
	###########

	#status, output = commands.getstatusoutput('pbsnodes | grep -E "np|free"')
	status, output = commands.getstatusoutput('pbsnodes')

	if status != 0 : # if command failed try calling it from diferent sources
		status, output = commands.getstatusoutput('/usr/local/bin/pbsnodes')
	if status != 0 :
		status, output = commands.getstatusoutput('$PBSNODESHOME/pbsnodes')
	elif status != 0 :
		print("Error: " + status + ": " + output);

	pbsnodes = re.split("\n\n", output)
	pbsdiv = '<div id="pbsnodes" class="fullwidth">\n'


	for pbsnode in pbsnodes:
		pbsnode = re.split("\n", pbsnode)
		pbsdiv += '<div class="pbsnode">\n'
		pbsdiv += "<h3>"+ pbsnode.pop(0) + "</h3>\n<ul>\n"
		for prop in pbsnode:
			prop = prop.strip()
		
			#if(re.compile("^cadejos|^zarate").match(prop)): pbsdiv += "<h3>"+ prop + "</h3>\n<ul>\n"
			if(re.compile("^properties").match(prop)): 
				prop = prop.replace("properties = ","")
				queueNames = prop.split(",")
				pbsdiv += "<li>" + "Queue(s):" + "\n<ul>"
				for qName in queueNames :
					pbsdiv += "<li>" + qName + "</li>\n"
				pbsdiv += "</ul></li>\n"
			elif(re.compile("^state").match(prop)): pbsdiv += "<li>" + prop.replace("state", "Node state") + "</li>\n"
			elif(re.compile("^jobs").match(prop)): pbsdiv += "<li>" + prop.replace("jobs", "Jobs") + "</li>\n"
			else: prop = ""
		pbsdiv += '</ul>\n</div>\n'
	pbsdiv += '</div>\n'

	os.system('echo "' + pbsdiv + '" > $TORQUITORHOME/data/pbsnodes.txt')


	###########
	### showq
	###########

	#status, output = commands.getstatusoutput('showq -v')
	#if status != 0 : # if command failed try calling it from diferent sources
	#	status, output = commands.getstatusoutput('/usr/local/maui/bin/showq -v')
	#elif status != 0 :
	#	status, output = commands.getstatusoutput('$SHOWQHOME/showq -v')
	#elif status != 0 :
	#	print("Error: " + status + ": " + output);

	#showq = re.split("\n", output)
	
	#for i in range(0, len(showq)):
	#	showq[i] = showq[i]+"<br>"
		#if "gpus" 	in showq[i]: showq[i] = ""
		

	#os.system('echo "' + ''.join(showq) + '" > $TORQUITORHOME/data/showq.txt')

	###########
	### qstat
	###########

	status, output = commands.getstatusoutput('qstat -a')
	
	if status != 0 : # if command failed try calling it from diferent sources
		status, output = commands.getstatusoutput('/usr/local/bin/qstat -a')
	elif status != 0 :
		status, output = commands.getstatusoutput('$QSTATHOME/qstat -a')
	elif status != 0 :
		print("Error: " + status + ": " + output);


	if output != "":
	
		output = output.replace("Job ID", "Job")

		body = '<table id="qstat" class="display" cellspacing="0" width="100%">\n'

		qstat = re.split("\n", output)

		#Remove first three lines (\n, meta.cnca:\n, \n)
		qstat.pop(0)
		qstat.pop(0)
		qstat.pop(0)

		#Remove the division line
		qstat.pop(1) 

		####
		#Create header and footer of the table
		####
		qstat[0] = qstat[0].replace("Time", "$R$", 1) 		#Replace first ocurrence of "Time" for wildcard R
		qstat[0] = qstat[0].replace("Time", "$E$", 1)		#Replace second ocurrence of "Time" for wildcard E
		qstat[0] = qstat[0].replace("$E$", "Elapsed-Time", 1)	#Replace wildcard E for "Elapsed_Time"
		qstat[0] = qstat[0].replace("$R$", "Required-Time", 1)	#Replace wildcard R for "Required_Time"

		#Split table for spaces and tabs and add the <td> tag
		qstatRow = re.split(" +|\t+", qstat[0])
		cols = len(qstatRow)
		head = "";
		for j in qstatRow:
			head += "\t<th>"+j+"</th>\n"

		#Header of the table
		body += "<thead>\n"
		body += "<tr>\n"
		body += head
		body += "</tr>\n"
		body += "</thead>\n"

		#Footer of the table
		body += "<tfoot>\n"
		body += "<tr>\n"
		body += head
	
		body += "</tr>\n"
		body += "</tfoot>\n"	


		#####
		# Parse contents of the table
		#####
	
		#Remove header of the table before processing contents
		qstat.pop(0);

		modal = '<div id="modal_dialogs">'
		body += "<tbody>\n"
		for i in range(0, len(qstat)):
	
			qstatRow = re.split(" +|\t+", qstat[i])
			body += "<tr>\n"

			# Array might contain whitespace elements at the end, if so remove them
			while(len(qstatRow) > cols) :
				qstatRow.pop(-1)

			# For each cell create the <td> tag
			# Identify the cells with the JobId (In this case represented by ".meta.cnca"
			for j in qstatRow:
				if(re.compile("^[0-9]{3,}\.meta\.cnca").match(j)): body += '\t<td id="' + j + '" class="jid dt-center">'+j+'</td>\n'
				else: body += '\t<td class="dt-center">'+j+'</td>\n'
		
			body += "</tr>\n"

			# Get status for the job specified in this row
			status, output = commands.getstatusoutput('qstat -f ' + qstatRow[0]);
			if status != 0 : # if command failed try calling it from diferent sources
				status, output = commands.getstatusoutput('/usr/local/bin/qstat -f ' + qstatRow[0])
			elif status != 0 :
				status, output = commands.getstatusoutput('$QSTATHOME/qstat -f ' + qstatRow[0])
			elif status != 0 :
				print("Error: " + status + ": " + output);
			jobinfo = re.split("\n", output)

			# Create a hidden div with the job status information, filter its entries and add them to a list
			modal += '<div id="Job.' + str(qstatRow[0]) + '" class="modal">\n<ul>\n'
			jobid = jobname = jobowner = jobqueue = jobstate = jobstderr = jobstdout = jobhosts = jobargs = jobqtime = jobetime = jobexitstatus = jobstarttime = jobcompletedtime = jobtotaltime = ""
			for j in jobinfo:
				j = j.strip()+"\n"
				if		(re.compile("^Job Id").match(j)): 		jobid = '<li><b>'+"Job ID: <tt>"+ j[j.find(":")+2:] +'</b></tt></li>'
				elif	(re.compile("^Job_Name").match(j)): 	jobname = '<li>'+"Job name: <tt>"+ j[j.find("=")+2:] +'</tt></li>'
				elif	(re.compile("^Job_Owner").match(j)):	jobowner = '<li>'+"Job owner: <tt>"+ j[j.find("=")+2:] +'</tt></li>'
				elif	(re.compile("^job_state").match(j)):	jobstate = '<li>'+"Job state: <tt>"+ j[j.find("=")+2:] +'</tt></li>'
				elif	(re.compile("^queue =").match(j)): 		jobqueue = '<li>'+"Queue: <tt>"+ j[j.find("=")+2:] +'</tt></li>'
				elif	(re.compile("^Error_Path").match(j)):	jobstderr = '<li>'+"stderr file: <tt>"+ j[j.find("=")+2:] +'</tt></li>'
				elif	(re.compile("^Output_Path").match(j)): 	jobstdout = '<li>'+"stdout file: <tt>"+ j[j.find("=")+2:] +'</tt></li>'
				elif	(re.compile("^exec_host").match(j)): 	jobhosts = '<li>'+"Execution host(s): <tt>"+ j[j.find("=")+2:] +'</tt></li>'
				elif	(re.compile("^qtime").match(j)): 		jobqtime = '<li>'+"Queued time: <tt>"+ j[j.find("=")+2:] +'</tt></li>'
				elif	(re.compile("^etime").match(j)): 		jobetime = '<li>'+"etime: <tt>"+ j[j.find("=")+2:] +'</tt></li>' #????
				elif	(re.compile("^exit_status").match(j)): 	jobexitstatus = '<li>'+"Job exit status: <tt>"+ j[j.find("=")+2:] +'</tt></li>'
				elif	(re.compile("^submit_args").match(j)): 	jobargs = '<li>'+"Submitted arguments: <tt>"+ j[j.find("=")+2:] +'</tt></li>'
				elif	(re.compile("^start_time").match(j)): 	jobstarttime = '<li>'+"Start time: <tt>"+ j[j.find("=")+2:] +'</tt></li>'
				elif	(re.compile("^comp_time").match(j)): 	jobcompletedtime = '<li>'+"Completed time: <tt>"+ j[j.find("=")+2:] +'</tt></li>'
				elif	(re.compile("^total_runtime").match(j)):jobtotaltime = '<li>'+"Total runtime: <tt>"+ j[j.find("=")+2:] + "seconds" + '</tt></li>'
		
			modal +=  jobid + jobname + jobowner + jobqueue + jobstate + jobstderr + jobstdout + jobhosts + jobargs + jobqtime + jobetime + jobexitstatus + jobstarttime + jobcompletedtime + jobtotaltime
			modal += "</ul>\n</div>\n"
		
		body += "</tbody>\n"
		body += "</table>"
		modal += "</div>"
		os.system("echo '" + body + "' > $TORQUITORHOME/data/qstat.txt")
		os.system("echo '" + modal + "' > $TORQUITORHOME/data/jobinfo.txt")
	
		

	time.sleep(5)

