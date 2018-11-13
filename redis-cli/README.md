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
```
   py redis_cli.py -host 127.0.0.1 -pwd password
```
And then you can do some things with the following cmd.
### Redis basic operation
- 
 1. **set** 
 2. **get**
 3. **pip**

 If you want save data to redis,following cmd will be used:
 ```
 set key value
 ```
 **Example:**
 ```
set sample 0001
 ```


 If you want get data to redis,following cmd will be used:
```
get key
```
**Example:**
```
get sample
```

If you have many data want save to reids,first you can save cmds to a file,and use following cmd:
```
pip file
```
**Example:**
```
```
The file content:
```
```

## Redis advance operation
- 
 1. **conn**  
 2. **import** 






