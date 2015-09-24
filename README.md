# tac_parse
parses tac_plus accounting log files into json

JSON object returned will be of the format
<pre>
[
   {
      "_username" : "user",
      "_log" : "sample/tac.acct",
      "cmd" : "aaa accounting exec default start-stop group tacacs+ <cr>",
      "_nas_name" : "10.200.201.71",
      "_nas_port" : "tty0",
      "task_id" : "2",
      "service" : "shell",
      "priv-lvl" : "15",
      "_nac_address" : "async",
      "_time" : "Sep 24 16:08:12",
      "timezone" : "UTC",
      "_acct_type" : "stop"
   },
   ...
   {
      "cmd" : "show privilege <cr>",
      "_log" : "filename_first.acct",
      "_nac_address" : "172.22.107.230",
      "task_id" : "64",
      "service" : "shell",
      "_nas_port" : "tty194",
      "_nas_name" : "10.200.201.71",
      "_acct_type" : "stop",
      "_username" : "ADMIN",
      "priv-lvl" : "1",
      "_time" : "Sep 24 16:44:07",
      "timezone" : "UTC"
   }
]
</pre>