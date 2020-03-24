#!/usr/bin/python

###############################################################################
#                                                                             #
#                        Pi-Star Auto Remote Control                          #
#                                                                             #
#    Version 1.8, Code, Design and Development by Andy Taylor (MW0MWZ).       #
#                                                                             #
#        Heavily modded by Tim VK3FTZD for Pine64 MMDVM hotspot.              #
#   Changes include removal of all extra non DMR function, adding POCSAG,     #
#                  and change D-Star functions to DMR/POCSAG                  #
#                                                                             #
#  This Python script is desiged to look for specific things in the logs for  #
#       MMDVMHost and act on those to give RF control over the repeater.      #
#                                                                             #
###############################################################################

import datetime
import time
import linecache
import os
import subprocess
import ConfigParser
import random

totCall1 = 0
totCall2 = 0
totCall3 = 0

# Read the config;
config = ConfigParser.RawConfigParser()
config.read('/opt/mmdvm-dmr2pocsag/dmr2pocsag.ini')

# Read the MMDVMHost config;
mmdvmConfig = ConfigParser.RawConfigParser()
mmdvmConfig.read('/opt/MMDVMHost/MMDVM.ini')

# Read the DMRGateway config
DMRGatewayFile = '/opt/DMRGateway/DMRGateway.ini'
DMRGatewayExe = '/opt/DMRGateway/DMRGateway'
DMRGatewayConfig = ConfigParser.RawConfigParser()
DMRGatewayConfig.read(DMRGatewayFile)

# If not enabled, die;
isEnabled = config.get('enable', 'enabled')
if (isEnabled != 'true'):
	quit()

# Substitute variables from config
mmdvmLogPath = mmdvmConfig.get('Log', 'FilePath')
mmdvmFileRoot = mmdvmConfig.get('Log', 'FileRoot')
keeperCall = config.get('keeper', 'callsign')

# ID for POCSAG Pager
if config.has_option('pocsag', 'id'):
	pageid = config.get('pocsag', 'id')
else:
	pageid = 'notset'

# DMR Control Options
if config.has_option('dmr', 'reboot'):
	dmrreboot = config.get('dmr', 'reboot')
else:
	dmrreboot = str(999999999999)
if config.has_option('dmr', 'getip'):
	dmrgetip = config.get('dmr', 'getip')
else:
	dmrgetip = str(999999999999)
if config.has_option('dmr', '8Ball'):
        dmr8ball = config.get('dmr', '8Ball')
else:
        dmr8ball = str(999999999999)
if config.has_option('dmr', 'battery'):
	dmrgetbat = config.get('dmr', 'battery')
else:
	dmrgetbat = str(999999999999)
if config.has_option('dmr', 'ping'):
        dmrping = config.get('dmr', 'ping')
else:
        dmrping = str(999999999999)

# dmr ota commands
if config.has_option('ota', 'en_network1'):
        en_network1 = config.get('ota', 'en_network1')
else:
        en_network1 = str(999999999999)
if config.has_option('ota', 'd_network1'):
        d_network1 = config.get('ota', 'd_network1')
else:
        d_network1 = str(999999999999)

if config.has_option('ota', 'en_network2'):
        en_network2 = config.get('ota', 'en_network2')
else:
        en_network2 = str(999999999999)
if config.has_option('ota', 'd_network2'):
        d_network2 = config.get('ota', 'd_network2')
else:
        d_network2 = str(999999999999)

if config.has_option('ota', 'en_network3'):
        en_network3 = config.get('ota', 'en_network3')
else:
        en_network3 = str(999999999999)
if config.has_option('ota', 'd_network3'):
        d_network3 = config.get('ota', 'd_network3')
else:
        d_network3 = str(999999999999)

if config.has_option('ota', 'en_network4'):
        en_network4 = config.get('ota', 'en_network4')
else:
        en_network4 = str(999999999999)
if config.has_option('ota', 'd_network4'):
        d_network4 = config.get('ota', 'd_network4')
else:
        d_network4 = str(999999999999)

if config.has_option('ota', 'en_network5'):
        en_network5 = config.get('ota', 'en_network5')
else:
        en_network5 = str(999999999999)
if config.has_option('ota', 'd_network5'):
        d_network5 = config.get('ota', 'd_network5')
else:
        d_network5 = str(999999999999)

if config.has_option('ota', 'en_xlx'):
        en_xlx = config.get('ota', 'en_xlx')
else:
        en_xlx = str(999999999999)
if config.has_option('ota', 'd_xlx'):
        d_xlx = config.get('ota', 'd_xlx')
else:
        d_xlx = str(999999999999)


# callsign paging
#callsign 1
call1Enabled = config.get('call1', 'enabled')
if (call1Enabled != 'true'):
	callSign1 = str(999999999999)
else:
	if config.has_option('call1','callsign'):
		callSign1 = config.get('call1','callsign')
	else:
	        callSign1 = str(999999999999)

#callsign 2
call2Enabled = config.get('call2', 'enabled')
if (call2Enabled != 'true'):
	callSign1 = str(999999999999)
else:
	if config.has_option('call2','callsign'):
		callSign2 = config.get('call2','callsign')
	else:
	        callSign2 = str(999999999999)

#callsign 3
call3Enabled = config.get('call3', 'enabled')
if (call3Enabled != 'true'):
	callSign3 = str(999999999999)
else:
	if config.has_option('call3','callsign'):
		callSign3 = config.get('call3','callsign')
	else:
	        callSign3 = str(999999999999)




# 8-Ball answers
magic8ball = [
        'It is certain',
        'It is decidedly so',
        'Without a doubt',
        'Yes definitely',
        'You may rely on it',
        'As I see it, yes',
        'Most likely',
        'Outlook good',
        'Yes',
        'Signs point to yes',
        'Reply hazy try agn',
        'Ask again later',
        'Tell you later',
        'Cannot predict now',
        'Concentrate, ask agn',
        'Dont count on it',
        'My reply is no',
        'My sources say no',
        'Outlook not so good',
        'Very doubtful'
        ]

# Some Variables that are important later
txtTransmitBin = '/opt/MMDVMHost/RemoteCommand 7642 page ' + pageid

# Now run the loop
while True:
	# Check that the process is running, if its not there is no point in trying to stop it.
	checkproc = subprocess.Popen('pgrep' + ' MMDVMHost', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	if checkproc.stdout.readlines():

		# This is the main loop that keeps waiting, we dont want to hammer the logs too often, every 30 secs should be enough.
		utcnow = datetime.datetime.utcnow()
		datenow = utcnow.strftime('%Y-%m-%d')
		dateminus60sec = datetime.datetime.utcnow() - datetime.timedelta(seconds=10)
		logstampnow = utcnow.strftime('%Y-%m-%d %H:%M:%S')
		logstampnowminus60sec = dateminus60sec.strftime('%Y-%m-%d %H:%M:%S')
		currentLog = mmdvmLogPath + '/' + mmdvmFileRoot + '-' + datenow + '.log'

		# Open the MMDVMHost Log
		logfile = open(currentLog, 'r')
		loglist = logfile.readlines()
		logfile.close()

		# Parse the log lines
		for line in loglist:
			# We only care about logs in the last 60 secs
			if line[3:22] >= logstampnowminus60sec and line[3:22] <= logstampnow:

				# DMR Restart the OS
				if str('received RF voice header from ' + keeperCall + ' to ' + dmrreboot) in line:
					# Restart the OS
					os.system(r'shutdown -r now')

				# DMR Get the current IP
				if str('received RF voice header from ' + keeperCall + ' to ' + dmrgetip) in line:
					# Get the IP
					myIP = os.popen('hostname -I | awk "{print $1}"')
					os.system(txtTransmitBin + ' IP: ' + myIP.read())

				# DMR 8Ball
                                if str('received RF voice header from ' + keeperCall + ' to ' + dmr8ball) in line:
                                        # Ask the 8Ball
                                        magic8ballanswer = random.choice(magic8ball)
                                        os.system(txtTransmitBin + ' ' + magic8ballanswer)

				# DMR Ping
                                if str('received RF voice header from ' + keeperCall + ' to ' + dmrping) in line:
                                        # respong with pong on success.
					ping = os.system('ping 8.8.8.8 -c 1 > /dev/null')
					if ping == 0:
		                                os.system(txtTransmitBin + ' pong')
					else:
						os.system(txtTransmitBin + ' ...no network')

                                # DMR Get the Battery Status
                                if str('received RF voice header from ' + keeperCall + ' to ' + dmrgetbat) in line:
                                        # Get the info
                                        Status = os.popen('cat /sys/class/power_supply/axp20x-battery/status | tr "\n" " "')
					Capacity = os.popen('cat /sys/class/power_supply/axp20x-battery/capacity | tr "\n" " "|sed "s/.$//"')
                                        os.system(txtTransmitBin + ' ' +  Capacity.read() + '% ' + Status.read())

				# Callsign 1 Page
                                if str('received network end of voice transmission from ' + callSign1) in line:
					page = line.split(",")
					page = page[1].split(" ", 7)
                                        # check to see if 10 mins has been up before paging otherwise we will flood with dup messages during long qso
					if totCall1 > 60 or totCall1 == 0:
						totCall1 = 1
		                                os.system(txtTransmitBin + ' ' + page[7])

				# Callsign 2 Page
                                if str('received network end of voice transmission from ' + callSign2) in line:
					page = line.split(",")
					page = page[1].split(" ", 7)
                                        # check to see if 10 mins has been up before paging otherwise we will flood with dup messages during long qso
					if totCall2 > 60 or totCall2 == 0:
						totCall2 = 1
		                                os.system(txtTransmitBin + ' ' + page[7])

				# Callsign 3 Page
                                if str('received network end of voice transmission from ' + callSign3) in line:
					page = line.split(",")
					page = page[1].split(" ", 7)
                                        # check to see if 10 mins has been up before paging otherwise we will flood with dup messages during long qso
					if totCall3 > 60 or totCall3 == 0:
						totCall3 = 1
		                                os.system(txtTransmitBin + ' ' + page[7])

				#OTA Commands for DMRGateway
					#network 1 enable and disable
                                if str('received RF voice header from ' + keeperCall + ' to ' + en_network1) in line:
					DMRGatewayConfig.set('DMR Network 1', 'Enabled', '1')
					with open(DMRGatewayFile, 'wb') as configfile:
						DMRGatewayConfig.write(configfile)
					os.system('killall DMRGateway')
					os.system(DMRGatewayExe + ' ' + DMRGatewayFile + ' &')
                                if str('received RF voice header from ' + keeperCall + ' to ' + d_network1) in line:
					DMRGatewayConfig.set('DMR Network 1', 'Enabled', '0')
					with open(DMRGatewayFile, 'wb') as configfile:
						DMRGatewayConfig.write(configfile)
					os.system('killall DMRGateway')
					os.system(DMRGatewayExe + ' ' + DMRGatewayFile + ' &')



		time.sleep(10)
		if totCall1 > 0:
			totCall1 = totCall1 + 1 # increases 1 every 10 second loop
			if totCall1 > 61:
				totCall1 = 0 # this is just to stop counting if over the loop value. waste of memory otherwise.
		if totCall2 > 0:
			totCall2 = totCall2 + 1 # increases 1 every 10 second loop
			if totCall2 > 61:
				totCall2 = 0 # this is just to stop counting if over the loop value. waste of memory otherwise.
		if totCall3 > 0:
			totCall3 = totCall3 + 1 # increases 1 every 10 second loop
			if totCall3 > 61:
				totCall3 = 0 # this is just to stop counting if over the loop value. waste of memory otherwise.



