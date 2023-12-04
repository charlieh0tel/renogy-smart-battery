## Renogy Smart Battery RS485 Data readout

This has been updated to match the Renogy Modbus V1.7 specification.

### Pinout

Both RJ45 jacks are connected to the same RS485 lines on the PCB, so
it does not matter which jack is used to connect to the battery.  The
UP port also has lines for the activation button which is connected to
lines 3 and 4 and allows putting the battery into shelf mode.
![pinout](https://github.com/Grmume/renogy-smart-battery/blob/main/UP_Pinout.png)

Note that the Renogy pin numbers in the specification are backwards
compared to normal RJ45 convention.

### Commandline options

--device: Which serial device to use for the RS485 communication

--address: Address of the battery (247 by default, but can be changed by other devices)

--scan-addresses: Scan all addresses to determine the address of the battery.

--list-devices: List all available serial devices to use for the --device option

### Sample output

Battery discharging at 36 A.

```
Register                      Address   Value               Binary                            
----------------------------------------------------------------------------------------------
cellvoltage_count             0x1388    15                  00000000 00001111                  
cellvoltage_1                 0x1389    3.20 V              00000000 00100000                  
cellvoltage_2                 0x138a    3.20 V              00000000 00100000                  
cellvoltage_3                 0x138b    3.20 V              00000000 00100000                  
cellvoltage_4                 0x138c    3.20 V              00000000 00100000                  
cellvoltage_5                 0x138d    3.20 V              00000000 00100000                  
cellvoltage_6                 0x138e    3.20 V              00000000 00100000                  
cellvoltage_7                 0x138f    3.20 V              00000000 00100000                  
cellvoltage_8                 0x1390    3.20 V              00000000 00100000                  
cellvoltage_9                 0x1391    3.20 V              00000000 00100000                  
cellvoltage_10                0x1392    3.20 V              00000000 00100000                  
cellvoltage_11                0x1393    3.20 V              00000000 00100000                  
cellvoltage_12                0x1394    3.20 V              00000000 00100000                  
cellvoltage_13                0x1394    3.20 V              00000000 00100000                  
cellvoltage_14                0x1396    3.20 V              00000000 00100000                  
cellvoltage_15                0x1397    3.20 V              00000000 00100000                  
cellvoltage_16                0x1398    0.00 V              00000000 00000000                  
celltemp_count                0x1399    15                  00000000 00001111                  
celltemp_1                    0x139a    22.00 °C            00000000 11011100                  
celltemp_2                    0x139b    22.00 °C            00000000 11011100                  
celltemp_3                    0x139c    22.00 °C            00000000 11011100                  
celltemp_4                    0x139d    22.00 °C            00000000 11011100                  
celltemp_5                    0x139e    22.00 °C            00000000 11011100                  
celltemp_6                    0x139f    22.00 °C            00000000 11011100                  
celltemp_7                    0x13a0    22.00 °C            00000000 11011100                  
celltemp_8                    0x13a1    22.00 °C            00000000 11011100                  
celltemp_9                    0x13a2    23.00 °C            00000000 11100110                  
celltemp_10                   0x13a3    23.00 °C            00000000 11100110                  
celltemp_11                   0x13a4    23.00 °C            00000000 11100110                  
celltemp_12                   0x13a5    23.00 °C            00000000 11100110                  
celltemp_13                   0x13a6    23.00 °C            00000000 11100110                  
celltemp_14                   0x13a7    23.00 °C            00000000 11100110                  
celltemp_15                   0x13a8    23.00 °C            00000000 11100110                  
celltemp_16                   0x13a9    0.00 °C             00000000 00000000                  
bmstemp                       0x13ab    0.00 °C             00000000 00000000                  
envtemp_count                 0x13ac    0                   00000000 00000000                  
envtemp_1                     0x13ad    25.00 °C            00000000 11111010                  
envtemp_2                     0x13ae    25.00 °C            00000000 11111010                  
heatertemp_count              0x13af    0                   00000000 00000000                  
heatertemp_1                  0x13b0    25.00 °C            00000000 11111010                  
heatertemp_2                  0x13b1    25.00 °C            00000000 11111010                  
current                       0x13b2    -36.18 A            11110001 11011110                  
voltage                       0x13b3    48.60 V             00000001 11100110                  
remaining_capacity            0x13b4    46.68 Ah            00000000 00000000 10110110 01010100
total_capacity                0x13b6    50.00 Ah            00000000 00000000 11000011 01010000
cycle_number                  0x13b8    0                   00000000 00000000                  
charge_voltage_limit          0x13b9    55.50 V             00000010 00101011                  
discharge_voltage_limit       0x13ba    41.60 V             00000001 10100000                  
charge_current_limit          0x13bb    55.00 A             00010101 01111100                  
discharge_current_limit       0x13bc    -55.00 A            11101010 10000100                  
cell_voltage_alarminfo        0x13ec    0                   00000000 00000000 00000000 00000000
cell_temp_alarminfo           0x13ee    0                   00000000 00000000 00000000 00000000
other_alarminfo               0x13f0    0                   00000000 00000000 00000000 00000000
status1                       0x13f2    14                  00000000 00001110                  
status2                       0x13f3    512                 00000010 00000000                  
status3                       0x13f4    0                   00000000 00000000                  
charging_status               0x13f5    192                 00000000 11000000                  
serial                        0x13f6    22RBH4A051020000    00110010 00110010 01010010 01000...
manu_version                  0x13fe    01                  00110000 00110001                  
mainline_version              0x13ff    0001                00110000 00110000 00110000 00110001
comms_version                 0x1401    19                  00110001 00111001                  
model                         0x1402    RBT50LFP48S         01010010 01000010 01010100 00110...
firmware_version              0x140a    V104                01010110 00110001 00110000 00110100
manufacturer                  0x140c    RENOGY              01010010 01000101 01001110 01001...
cell_over_volt_limit          0x1450    3.70 V              00000000 00100101                  
cell_high_volt_limit          0x1451    3.60 V              00000000 00100100                  
cell_low_volt_limit           0x1452    3.00 V              00000000 00011110                  
cell_under_volt_limit         0x1453    2.80 V              00000000 00011100                  
charge_over_temp_limit        0x1454    55.00 °C            00000010 00100110                  
charge_high_temp_limit        0x1455    50.00 °C            00000001 11110100                  
charge_low_temp_limit         0x1456    3.00 °C             00000000 00011110                  
charge_under_temp_limit       0x1457    0.00 °C             00000000 00000000                  
charge_over2_limit            0x1458    120.00 A            00101110 11100000                  
charge_over1_limit            0x1459    55.00 A             00010101 01111100                  
charge_high_limit             0x145a    51.00 A             00010011 11101100                  
module_over_volt_limit        0x145b    55.50 V             00000010 00101011                  
module_high_volt_limit        0x145c    54.00 V             00000010 00011100                  
module_low_volt_limit         0x145d    45.70 V             00000001 11001001                  
module_under_volt_limit       0x145e    41.60 V             00000001 10100000                  
discharge_over_temp_limit     0x145f    60.00 °C            00000010 01011000                  
discharge_high_temp_limit     0x1460    55.00 °C            00000010 00100110                  
discharge_low_temp_limit      0x1461    -10.00 °C           11111111 10011100                  
discharge_under_temp_limit    0x1462    -20.00 °C           11111111 00111000                  
discharge_over2_limit         0x1463    -120.00 A           11010001 00100000                  
discharge_over1_limit         0x1464    -55.00 A            11101010 10000100                  
discharge_high_limit          0x1465    -51.00 A            11101100 00010100                  
shutdown_command              0x1466    0                   00000000 00000000                  
device_address                0x1467    48                  00000000 00110000                  
unique_id                     0x146a    0                   00000000 00000000 00000000 00000000
charge_power                  0x146c    12850 W             00110010 00110010                  
discharge_power               0x146d    21058 W             01010010 01000010
```
