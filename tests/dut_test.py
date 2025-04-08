import cocotb
from cocotb.triggers import Timer, RisingEdge, ReadOnly, NextTimeStep
from cocotb_bus.drivers import BusDriver


@cocotb.test()
async def dut_test(dut):
    a=(0,0,1,1)
    b=(0,1,0,1)
    y=(0,1,1,1)
    for i in range(4):
        dut.a$whas.value=a[i]
        dut.b$whas.value=b[i]
        assert dut.y$whas.value==y[i], "TEST FAILED"
    
