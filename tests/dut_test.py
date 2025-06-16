import cocotb
from cocotb.triggers import Timer,RisingEdge,ReadOnly
from cocotb.clock import Clock
from cocotb_bus.drivers import BusDriver

@cocotb.test()
async def dut_test(dut):
    clk=dut.CLK
    dut.RST_N.value = 0
    await Timer(1, units='ns')
    dut.RST_N.value = 1
    await Timer(1, units='ns')
    await RisingEdge(dut.CLK)
    dut.RST_N.value = 1
    input_drv=InputDriver(dut,"write",clk)
    output_drv=OutputDriver(dut,"read",clk,sb_callback=print)
    cocotb.start_soon(my_monitor())
    await input_drv._driver_send(1)
    await input_drv._driver_send(0)
    await output_drv._driver_send(0)

class InputDriver(BusDriver):
    _signals=['rdy','en','data']

    def __init__(self,dut,name,clk):
        BusDriver.__init__(self,dut,name,clk)
        self.bus.en.value=0
        self.clk=clk

    async def _driver_send(self,value,sync=True):
        if self.bus.rdy.value!=1:
            await RisingEdge(self.bus.rdy)
        self.bus.en.value=1
        self.bus.data.value=value
        await ReadOnly()
        await RisingEdge(self.clk)
        self.bus.en.value=1
        await NextTimeStep()
class OutputDriver(BusDriver):
    _signals=['rdy','en','data']

    def __init__(self,dut,name,clk,sb_callback):
        BusDriver.__init__(self,dut,name,clk)
        self.bus.en.value=0
        self.clk=clk
        self.callback=sb_callback

    async def monitor(self,value,sync=True):
        if self.bus.rdy.value!=1:
            await RisingEdge(self.bus.rdy)
        self.bus.en.value=1
        #self.bus.data=value
        await ReadOnly()
        self.callback(self.bus.data.value)
        await RisingEdge(self.clk)
        self.bus.en.value=1
        await NextTimeStep()

