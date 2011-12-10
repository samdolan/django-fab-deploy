from fabric.api import run, env

def package_exists(package):
    """Check if a package exists."""
    # borrowed from cuisine (should commit this check package_exists?)
    status = run("dpkg-query -W -f='${Status}' %s; true" % package)
    return status.find("not-installed") == -1 or status.find("installed") != -1

def get_ip(interface=None):
    """Get the ip address of a server."""
    interface = env.get('private_ip_interface', 'eth1')
    ip = run(r"ifconfig %s | grep 'inet addr' | cut -d: -f2 | awk {'print $1'}" % interface)
    return ip

