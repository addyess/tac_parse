# tac_parse
parses tac_plus accounting log files into json

JSON object returned will be of the format
<pre>
{
	"filename_first.acct" : [
      {
         "ct" : "Sep 24 16:08:12",
         "nas_port" : "tty0",
         "nas_name" : "10.200.201.71",
         "username" : "user",
         "details" : [
            "task_id=2",
            "timezone=UTC",
            "service=shell",
            "priv-lvl=15",
            "cmd=aaa accounting exec default start-stop group tacacs+ <cr>"
         ],
         "nac_address" : "async",
         "acct_type" : "stop"
      },
      ...
	],
	...
	"filename_last.acct" : [
	],
}
</pre>