from __future__ import absolute_import
import sys
from Chandelier.chandelier import main

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
if __name__ == "__main__":
  sys.exit(main())