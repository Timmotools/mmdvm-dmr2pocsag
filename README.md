DMR to POCSAG python script.

Desiged to be used with MMDVMHost with DMR mode enabled to send private talkgroups to get status messages from the hotspot onto a pocsag pager.

Original code is by Andy Taylor (MW0MWZ) and was called pistar-remote.py. while this version maintains some of the original code but has been changed a lot and cannot be forked.

This version started as a few changes to the original code, then the removal of the extra modes and allowing the status messages to be returned by using the RemoteCommand included with the MMDVMHost package.
Later I have added paging for when selected users kerchunk the talk group you have running on your hotspot without the need for your radio to be on.
These users are setup in the config file and I will be adding a talkgroup filter for if you are like me and have more than one network running (BM and DMR-MARC)

Lots of credit goes to Andy the original creater of the script pistar-remote as without his script I would not have made this.

Credit also goes to Terry (VK3FTJS) who has been there to help me along the way with a lot of testing and kerchunking. especially with the user paging stuff.



Setup is simple.

Make sure you have all of the POCSAG stuff enabled in your MMDVMHost config. This includes the POCSAG network just dont have the POCSAG gateway running. You could always setup a DAPNET account.

Also make sure remote control is enabled in the MMDVMHost config. If you have changed the default port then this will need to be changed in the main python code.

Setup the config file for your settings. commenting out the talkgroups will disable them. Everything else should be self explainatory.

Dont forget to your pager CAP number. This wont effect anything network side but you wont rx on your pager if this is not setup.

Enter "/opt/mmdvm-dmr2pocsag/dmr2pocsag.py > /dev/null &" into your startup script to start the program. Or crontab it if preferred.

Cheers 73's
Tim VK3FTZD
