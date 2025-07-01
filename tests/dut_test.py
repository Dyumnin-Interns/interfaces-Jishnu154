import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer
from cocotb_bus.drivers import BusDriver
from cocotb_coverage.coverage import CoverPoint, coverage_db


@CoverPoint("top.write_address", xf=lambda addr, data: addr, bins=list(range(8)))
def cwrite_add(addr, data):
    pass

@CoverPoint("top.read_address", xf=lambda addr: addr, bins=list(range(8)))
def cread_add(addr):
    pass

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
    await read_drv.read(4)
    await read_drv.read(5)

    coverage_db.export_to_yaml(filename="coverage_report.yaml")
    cocotb.log.info("Functional coverage written to coverage_report.yaml")

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
        cwrite_add(address, data)

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
        cread_add(address)
