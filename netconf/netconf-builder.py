import csv
from dhcp_leases import DhcpLeases
from ncclient import manager
from jinja2 import Environment, FileSystemLoader
from lxml import  etree

leases = DhcpLeases('/var/lib/dhcp/dhcpd.leases')
#current_ips = leases.get()
current_ips_active = leases.get_current()
current_ips = list(current_ips_active.values())
#list(my_dict.values())
#quit()

#load the templates folder
env = Environment(loader=FileSystemLoader('./templates/'))
#load the templates  into variables
system_temp = env.get_template('system-config.xml')
license_temp = env.get_template('license-mgmt.xml')
cos_temp = env.get_template('cos-to-frame-maps.xml')
fds_temp = env.get_template('fds.xml')
fps_temp = env.get_template('fps.xml')
class_temp = env.get_template('classifiers.xml')
int_temp = env.get_template('interface.xml')
port_temp = env.get_template('logical-ports.xml')
bfd_temp = env.get_template('bfd.xml')
seg_temp = env.get_template('segmented-routing.xml')
isis_temp = env.get_template('isis.xml')
isis_int_temp = env.get_template('isis_interfaces.xml')
port_temp = env.get_template('logical-ports.xml')
mpls_temp = env.get_template('mpls.xml')


with open('device-list-csv.csv', 'r') as file:
    csv_reader = csv.reader(file)
    csv_dict = csv.DictReader(file)
    data = list(csv_dict)
#    print(data)


for lease_ip in current_ips:
 lease_data = lease_ip.data
 lease_keys = lease_data.keys()



 if 'uid' in lease_keys:
  lease_serial = lease_data['uid']
  lease_ip = lease_ip.ip
  n = 5
  e = -1
  #print(lease_serial[n:e], lease_ip)
  for row in data:
        #print(row['serial'])
        if lease_serial[n:e] in row['serial']:
         #print(row)
         devMatch = row

         context = {
           "HOSTNAME": row['device'],
           "UPSTREAM_DEV": row['upstream-dev'],
           "DEV_TYPE": row['type'],
           "FD_VLAN": row['vlan'],
           "LOOPBACK_IP": row['loopback'],
           "P2P_IP": row['p2p'],
           "ISIS_NET": row['isis'],
           "SID": row['sid'],
         }
         print(context)
         #render each template individual for loading
         system_conf = system_temp.render(context)
         license_conf = license_temp.render(context)
         cos_conf = cos_temp.render(context)
         fds_conf = fds_temp.render(context)
#         print(fds_conf)
         fps_conf = fps_temp.render(context)
         class_conf = class_temp.render(context)
         #print(class_conf)
         int_conf = int_temp.render(context)
#         print(int_conf)
         port_conf = port_temp.render(context)
         bfd_conf = bfd_temp.render(context)
         isis_conf = isis_temp.render(context)
         isis_int_conf = isis_int_temp.render(context)
#         print(isis_conf)
#         quit()
         seg_conf = seg_temp.render(context)
         port_conf = port_temp.render(context)
         mpls_conf = mpls_temp.render(context)
         with manager.connect_ssh(host=lease_ip, username='diag', password='ciena123', hostkey_verify=False) as m:
          try:
            system = m.edit_config(target="running", config=system_conf, default_operation = "merge")
            print("system =")
            print(system)

            rpc_reply_b = m.edit_config(target="running", config=license_conf, default_operation = "merge")
            print("license =")
            print(rpc_reply_b)

            cos = m.edit_config(target="running", config=cos_conf, default_operation = "merge")
            print("cos =")
            print(cos)

            fds = m.edit_config(target="running", config=fds_conf, default_operation = "merge")
            print("fds =")
            print(fds)

            int = m.edit_config(target="running", config=int_conf, default_operation = "merge")
            print("interface =")
            print(int)


            classf = m.edit_config(target="running", config=class_conf, default_operation = "merge")
            print("classifiers =")
            print(classf)

            port = m.edit_config(target="running", config=port_conf, default_operation = "merge")
            print("ports =")
            print(port)

            mpls = m.edit_config(target="running", config=mpls_conf, default_operation = "merge")
            print("mpls =")
            print(mpls)

            bfd = m.edit_config(target="running", config=bfd_conf, default_operation = "merge")
            print("bfd =")
            print(bfd)

            fps  = m.edit_config(target="running", config=fps_conf, default_operation = "merge")
            print("fps =")
            print(fps)

            seg = m.edit_config(target="running", config=fps_conf, default_operation = "merge")
            print("segmented routing =")
            print(seg)

            isis = m.edit_config(target="running", config=isis_conf, default_operation = "merge")
            print("isis =")
            print(isis)

            isis_int = m.edit_config(target="running", config=isis_int_conf, default_operation = "merge")
            print("isis interfaces =")
            print(isis_int)

          finally:
            continue
 else:
  continue