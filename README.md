# netconf-ciena
netconf configuration for ciena devices via DHCP server matching on the serial numbers

It is important to make sure the serial numbers match the devices you want to configure
the serial numbers in CSV are the actual serial numbers
DHCP server will have serial numbers with a prepend of \0000 which is accounted for 
in the code. 

The templates assume the naming you want to use conforms to


location-town-devicetype-ce 

location = name of the place the equipment is

town = this is the US postal town/city abbreviation

devicetype = 3928,5164,8114 etc...

ce = is always at the end of the devices to denote these are carrier ethernet devices

