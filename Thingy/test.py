# DO NOT USE THIS FILE!!!!!!

# import bluepy
# import subprocess


# MAC_ADDRESS = None

# print("# Looking for Thingy advertisment...")
# scanner = bluepy.btle.Scanner()
# devices = scanner.scan(timeout = 3)
# for dev in devices:
#     # print("Device {} ({}), RSSI={} dB".format(dev.addr, dev.addrType, dev.rssi))
#     for (adtype, desc, value) in dev.getScanData():
#         # print("  {}, {} = {}".format(adtype, desc, value))
#         if (value == "Thingy"):
#             print("# Thingy found with address: {}".format(dev.addr))
#             MAC_ADDRESS = dev.addr
#         # end
#     # end
# # end

# if (MAC_ADDRESS == None):
#     print("### ERROR: MAC_ADDRESS is not set (and Thingy was not found)...")
#     exit(0)
# # end

# subprocess.run(['python3', 'thingy.py', str(MAC_ADDRESS), '--temperature', '--pressure', '--humidity', '--gas'])

""" 
Notes:
I found a main() in bluepy.thingy52 file. Then I do a test and found that it workds but will only receive the data with the number of arguments.
i.e, if some data cannot be received in the correct time, we cannot get it. Moreover, due to we will use the subprocess, it is not a good idea 
to run it as a loop.
"""