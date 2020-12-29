from obd import OBDCommand
from obd.protocols import ECU
from obd.decoders import raw_string
from .decoders import bms_2101, cell_voltages, bms_2105, odometer, vin
from .decoders import vmcu_2101, vmcu_2102, tpms, external_temperature

# flake8: noqa E501

ext_commands = {
    #                                      name                       description                                                                    cmd        bytes decoder               ECU         fast
    'BMS_CAN_HEADER_7E4':      OBDCommand("BMS_CAN_HEADER_7E4",      "Set CAN module ID to 7E4 - BMS - Battery Management System",                   b"ATSH7E4",   0, raw_string,           ECU.UNKNOWN, False),
    'CLU_CAN_HEADER_7C6':      OBDCommand("CLU_CAN_HEADER_7C6",      "Set CAN module ID to 7C6 - CLU - Cluster Module",                              b"ATSH7C6",   0, raw_string,           ECU.UNKNOWN, False),
    'VMCU_CAN_HEADER_7E2':     OBDCommand("VMCU_CAN_HEADER_7E2",     "Set CAN module ID to 7E2 - VMCU",                                              b"ATSH7E2",   0, raw_string,           ECU.UNKNOWN, False),
    'TPMS_CAN_HEADER_7A0':     OBDCommand("TPMS_CAN_HEADER_7A0",     "Set CAN module ID to 7A0 - TPMS - Tire Pressure Management System",            b"ATSH7A0",   0, raw_string,           ECU.UNKNOWN, False),
    'CAN_HEADER_7E6':          OBDCommand("CAN_HEADER_7E6",          "Set CAN module ID to 7E6 - External temp information",                         b"ATSH7E6",   0, raw_string,           ECU.UNKNOWN, False),
    'IGPM_CAN_HEADER_770':     OBDCommand("IGPM_CAN_HEADER_770",     "Set CAN module ID to 770 - IGPM - Intergrated Gateway & Power control Module", b"ATSH770",   0, raw_string,           ECU.UNKNOWN, False),
    'AIR_CON_CAN_HEADER_7B3':  OBDCommand("AIR_CON__CAN_HEADER_7B3", "Set CAN module ID to 7B3 - Air Conditioning",                                  b"ATSH7B3",   0, raw_string,           ECU.UNKNOWN, False),

    'CAN_RECEIVE_ADDRESS_7EC': OBDCommand("CAN_RECEIVE_ADDRESS_7EC", "Set the CAN receive address to 7EC",                                           b"ATCRA7EC",  0, raw_string,           ECU.UNKNOWN, False),
    'CAN_RECEIVE_ADDRESS_7EA': OBDCommand("CAN_RECEIVE_ADDRESS_7EA", "Set the CAN receive address to 7EA",                                           b"ATCRA7EA",  0, raw_string,           ECU.UNKNOWN, False),
    'CAN_RECEIVE_ADDRESS_7A8': OBDCommand("CAN_RECEIVE_ADDRESS_7A8", "Set the CAN receive address to 7A8",                                           b"ATCRA7A8",  0, raw_string,           ECU.UNKNOWN, False),
    'CAN_RECEIVE_ADDRESS_7EE': OBDCommand("CAN_RECEIVE_ADDRESS_7EE", "Set the CAN receive address to 7EE",                                           b"ATCRA7EE",  0, raw_string,           ECU.UNKNOWN, False),

    'CAN_FILTER_7CE':          OBDCommand("CAN_FILTER_7CE",          "Set the CAN filter to 7CE",                                                    b"ATCF7CE",   0, raw_string,           ECU.UNKNOWN, False),

    # length 61
    'BMS_2101':                OBDCommand("BMS_2101",                "Extended command - BMS Battery information",                                   b"2101",      0, bms_2101,             ECU.ALL,     False),
    # length 38
    'BMS_2102':                OBDCommand("BMS_2102",                "Extended command - BMS Battery information",                                   b"2102",      0, cell_voltages,        ECU.ALL,     False),
    # length 38
    'BMS_2103':                OBDCommand("BMS_2103",                "Extended command - BMS Battery information",                                   b"2103",      0, cell_voltages,        ECU.ALL,     False),
    # length 38
    'BMS_2104':                OBDCommand("BMS_2104",                "Extended command - BMS Battery information",                                   b"2104",      0, cell_voltages,        ECU.ALL,     False),
    # length 45
    'BMS_2105':                OBDCommand("BMS_2105",                "Extended command - BMS Battery information",                                   b"2105",      0, bms_2105,             ECU.ALL,     False),

    # length 15
    'CLU_22B002':             OBDCommand("CLU_22B002",               "Extended command - Odometer information",                                      b"22b002",    0, odometer,             ECU.ALL,     False),
    # length 99
    'VMCU_1A80':              OBDCommand("VMCU_1A80",                "Extended command - Vehicle Identification Number",                             b"1A80",      0, vin,                  ECU.ALL,     False),
    # length 22
    'VMCU_2101':              OBDCommand("VMCU_2101",                "Extended command - VMCU information",                                          b"2101",      0, vmcu_2101,            ECU.ALL,     False),
    # Pending to define decoder
    'VMCU_2102':              OBDCommand("VMCU_2102",                "Extended command - Aux battery current information",                           b"2102",      0, vmcu_2102,            ECU.ALL,     False),
    # length 23
    'TPMS_22C00B':            OBDCommand("TPMS_22C00B",              "Extended command - TPMS information",                                          b"22C00B",    0, tpms,                 ECU.ALL,     False),
    # length 25
    'EXT_TEMP_2180':          OBDCommand("EXT_TEMP_2180",            "Extended command - External temperature",                                      b"2180",      0, external_temperature, ECU.ALL,     False),
    # Pending to define decoder
    'IGPM_22BC03':            OBDCommand("IGPM_22BC03",              "Extended command - Head and day lights",                                       b"22BC03",    0, raw_string,           ECU.ALL,     False),
    # Pending to define decoder
    'IGPM_22BC06':            OBDCommand("IGPM_22BC06",              "Extended command - Brake lights",                                              b"22BC06",    0, raw_string,           ECU.ALL,     False),
    # Pending to define decoder
    'AIR_CON 220100':         OBDCommand("AIR_CON 220100",           "Extended command - Indoor / outdoor temperature",                              b"220100",    0, raw_string,           ECU.ALL,     False),
    # Pending to define decoder
    'AIR_CON 220102':         OBDCommand("AIR_CON 220102",           "Extended command - Coolant temperature",                                       b"220102",    0, raw_string,           ECU.ALL,     False)
}
