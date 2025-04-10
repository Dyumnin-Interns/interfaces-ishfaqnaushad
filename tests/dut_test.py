import cocotb
from cocotb.triggers import Timer, RisingEdge, ReadOnly, NextTimeStep
from cocotb_bus.drivers import BusDriver

j=0
def sb_fn(actual_value):
    global j
    global expected_value
    actual=actual_value.integer
    assert actual_value==expected_value[j], f"TEST FAILED, expected{j}={expected_value[j]},actual={actual}"
    j+=1

@cocotb.test()
async def dut_test(dut):
    global expected_value
    a=(0,0,1,1)
    b=(0,1,0,1)
    expected_value=[0,1,1,1]
    dut.RST_N.value=1
    await Timer(1, 'ns')
    dut.RST_N.value=0
    await Timer(1, 'ns')
    await RisingEdge(dut.CLK)
    dut.RST_N.value=1
    await Timer(1,'ns')
    adrv=WriteDriver(dut,'write',dut.CLK, 4)
    adrv.append(a[i])
    await Timer(6,'ns')
    bdrv=WriteDriver(dut,'write',dut.CLK, 5)
    bdrv.append(b[i])
    await Timer(100,'ns')
        
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
    def __init__(self, dut, name, clk, sb_callback,address):
        BusDriver.__init__(self, dut, name, clk)
        self.bus.en.value=0
        self.clk=clk
        self.callback=sb_callback
        self.bus.address.value=address
        self.append(0)
    
    async def _driver_send(self,value,sync=True):
        while True:
            if self.bus.rdy.value!=1:
                await RisingEdge(self.bus.rdy)
            self.bus.en.value=1
            await RisingEdge(self.clk)
            await NextTimeStep()
            self.bus.en.value=0
            await ReadOnly()
            self.callback(self.bus.data.value)
            await NextTimeStep()

            
            

