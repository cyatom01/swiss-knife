#!/usr/bin/python3
import re
from prettytable import PrettyTable
    
x = PrettyTable(field_names=["Key", "Value", "Operation"],sortby="Operation",reversesort=True)

x.align = "l"
x.add_row(["Adelaide", 1295, 0])
x.add_row(["Brisbane", 5905, 1])
x.add_row(["Darwin", 112, 1])
x.add_row(["Hobart", 1357, 0])
x.add_row(["Sydney", 2058, 0])
x.add_row(["Melbourne", 1566, 0])
x.add_row(["Perth", 5386, 0])

print(x.get_string(sortby="Operation"))

urlReg= re.compile('(?P<provider>(\\w+))://(?P<host>(\\d+.\\d+.\\d+.\\d+)):(?P<port>(\d+))/(?P<db>(\w+))')
url='mysql://10.124.144.98:3306/test_zyzx_dresource'
regMatch = urlReg.search(url)
v = regMatch.group('provider')
print(v)
print(regMatch.group('host'))
print(regMatch.group('port'))
#print(reg.search(url).group())
