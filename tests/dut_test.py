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
    dut.write_en.value=0
    dut.read_en.value=0
    
    
    for i in range(4):
        await RisingEdge(dut.CLK)
        await NextTimeStep()
        dut.read_en.value=0
        dut.write_address.value=4
        dut.write_data.value=a[i]
        dut.write_en.value=1
        await RisingEdge(dut.CLK)
        await NextTimeStep()
        dut.write_en.value=0
        await NextTimeStep()
        dut.write_address.value=5
        dut.write_data.value=b[i]
        dut.write_en.value=1
        await RisingEdge(dut.CLK)
        await NextTimeStep()
        dut.write_en.value=0
        await RisingEdge(dut.CLK)
        await NextTimeStep()
        dut.read_address.value=3
        dut.read_en.value=1
        await ReadOnly()
        actual = dut.read_data.value.integer
        assert actual == expected_value[i], f"Test Failed: A={a[i]}, B={b[i]}, Expected={expected_value[i]}, Got={actual}"

