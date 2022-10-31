from server import Server, ServerInstace
import time

s = Server(50007, "localhost", ServerInstace)

s.run()

ip, host = s.getIpAndHost()

print("{}, {}".format(ip, host))

time.sleep(1000)

s.shutdown()
