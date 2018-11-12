
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
from prettytable import PrettyTable

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
	def __init__(self, cmd):
		pass

	def select(self,sql):
		try:
			with self.conn as cursor:
				cursor.execute(sql)
				for row in cursor:
					print(row)
    
		except Exception as e:
			print(e);return


	def destory(self):
		if self.conn is not NoneType:
			self.conn.close()


class RedisCmdExcutor:
	__supportCmds=["quit","set","get","pip","cls","delete","append"]
	def __init__(self, redisOperator):
		self.redisOperator=redisOperator

	def support(self,cmd):
		cmdLines=cmdLines=cmd.split();
		return self.supportCmds.conut(cmdLines[0])>0

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
	__supportCmds=["conn"]
	def __init__(self, redisOperator):
		self.redisOperator=redisOperator
		self.subCmdParser=__getSubCmdParaser()

	def __getSubCmdParaser(self):
		parser=argparse.ArgumentParser(prog='import', usage="import sql")
		parser.add_argument('sql', nargs='?')
		return parser

	def support(self,cmd):
		cmdLines=cmdLines=cmd.split();
		return self.supportCmds.conut(cmdLines[0])>0

	def getCmdParser(self):
		if(self.parser is not None):
			return self.parser
		parser=argparse.ArgumentParser(prog='conn', usage="conn [options]",
									 formatter_class=argparse.RawDescriptionHelpFormatter,
									 description=textwrap.dedent('''
									 Sub cli to connection db. 
									 '''))
		parser.add_argument("-url",
						required=True,
						type=str,
						help='db connect url')
		parser.add_argument('-u',
						required=False,
						type=str,
						help='db connect auth user account')
		parser.add_argument('-p',
						required=False,
						type=str,
						help='db connect user password')
		self.parser=parser
		return self.parser
     	
     	
	
    #get sql connector
	def execute(self,cmd):
		 	cmdLines=cmd.split()
		 	if(len(cmdLines)<2):
		 		print("Express error,such as:conn -url url -u user -p pwd")
		 		return
		 	parser,args=None
		 	try:
		 		parser=getCmdParser()
		 		args=parser.parse_args(cmdLines[1:])
		 		self.sqlOperator=getSqlOperator(slef,args)
		 	except Exception as e:
		 		print("Cmd error,{}".format(e))
		 		parser.print_help()
		 		return
		 	#
		 	dataList=[]
		 	supportCmds=["import","cls","quit"]
		 	while True:
		 		cmd=input('$ ');
		 		if len(cmd.strip())<1:
		 			continue
		 		cmdLines=cmd.split()
		 		if supportCmds.count(cmdLines[0])<1:
		 			print("This cmd:{} is not support".format(cmdLines[0]))
		 			self.subCmdParser.print_help()
		 			continue
		 		if "cls"==cmdLines[0]:
		 			self.cls()
		 			continue
		 		if "quit"==cmdLines[0]:
		 			return

	def __cls(self,line):
		os.system('cls')
	def __operRedis(self,cmds):
		pass
	def getSqlOperator(self,cmd):
		return MysqlOperator(cmd)
	    
 
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
	while True:
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