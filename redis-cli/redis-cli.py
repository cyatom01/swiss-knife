#! /usr/bin/env python
#
# This script want to getting modified modules.
#
# -*- coding: UTF-8 -*-
import redis
import argparse
import re
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
			return False
		redis=self.redis
		redis.set(cmdLines[1], bytes(cmdLines[2:].join(), "utf8"))
		return True
		
	def get(self,line):
		cmdLines=line.split()
		if (len(cmdLines)<2):
			print("Express error,such as: get key")
			return False
		redis=self.redis
		print(str(redis.get(cmdLines[1]),"utf8").strip())
		return True

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
			 			 operator.methodcaller(cmdLines[0],cmdLines[1:].join())(pipeline)
			 		if(len(cmdLines)>=3):
			 			 operator.methodcaller(cmdLines[0],cmdLines[1],cmdLines[2:].join())(pipeline)
			 	except AttributeError as e:
			 		 print('Unsupported operation,this cmd will be ignored:{}'.format(e))
		pipeline.execute()

	def delete(self,line):
		cmdLines=line.split()
		if (len(cmdLines)<2):
			print("Express error,such as: delete key")
			return False
		redis=self.redis
		redis.delete(cmdLines[1])
		return True

	def cls(self,line):
		os.system('cls')

	def append(self,line):
		cmdLines=line.split()
		if (len(cmdLines)<2):
			print("Express error,such as: append key value")
			return
		redis=self.redis
		redis.append(cmdLines[1], cmdLines[2:].join())
		print(str(redis.get(cmdLines[1]),"utf8").strip())

class MysqlOperator:
	def __init__(self, config):
		self.conn=pymysql.connect(host=config['host'],
			user=config['user'],
			password=config['password'],
			db=config['db'],
			charset='utf8mb4',
			cursorclass=pymysql.cursors.DictCursor)		

	def select(self,sql):
		data_rows=[]
		try:
			with self.conn as cursor:
				 cursor.execute(sql)
				 rows = cursor.fetchall()
				 for row in rows:
				 	row=[row['Key'],row['Value'],row['O']]
				 	data_rows.append(row)
			return data_rows
		except Exception as e:
			print("Excute sql error:{}".format(e))
			return data_rows

	def destroy(self):
		if self.conn is not NoneType:
			self.conn.close()


class RedisCmdExcutor:
	__supportCmds=["quit","set","get","pip","cls","delete","append"]
	def __init__(self, redisOperator):
		self.redisOperator=redisOperator

	def support(self,cmd):
		cmdLines=cmdLines=cmd.split();
		return self.__supportCmds.count(cmdLines[0])>0

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
		self.subCmdParser=self.__getSubCmdParaser()

	def __getSubCmdParaser(self):
		parser=argparse.ArgumentParser(prog='import', usage="import sql")
		parser.add_argument('sql', nargs='?')
		return parser

	def support(self,cmd):
		cmdLines=cmdLines=cmd.split();
		return self.__supportCmds.count(cmdLines[0])>0

	def getCmdParser(self):
		if hasattr(self,"parser"):
			return self.parser

		parser=argparse.ArgumentParser(prog='conn', usage="conn [options]",
									 formatter_class=argparse.RawDescriptionHelpFormatter)
		parser.add_argument("-url",
						required=True,
						type=str,
						help='db connect url')
		parser.add_argument('-u',
						required=True,
						type=str,
						help='db connect auth user account')
		parser.add_argument('-p',
						required=True,
						type=str,
						help='db connect user password')
		self.parser=parser
		return self.parser
     	
     	
	
    #get sql connector
	def execute(self,cmd):
		 	cmdLines=cmd.split()
		 	if(len(cmdLines)<2):
		 		print("Cmd error,such as:conn -url url -u user -p pwd")
		 		return
		 	parser,args=None,None
		 	try:
		 		parser=self.getCmdParser()
		 		args=parser.parse_args(cmdLines[1:])
		 		self.sqlOperator=self.getSqlOperator(args)
		 	except Exception as e:
		 		print("Cmd error,{}".format(e))
		 		parser.print_help()
		 		return
		 	#
		 	dataList=[]
		 	try:
		 		supportCmds=["import","cls","quit"]
			 	while True:
			 		cmd=input('$ ');
			 		if len(cmd.strip())<1:
			 			continue
			 		cmdLines=cmd.split()
			 		if supportCmds.count(cmdLines[0])<1:
			 			print("This cmd:{} is not supported.".format(cmdLines[0]))
			 			self.subCmdParser.print_help()
			 			continue
			 		if "cls"==cmdLines[0]:
			 			self.__cls()
			 			continue
			 		if "quit"==cmdLines[0]:
			 			print("Successfuly quit sub cli.")
			 			return
			 		dataRows=self.sqlOperator.select(' '.join(cmdLines[1:]))
			 		self.__operRedis(dataRows)
		 	except Exception as e:
		 		print("Occured error:{}".format(e))
		 	finally:
		 		if self.sqlOperator is not None:
		 			self.sqlOperator.destroy()

	def __cls(self,line):
		os.system('cls')

	def __operRedis(self,dataRows):
		table = PrettyTable(field_names=["Key", "Value", "O"],sortby="O",reversesort=True)
		table.align = "l"
		if len(dataRows)<1:
			print("0 rows data found.")
			print(table.get_string())
			return
		for i,v in enumerate(dataRows):
			table.add_row(v)
		print("********************")
		print('{} rows fuound.'.format(len(dataRows)))
		print(table.get_string())
		print('{} rows fuound.'.format(len(dataRows)))
		print("********************")
		if len(dataRows) >0 :
			while True:
				cmd=input('Are you sure save data to redis? (0:No,1:Yes):')
				cmd=cmd.strip()
				if '1'==cmd :
					break
				elif '0'==cmd:
					print("Data will not be saved to redis.")
					dataRows=[]
					return
				else:
					print("Your choice is wrong. Please try agin.")
					continue
		failedRows=[]
		for i,v in enumerate(dataRows):
			cmd
			try:
				if '1'==dataRows[2].strip():
					cmd='set '+dataRows[0]+' '+dataRows[1]
				if '0'==dataRows[2].strip():
					cmd='delete '+dataRows[0]
				cmdLines=cmd.split()
				operator.methodcaller(cmdLines[0],cmd)(self.redisOperator)
			except Exception as e:
				failedRows.append(v)
		if len(failedRows)>0:
			table.clear()
			for i,v in enumerate(failedRows):
				table.add_row(v)
				print("********************")
				print('{} rows save failed.'.format(len(failedRows)))
				print(table.get_string())
				print('{}  rows save failed.'.format(len(failedRows)))
				print("********************")
		else:
			print("Save {} rows data to redis successfuly.".format(len(failedRows)))

	def getSqlOperator(self,args):
		urlReg= re.compile('(?P<provider>(\\w+))://(?P<host>(\\d+.\\d+.\\d+.\\d+)):(?P<port>(\d+))/(?P<db>(\w+))')
		supportDBs=['mysql']
		dbConfig={}
		try:
			regMatch = urlReg.search(args.url)
			dbConfig['provider']=regMatch.group('provider')
			if supportDBs.count(dbConfig['provider'])<1:
				print("Unsupport db:{}".format(dbConfig['provider']))
				return
			dbConfig['host']=regMatch.group('host')
			dbConfig['port']=regMatch.group('port')
			dbConfig['db']=regMatch.group('db')
			dbConfig['user']=args.u
			dbConfig['password']=args.p
			return MysqlOperator(dbConfig)
			print("Login {} successfuly.".format(dbConfig['provider']))
		except Exception as e:
			print("URL sytnax error.{}".format(e))
			return
	    
 
class CmdExcutorFactory:
	def __init__(self,redisClient):
		self.redisClient=redisClient
		self.redisOperator=RedisOperator(redisClient);
		self.excutors=[RedisCmdExcutor(self.redisOperator),SqlCmdExcutor(self.redisOperator)]

	def getExcutor(self,cmd):
		for i, e in enumerate(self.excutors):
			if e.support(cmd):
				return e
		print("This cmd:{} is not supported".format(cmd))
		return None
		

def cmd_define():
	uasge ="""
	%(prog)s [options]"""
	parser=argparse.ArgumentParser(prog='redis-cli', usage=uasge,
									 formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument("-host",
						required=True,
						type=str,
						help='redis host')
	parser.add_argument('-pwd',
						required=False,
						type=str,
						help='auth password')
	return parser

def parse_options():
	parser=cmd_define()
	args = parser.parse_args()
	return args

def execute():
	rclient=redis.Redis(connection_pool = redis_pool);
	while True:
		try:
			cmd=input('$ ');
			if len(cmd.strip())<=0:
				continue
			cmdLines=cmd.split()
			if 'help'== cmdLines[0]:
				cmd_define().print_help()
				continue
			excutor=CmdExcutorFactory(rclient).getExcutor(cmd);
			if excutor is None:
				continue
			excutor.execute(cmd)			
		except Exception as e:
			 print('Unexpected error:{}'.format(e))
			 return	
def print_help():
	pass

if __name__ == "__main__":
	args=parse_options()
	host=args.host.split(":")
	passwd=args.pwd
	redis_pool=redis.ConnectionPool(host = host[0] , port = 6379, db = 0, password = passwd)
	execute()