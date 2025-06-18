import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer
from cocotb_bus.drivers import BusDriver

@cocotb.test()
async def test_dut(dut):
    cocotb.start_soon(Clock(dut.CLK, 10, units="ns").start())
    dut.RST_N.value = 0
    await Timer(20, units='ns')
    dut.RST_N.value = 1
    await Timer(20, units='ns')
    write_drv = Wbus(dut, "", dut.CLK)
    read_drv = Rbus(dut, "", dut.CLK)
    await write_drv.write(4, 1)
    await write_drv.write(5, 1)

class Wbus(BusDriver):
    _signals = ["write_address", "write_data", "write_en"]

    def __init__(self, dut, name, clock):
        BusDriver.__init__(self,dut, name, clock)
        self.bus.write_address.value=0
        self.bus.write_data.value=0
        self.bus.write_en.value=0

    async def write(self, address, data):
        self.bus.write_address.value = address
        self.bus.write_data.value = data
        self.bus.write_en.value = 1
        await RisingEdge(self.clock)
        self.bus.write_en.value = 0

class Rbus(BusDriver):
    _signals = ["read_address", "read_en"]

    def __init__(self, dut, name, clock):
        BusDriver.__init__(self,dut, name, clock)
        self.bus.read_address.value=0
        self.bus.read_en.value=0

    async def read(self, address):
        self.bus.read_address.value = address
        self.bus.read_en.value = 1
        await RisingEdge(self.clock)
        data = int(self.entity.read_data.value)
        self.bus.read_en.value = 0
