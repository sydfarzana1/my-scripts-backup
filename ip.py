#!/bin/bash
if [ -z "$1" ]; then
        echo "Expecting 1 argument, ./SCOUT_K2V4_TESTS.sh Server_SN. Exiting."
        exit 1
fi


function get_droplet() {

PYTHON_ARG="$1" PYTHON_ARG2="$2" python - << END

import time
import os
import json
import requests

requests.packages.urllib3.disable_warnings()

def get_sfcs_api_spec():
        sfcs_site_specs = {
                ('PST', 'PDT'): ('sfcs-api.hyvesolutions.org', 'bld1'),
                ('CST', 'CDT'): ('sfcs-api.hyvesolutions.org', 'ob'),
                ('GMT', 'BST'): ('sfcs-api.hyvesolutions.org', 'Telford'),
                ('CST', 'CST'): ('sfcs-api.hyvesolutions.org', 'Wuxi')
        }
        try:
                return sfcs_site_specs[time.tzname]
        except KeyError:
                print "no good"


def get_ip(mac, name):
        fixed_mac = ':'.join(mac.rstrip().zfill(12)[x:x+2] for x in range(0,12,2))
        url_ip = "http://hyve-vm-kminion001-%s.synnex.org:31500/api/v1/mac/%s" % (get_sfcs_api_spec()[1] , fixed_mac)
        r = requests.get(url=url_ip)
        if str(r.status_code) != "200" or os.environ['PYTHON_ARG2'] == "MAC":
                print mac
        else:
                print r.json()["ip"]

headers = {
    'token': 'XobgLZiqqR8g23IBc0O46zBSD7SSpWN4gbSlitbc',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}


url_mac = 'https://%s/mfg-sfcs-api/api/serverInfo/sn/%s' % (get_sfcs_api_spec()[0] , os.environ['PYTHON_ARG'])
r = requests.get(url=url_mac, headers=headers, verify=False)
mac_json = r.json()["data"]
#print mac_json
for i in range(len(mac_json["components"])):
        if mac_json["components"][i]["children"]:
                for x in range(len(mac_json["components"][i]["children"])):
 #                       print mac_json["components"][i]["children"]
                        if "MAC0" in mac_json["components"][i]["children"][x]["profileType"] and "K2V4" in mac_json["components"][i]["partNo"]:
                                eth0=mac_json["components"][i]["children"][x]["profileValue"]
                        if "MAC4" in mac_json["components"][i]["children"][x]["profileType"] and "K2V4" in mac_json["components"][i]["partNo"]:
                                eth4=mac_json["components"][i]["children"][x]["profileValue"]
                        if "MAC" in mac_json["components"][i]["children"][x]["profileType"] and "MB" in mac_json["components"][i]["category"]:
                                bmc=mac_json["components"][i]["children"][x]["profileValue"]


#print "Name\tMAC\t\t  IP \t\tStatus"
get_ip(eth0, "Droplet")
#get_ip(eth4, "ETH")
#get_ip(bmc, "BMC")

END
}

#DROPLET=172.18.68.194
DROPLET=$(get_droplet $1)
ping -c 1 -W 4 $DROPLET > /dev/null 2>&1
if [ $? != 0 ]; then
    DROPLET=$(get_droplet $1 MAC)
    DROPLET=$(./getIPfromMAC.sh $DROPLET | tail -n1)
    ping -c 1 -W 4 $DROPLET > /dev/null 2>&1
    if [ $? != 0 ]; then
        echo "Unable to ping droplet IP"
        exit
    fi
fi

echo
echo "********************************************"
echo "  1) AlUartLoopback (USB raspberry pi test)"
echo "  2) AlI2cNSK (Atlas key test)"
echo "  3) AlI2cNFC (NFC test)"
echo "  4) AlEthSwitch (K2X 1g cabling check)"
echo "********************************************"
echo
echo -n "Which test do you want to run? (1-4) : "
read n
echo

case $n in
  1) act="AlUartLoopback"
     secs=60;;
  2) act="EdgeAtlasKeyTest"
     secs=30;;
  3) act="NfcGetUids"
     secs=300;;
  4) act="AlEthSwitch"
     secs=30;;
  *) echo "invalid option"; exit;;
esac

mode="odm"
action_id=$RANDOM

coap -O65001,0 -Y -m PUT -c "{ mode = '"${mode}"' }" coaps+tcp://$DROPLET/api-v1/provisioning-test-config/set_provisioning_mode > /dev/null 2>&1
coap -Y -O65001,0 -m PUT -c "{ actionType = '${act}' }" coaps+tcp://${DROPLET}/api-v1/provisioning-action/target/card0/asset/1/action/${action_id}  > /dev/null 2>&1

echo "RUNNING $act check"

while [ $secs -gt 0 ]; do
   echo -ne "$secs\033[0K\r"
   sleep 1
   : $((secs--))
   if coap -Y -O65001,0 -m GET coaps+tcp://${DROPLET}/api-v1/provisioning-action/target/card0/asset/1/action/${action_id}  | grep -a "Test $act:" | grep -i 'pass\|fail'; then
    coap -Y -O65001,0 -m GET coaps+tcp://${DROPLET}/api-v1/provisioning-action/target/card0/asset/1/action/${action_id}
    exit
   fi
done

coap -Y -O65001,0 -m GET coaps+tcp://${DROPLET}/api-v1/provisioning-action/target/card0/asset/1/action/${action_id}