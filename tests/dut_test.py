import cocotb
from cocotb.triggers import Timer,RisingEdge,ReadOnly
from cocotb.clock import Clock

@cocotb.test()
async def dut_test(dut):
    clk=dut.CLK
    cocotb.start_soon(Clock(dut.CLK,10,units="ns").start())
    dut.RST_N.value = 0
    await Timer(2, units='ns')
    dut.RST_N.value = 1
    await RisingEdge(clk)
    dut.write_en.value = 1
    dut.write_data.value = 1
    dut.write_address.value = 4
    await RisingEdge(clk)
    dut.write_en.value = 0
    dut.write_en.value = 1
    dut.write_data.value = 0
    dut.write_address.value = 5
    await RisingEdge(clk)
    dut.write_en.value = 0
    dut.read_en.value = 1
    dut.read_address.value = 0
    await RisingEdge(clk)
    dut.read_en.value = 0
    await Timer(1, units='ns')

