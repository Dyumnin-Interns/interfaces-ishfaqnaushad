import cocotb
from cocotb.triggers import Timer, RisingEdge, ReadOnly, NextTimeStep
from cocotb_bus.drivers import BusDriver

def sb_fn(actual_value):
    global expected_value
    assert actual_value==expected_value.pop(0), f"TEST FAILED"

@cocotb.test()
async def dut_test(dut):
    global expected_value
    a=(0,0,1,1)
    b=(0,1,0,1)
    expected_value=[0,1,1,1]
    awdrv=WriteDriver(dut,'a',dut.CLK)
    bwdrv=WriteDriver(dut,'b',dut.CLK)
    ReadDriver(dut,'y',dut.CLK,sb_fn)
    
    for i in range(4):
        awdrv.append(a[i])
        bwdrv.append(b[i])
        while len(expected_value)>0:
            await Timer(2,'ns')

class WriteDriver(BusDriver):
    _signals=['address','rdy','en','data']
    def __init__(self, dut, name, clk):
        BusDriver.__init__(self, dut, name, clk)
        self.bus.en=0
        self.clk=clk
        self.name=name

    async def _driver_send(self, value, sync=True):
        if self.bus.rdy!=1:
            await RisingEdge(self.bus.rdy)
        self.bus.en=1
        self.bus.data=value
        await Timer(1,'ns')
        if self.name=='a':
            self.bus.address[3]=self.bus.data
        else:
            self.bus.address[4]=self.bus.data
        await ReadOnly()
        await RisingEdge(self.clk)
        self.bus.en=0
        await NextTimeStep()
 
class ReadDriver(BusDriver):
    _signals=['address','rdy','en','data']
    def __init__(self, dut, name, clk, sb_callback):
        BusDriver.__init__(self, dut, name, clk)
        self.bus.en=0
        self.clk=clk
        self.callback=sb_callback

    async def _driver_send(self, value, sync=True):
        while True:
            if self.bus.rdy!=1:
                await RisingEdge(self.bus.rdy)
            self.bus.en=1
            await ReadOnly()
            self.bus.data=self.bus.address[5]
            self.callback(self.bus.data)
            await RisingEdge(self.clk)
            self.bus.en=0
            await NextTimeStep()       
    
