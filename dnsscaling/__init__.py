
from string import Template


#ExecStart=sudo /usr/bin/dnsscaling -d $url
_init_script_normal = Template(
'''
[Unit]
Description=Delete DNS IP
DefaultDependencies=no
Conflicts=reboot.target
Wants=network-online.target
After=network-online.target
Before=poweroff.target halt.target shutdown.target kexec.target
Requires=poweroff.target

[Service]
Type=oneshot
ExecStart=/tmp/tmpscript.sh
RemainAfterExit=yes
TimeoutStartSec=0

[Install]
WantedBy=shutdown.target poweroff.target halt.target kexec.target 
'''
)


_init_script_old = Template(
'''#!/bin/sh
# chkconfig: 345 99 1
# description: Script for DNS deregistration

start(){
    touch /var/lock/subsys/dnsscalingdelete
    sudo dnsscaling -a $url
    sleep 3
}

stop(){
    sudo dnsscaling -d $url
    sleep 3	
    rm -f /var/lock/subsys/dnsscalingdelete
}

restart(){
    stop
    start
}

case $$1 in
start)
        start
        ;;
stop)
        stop
        ;;
restart)
        restart
        ;;
*)
        echo "Wrong Argument"
        exit 1
esac
exit 0
''')


def write_init_script(url, path):
    with open(path + 'dnsscalingdelete.service', 'w') as f:
        f.write(_init_script_normal.substitute({'url': url}).strip())

    with open('/tmp/tmpscript.sh', 'w') as f:
        s = '#!/bin/bash\n' + 'sudo /usr/bin/dnsscaling -d' + url
        f.write(s)
