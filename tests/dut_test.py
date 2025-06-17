import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock


@cocotb.test()
async def test_dut(dut):
    # Start clock
    cocotb.start_soon(Clock(dut.CLK, 10, units="ns").start())

    # Reset the DUT
    dut.RST_N.value = 0
    await Timer(20, units="ns")
    dut.RST_N.value = 1
    await Timer(20, units="ns")

    # Step 1: Write to address 4 (a_ff)
    dut.write_address.value = 4
    dut.write_data.value = 1
    dut.write_en.value = 1
    await RisingEdge(dut.CLK)
    dut.write_en.value = 0

    # Step 2: Write to address 5 (b_ff)
    dut.write_address.value = 5
    dut.write_data.value = 1
    dut.write_en.value = 1
    await RisingEdge(dut.CLK)
    dut.write_en.value = 0

    # Step 3: Wait for internal processing
    for _ in range(10):
        await RisingEdge(dut.CLK)

    # Step 4: Read from address 3 (should trigger y_ff DEQ)
    dut.read_address.value = 3
    dut.read_en.value = 1
    await RisingEdge(dut.CLK)
    dut.read_en.value = 0

    await Timer(10, units="ns")
    result = dut.read_data.value.integer
    dut._log.info(f"Read result from y_ff: {result}")

