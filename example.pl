#!/usr/bin/perl
#
# the traditional first program

#
# Strict and warnings are recommended.
#

=pod

=head4 DESCRIPTION

	This project focus on generating VERILOG RTL / TEST BENCH for shift registers. The Perl script is used to generate the code. The parameters for the shift registers are width ( number of bits ), stages ( number of shift registers), reset ( value assigned to shift register ) , outputfile name ( the name on which the module and verilog.v file should be created ).

	The parameters for verilog could be given in two ways. Either user can give the values in command line or they can have a file with values. Either case, perl script has to accept these values and generate verilog and testbench respectively. 

=head4 PARAMETERS

The parameters has it own limit and so user should select the values between those values
width should be between 1-64.
stages should be between 1-128.
Reset shoule be less than 2*width. 
If these restrictions are not followed by the user, the perl script should throw an appropriate error. 

=head4 bugs

	There is no bugs, the program works fine with respect to user input and parsing the values
 
=head4 ACKNOWLEDGEMENTS

	I would like to Thank professor Mark. A. Indovina for guiding and assisting all over the project.

=head4 COPYRIGHT

	All Rights provided to use this code in any part.

=head4 AUTHOR 

	Dinesh Anand Bashkaran

=cut



use strict;
use warnings;
use Getopt::Long ;
use Term::ANSIColor;
my $source_stages ; 
my $source_width; 
my $source_reset; 
my $source_output;
my $source_filename;
my $source_Parameter; 
my $outfile ; 


    GetOptions('width=i' => \ $source_width, 'stages=i' => \ $source_stages , 'reset=i' => \ $source_reset ,'outputfile=s' => \ $source_filename , 'param=s' => \ $source_Parameter) or die " please enter correct values\n" ; 

	if ($source_width && $source_stages && $source_reset && $source_filename && !$source_Parameter) 
	{
		($outfile = $source_filename) =~ s/\.[^.]+$//;
		
		
		if( ($source_width > 32 || $source_width < 0) || ($source_stages > 128 || $source_stages < 0 ) || ($source_reset > 2**$source_width) )
		{
		help();
		print color('bold red');
		print " your width is $source_width , choose between (0-64) \n";
		print " your stages is $source_stages , choose between (0-128) \n";
		print " your reset is $source_reset , choose value (reset < 2*width)\n";
		 print color('reset');
	
		}

		else 
		{
		print " worked!, File Generated\n"; 	
		verilog ();
		testbench ();
		}
	}	

	elsif(($source_width || $source_stages || $source_reset || $source_filename) && !$source_Parameter)
	{

			help ();
  		 print color('bold red');
		 print "\nERROR\n";
		 print color('bold  white');
		 print "\nPlease provide values for all parameters\n\n\n";
		 print color('reset');
	}

	elsif (($source_width || $source_stages || $source_reset || $source_filename) && ($source_Parameter))
	{
		help ();
		print color('bold red');
		print "\nERROR\n";
		print color('bold  magenta');
		print "\nPlease type -param yourfile.txt or give independent values for all variables\n\n\n";
		print color('reset');
	}

	
	elsif ($source_Parameter)
	{
		my $infile = "$source_Parameter" ;
		open ( my $fh1 , "<  $infile") || die "couldnt open the file $!";
		chomp(my @lines = <$fh1>);
        	my $array = join ' ', @lines;
		close $fh1;

		if ( ($source_stages, $source_width, $source_reset, $source_filename) = $array =~ m{stages = (\d+) ; width = (\d+) ; reset = (\d+) ; output = (\w+.v) ;})
			{
			
			( $outfile = $source_filename) =~ s/\.[^.]+$//;
			
			print " Worked! File Generated!\n " ; 
			verilog();
			testbench();
			}
		else 
			{
			print "\n Values are missing in the $source_Parameter\n";
			 }
	}






sub help
	{
	  	 print color('bold red');
		 print "\nERROR\n";
		 print color('bold  yellow');
		 print "To generate verilog/testbench you can choose your values or select from param file\n" ;
		 print "Please provide values for\n -width(0-64)\n -stages(0-128)\n -reset(<width)\n -outputfile.v\n";
		 print "or type -param param.txt\n\n\n\n" ;
		 print color('reset');
	}


sub verilog 
	{
		
my $a = 1; 
my $w = ($source_width - 1) ; 
my $c = ($source_stages - 2) ;	

			
	open (my $fh, '>',"$outfile\.v") || die "Could not open file '$source_filename' !";

print $fh "module $outfile (
           reset,
           clk,
           scan_in0,
           scan_en,
           test_mode,
           scan_out0,
	   in,
           out
           );
       

input
    reset,                      // system reset
    clk;                        // system clock

input
    scan_in0,                   // test scan mode data input
    scan_en,                    // test scan mode enable
    test_mode;                  // test mode select

output
    scan_out0;                  // test scan mode data output

input [$w:0] in;
output reg [$w:0] out;\n";

	for (my $j=0; $j < $source_stages; $j++)
	{
	print $fh "	reg[$w:0] sr$j;\n" ;
	}
print $fh "\nalways @(posedge clk or posedge reset)
begin
if (reset)
	begin
	out <= $source_reset;\n\n" ;
	for (my $i=0 ; $i < $source_stages; $i++)
	{
	print $fh "	sr$i [$w:0] <= $source_reset;\n";
	}
print $fh "
	end
else
	begin\n
	sr0[$w:0] <= in;\n ";
	
	for (my $j=0; $j < $c; $j++)
	{
	print $fh "	sr$a [$w:0] <= sr$j [$w:0];\n";
	$a = $a+1 ; 
	}
		
print $fh "
	out <= sr$c;\n\n
	end
end
endmodule  " ;
}

sub testbench 
{
my $a = 1; 
my $w = ($source_width - 1) ; 
my $c = ($source_stages - 1) ;
open (my $fh, '>', "$outfile\_test.v") || die "Could not open file '$source_filename' !";
print $fh "
module test;

wire  scan_out0;

reg  clk, reset;
reg  scan_in0, scan_en, test_mode;
reg [$w:0] in; 
wire [$w:0] out; 

$outfile top (
.reset(reset),
        .clk(clk),
        .scan_in0(scan_in0),
        .scan_en(scan_en),
        .test_mode(test_mode),
        .scan_out0(scan_out0),
	   .in(in),
	.out(out)
    );	
initial
begin
    \$timeformat(-9,2,\"ns\", 16);
`ifdef SDFSCAN
    \$sdf_annotate(\"sdf/chkrpl_tsmc18_scan.sdf\", test.top);
`endif
    clk = 1'b0;
    reset = 1'b0;
    scan_in0 = 1'b0;
    scan_en = 1'b0;
    test_mode = 1'b0;

#10 reset = 1'b1;

#10
    reset = 1'b0;
    repeat (1000)
	@(posedge clk) ;
    \$finish;
end

// 50 MHz clock
always
    #10 clk = ~clk ;

initial
begin
#20;
@(posedge clk)
in <= \$urandom;";

my $timeperiod = ( 100 + $source_stages * 50 );
print $fh "
#$timeperiod

if(out == in)
begin
\$display (\"Input matches the output\");
end

end
endmodule";

}







