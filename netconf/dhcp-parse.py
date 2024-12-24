from dhcp_leases import DhcpLeases

#this is just an exmaple script for looking through dhcp leases

leases = DhcpLeases('/var/lib/dhcp/dhcpd.leases')
current_ips = leases.get()
#print(current_ips[2])
for lease_ip in current_ips:
 lease_data = lease_ip.data
 lease_keys = lease_data.keys()
#look for the uid which is the serial number for Ciena devices they prepended with backslash and some 
#zeros
 if 'uid' in lease_keys:
  lease_serial = lease_data['uid']
  lease_ip = lease_ip.ip
  n = 5
  e = -1
  print(lease_serial[n:e], lease_ip)
 else:
  continue
