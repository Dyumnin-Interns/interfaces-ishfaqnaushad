module dut_test(CLK,
	   RST_N,

	   write_address,
	   write_data,
	   write_en,
	   write_rdy,

	   read_address,
	   read_en,
	   read_data,
	   read_rdy);
  output reg  CLK;
  input  RST_N;

  // action method write
  input  [2 : 0] write_address;
  input  write_data;
  input  write_en;
  output wire write_rdy;

  // actionvalue method read
  input  [2 : 0] read_address;
  input  read_en;
  output reg read_data;
  output wire read_rdy;
	
dut dut(
	.CLK(CLK),
	.RST_N(RST_N),
	.write_address(write_address),
	.write_data(write_data),
	.write_en(write_en),
	.write_rdy(write_rdy),
	.read_address(read_address),
	.read_en(read_en),
	.read_data(read_data),
	.read_rdy(read_rdy),
	.read_data(read_data)
);
	initial begin
		$dumpfile("waves.vcd");
		$dumpvars;
		CLK=0;
		forever begin
			#5;CLK=~CLK;
		end
	end
endmodule


