from hdfs import Config
from hdfs import InsecureClient

# http://blog.cloudera.com/blog/2009/08/hadoop-default-ports-quick-reference/
# PORT_LIST = [50070, 50075, 50090, 50105, 50030, 50060]
#
# PORT = 9000
# USER = ''
# IP_ADDRESS = '192.168.0.100'
# PROTOCOL = 'hdfs'
#
# # while PORT < 100000:
# try:
# 	client = InsecureClient(PROTOCOL + '://' + IP_ADDRESS + ':' + PORT)
# 	# client = InsecureClient('http://'+IP_ADDRESS+':'+PORT, user=USER)
# 	# break
# except Exception as ex:
# 	print('\nCould not create client with the following connection information:\n ' + PROTOCOL + '://' + IP_ADDRESS + ':' + str(PORT) + '\n')
# 	# PORT += 1

# #client = Config().get_client('dev')
#
# # Loading a file in memory.
# with client.read('features') as reader:
# 	features = reader.read()
#
# # Directly deserializing a JSON object.
# with client.read('model.json', encoding='utf-8') as reader:
# 	from json import load
# 	model = load(reader)
#
# # Stream a file.
# with client.read('features', chunk_size=8096) as reader:
# 	for chunk in reader:
# 		pass
#
# # with a specified delimiter
# with client.read('samples.csv', encoding='utf-8', delimiter='\n') as reader:
# 	for line in reader:
# 		pass

# pig -param input=<input file> -param output=<output file> -param reducer-num=1 -param date=1980-12-24
try:
    client = Config().get_client('dev')


    with client.read('Serien_de',encoding='utf-8',delimiter='\n') as reader:
        for line in reader:
            print(line)
except:
    print("schief gelaufen beim Lesen aus HDFS")
    raise
