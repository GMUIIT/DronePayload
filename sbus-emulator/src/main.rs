//! Blinks the LED on a Pico board
//!
//! This will blink an LED attached to GP25, which is the pin the Pico uses for the on-board LED.
#![no_std]
#![no_main]

use cortex_m_rt::entry;
use defmt::*;
use defmt_rtt as _;
use embedded_hal::digital::v2::OutputPin;
use embedded_time::fixed_point::FixedPoint;
use panic_probe as _;

// Provide an alias for our BSP so we can switch targets quickly.
// Uncomment the BSP you included in Cargo.toml, the rest of the code does not need to change.
use rp_pico as bsp;

use bsp::hal::{
    clocks::{init_clocks_and_plls, Clock},
    pac,
    sio::Sio,
    watchdog::Watchdog,
};

use bsp::hal::uart as uart;
use usb_device::{class_prelude::*, prelude::*};
use usbd_serial::SerialPort;


#[entry]
fn main() -> ! {
    info!("Program start");
    let mut pac = pac::Peripherals::take().unwrap();
    let core = pac::CorePeripherals::take().unwrap();
    let mut watchdog = Watchdog::new(pac.WATCHDOG);
    let sio = Sio::new(pac.SIO);  // Single-cycle IO

    // External high-speed crystal on the pico board is 12Mhz
    let external_xtal_freq_hz = 12_000_000u32;
    let clocks = init_clocks_and_plls(
        external_xtal_freq_hz,
        pac.XOSC,
        pac.CLOCKS,
        pac.PLL_SYS,
        pac.PLL_USB,
        &mut pac.RESETS,
        &mut watchdog,
    )
    .ok()
    .unwrap();

    let mut delay = cortex_m::delay::Delay::new(core.SYST, clocks.system_clock.freq().integer());

    // Set pins to their default states
    let pins = bsp::Pins::new(
        pac.IO_BANK0,
        pac.PADS_BANK0,
        sio.gpio_bank0,
        &mut pac.RESETS,
    );

    // ****** Done with the boilerplate code, now for the actual program ******

    // Setup LED pin
    let mut led_pin = pins.led.into_push_pull_output();

    // ******** Setup physical UART ********
    let uart_pins = (
        pins.gpio0.into_mode::<bsp::hal::gpio::FunctionUart>(),
        pins.gpio1.into_mode::<bsp::hal::gpio::FunctionUart>()
    );
    // Uart config is difficult
    let mut uart_config = uart::UartConfig::default();
    uart_config.baudrate = embedded_time::rate::Baud::new(100000);
    uart_config.data_bits = uart::DataBits::Eight;
    uart_config.stop_bits = uart::StopBits::Two;
    uart_config.parity = Some(uart::Parity::Even);
    let mut uart0 = uart::UartPeripheral::new(pac.UART0, uart_pins, &mut pac.RESETS)
                    .enable(uart_config, clocks.peripheral_clock.freq())
                    .unwrap();

    // ********* USB UART setup *********
    // Set up the USB driver
    let usb_bus = UsbBusAllocator::new(bsp::hal::usb::UsbBus::new(
        pac.USBCTRL_REGS,
        pac.USBCTRL_DPRAM,
        clocks.usb_clock,
        true,
        &mut pac.RESETS,
    ));

    // Set up the USB Communications Class Device driver
    let mut serial = SerialPort::new(&usb_bus);

    // Create a USB device with a fake VID and PID
    let mut usb_dev = UsbDeviceBuilder::new(&usb_bus, UsbVidPid(0x16c0, 0x27dd))
        .manufacturer("Fake company")
        .product("Serial port")
        .serial_number("TEST")
        .device_class(2) // from: https://www.usb.org/defined-class-codes
        .build();

    loop {
        /* uart0.write_full_blocking(b"Hello World!\r\n");
        serial.write(b"Hello World!\r\n").ok();
        led_pin.set_high().unwrap();
        delay.delay_ms(1000);
        info!("off!");
        led_pin.set_low().unwrap();
        delay.delay_ms(500); */

        usb_dev.poll(&mut [&mut serial]);
    }
}
