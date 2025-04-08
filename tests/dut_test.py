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
    expected_value=(0,1,1,1)
    
    
    for i in range(4):
        dut.write_address.value[3]=a[i]
        dut.write_address.value[4]=b[i]
        await ReadOnly()
        assert dut.read_address.value[5]==expected_value[i], "Test Failed"

