import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock


@cocotb.test()
async def test_dut(dut):

    cocotb.start_soon(Clock(dut.CLK, 10, units="ns").start())

    dut.RST_N.value = 0
    await Timer(20, units="ns")
    dut.RST_N.value = 1
    await Timer(20, units="ns")

    dut.write_address.value = 4
    dut.write_data.value = 1
    dut.write_en.value = 1
    await RisingEdge(dut.CLK)
    dut.write_en.value = 0

    dut.write_address.value = 5
    dut.write_data.value = 1
    dut.write_en.value = 1
    await RisingEdge(dut.CLK)
    dut.write_en.value = 0

    for _ in range(10):
        await RisingEdge(dut.CLK)

    dut.read_address.value = 3
    dut.read_en.value = 1
    await RisingEdge(dut.CLK)
    dut.read_en.value = 0

