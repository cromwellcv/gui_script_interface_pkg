import serial.tools.list_ports
from multiprocessing import shared_memory
import threading

class gui_script_interface:
    def __init__(self, send_segment, receive_segment):
        self.shared_memory_manager = self.SharedMemoryManager(send_segment, receive_segment)
        # Initialize any other required variables or states

    class SharedMemoryManager:
        def __init__(self, send_segment, receive_segment):
            try:
                self.send_memory = shared_memory.SharedMemory(send_segment)
                self.receive_memory = shared_memory.SharedMemory(receive_segment)
            except FileNotFoundError:
                print("Shared memory segments not found. Please start Script 2 first.")
                raise

        def receive_messages(self):
            while True:
                message = self.receive_memory.buf[:].tobytes().rstrip(b'\0').decode()
                if message:
                    print("Received:", message)
                    for i in range(1024):
                        self.receive_memory.buf[i] = 0

        def send_message(self, message, counter):
            stm_command = message + " #" + str(counter)
            encoded_message = stm_command.encode()
            self.send_memory.buf[:len(encoded_message)] = encoded_message
            for i in range(len(encoded_message), 1024):
                self.send_memory.buf[i] = 0
            print("Sent:", stm_command)

    def send_via_shared_memory(self, message, counter):
        self.shared_memory_manager.send_message(message, counter)

    
    ##////////////////////////////////////////////////////////////
    def readWrite(self, mode, reg_address, dataOne, dataTwo):
        """
        Function to write data to a register, store parameters as instance variables, and return them.

        :param mode: Operation mode.
        :param reg_address: Register address.
        :param dataOne: First piece of data to write.
        :param dataTwo: Second piece of data to write.
        :return: Dictionary of written values.
        """
        self.write_mode = "0b001" #"0x1"
        self.write_reg_address = reg_address
        self.write_dataOne = dataOne
        self.write_dataTwo = dataTwo

        # Implement the write logic here

        # Format the string with the instance variable values
        formatted_string = f"spi read_write spi1 [ {self.write_mode} {self.write_reg_address} {self.write_dataOne} {self.write_dataTwo} ] #LOCAL"

        return formatted_string

    def read(self,mode,reg_address):
        """
        Function to read data from a register, store the parameter as an instance variable, and return it.

        :param reg_address: Register address to read from.
        :return: Register address read.
        """
        self.read_mode = mode # "0b000" #"0x0"
        self.read_reg_address = reg_address

        self.read_dataOne = "0b00000000"
        self.read_dataTwo = "0b00000000"

        # Implement the read logic here
        formatted_string = f"spi read_write spi1 [ {self.read_mode} {self.read_reg_address} {self.read_dataOne} {self.read_dataTwo} ] #LOCAL"
        return formatted_string


    def readWriteLUT(self, mode, lut_address, lut_ch, dataOne, dataTwo):
        """
        Function to write data to a register, store parameters as instance variables, and return them.

        :param mode: Operation mode.
        :param reg_address: Register address.
        :param dataOne: First piece of data to write.
        :param dataTwo: Second piece of data to write.
        :return: Dictionary of written values.
        """
        self.write_mode = mode #"0b001" #"0x1"
        self.write_lut_address = lut_address
        self.write_lut_ch_value = lut_ch
        self.write_lut_dataOne = dataOne
        self.write_lut_dataTwo = dataTwo

        # Implement the write logic here
        #f"spi read_write spi1 [0b11000000 {LUTaddr} {LUTch} {data_write1} {data_write2}]"

        # Format the string with the instance variable values
        formatted_string = f"spi read_write spi1 [ {self.write_mode} {self.write_lut_address} {self.write_lut_ch_value} {self.write_lut_dataOne} {self.write_lut_dataTwo} ] #LUT"

        return formatted_string

    def readLUT(self,mode,reg_address):
        """
        Function to read data from a register, store the parameter as an instance variable, and return it.

        :param reg_address: Register address to read from.
        :return: Register address read.
        """
        self.read_lut_mode = mode # "0b000" #"0x0"
        self.read_lut_address = reg_address
        self.read_lut_ch = "0b00000000"
        self.read_dataOne = "0b00000000"
        self.read_dataTwo = "0b00000000"
        #f"spi read_write spi1 [0b11000000 {LUTaddr} {LUTch} {data_write1} {data_write2}]"
        # Implement the read logic here
        formatted_string = f"spi read_write spi1 [ {self.read_lut_mode} {self.read_lut_address} {self.read_lut_ch} {self.read_dataOne} {self.read_dataTwo} ] #LUT"
        return formatted_string


    def readWriteOPT(self, mode, reg_address, dataOne, dataTwo):
        """
        Function to write data to a register, store parameters as instance variables, and return them.

        :param mode: Operation mode.
        :param reg_address: Register address.
        :param dataOne: First piece of data to write.
        :param dataTwo: Second piece of data to write.
        :return: Dictionary of written values.
        """
        self.write_mode = "0b001" #"0x1"
        self.write_reg_address = reg_address
        self.write_dataOne = dataOne
        self.write_dataTwo = dataTwo

        # Implement the write logic here

        # Format the string with the instance variable values
        formatted_string = f"spi read_write spi1 [ {self.write_mode} {self.write_reg_address} {self.write_dataOne} {self.write_dataTwo} ] #OTP"

        return formatted_string

    def readOTP(self,mode,reg_address):
        """
        Function to read data from a register, store the parameter as an instance variable, and return it.

        :param reg_address: Register address to read from.
        :return: Register address read.
        """
        self.read_mode = mode # "0b000" #"0x0"
        self.read_reg_address = reg_address

        self.read_dataOne = "0b00000000"
        self.read_dataTwo = "0b00000000"

        # Implement the read logic here
        formatted_string = f"spi read_write spi1 [ {self.read_mode} {self.read_reg_address} {self.read_dataOne} {self.read_dataTwo} ] #OTP"
        return formatted_string
    

    def initCom(self, comport, baudrate):
        # List of allowed baudrate values
        allowed_baudrates = ['9600', '57600', '115200']

        # Check if the baudrate is in the allowed list
        if str(baudrate) not in allowed_baudrates:
            return "Error" #["Error: Invalid baudrate. Allowed values are 9600, 57600, 115200."]

        # Check if the comport starts with 'COM' and is followed by numbers
        if not (comport.startswith('COM') and comport[3:].isdigit()):
            return ["Error: Invalid comport. Comport should start with 'COM' followed by numbers."]
        if not self.check_serial_port(comport):
            return "Error"
        # Store the values in instance variables
        self.comport = comport
        self.baudrate = baudrate 

        # Placeholder for actual initialization code
        # ...
       # formatted_string = "[" + {self.comport}  {self.baudrate} + "] #COM"
        formatted_string = f" {self.comport} {self.baudrate} #COM"

        return  formatted_string #self.comport, self.baudrate #+"#COM"
    
    def settings(self, asic_prescaler_rate, cpol, cpha, mbsFirst, cs):
        # List of allowed asic_prescaler_rate values
        allowed_rates = ["2", "4", "8", "16", "32", "64", "128", "256"]

        # Check if the asic_prescaler_rate is in the allowed list
        if str(asic_prescaler_rate) not in allowed_rates:
            return f"Error: Invalid asic_prescaler_rate. Allowed values are {', '.join(allowed_rates)}."

        # Store the values in instance variables
        self.asic_prescaler_rate = asic_prescaler_rate
        self.cpol = cpol
        self.cpha = cpha
        self.mbsFirst = mbsFirst
        self.cs = cs

        # Format the string with the instance variable values
        formatted_string = f"spi set_settings {self.asic_prescaler_rate} {self.cpol} {self.cpha} {self.mbsFirst} {self.cs} #setting"

        return formatted_string
    
    # Function to check if the variable is a list and encode if it is
    def encode_if_list(self, command):
        if isinstance(command, list):
            # If it's a list, encode it
            message = command.encode()
            return message
        else:
            # If it's not a list, print an error message
            print("Error: Expected a list, but received a different type.")
            return None


    def check_serial_port(self, port_name):
        """
        Check if a specific serial port is present.

        :param port_name: The name of the serial port to check (e.g., 'COM3' on Windows or '/dev/ttyUSB0' on Linux).
        :return: True if the port is present, False otherwise.
        """
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if port.device == port_name:
                return True
        return False

