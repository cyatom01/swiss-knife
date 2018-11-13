# Python redis cli


## Prepare environment
1. Install python,you can access [python site](https://www.python.org/)
2. Install dependens library with the following cmd:
```
  pip install reids
  pip install pymysql
  pip install PrettyTable
```
## Cli Usage
```
 usage: redis-cli [options]
	 -host redis connection ip and port,like ip:port
	 -pwd redis connected passowd
```
First you should use cli connect redis.
```shell
   py redis_cli.py -host 127.0.0.1 -pwd password
```
And then you can do some things with the following cmd.
### Redis basic operation
 1.	**set**  add key value to redis
 2. **get**  get data from redis by key
 3. **pip**  excute batch cmds

 If you want save data to redis,following cmd will be used:
 ```shell
 set key value
 ```
**Example:**
 ```
set sample 0001
 ```


 If you want get data to redis,following cmd will be used:
```shell
get key
```
**Example:**
```shell
get sample
```

If you have many data want save to reids,first you can save cmds to a file,and use following cmd:
```shell
pip file
```
**Example:**
```shell
pip /home/user/data.txt
```
The file content:
```shell
set SERVICE_SWITCH_GLOBAL	0
set SERVICE_SWITCH_TERMINALSALREQSERVICE_31	0
set SERVICE_SWITCH_SINTERMCLESALEPRESERIVE_31	0
set SERVICE_SWITCH_QRYCHKTERMSERVICE_31	0
set SERVICE_SWITCH_TERMCLESALEPRESERVICE_31	0
set SERVICE_SWITCH_TERMINALSTATECHGREQSERVICE_31	0
set SERVICE_SWITCH_SELFTERMSUBSERVICE_31	0
set SERVICE_SWITCH_BATCHTERMSALESERVICE_31	0
set SERVICE_SWITCH_SINTERMCLESALEINTFSERVICE_31	0
delete SERVICE_SWITCH_TERMINALSALREQSERVICE_34
delete SERVICE_SWITCH_SINTERMCLESALEPRESERIVE_34
delete SERVICE_SWITCH_QRYCHKTERMSERVICE_34
```

## Redis advance operation
 
 1. **conn**  connect to datebase
 2. **import** import from db data with sql query to redis

First connect database with some args:
```shell
 conn -url provider://ip:port/db -u user -p passowd
```

And then,use the following cmd to import data to redis.
```shell
import select sql
```
>**Note:** select sql express must contains only 3 columns of data,the column named must be `Key` `Value` `O`.
`O`values range 0-1，1 means set data to redis,0 means delete data from redis.

**Example:**
```shell
import select code as 'Key',name as 'Value','1' as 'O' from table_name
```







