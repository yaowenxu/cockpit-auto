import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from avocado import Test
from utils.machine import Machine


class TestMachinesLibvirtPackage(Test):
    """
    :avocado: enable
    :avocado: tags=machines_pkg
    """

    def setUp(self):
        host_string = os.environ.get('HOST_STRING')
        username = os.environ.get('USERNAME')
        passwd = os.environ.get('PASSWD')
        self.host = Machine(host_string, username, passwd)
        self.old_ver = self.params.get('old_machines_rpm_ver')
        self.new_ver = self.params.get('new_machines_rpm_ver')
        self.base_url = self.params.get('base_url')
        for rpm_name in [self.old_ver, self.new_ver]:
            cmd = 'test -e {}'.format(rpm_name)
            ret = self.host.execute(cmd, raise_exception=False)
            if ret.succeeded:
                continue
            split_dash = rpm_name.split('-')
            split_dot = split_dash[-1].split('.')
            args = {}
            args['ver1'] = split_dash[2]
            args['ver2'] = '.'.join([split_dot[0], split_dot[1]])
            args['arch'] = split_dot[2]
            args['name'] = rpm_name
            url = self.base_url.format(**args)
            cmd = 'wget {}'.format(url)
            self.host.execute(cmd)

    def test_upgrade_pkg(self):
        cmd = "rpm -i {}".format(self.old_ver)
        self.host.execute(cmd)
        cmd = "rpm -U {}".format(self.new_ver)
        self.host.execute(cmd)
        cmd = 'rpm -qa | grep cockpit-machines --color=never'
        ret = self.host.execute(cmd, raise_exception=False)
        self.assertEqual(ret + '.rpm', self.new_ver)

    def test_remove_pkg(self):
        cmd = 'rpm -e cockpit-machines'
        self.host.execute(cmd)
        cmd = 'rpm -qa | grep cockpit-machines'
        ret = self.host.execute(cmd, raise_exception=False)
        self.assertEqual(ret, '')

    def test_install_pkg(self):
        cmd = 'rpm -i {}'.format(self.new_ver)
        self.host.execute(cmd)
        cmd = 'rpm -qa | grep cockpit-machines --color=never'
        ret = self.host.execute(cmd, raise_exception=False)
        self.assertEqual(ret + '.rpm', self.new_ver)

    def test_start_cockpit(self):
        cmd = 'systemctl enable cockpit.socket && systemctl start cockpit.socket'
        self.host.execute(cmd)
