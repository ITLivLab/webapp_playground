#Requirements:
Minimega v.2.0: minimega.org
Before compiling, modify a line in vminfo.go file located under src/minimega folder
Change from: args = append(args, "0.0.0.0:"+sId)
Change to: args = append(args, "0.0.0.0:"+sId+",password")

VNC2FLV: http://www.unixuser.org/~euske/python/vnc2flv/ (install by running "pip install vnc2flv")
