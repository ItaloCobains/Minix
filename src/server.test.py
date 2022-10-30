from server import Server, ServerInstace
import time

s = Server(9000, "localhost", ServerInstace)

s.run()

ip, host = s.getIpAndHost()

print("{}, {}".format(ip, host))

time.sleep(110)

s.shutdown()
