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
    adrv=WriteDriver(dut,'write',dut.CLK, 4)
    bdrv=WriteDriver(dut,'write',dut.CLK, 5)
    ReadDriver(dut,'read',dut.CLK,sb_fn, 3)

    for i in range(4):
        adrv.append(a[i])
        bdrv.append(b[i])
        while len(expected_value)>0:
            await Timer(2,'ns')
        
        
class WriteDriver(BusDriver):
    _signals=['address', 'rdy', 'en', 'data']
    def __init__(self, dut, name, clk, address):
        BusDriver.__init__(self, dut, name, clk)
        self.bus.en.value=0
        self.clk=clk
        self.bus.address.value=address
        
    async def _driver_send(self,value,sync=True):
        if self.bus.rdy.value!=1:
            await RisingEdge(self.bus.rdy)
        self.bus.en.value=1
        self.bus.data.value=value
        await ReadOnly()
        await RisingEdge(self.clk)
        self.bus.en.value=0
        await NextTimeStep()
        
class ReadDriver(BusDriver):
    _signals=['address', 'rdy', 'en', 'data']
    def __init__(self, dut, name, clk, sb_callback, address):
        BusDriver.__init__(self, dut, name, clk)
        self.bus.en.value=0
        self.clk=clk
        self.callback=sb_callback
        self.bus.address.value=address
    
    async def _driver_send(self,value,sync=True):
        while True:
            if self.bus.rdy.value!=1:
                await RisingEdge(self.bus.rdy)
            self.bus.en.value=1
            await ReadOnly()
            self.callback(self.bus.data.value)
            await RisingEdge(self.clk)
            await NexTimeStep()
            self.bus.en.value=0
            await NextTimeStep()
            self.append(0)
            

