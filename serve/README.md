# serve

Utterly trivial HTTP server - written in python because this means I can bound its functionality to something I actually want.
Built using fastAPI because I already knew flask ..

You'll need:

```
pip install fastapi uvicorn[standard]
```

And if you want to forward ports out of an ssh tunnel, to enable `GatewayPorts yes` in your `/etc/ssh/sshd_config` and run


```sh
ssh my_host -R *:14582:127.0.0.1:14582
```
