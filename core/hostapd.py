import os
import time

CONF_PATH = '/etc/mana-toolkit/hostapd-configs.conf'
HOSTAPD_PATH = '/usr/lib/mana-toolkit/hostapd'

class Hostapd(object):

    def __init__(self, options):

        if options.nat:

            with open(CONF_PATH, 'w') as fd:
                fd.write((
                    'interface=%s'
                    'bssid=%s'
                    'driver=nl80211'
                    'ssid=%s'
                    'channel=%d'
                    ''
                    '# Prevent dissasociations'
                    'disassoc_low_ack=0'
                    'ap_max_inactivity=3000'
                    ''
                    '# Both open and shared auth'
                    'auth_algs=3'
                    ''
                    '# no SSID cloaking'
                    '#ignore_broadcast_ssid=0'
                    ''
                    '# -1 = log all messages'
                    'logger_syslog=-1'
                    'logger_stdout=-1'
                    ''
                    '# 2 = informational messages'
                    'logger_syslog_level=2'
                    'logger_stdout_level=2'
                    ''
                    'ctrl_interface=/var/run/hostapd'
                    'ctrl_interface_group=0'
                    ''
                    '# 0 = accept unless in deny list'
                    '#macaddr_acl=0'
                    ''
                    '# only used if you want to do filter by MAC address'
                    '#accept_mac_file=/etc/hostapd/hostapd.accept'
                    '#deny_mac_file=/etc/hostapd/hostapd.deny'
                    ''
                    '# Enable karma mode'
                    'enable_karma=1'
                    '# Limit karma to responding only to the device probing (0), or not (1)'
                    'karma_loud=0'
                    ''
                    '# Black and white listing'
                    '# 0 = white'
                    '# 1 = black'
                    '#karma_black_white=1'
                ) % (options.phy, options.bssid, options.ssid, options.channel))
    
    @staticmethod
    def _start(configs):
        os.system('%s %s' % (HOSTAPD_PATH, CONF_PATH))
    
    def start(self):
    
        self.proc = Process(target=self._start, args=({},))
        self.proc.daemon = True
        self.proc.start()
        time.sleep(5)

    def stop(self):

        self.proc.terminate()
        self.proc.join()