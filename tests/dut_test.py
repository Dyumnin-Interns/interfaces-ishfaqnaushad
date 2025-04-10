import cocotb
from cocotb.triggers import Timer, RisingEdge, FallingEdge, ReadOnly, NextTimeStep
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
    expected_value=(0,1,1,1)
    dut.write_en.value=0
    dut.read_en.value=0
    await Timer(1,'ns')
    for i in range(4):
        dut.write_address.value=4
        dut.write_en.value=1
        dut.write_data.value=a[i]
        await Timer(1,'ns')
        await RisingEdge(dut.CLK)
        dut.write_en.value=0
        await NextTimeStep()
        dut.write_address.value=5
        dut.write_en.value=1
        dut.write_data.value=b[i]
        await Timer(1,'ns')
        await RisingEdge(dut.CLK)
        dut.write_en.value=0
        dut.read_address.value=2
        if dut.read_data.value!=1:
            await RisingEdge(dut.read_data)  
        dut.read_en.value=1
        dut.read_address.value=3
        await ReadOnly()
        assert dut.read_data.value==expected_value[i], f"Test Failed,A={a[i]},B={b[i]},actual={dut.read_data.value.integer},expected={expected_value[i]}"
        await NextTimeStep()
        dut.read_en.value=0
        dut.read_address.value=2
        if dut.read_data.value!=0:
            await FallingEdge(dut.read_data)  

        
        

        

 

            
            

