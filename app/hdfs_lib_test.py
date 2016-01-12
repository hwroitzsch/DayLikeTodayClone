from hdfs import Config
from hdfs import InsecureClient

# pig -param input=<input file> -param output=<output file> -param reducer-num=1 -param date=1980-12-24
try:
    client = Config().get_client('dev')


	with client.read('Serien_de',encoding='utf-8',delimiter='\n') as reader:
		for line in reader:
			print(line)
except:
	print("schief gelaufen beim Lesen aus HDFS")
	raise
