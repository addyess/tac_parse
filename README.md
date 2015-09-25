# tac_parse
parses tac_plus accounting log files into json

JSON object returned will be of the format
<pre>
[
   {
      "username" : "user",
      "log" : "sample/tac.acct",
      "cmd" : "aaa accounting exec default start-stop group tacacs+",
      "nas_name" : "10.200.201.71",
      "nas_port" : "tty0",
      "task_id" : "2",
      "service" : "shell",
      "priv-lvl" : "15",
      "nac_address" : "async",
      "time" : "2015/09/24 16:08:12",
      "imezone" : "UTC",
      "acct_type" : "stop"
   },
   ...
   {
      "cmd" : "show privilege",
      "log" : "filename_first.acct",
      "nac_address" : "172.22.107.230",
      "task_id" : "64",
      "service" : "shell",
      "nas_port" : "tty194",
      "nas_name" : "10.200.201.71",
      "acct_type" : "stop",
      "username" : "ADMIN",
      "priv-lvl" : "1",
      "time" : "2015/09/24 16:44:07",
      "timezone" : "UTC"
   }
]
</pre>

-----------------
Changes
---------------
* 09/25/2015 - support multiple date formats of various tac_plus accounting log files


---------------

