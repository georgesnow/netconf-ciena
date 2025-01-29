from dhcp_leases import DhcpLeases

leases = DhcpLeases('/var/lib/dhcp/dhcpd.leases')
current_ips = leases.get()
#print(current_ips[2])
for lease_ip in current_ips:
 lease_data = lease_ip.data
 lease_keys = lease_data.keys()
 print(lease_data)
 if 'uid' in lease_keys:
  lease_serial = lease_data['uid']
  lease_ip = lease_ip.ip
  lease_hw = lease_data['hardware']
  print(lease_hw)
  n = 5
  e = -1
  print(lease_serial[n:e], lease_ip)
 else:
  continue
