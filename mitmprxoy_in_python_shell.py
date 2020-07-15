# monitor all request using mitmproxy in Python shell , by launch mitmproxy here 

# inform source comes here : https://github.com/mitmproxy/mitmproxy/issues/3306

from mitmproxy import proxy, options
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.addons import core
from mitmproxy.addons import block

opts = options.Options(listen_host='<IP of machine mitmproxy runs>', listen_port=8080)
pconf = proxy.config.ProxyConfig(opts)

m = DumpMaster(opts)
m.options.set('block_global=false')
m.server = proxy.server.ProxyServer(pconf)

try:
    m.run()
except KeyboardInterrupt:
    m.shutdown()

