# Hardware

## Schematic

Figure 1 schows the schematic of the matrixpi hardware. The PCM_CLK pin is the pin that send the data to the logic level shifter. The shifter the sends the data to the neopixel. The neopixels and the logic level shifter are powered by the 5V power supply. The RPI is powered by its own USB power supply.

![matrixpi schematic](Design/matrixpi_schem.png)
*Figure 1: matrixpi schematic*

### RPI pins

| Pin | Description | Connected to |
|---|---|---|
| GPIO18 (PCM_CLK) | Sends the neopixel data to the logic level shiter | 74AHCT125 1A |
| GND | Ground | Ground |

### 74AHCT125 pins

| Pin | Description | Connected to |
|---|---|---|
| 1!EO | Enables the first buffer gate when tied to ground | Ground |
| 1A | 3.3V input signal for data | RPI GPIO18 (PCM_CLK) |
| 1Y | 5V output signal for data | Neopixel Data |
| GND | Ground | Ground |
| VCC | VCC | VCC |

### Neopixel pins

| Pin | Description | Connected to |
|---|---|---|
| Data | Data input for neopixels | 74AHCT125 1Y |
| GND | Ground | Ground |
| VCC | VCC | VCC |

## Physical layout

Figure 2 shows the layout of the matrixpi hardware on a breadboard.

![matrixpi physical layout](Design/matrixpi_bb.png)
*Figure 2: matrixpi physical layout*
