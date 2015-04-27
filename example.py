#!/usr/bin/env python3
'''
Created on 11 Mar 2015

@author: aclark
'''
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

from ConfExtractor.ConfExtractor import  ConfExtractor

if __name__ == '__main__':
    c = ConfExtractor()
    c.fromFile('cisco.config')
    print (c.include(r'^interface').exclude(r'[Cc]ellular'))

 
    config = '''
router bgp 65000
 bgp log-neighbor-changes
 bgp listen range 0.0.0.0/0 peer-group InternetL3VPN
 no bgp default ipv4-unicast
 timers bgp 7 21
 neighbor InternetL3VPN peer-group
 neighbor InternetL3VPN remote-as 65535
 neighbor InternetL3VPN ebgp-multihop 255
 !
 address-family ipv4
  redistribute connected
 exit-address-family
 !
 address-family vpnv4
  neighbor InternetL3VPN activate
  neighbor InternetL3VPN send-community both
  neighbor InternetL3VPN route-map L3VPN_Internet in
 exit-address-family
 !
 address-family ipv4 vrf cust1
  redistribute connected
  redistribute static
  default-information originate
 exit-address-family
'''
    c = ConfExtractor()
    c.fromString(config)
    print (c.section(r'router bgp').section(r'vrf cust1').include(r'redist').exclude(r'static'))

