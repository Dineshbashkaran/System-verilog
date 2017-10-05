#!/usr/bin/python
#

#
"""This Project is done using 'PYTHON'. The concepts learned are opening/closing/writing/reading flies using python. The project deals with generation of verilog RTL and test bench for Shift registers. The parameters like width,stages,reset of the shift registers is explicit and it could be changed in real time. The python should basically get these values from user and generate the RTl and Test bench for the Shift register. The RTL should be covering good amount of test coverage. With respect to Test Bench, Number of test cases passes should be 100xstages and the simulation should finish after the execution of test cases.
Command Line:The parameters for this project are " Width, Stages, Reset, Outfile ". How this works is, the user can give any value for this parameter choosing how many stages and width they want and what value of reset they require. They also get chance to choose the outfile name. This is given in command line by user.
Parsing: A new parameter -param is included, which means the user can select to parse the values of ( width, stages, reset, outfile ) from the file he has. So basically user types the file name from which he wants the value to be extacted.
The parameters has it own limit and so user should select the values between those values
width should be between 1-64.
stages should be between 1-128.
Reset shoule be less than 2*width. 
The format on command line is 
    -width
    -stages
    -reset
    -outputfile
PROGRAM FLOW:
The program consists of 2 sub routines, One for RTL and One for Testbench. The values on which the shift register has to be generated is extracted from the user as discussed above. 
"""
import re
import sys
import getopt

def verilog ():
	rese = str(reset)
	widt = str(width)
	outputfile = ''.join((outfile + '.v'))
	
	
	file = open (outputfile, "w")

	file.write("module "  )
	file.write(outfile)
	file.write("(\nreset,\nclk,\nscan_in0,\nscan_en,\ntest_mode,\nscan_out0,\nin,\nout,\n);\n\n\n\ninput\n   reset,\n   clk;\n\n\n input\n")
      	file.write("scan_in0,\n    scan_en,\n    test_mode;\n\n output\n    scan_out0;\n  input [")
	file.write(width)
	file.write(":0] in;\n  output reg [")
	file.write(width)
	file.write(":0] out;")
	 
	
	for x in range(int(stages)):
		file.write  ("\n	reg[" + width + ":0] sr"+ str(x) + ";")

	file.write("\nalways @(posedge clk or posedge reset)\n begin\n if (reset)\n	begin\n		out<="+ str(reset)+";\n") 
	 
	for x in range(int(stages)):
		file.write("	sr" + str(x)+ " [" + widt + ":0] <= " + rese + ";\n" )	 
	
	file.write("	end\nelse\n	begin\n		sr0[" + width + ":0] <= in;\n" )
	
	n = int(stages) - 1 
	m = int(stages) - 2
		
	for x, y in zip(range(n),range(m)):
		file.write("	sr" +str(x+1) +" [" + width + ":0] <= sr" + str(y) + " [" + width + ":0];\n") 
	
	file.write("	out <= sr" + str(m)+ ";\n	end\nend\nendmodule")	
	
def testbench (): 
	
	outputfile = ''.join((outfile + '_test.v'))
	k = int(stages)
	j = k *100 
	l = k *25
	l = str(l)
	j = str (j)
	file = open (outputfile, "w")
	file.write("module test;\n wire scan_out0;\n reg clk,reset;\n reg scan_in0,scan_en,test_mode;\n")
	file.write(" reg[" + width + ":0]in;\n wire[" + width + ":0]out ;\n integer i;\n\n\n" + outfile + " top (\n") 
	file.write( ".reset(reset),\n.clk(clk),\n.scan_in0(scan_in0),\n.scan_en(scan_en),\n.test_mode(test_mode),\n.scan_out0(scan_out0),\n.in(in),\n.out(out)\n );\n") 
	file.write("initial \n begin \n$timeformat(-9,2,"+ '"ns",16);\n')
	file.write('`ifdef SDFSCAN\n   $sdf_annotate("sdf/'+ outfile+'_tsmc18_scan.sdf", test.top);\n`endif\n')
	file.write("	in = 0;\n	i=0;\n	clk = 1'b0;\n	reset = 1'b0;\n	scan_in0 = 1'b0;\n	scan_en = 1'b0;\n	test_mode = 1'b0;\n")
        file.write("#10 reset = 1'b1;\n\n#10\n reset = 1'b0;\n	repeat(3000)\n		@(posedge clk);\n	$finish;\nend\n// 50 MHz clock\nalways\n	 #10 clk = ~clk ;")
	file.write("\nalways\nbegin\n@(posedge clk)\nif( i < " + j + ")\nbegin\nin <= $urandom;\ni <= i + 1 ;\nend\nif( i =="+j+")\nbegin\n#"+	l+'\n	if(in == out)\n	begin\n ')
	file.write('$display ("TEST PASSED");\n	$display ( " in:%d, Out:%d, test cases:%d " , in , out, i );\n	$finish ;\n\n	end\n	else\n	begin\n	$display ( " test failed " ) ;\n	$display ( " in:%d, Out:%d, test cases:%d " , in , out, i );\n	$finish ;\n	end\n	\nend\nend\nendmodule')
        
       
def parameter():
	
	
	f = open(param,"r")
	data = f.readlines()
	f.close()
	#print data 
	#if f.mode == 'r':
		#contents=f.read()
		#print contents 
	global width
	global stages
	global reset
	global outfile  
	
	for line in data:
		if "width" in line:
			gwidth = line ; 
						 	
			awidth = re.findall(r'\d+', gwidth)
			width= ''.join(awidth)
			
		if "stages" in line:
			gstages = line ; 
			astages = re.findall(r'\d+', gstages)
			stages= ''.join(astages)
			 
		if "reset" in line: 
			greset = line ; 
			areset = re.findall(r'\w+', greset)
			reset= ''.join(areset)
			a = "reset"
			for char in a:
				reset = reset.replace(char,"")
			if "x" in reset:
				reset = int ( reset, 16)
		if "outfile" in line: 
			goutfile = line; 
			aoutfile = re.findall(r'\w+', goutfile)
			outfile = ''.join(aoutfile)
			a = "outfilev"
			for char in a:
				outfile = outfile.replace(char,"")
	
	
		

def usage():
	print "Usage: " +  sys.argv[0] + " [OPTIONS]"
	print "\t--width \tWidth should be between 0-64" 
	print "\t--stages \tStages should be between 0-128"
	print "\t--reset   \tReset should be < 2*width"
	print "\t--outfile \toutfile Should be with '.v' extension " 
	print "\t--help    \tThis help menu\n"

	print "Example:"
	print "\t" + sys.argv[0] + " --width 12 --stages 15 --reset 12 --outfile example.v"
	sys.exit(1)

if __name__ == "__main__":

	stages   = None
	width = None
	reset  = None
	outfile=None
	param= None

	try:
		opts, args = getopt.getopt(sys.argv[1:], "o:w:s:r:ph", ["outfile=","width=", "stages=", "reset=" , "param=", "help"] )
	except getopt.GetoptError, err:
		# print help information and exit:
		print(err) # will print something like "option -a not recognized"
		sys.exit(-1)

	for o, a in opts:
		if o in ("-o", "--outfile" ):
			outfile = a
		elif o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-r", "--reset"):
			reset = a
		elif o in ("-s", "--stages"):
			stages = a
		elif o in ("-w","--width"):
			width = a
		elif o in ("-p", "--param"):
			param = a
		elif o in ("-V", "--version"):
			print VERSION
			sys.exit(0)
		


	if width == None:
		print " " 
	else:
		width = int ( width ) 
	if stages == None:
		print " " 
	else:
		stages = int ( stages ) 	

	if reset == None:
		print " " 
	elif "x" in reset:
		reset = int ( reset, 16)
	else:
		reset = int ( reset ) 


	if outfile == None:
		print ("  ")
	elif ".v" in outfile:
		a = ".v"		
		for char in a:
			outfile = outfile.replace(char,"")
	width = str(width)
	stages = str(stages)
	reset = str(reset)
	outfile = str(outfile)

	
	if (((width != "None") or (stages != "None") or (reset != "None") or (outfile != "None")) and (param != None)):
		print	"\nPlease choose values from command lines or Parse the values ( NOT BOTH)\n" 

	if (param == None):
		if ((width != "None") and ((stages == "None") or (reset == "None") or (outfile == "None"))):
			print "\n ERROR \n Enter all the parameters(one of these missing->'stages,reset,outfile') "
	

	if ((reset != "None") and ((stages == "None") or (width == "None") or (outfile == "None"))):
		print "\n ERROR \n Enter all the parameters(one of thse missing->'width,stages,reset,outfile') "


	if ((stages != "None") and ((width == "None") or (reset == "None") or (outfile == "None"))):
		print "\n ERROR \n Enter all the parameters(one of these missing ->'width,reset,outfile') "

	if ((outfile != "None") and ((stages == "None") or (reset == "None") or (width == "None"))):
		print "\n ERROR \n Enter all the parameters(one of these missing -> 'width,stages,reset') "

	if ((width != "None") and (stages != "None") and (reset != "None") and (outfile != "None")):
		reset = int ( reset )
		width = int ( width ) 
		stages = int(stages)
	

	if(param == None):
		
		if ( (( width > 0) and (width < 64)) and ((stages > 0 ) and (stages < 128)) and  ((reset == 0) or (reset < 2**width ))  ):  
			print "\n gz! you have generated from your command line values\n" 
			reset = str(reset)
			width = str(width)
			verilog()
			testbench()
		else:
			print " Program Works Fine , Use -h or --help for contrains\n"
	if ((width == "None") and (stages == "None") and (reset == "None") and (outfile == "None")):
		if (param != None):
			print	"\nGz! You have generated the file sucessfully from your file "
			parameter()
			
			print(width)
			print(reset)
			print(outfile)
			print(stages)
			print(param)
	
			verilog()
			testbench()


           

    

    
    
    
    
    
        
	   
	







