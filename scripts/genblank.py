# *******************************************************************************************
# *******************************************************************************************
#
#		Name : 		genblank.py
#		Purpose :	Create blank for 4510 code execution.
#		Date :		1st August 2019
#		Author : 	paul@robsons.org.uk
#
# *******************************************************************************************
# *******************************************************************************************

import re

instructions = {}

reject = ["smb","rmb","bbr","bbs","aug","brk","asw","row"]
bit32 = "lda,sta,adc,sbc,cmp,ora,eor,and,inc,dec,asl,ror,lsr,rol".split(",")

for s in [x.strip().lower() for x in open("65CE02.txt","r").readlines() if x.strip() != ""]:
	s = s.replace("\t"," ")
	m = re.match("^([0-9a-f]+)\s*([0-7a-z]+)\s*([a-z0-9]*)\s*\d+\s*(\d)$",s)
	assert m is not None,s
	amode = m.group(3) if m.group(3) != "" else "x"
	mode = amode+":"+m.group(1)+":"+m.group(4)
	opcode = m.group(2)
	if not opcode[:3] in reject:
		if opcode not in instructions:
			instructions[opcode] = []
		instructions[opcode].append(mode)
		if amode == "iz":
			instructions[opcode].append("fiz:{0:x}:{1}".format(0x100+int(m.group(1),16),m.group(4)))
k = [x for x in instructions.keys()]
k.sort(key = lambda k:chr(90-len(instructions[k]))+k)

comment = "; **************************************************************************"
for i in k:
	print(comment)
	print(";{0}{1}".format(" "*(36-(len(i)>>1)),i.upper()))
	print(comment)
	print("")
	options = instructions[i]
	options.sort()
	options = "("+" ".join(options)+")"
	print("{0}\t\t{1}\n".format(i,options))
	if i in bit32:
		options = [x[:2]+"2"+x[2:] for x in instructions[i] if x.startswith("a:") or x.startswith("z:")]
		options.sort()
		options = "("+" ".join(options)+")"
	print("{0}32\t{1}\n".format(i,options))

