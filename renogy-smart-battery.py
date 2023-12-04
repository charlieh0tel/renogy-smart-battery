#!/usr/bin/python3

'''
Renogy smart battery RS485 readout.
This script features:
  - Detection of slave address
  - Readout of register data

The intention is to use it as a starting point to figure out the meaning of the register data of the renogy LIFEPO smart batteries.
The global dictionary contains a complete list of all registers that the batteries respond to (although the meaning of many registers is still unknown)
'''
import minimalmodbus
import serial.tools.list_ports
import argparse
import time

REGISTERS = {
    # Cell information
    'cellvoltage_count':{        'address':0x1388, 'length':1, 'type':'uint',   'scaling':'identical',        'unit':''},
    'cellvoltage_1':{            'address':0x1389, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit':'V'},
    'cellvoltage_2':{            'address':0x138a, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit':'V'},
    'cellvoltage_3':{            'address':0x138b, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit':'V'},
    'cellvoltage_4':{            'address':0x138c, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit':'V'},
    'cellvoltage_5':{            'address':0x138d, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit':'V'},
    'cellvoltage_6':{            'address':0x138e, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit':'V'},
    'cellvoltage_7':{            'address':0x138f, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit':'V'},
    'cellvoltage_8':{            'address':0x1390, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit':'V'},
    'cellvoltage_9':{            'address':0x1391, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit':'V'},
    'cellvoltage_10':{           'address':0x1392, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit':'V'},
    'cellvoltage_11':{           'address':0x1393, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit':'V'},
    'cellvoltage_12':{           'address':0x1394, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit':'V'},
    'cellvoltage_13':{           'address':0x1394, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit':'V'},
    'cellvoltage_14':{           'address':0x1396, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit':'V'},
    'cellvoltage_15':{           'address':0x1397, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit':'V'},
    'cellvoltage_16':{           'address':0x1398, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit':'V'},

    'celltemp_count':{           'address':0x1399, 'length':1, 'type':'uint',   'scaling':'identical',        'unit':''},
    'celltemp_1':{               'address':0x139a, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},
    'celltemp_2':{               'address':0x139b, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},
    'celltemp_3':{               'address':0x139c, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},
    'celltemp_4':{               'address':0x139d, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},
    'celltemp_5':{               'address':0x139e, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},
    'celltemp_6':{               'address':0x139f, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},
    'celltemp_7':{               'address':0x13a0, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},
    'celltemp_8':{               'address':0x13a1, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},
    'celltemp_9':{               'address':0x13a2, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},
    'celltemp_10':{              'address':0x13a3, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},
    'celltemp_11':{              'address':0x13a4, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},
    'celltemp_12':{              'address':0x13a5, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},
    'celltemp_13':{              'address':0x13a6, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},
    'celltemp_14':{              'address':0x13a7, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},
    'celltemp_15':{              'address':0x13a8, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},
    'celltemp_16':{              'address':0x13a9, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},

    'bmstemp':{                  'address':0x13ab, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},

    'envtemp_count':{            'address':0x13ac, 'length':1, 'type':'uint',   'scaling':'identical',        'unit':''},
    'envtemp_1':{                'address':0x13ad, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},
    'envtemp_2':{                'address':0x13ae, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},

    'heatertemp_count':{         'address':0x13af, 'length':1, 'type':'uint',   'scaling':'identical',        'unit':''},
    'heatertemp_1':{             'address':0x13b0, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},
    'heatertemp_2':{             'address':0x13b1, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},

    # Battery information
    'current':{                  'address':0x13b2, 'length':1, 'type':'sint',   'scaling':'linear(0.01,0)',   'unit': 'A'},
    'voltage':{                  'address':0x13b3, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit':'V'},
    'remaining_capacity':{       'address':0x13b4, 'length':2, 'type':'uint',   'scaling':'linear(0.001,0)',  'unit':'Ah'},
    'total_capacity':{           'address':0x13b6, 'length':2, 'type':'uint',   'scaling':'linear(0.001,0)',  'unit':'Ah'},
    'cycle_number':{             'address':0x13b8, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'charge_voltage_limit':{     'address':0x13b9, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit':'V'},
    'discharge_voltage_limit':{  'address':0x13ba, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit':'V'},
    'charge_current_limit':{     'address':0x13bb, 'length':1, 'type':'sint',   'scaling':'linear(0.01,0)',   'unit': 'A'},
    'discharge_current_limit':{  'address':0x13bc, 'length':1, 'type':'sint',   'scaling':'linear(0.01,0)',   'unit': 'A'},

    # Alarms/status
    'cell_voltage_alarminfo':{   'address':0x13ec, 'length':2, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'cell_temp_alarminfo':{      'address':0x13ee, 'length':2, 'type':'uint',   'scaling':'identical',        'unit': ''}, 
    'other_alarminfo':{          'address':0x13f0, 'length':2, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'status1':{                  'address':0x13f2, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'status2':{                  'address':0x13f3, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'status3':{                  'address':0x13f4, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'charging_status':{          'address':0x13f5, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    
    # General information
    'serial':{                   'address':0x13f6, 'length':8, 'type':'string', 'scaling':'identical',        'unit': ''},
    'manu_version':{             'address':0x13fe, 'length':1, 'type':'string', 'scaling':'identical',        'unit': ''},
    'mainline_version':{         'address':0x13ff, 'length':2, 'type':'string', 'scaling':'identical',        'unit': ''},
    'comms_version':{            'address':0x1401, 'length':1, 'type':'string', 'scaling':'identical',        'unit': ''},
    'model':{                    'address':0x1402, 'length':8, 'type':'string', 'scaling':'identical',        'unit': ''},
    'firmware_version':{         'address':0x140a, 'length':2, 'type':'string', 'scaling':'identical',        'unit': ''},
    'manufacturer':{             'address':0x140c, 'length':10, 'type':'string', 'scaling':'identical',        'unit': ''},

    # Cell voltage protection
    'cell_over_volt_limit':{     'address':0x1450, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit': 'V'},
    'cell_high_volt_limit':{     'address':0x1451, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit': 'V'},
    'cell_low_volt_limit':{      'address':0x1452, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit': 'V'},
    'cell_under_volt_limit':{    'address':0x1453, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit': 'V'},

    # Temperature protection
    'charge_over_temp_limit':{   'address':0x1454, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},
    'charge_high_temp_limit':{   'address':0x1455, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},
    'charge_low_temp_limit':{    'address':0x1456, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},
    'charge_under_temp_limit':{  'address':0x1457, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},

    # Charge limits.
    'charge_over2_limit':{       'address':0x1458, 'length':1, 'type':'sint',   'scaling':'linear(0.01,0)',   'unit': 'A'},
    'charge_over1_limit':{       'address':0x1459, 'length':1, 'type':'sint',   'scaling':'linear(0.01,0)',   'unit': 'A'},
    'charge_high_limit':{        'address':0x145a, 'length':1, 'type':'sint',   'scaling':'linear(0.01,0)',   'unit': 'A'},

    # Module voltage limits.
    'module_over_volt_limit':{   'address':0x145b, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit': 'V'},
    'module_high_volt_limit':{   'address':0x145c, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit': 'V'},
    'module_low_volt_limit':{    'address':0x145d, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit': 'V'},
    'module_under_volt_limit':{  'address':0x145e, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit': 'V'},
    
    # Discarge limits.
    'discharge_over_temp_limit':{'address':0x145f, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},
    'discharge_high_temp_limit':{'address':0x1460, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},
    'discharge_low_temp_limit':{ 'address':0x1461, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},
    'discharge_under_temp_limit':{'address':0x1462, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},
    'discharge_over2_limit':{    'address':0x1463, 'length':1, 'type':'sint',   'scaling':'linear(0.01,0)',   'unit': 'A'},
    'discharge_over1_limit':{    'address':0x1464, 'length':1, 'type':'sint',   'scaling':'linear(0.01,0)',   'unit': 'A'},
    'discharge_high_limit':{     'address':0x1465, 'length':1, 'type':'sint',   'scaling':'linear(0.01,0)',   'unit': 'A'},
    
    #
    'shutdown_command':{         'address':0x1466, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'device_address':{           'address':0x1467, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unique_id':{                'address':0x146a, 'length':2, 'type':'uint',   'scaling':'identical',        'unit': ''},

    #
    'charge_power':{             'address':0x146c, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': 'W'},
    'discharge_power':{          'address':0x146d, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': 'W'},
}


def linear(factor, offset, input):
    '''
    Linear conversion method. 
    Used to convert fixed point integers to physical values.
    '''
    return (input*factor)+offset

def read_register(instrument, reg: dict):
    '''
    Read a single register (can be more than 2 bytes).
    Reads the raw data from one or multiple consecutive registers
    and converts the raw data to physical values (if required).
    Return a dictionary with the following keys:
        * value: Physical value or string
        * raw_bytes: List containing the register data (one byte per list entry)
    '''
    raw_data = instrument.read_registers(reg['address'], reg['length'])
    raw_bytes = []
    idx = 0
    for uint16 in raw_data:
        raw_bytes.append(uint16 >> 8)
        raw_bytes.append(uint16 & 0x00ff)
        idx = idx + 2
    value = 0
    
    # Calculate raw value
    if reg['type'] == 'sint':
        value = int.from_bytes(raw_bytes, signed=True,  byteorder='big')
    elif reg['type'] == 'uint':
        value = int.from_bytes(raw_bytes, signed=False, byteorder='big')
    elif reg['type'] == 'string':
        string = ''
        for reg in raw_data:
            string = string+chr(reg >> 8)
            string = string+chr(reg & 0xff)
        # If the string does not match the register length exactly it will contain a termination character (0x00)
        # Truncate the string if required:
        string = string.split("\x00")[0]
        return {'value':string, 'raw_bytes': raw_bytes}
    else:
        print(f'Warning: Unsupported register type {reg["type"]}.')
        return None
    
    # Apply scaling
    if reg['scaling']=='identical':
        return {'value':value, 'raw_bytes': raw_bytes}
    else:
        # Add paramter for the input value
        head, _sep, tail = partitioned = reg['scaling'].rpartition(')')
        fnc_call = head+', value)'
        scaled = eval(fnc_call)
        return {'value':scaled, 'raw_bytes': raw_bytes}

def scan_addresses(instrument):
    '''
    Scan slave address.
    Iterates through all RS485 addresses and checks whether the register 0x13b3 can be read from any of them.
    If an address is found it is returned, returns None otherwise.
    '''
    TEST_REGISTER = {'address':0x13b3, 'length':1, 'type':'uint',   'scaling':'identical'}
    instrument.serial.timeout = 0.1
    for address in range(0x01, 0xf8):
        instrument.address = address
        try:
            read_register(instrument, TEST_REGISTER)
            return address
        except:
            pass           
    
    return None

def read_registers(instrument):
    '''
    Read all registers from the slave.
    Iterates through all registers defined in the global variables
    and parses the returned data.
    '''
    global REGISTERS
    values = {}
    for reg in REGISTERS:
        try:
            values[reg] = read_register(instrument, REGISTERS[reg])
        except Exception as inst:
            print(f'Error: Exception reading register {reg}: {inst}.')    
    return values

def print_values_loop(instrument):
    '''
    Read all register data and present them in a human readable form.
    Data is updated every 1s and printed to console in a table.
    '''
    global REGISTERS

    name_len=30
    while(True):
        values = read_registers(instrument)
        print('')
        print('Register'.ljust(name_len)+'Address'.ljust(10)+'Value'.ljust(20).ljust(10)+'Binary'.ljust(35))
        print('----------------------------------------------------------------------------------------------')
        for key in values:
            register_name = key.ljust(name_len)
            address_string = "{0:#0{1}x}".format(REGISTERS[key]['address'],6).ljust(10)
            if isinstance(values[key]['value'], float):
                value_number_string = '{:.2f}'.format(values[key]['value'])
            else:
                value_number_string = str(values[key]['value'])
            value_string = (value_number_string+' '+REGISTERS[key]['unit']).ljust(20)
            binary_string = (' '.join(format(byte, '08b') for byte in values[key]['raw_bytes'])).ljust(35)
            if len(binary_string) > 35:
                binary_string = binary_string[:32]+'...'
            print(register_name+address_string+value_string+binary_string)
        time.sleep(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Renogy Smart Battery RS485 readout.')
    parser.add_argument('--device', default='/dev/ttyUSB0', help='Serial device to use for RS485 communication')
    parser.add_argument('--address', default=0xf7, type=lambda x: int(x,0), help='Slave address of the RS485 device')
    parser.add_argument('--scan-addresses', default=False, help='Determine slave address by brute force.', action='store_true')
    parser.add_argument('--list-devices', default=False, help='List serial devices', action='store_true')
    args = parser.parse_args()

    if args.list_devices:
        print('device'.ljust(20)+'manufacturer'.ljust(25)+'product'.ljust(25)+'description')
        print('---------------------------------------------------------------------------------------')
        for port in serial.tools.list_ports.comports():
            dev = port.device or 'n/a'
            manf = port.manufacturer or 'n/a'
            prod = port.product or 'n/a'
            desc = port.description or 'n/a'
            print(dev.ljust(20)+manf.ljust(25)+prod.ljust(25)+desc)
    else:
        # 247 (0xf7) is the default address. If another renogy device is connected it might have reprogrammed the address to another value.
        instrument = minimalmodbus.Instrument(args.device, slaveaddress=247)
        instrument.serial.baudrate = 9600
        instrument.serial.timeout = 0.2

        if args.scan_addresses:
            print('Scanning addresses...')
            slave_address = scan_addresses(instrument)

            if(slave_address != None):
                print(f'Slave address: {hex(slave_address)}')
            else:
                print('Error: could not determine slave address.')
        else:
            slave_address = args.address

        if slave_address != None:
            instrument.address = slave_address
            instrument.serial.timeout = 0.2
            print_values_loop(instrument)


