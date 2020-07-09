# Micromouse-Embedded
Extension of (Micromouse) adds Hardware implementation to the logic algorithms

**PLANS WITH THE CODE**
- Implement the ability to save and load maze configuration from file. + Add color implementation for
added clarity

**HARDWARE**
 ESP32-WROOM-32D (8MB flash) chip --> lightweight, fast, built-in Wifi for easier debugging, ADC, low-power, support both Python and Arduino
 Algorithm switch --> back up in case any algorithm fails
  + Pololu 10:1 Micro Metal Gearmotor HP 6V --> fast, just enough torque, medium power usage, lightweight
  + Pololu Magnetic Encoders for the Micro Metal Gearmotors
  + Pololu Wheel 32×7mm --> featured horizontal treads for improved traction, small and lightweight
  + Voltage Regulator Options:
    ~ 6V Step-up Voltage Regulator --> for the 6V DC Motor above
    ~ Step-down Voltage Regulator --> ESP32 uses 3.3V logic
    ~ Step-Up/Step-Down Voltage Regulator --> maintain a fixed voltage with either lower or higher than expected voltage
  + Tattu 3.7V 800mAh 25C 1S LiPo Battery --> used by Truncale's Micromouse, stable, lightweight, no issue so far
  + PCB design
  + Four wheel configuration, which requires a gear system
  + Reset button for the chip


**3-D printed Chassis**

**NOTE:**
- ESP32 uses 3.3V logic
- Battery is 3.7V. Motors are 6V

**LINK** 
- ESP32-WROOM-32D (8MB flash): https://www.digikey.com/product-detail/en/espressif-systems/ESP32-WROOM-32D-8MB/1904-1024-1-ND/9381733
- Pololu Ball Caster: https://www.pololu.com/product/951
- Pololu 10:1 Micro Metal Gearmotor HP 6V dual-shaft: https://www.pololu.com/product/2211
- Pololu 32x7mm Wheels: https://www.pololu.com/product/1087
- Pololu magnetic Encoders for Metal Micro Gearmotors (with top-entry connector): https://www.pololu.com/product/4760
- Battery, link used by Truncale: https://www.amazon.com/gp/product/B01N74TTW6/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1
- Pololu 3.3V, 500mA Step-Down Voltage Regulator: https://www.pololu.com/product/2842
- Pololu 6V Step-Up Voltage Regulator: https://www.pololu.com/product/2892
