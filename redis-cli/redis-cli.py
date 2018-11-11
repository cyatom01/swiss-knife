
#! /usr/bin/env python
#
# This script want to getting modified modules.
#
# -*- coding: UTF-8 -*- 
import redis
import argparse
import textwrap
import sys
import operator
import os
import pymysql.cursors


global redis_pool

class RedisOperator:

	def __init__(self,redis):
		self.redis=redis

	def quit(self,line):
		try:
			sys.exit(0)
		except Exception as e:
			print("OS error: {0}".format(e))

	def set(self,line):
		cmdLines=line.split()
		if (len(cmdLines)<3):
			print("Express error,such as: set key value")
			return
		redis=self.redis
		redis.set(cmdLines[1], bytes(cmdLines[2], "utf8"))
		value=redis.get(cmdLines[1])
		print((value is None and '' or str(value ,"utf8").strip()))
		
	def setnx(self,line):
		cmdLines=line.split()

	def get(self,line):
		cmdLines=line.split()
		if (len(cmdLines)<2):
			print("Express error,such as: get key")
			return
		redis=self.redis
		print(str(redis.get(cmdLines[1]),"utf8").strip())

	def pip(self,line):
		cmdLines=line.split()
		if (len(cmdLines)<2):
			print("Express error,such as: pip path")
			return
		exists=os.path.exists(cmdLines[1])
		if not exists:
			print("File not found.")
		redis=self.redis
		pipeline = redis.pipeline(transaction=False)
		with open(cmdLines[1], 'rt') as f:
			 for (num,line) in enumerate(f):
			 	line=line.strip()
			 	if(len(line)<0):
			 		continue
			 	cmdLines=line.split()
			 	print(cmdLines)
			 	try:
			 		if(len(cmdLines)==2):
			 			 operator.methodcaller(cmdLines[0],cmdLines[1])(pipeline)
			 		if(len(cmdLines)>=3):
			 			 operator.methodcaller(cmdLines[0],cmdLines[1],cmdLines[2])(pipeline)
			 	except AttributeError as e:
			 		 print('Unsupported operation,this cmd will be ignored:{}'.format(e))
		pipeline.execute()

	def delete(self,line):
		cmdLines=line.split()
		if (len(cmdLines)<2):
			print("Express error,such as: delete key")
			return
		redis=self.redis
		redis.delete(cmdLines[1])

	def cls(self,line):
		os.system('cls')

	def append(self,line):
		cmdLines=line.split()
		if (len(cmdLines)<2):
			print("Express error,such as: append key value")
			return
		redis=self.redis
		redis.append(cmdLines[1], cmdLines[2])
		print(str(redis.get(cmdLines[1]),"utf8").strip())

class MysqlOperator:
	def select():
		pass


class RedisCmdExcutor:
	def __init__(self, redisOperator):
		self.redisOperator=redisOperator

	def support(self,cmd):
		pass

	def execute(self,cmd):
		try:
		   cmdLines=cmd.split()
		   operator.methodcaller(cmdLines[0],cmd)(self.redisOperator)
		except Exception as e:
			print('Unexpected error:{}'.format(e))
			raise e
#conn -url mysql://localhost:3306/mydb?charset=utf8mb4 -u xx -p
#import select 'a' as key,'v' as value,'1' as op from x_table
class SqlCmdExcutor:
	def __init__(self, redisOperator):
		self.redisOperator=redisOperator

	def support(self,cmd):
		pass
    #get sql connector
	def execute(self,cmd):
		self.c
		pass
		



class CmdExcutorFactory:
	def __init__(self,redisClient):
		self.redisClient=redisClient
		self.redisOperator=RedisOperator(redisClient);
		self.excutors=[RedisCmdExcutor(self.redisOperator),SqlCmdExcutor(self.redisOperator)]

	def getExcutor(self,cmd):
		return self.excutors[0]


def parse_options():
	"""Return a dictionary of options parsed from command line arguments."""
	uasge ="""%(prog)s [options]
	 -host redis connection ip and port,like ip:port
	 -pwd redis connected passowd
	"""
	parser=argparse.ArgumentParser(prog='redis-cli', usage=uasge,
									 formatter_class=argparse.RawDescriptionHelpFormatter,
									 description=textwrap.dedent('''\
									 You can used this cli operate redis. 
									 '''))
	parser.add_argument("-host",
						required=True,
						type=str,
						help='redis host')
	parser.add_argument('-pwd',
						required=False,
						type=str,
						help='auth password')
	args = parser.parse_args()
	return args

def executeCmd():
	rclient=redis.Redis(connection_pool = redis_pool);
	while 1<2:
		try:
			cmd=input('$ ');
			if len(cmd.strip())<=0:
				continue
			#cmdLines=cmd.split()
			excutor=CmdExcutorFactory(rclient).getExcutor(cmd);
			excutor.execute(cmd)			
		except Exception as e:
			 print('Unexpected error:{}'.format(e))
		

if __name__ == "__main__":
	args=parse_options()
	host=args.host.split(":")
	passwd=args.pwd
	redis_pool=redis.ConnectionPool(host = host[0] , port = 6379, db = 0, password = passwd)
	executeCmd()