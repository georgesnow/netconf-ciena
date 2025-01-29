# netconf-ciena
netconf configuration for ciena devices via DHCP server matching on the serial numbers

It is important to make sure the serial numbers match the devices you want to configure
the serial numbers in CSV are the actual serial numbers
DHCP server will have serial numbers with a prepend of \0000 which is accounted for 
in the code. 

The templates assume the naming you want to use conforms to


device = name of the device you want to use 
serial = M1111111
ip-device	= not currently used - future use after devices are deployed to network
upstream-dev = name of the upstream device used for naming interfaces etc..
type = used in the name of the device 
vlan = vlan tag being used for point to point connection for isis
loopback = this is only for lateral devices when baselining to set them up from scratch for isis
p2p = point to point ip for isis connection
isis = isis net address 49.000x.xxx.xxx only for lateral
sid = sid value for isis only for lateral
deploy-location	= core/lateral --- so the change is being applied to the device's serial number listed. 
port = physical port the interfaces should be built on
delete = 0/1 0 means add the configuration above to the device. if you want to undo the change change to 1

