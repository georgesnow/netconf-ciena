#saos 10 netconf router builder
import csv
from dhcp_leases import DhcpLeases
from ncclient import manager
from jinja2 import Environment, FileSystemLoader
from lxml import  etree


#load the templates folder
env = Environment(loader=FileSystemLoader('./templates/'))
#load the templates  into variables
system_temp = env.get_template('system-config.xml')
license_temp = env.get_template('license-mgmt.xml')
cos_temp = env.get_template('cos-to-frame-maps.xml')
fds_temp = env.get_template('fds.xml')
fps_temp = env.get_template('fps.xml')
#updated template with jinja logic
#class_temp = env.get_template('classifiers.xml')

class_temp = env.get_template('classifiers-defined.xml')
int_temp = env.get_template('interface.xml')
port_temp = env.get_template('logical-ports.xml')
ldp_temp = env.get_template('ldp.xml')
ldp_lo_temp = env.get_template('ldp_lo.xml')
bfd_temp = env.get_template('bfd.xml')
seg_temp = env.get_template('segmented-routing.xml')
isis_temp = env.get_template('isis.xml')
isis_int_temp = env.get_template('isis_interfaces.xml')
port_temp = env.get_template('logical-ports.xml')
mpls_temp = env.get_template('mpls.xml')
mpls_upl_temp = env.get_template('mpls-uplink.xml')



def get_leases(serial_number):
            leases = DhcpLeases('/var/lib/dhcp/dhcpd.leases')
            #current_ips = leases.get()
            current_ips_active = leases.get_current()
            current_ips = list(current_ips_active.values())
            #list(my_dict.values())
            
            for lease_ip in current_ips:
                lease_data = lease_ip.data
                lease_keys = lease_data.keys()
#                print(lease_keys)
                if 'uid' in lease_keys:
                    lease_serial = lease_data['uid']
                    lease_ip = lease_ip.ip
                     
#                    print(lease_ip)
                    
                    n = 5
                    e = -1
#                    print(lease_serial[n:e])
                    if lease_serial[n:e] in serial_number:
                        
                        return lease_ip
                    else:
                        continue
                else:
                    continue
            
def context_mapper(core_lat, row):
            if "lateral" in core_lat:
                context = {
                       "LATERAL": True,
                       "HOSTNAME": row['device'],
                       "UPSTREAM_DEV": row['upstream-dev'],
                       "DEV_TYPE": row['type'],
                       "FD_VLAN": row['vlan'],
                       "LOOPBACK_IP": row['loopback'],
                       "P2P_IP": row['p2p'],
                       "ISIS_NET": row['isis'],
                       "SID": row['sid'],
                       "PORT": row['port'],
                }
                return context
            elif "core" in core_lat:
                context = {
                    "LATERAL": False,
                    "UPSTREAM_DEV": row['upstream-dev'],
                    "DEV_TYPE": row['type'],
                    "FD_VLAN": row['vlan'],
                    "P2P_IP": row['p2p'],
                    "PORT": row['port'],
                 }
            return context

def delete_int_render(dev_ip, dev_upstream, device_type):
            print('delete function running..')
            isis_int_conf = isis_int_temp.render(
            INT_DELETE=True,
            UPSTREAM_DEV=dev_upstream,
            DEV_TYPE=device_type
            )
#            print(isis_int_conf)

            mpls_uplink_conf = mpls_upl_temp.render(
            INT_DELETE=True,
            UPSTREAM_DEV=dev_upstream,
            DEV_TYPE=device_type
            )

            bfd_conf = bfd_temp.render(
            INT_DELETE=True,
            UPSTREAM_DEV=dev_upstream,
            DEV_TYPE=device_type
            )

            classf_conf = class_temp.render(
            INT_DELETE=True,
            UPSTREAM_DEV=dev_upstream,
            DEV_TYPE=device_type
            )            

            fps_conf=fps_temp.render(
            INT_DELETE=True,
            UPSTREAM_DEV=dev_upstream,
            DEV_TYPE=device_type
            )
            
            fds_conf=fds_temp.render(
            INT_DELETE=True,
            UPSTREAM_DEV=dev_upstream,
            DEV_TYPE=device_type
            )            
            print(fds_conf)
            
            int_conf = int_temp.render(
            INT_DELETE=True,
            UPSTREAM_DEV=dev_upstream,
            DEV_TYPE=device_type
            )
            with manager.connect_ssh(host=dev_ip, username='diag', password='ciena123', hostkey_verify=False) as m:
               try:
                    isis_int = m.edit_config(target="running", config=isis_int_conf, default_operation = "merge")
                    print("isis delete interfaces =")
                    print(isis_int)

                    mpls_int = m.edit_config(target="running", config=mpls_uplink_conf, default_operation = "merge")
                    print(mpls_uplink_conf)
                    print("mpls = ")
                    print(mpls_int)

#                    print(bfd_conf)
                    bfd_int = m.edit_config(target="running", config=bfd_conf, default_operation = "merge")
                    print("bfd = ")
                    print(bfd_int)

#                    need to fix the template to core for a router
#                    classf_int = m.edit_config(target="running", config=classf_conf, default_operation = "merge")
#                    print("classf = ")
#                    print(classf_int)

                    fps = m.edit_config(target="running", config=fps_conf, default_operation = "merge")
                    print("fps = ")
                    print(fps)
                    
                    fds = m.edit_config(target="running", config=fds_conf, default_operation = "merge")
                    print("fds = ")
                    print(fds)

#                    print(int_conf)
#                    quit()
                    int_int = m.edit_config(target="running", config=int_conf, default_operation = "merge")
                    print("int = ")
                    print(int_int)
               except Exception as e:
                   print("error on " + dev_ip + ": ", e)
                   pass
               finally:
                    print("it tried")

def build_p2p_rtr(dev_ip, context, dev_type):
            #render each template individual for loading
            system_conf = system_temp.render(context)
            license_conf = license_temp.render(context)
            cos_conf = cos_temp.render(context)
            fds_conf = fds_temp.render(context)
#            print(fds_conf)
            fps_conf = fps_temp.render(context)
            class_conf = class_temp.render(context)
            #print(class_conf)
            int_conf = int_temp.render(context)
#          print(int_conf)
            port_conf = port_temp.render(context)
            ldp_conf = ldp_temp.render(context)
            ldp_lo_conf = ldp_lo_temp.render(context)
            bfd_conf = bfd_temp.render(context)
            isis_int_conf = isis_int_temp.render(context)
            mpls_upl_conf = mpls_upl_temp.render(context)
            isis_conf = isis_temp.render(context)
            mpls_conf = mpls_temp.render(context)
            seg_conf = seg_temp.render(context)
            
            with manager.connect_ssh(host=dev_ip, username='diag', password='ciena123', hostkey_verify=False) as m:
                if "lateral" in dev_type:
                   print("building lateral device and p2p")
                   try:
                        system = m.edit_config(target="running", config=system_conf, default_operation = "merge")
                        print("system =")
                        print(system)
    
                        rpc_reply_b = m.edit_config(target="running", config=license_conf, default_operation = "merge")
                        print("license =")
                        print(rpc_reply_b)
    
                        fds = m.edit_config(target="running", config=fds_conf, default_operation = "merge")
                        print("fds =")
                        print(fds)

                        cos = m.edit_config(target="running", config=cos_conf, default_operation = "merge")
                        print("cos =")
                        print(cos)
    

    
    
                        print(int_conf)
                        intf = m.edit_config(target="running", config=int_conf, default_operation = "merge")
                        print("interface =")
                        print(intf)
    
    
                        classf = m.edit_config(target="running", config=class_conf, default_operation = "merge")
                        print("classifiers =")
                        print(classf)
    
                        port = m.edit_config(target="running", config=port_conf, default_operation = "merge")
                        print("ports =")
                        print(port)
                        
                        fps  = m.edit_config(target="running", config=fps_conf, default_operation = "merge")
                        print("fps =")
                        print(fps)
 
 
                        ldp = m.edit_config(target="running", config=ldp_conf, default_operation = "merge")
                        print("ldp =")
                        print(ldp)
    
                        ldp_lo = m.edit_config(target="running", config=ldp_lo_conf, default_operation = "merge")
                        print("ldp_lo =")
                        print(ldp_lo)
                        
   
    
                        bfd = m.edit_config(target="running", config=bfd_conf, default_operation = "merge")
                        print("bfd =")
                        print(bfd)
                        

                        mpls = m.edit_config(target="running", config=mpls_conf, default_operation = "merge")
                        print("mpls =")
                        print(mpls)

                        
    
                        isis = m.edit_config(target="running", config=isis_conf, default_operation = "merge")
                        print("isis =")
                        print(isis)

                        isis_int = m.edit_config(target="running", config=isis_int_conf, default_operation = "merge")
                        print("isis interfaces =")
                        print(isis_int)

                        mpls_upl = m.edit_config(target="running", config=mpls_upl_conf, default_operation = "merge")
                        print("mpls_uplink =")
                        print(mpls)



                        seg = m.edit_config(target="running", config=seg_conf, default_operation = "merge")
                        print("segmented routing =")
                        print(seg)
                    
                   except Exception as e:
                       print("error on " + dev_ip + ": ", e)
                       pass
                        
                   finally:
                        print("it tried")
                elif "core" in dev_type:
                    print("building core p2p")
                    try:
                       with manager.connect_ssh(host=dev_ip, username='diag', password='ciena123', hostkey_verify=False) as m:
                           fds = m.edit_config(target="running", config=fds_conf, default_operation = "merge")
                           print("fds =")
                           print(fds)
    
    
#                           print(int_conf)
                           intf = m.edit_config(target="running", config=int_conf, default_operation = "merge")
                           print("interface =")
                           print(intf)
    
    
                           classf = m.edit_config(target="running", config=class_conf, default_operation = "merge")
                           print("classifiers =")
                           print(classf)
    
                           port = m.edit_config(target="running", config=port_conf, default_operation = "merge")
                           print("ports =")
                           print(port)
                           bfd = m.edit_config(target="running", config=bfd_conf, default_operation = "merge")
                           print("bfd =")
                           print(bfd)
    
                           fps  = m.edit_config(target="running", config=fps_conf, default_operation = "merge")
                           print("fps =")
                           print(fps)
    
                           isis_int = m.edit_config(target="running", config=isis_int_conf, default_operation = "merge")
                           print("isis interfaces =")
                           print(isis_int)
                           mpls_upl = m.edit_config(target="running", config=mpls_upl_conf, default_operation = "merge")
                           print("mpls_uplink =")
                           print(mpls_upl)

                    except Exception as e:
                       print("error on " + dev_ip + ": ", e)
                       pass


def main():

            with open('device-list-csv.csv', 'r') as file:
                csv_reader = csv.reader(file)
                csv_dict = csv.DictReader(file)
                data = list(csv_dict)
                print(data)
                
            for row in data:
                location = row['deploy-location']
#                print(location)
                print(row['delete'])
                if "1" in row['delete']:
                    print("going to delete")
                    ip_lease = get_leases(row['serial'])
                    print(ip_lease)
                    delete_int_render(ip_lease, row['upstream-dev'], row['type'])
                
                elif "lateral" in location:
                    print("this is lateral")
#                    not on ztp server so commmented out
                    current_context = context_mapper("lateral",row)
                    ip_of_device = get_leases(row['serial'])
                    print(ip_of_device)
                    builder = build_p2p_rtr(ip_of_device, current_context, "lateral")
#                    print(current_context)
#                    continue
                    
                    
                
                elif "core" in location:
                    current_context = context_mapper("core",row)
#                    print(current_context)
                    print("core device")
#                    continue
                    ip_of_device = get_leases(row['serial'])
                    print(ip_of_device)
                    builder = build_p2p_rtr(ip_of_device, current_context, "core")

#                    builder = build_p2p_rtr(row['ip-device'], current_context)

                else:
                    continue



if __name__ == '__main__':
            main()
    