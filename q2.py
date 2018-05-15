from websocket import create_connection
ws = create_connection('ws://206.189.172.118')
result = ws.recv()
print("raw result: \n{}".format(result))
rresult = [chr(int(x)) for x in result.split(' ')]
rrresult = [chr(int(x)%26 + 65) for x in result.split(' ')]
print('rresult: \n{}'.format(rresult))
print('rrresult: \n{}'.format(rrresult))
