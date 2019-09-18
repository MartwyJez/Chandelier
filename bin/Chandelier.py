from __future__ import print_function
import sys
from datetime import datetime
import chandelier

def eprint(*args, **kwargs):
    print(datetime.now(), *args, file=sys.stderr, **kwargs)

bts_speaker = chandelier.bluetooth_speaker.BluetoothSpeaker("0C:A6:94:62:67:40")

#def whats_nearby():
#    name_by_addr = {}
#    nearby = bluetooth.discover_devices(flush_cache=True)
#    for bd_addr in nearby:
#        name = bluetooth.lookup_name( bd_addr, 5)
#        print(bd_addr, name)
#        name_by_addr[bd_addr] = name
#    return name_by_addr
#
#def what_services( addr, name ):
#    print(" %s - %s" % ( addr, name ))
#    for services in bluetooth.find_service(address = addr): 
#        print("\t Name:           %s" % (services["name"]) )
#        print("\t Description:    %s" % (services["description"]) )
#        print("\t Protocol:       %s" % (services["protocol"]) )
#        print("\t Provider:       %s" % (services["provider"]) )
#        print("\t Port:           %s" % (services["port"]) )
#        print("\t service-classes %s" % (services["service-classes"]))
#        print("\t profiles        %s" % (services["profiles"]))
#        print("\t Service id:  %s" % (services["service-id"]) )
#        print("" )
#
#if __name__ == "__main__":
#    name_by_addr = whats_nearby()
#    for addr in name_by_addr.keys():
#        what_services(addr, name_by_addr[addr])