import os
from python_hosts import Hosts, HostsEntry

# 获取exe文件所在目录的路径
exe_path = os.path.dirname(os.path.abspath(__file__))
# 定义文件路径
block_sites_file_path = os.path.join(exe_path, 'block_web.txt')


# 从文件中读取网站列表
def read_blocked_sites():
    with open(block_sites_file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]


def block_sites(blocked_sites):
    hosts = Hosts()
    entries = []
    for site in blocked_sites:
        new_entry = HostsEntry(entry_type='ipv4', address='0.0.0.0', names=[site])
        entries.append(new_entry)
    hosts.add(entries, force=True)
    hosts.write()


def unblock_sites():
    hosts = Hosts()
    hosts.remove_all_matching(address='0.0.0.0')
    hosts.write()
