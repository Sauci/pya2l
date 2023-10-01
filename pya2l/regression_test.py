from .parser import A2lParser as Parser


def test_issue_15():
    a2l_string = """
    /begin PROJECT project_name "project long identifier"
        /begin MODULE first_module_name "first module long identifier"
            /begin MOD_PAR "_default_ModParComment"
                /begin MEMORY_SEGMENT _CALIBRATIONS
                    "calibrations"
                    DATA
                    FLASH
                    INTERN
                    0xe0000
                    0x21c
                    -1 -1 -1 -1 -1
                    /begin IF_DATA XCPplus 0x102
                        /begin SEGMENT
                            0x0 /* segment logical number */
                            0x1 /* number of pages */
                            0x0 /* address extension */
                            0x0 /* compression method */
                            0x0 /* encryption method */
                            /begin CHECKSUM
                                XCP_CRC_16_CITT
                                MAX_BLOCK_SIZE 0x00001000 /* kXcpChecksumBlockSize */
                            /end CHECKSUM
                            /begin PAGE
                                0x0 /* page number */
                                ECU_ACCESS_WITH_XCP_ONLY
                                XCP_READ_ACCESS_WITH_ECU_ONLY
                                XCP_WRITE_ACCESS_WITH_ECU_ONLY
                                INIT_SEGMENT 0x0
                            /end PAGE
                            /begin ADDRESS_MAPPING
                                0xe0000
                                0x40000400
                                0x21c
                            /end ADDRESS_MAPPING
                        /end SEGMENT
                    /end IF_DATA
                /end MEMORY_SEGMENT
                /begin MEMORY_SEGMENT _ECU_CODE0
                    ""
                    CODE
                    FLASH
                    INTERN
                    0x10000
                    0x5d3f0
                    -1 -1 -1 -1 -1
                    /begin IF_DATA XCPplus 0x102
                        /begin SEGMENT
                            0x1 // segment logical number
                            0x1 // number of pages
                            0x0 // address extension
                            0x0 // compression method
                            0x0 // encryption method
                            /begin CHECKSUM
                                XCP_CRC_16_CITT
                                MAX_BLOCK_SIZE 0x00001000       // kXcpChecksumBlockSize
                            /end CHECKSUM
                            /begin PAGE
                                0x0 // page number
                                ECU_ACCESS_DONT_CARE
                                XCP_READ_ACCESS_WITH_ECU_ONLY
                                XCP_WRITE_ACCESS_NOT_ALLOWED
                                INIT_SEGMENT 0x1
                            /end PAGE
                        /end SEGMENT
                    /end IF_DATA
                /end MEMORY_SEGMENT
            /end MOD_PAR

            /begin MOD_COMMON
                ""    /* Comment */
                ALIGNMENT_BYTE 1
                ALIGNMENT_WORD 1
                ALIGNMENT_LONG 1
                ALIGNMENT_FLOAT32_IEEE 1
                ALIGNMENT_FLOAT64_IEEE 1
                BYTE_ORDER MSB_FIRST
                DEPOSIT ABSOLUTE
            /end MOD_COMMON

            /begin IF_DATA XCPplus 0x102

                /begin PAG
                    0x01                          /* MAX_SEGMENTS */
                /end PAG

                /begin XCP_ON_CAN
                    0x0102                             /* XCP on CAN 1.2 */
                    CAN_ID_MASTER      0x7A0
                    CAN_ID_SLAVE       0x7A1
                    BAUDRATE           500000
                    MAX_DLC_REQUIRED
                    MAX_BUS_LOAD       50
                    /begin PROTOCOL_LAYER
                        0x0102                         /* XCP protocol layer 1.2 */
                        0x00190                        /* T1 [ms] */
                        0x00190                        /* T2 [ms] */
                        0x00190                        /* T3 [ms] */
                        0x00190                        /* T4 [ms] */
                        0x00190                        /* T5 [ms] */
                        0x00190                        /* T6 [ms] */
                        0x00C80                        /* T7 [ms] */
                        0x08                           /* MAX_CTO */
                        0x08                           /* MAX_DTO */
                        BYTE_ORDER_MSB_FIRST
                        ADDRESS_GRANULARITY_BYTE
                        /* SEED_AND_KEY_EXTERNAL_FUNCTION     "MyS&K.DLL"*/
                        OPTIONAL_CMD  GET_ID
                        OPTIONAL_CMD  SET_REQUEST
                        OPTIONAL_CMD  GET_SEED
                        OPTIONAL_CMD  UNLOCK
                        OPTIONAL_CMD  SET_MTA
                        OPTIONAL_CMD  UPLOAD
                        OPTIONAL_CMD  SHORT_UPLOAD
                        OPTIONAL_CMD  BUILD_CHECKSUM
                        OPTIONAL_CMD  DOWNLOAD
                        OPTIONAL_CMD  DOWNLOAD_NEXT
                        OPTIONAL_CMD  COPY_CAL_PAGE
                        OPTIONAL_CMD  FREE_DAQ
                        OPTIONAL_CMD  ALLOC_DAQ
                        OPTIONAL_CMD  ALLOC_ODT
                        OPTIONAL_CMD  ALLOC_ODT_ENTRY
                        OPTIONAL_CMD  CLEAR_DAQ_LIST
                        OPTIONAL_CMD  SET_DAQ_PTR
                        OPTIONAL_CMD  WRITE_DAQ
                        OPTIONAL_CMD  SET_DAQ_LIST_MODE
                        OPTIONAL_CMD  START_STOP_DAQ_LIST
                        OPTIONAL_CMD  START_STOP_SYNCH
                    /end PROTOCOL_LAYER
                    /begin DAQ
                        DYNAMIC                                /* DAQ_CONFIG_TYPE */
                        0x00                                  /* MAX_DAQ */
                        0x02                                  /* MAX_EVENT_CHANNEL */
                        0x00                                  /* MIN_DAQ */
                        OPTIMISATION_TYPE_DEFAULT
                        ADDRESS_EXTENSION_FREE
                        IDENTIFICATION_FIELD_TYPE_ABSOLUTE
                        GRANULARITY_ODT_ENTRY_SIZE_DAQ_BYTE
                        0x04                                 /* MAX_ODT_ENTRY_SIZE_DAQ */
                        NO_OVERLOAD_INDICATION
                        PRESCALER_SUPPORTED
                        RESUME_SUPPORTED
                        /begin DAQ_MEMORY_CONSUMPTION
                            1328  /* 2*24 + 2*16*8 + 2*16*4*8  ulong; "DAQ_MEMORY_LIMIT"  : in Elements[AG] */
                            24   /* uint;  "DAQ_SIZE"    : Anzahl Elements[AG] pro DAQ-Liste */
                            8   /* uint;  "ODT_SIZE"    : Anzahl Elements[AG] pro ODT */
                            8   /* uint;  "ODT_ENTRY_SIZE"   : Anzahl Elements[AG] pro ODT_Entry */
                            0   /* uint;  "ODT_DAQ_BUFFER_ELEMENT_SIZE" : Anzahl Payload-Elements[AG]*Faktor = sizeof(Sendepuffer)[AG] */
                            0   /* uint;  "ODT_STIM_BUFFER_ELEMENT_SIZE": Anzahl Payload-Elements[AG]*Faktor = sizeof(Empfangspuffer)[AG] */
                        /end DAQ_MEMORY_CONSUMPTION
                        /begin EVENT
                            "DAQ_10"                 /* name */
                            "10ms"                  /* short name */
                            0x0000                       /* EVENT_CHANNEL_NUMBER */
                            DAQ
                            0x01                         /* MAX_DAQ_LIST */
                            0x0A                         /* TIME_CYCLE */
                            0x06                         /* TIME_UNIT */
                            0x00                         /* PRIORITY */
                        /end EVENT
                        /begin EVENT
                            "DAQ_100"                /* name */
                            "100ms"                     /* short name */
                            0x0001                       /* EVENT_CHANNEL_NUMBER */
                            DAQ
                            0x02                         /* MAX_DAQ_LIST */
                            0x64                         /* TIME_CYCLE */
                            0x06                         /* TIME_UNIT */
                            0x00                         /* PRIORITY */
                        /end EVENT
                    /end DAQ
                    TRANSPORT_LAYER_INSTANCE "VEHICLE CAN 500K"
                /end XCP_ON_CAN
                /begin XCP_ON_TCP_IP
                    0x0102                             /* XCP on TCP_IP 1.2 */
                    0x5555                             /* PORT           */
                    ADDRESS "127.0.0.1"                /* ADDRESS   */
                    /begin PROTOCOL_LAYER
                        0x0102                         /* XCP protocol layer 1.2 */
                        0x00190                        /* T1 [ms] */
                        0x00190                        /* T2 [ms] */
                        0x00190                        /* T3 [ms] */
                        0x00190                        /* T4 [ms] */
                        0x00190                        /* T5 [ms] */
                        0x00190                        /* T6 [ms] */
                        0x00C80                        /* T7 [ms] */
                        0xff                           /* MAX_CTO */
                        0x400                          /* MAX_DTO */
                        BYTE_ORDER_MSB_FIRST
                        ADDRESS_GRANULARITY_BYTE
                        /* SEED_AND_KEY_EXTERNAL_FUNCTION     "MyS&K.DLL"*/
                        OPTIONAL_CMD  GET_ID
                        OPTIONAL_CMD  SET_REQUEST
                        OPTIONAL_CMD  GET_SEED
                        OPTIONAL_CMD  UNLOCK
                        OPTIONAL_CMD  SET_MTA
                        OPTIONAL_CMD  UPLOAD
                        OPTIONAL_CMD  SHORT_UPLOAD
                        OPTIONAL_CMD  BUILD_CHECKSUM
                        OPTIONAL_CMD  DOWNLOAD
                        OPTIONAL_CMD  DOWNLOAD_NEXT
                        OPTIONAL_CMD  COPY_CAL_PAGE
                        OPTIONAL_CMD  FREE_DAQ
                        OPTIONAL_CMD  ALLOC_DAQ
                        OPTIONAL_CMD  ALLOC_ODT
                        OPTIONAL_CMD  ALLOC_ODT_ENTRY
                        OPTIONAL_CMD  CLEAR_DAQ_LIST
                        OPTIONAL_CMD  SET_DAQ_PTR
                        OPTIONAL_CMD  WRITE_DAQ
                        OPTIONAL_CMD  SET_DAQ_LIST_MODE
                        OPTIONAL_CMD  START_STOP_DAQ_LIST
                        OPTIONAL_CMD  START_STOP_SYNCH
                        COMMUNICATION_MODE_SUPPORTED  BLOCK MASTER 0xff 0x0
                    /end PROTOCOL_LAYER
                    /begin DAQ
                        DYNAMIC                         /* DAQ_CONFIG_TYPE */
                        0x0100                          /* MAX_DAQ */
                        0x0100                          /* MAX_EVENT_CHANNEL */
                        0x00                            /* MIN_DAQ */
                        OPTIMISATION_TYPE_DEFAULT
                        ADDRESS_EXTENSION_FREE
                        IDENTIFICATION_FIELD_TYPE_RELATIVE_WORD_ALIGNED
                        GRANULARITY_ODT_ENTRY_SIZE_DAQ_BYTE
                        0x04                     /* MAX_ODT_ENTRY_SIZE_DAQ */
                        NO_OVERLOAD_INDICATION
                        PRESCALER_SUPPORTED
                        RESUME_SUPPORTED
                        /begin TIMESTAMP_SUPPORTED
                            0x01                /* TIMESTAMP_TICKS */
                            SIZE_DWORD
                            UNIT_1US
                            TIMESTAMP_FIXED
                        /end TIMESTAMP_SUPPORTED
                        /begin EVENT
                            "DAQ_10"                     /* name */
                            "10ms"                       /* short name */
                            0x0001                       /* EVENT_CHANNEL_NUMBER */
                            DAQ
                            0x02                         /* MAX_DAQ_LIST */
                            0x0a                         /* TIME_CYCLE */
                            0x06                         /* TIME_UNIT */
                            0x00                         /* PRIORITY */
                        /end EVENT
                        /begin EVENT
                            "DAQ_100"                    /* name */
                            "100ms"                      /* short name */
                            0x0002                       /* EVENT_CHANNEL_NUMBER */
                            DAQ
                            0x02                         /* MAX_DAQ_LIST */
                            100                          /* TIME_CYCLE */
                            0x06                         /* TIME_UNIT */
                            0x00                         /* PRIORITY */
                        /end EVENT
                        /begin EVENT
                            "DAQ_0"                      /* name */
                            "0ms"                        /* short name */
                            0x0003                       /* EVENT_CHANNEL_NUMBER */
                            DAQ
                            0x02                         /* MAX_DAQ_LIST */
                            0x00                         /* TIME_CYCLE */
                            0x00                         /* TIME_UNIT */
                            0x00                         /* PRIORITY */
                        /end EVENT
                        /begin EVENT
                            "DAQ_1"                      /* name */
                            "1ms"                        /* short name */
                            0x0000                       /* EVENT_CHANNEL_NUMBER */
                            DAQ
                            0x02                         /* MAX_DAQ_LIST */
                            0x01                         /* TIME_CYCLE */
                            0x06                         /* TIME_UNIT */
                            0x00                         /* PRIORITY */
                        /end EVENT
                    /end DAQ
                    TRANSPORT_LAYER_INSTANCE "JTAG-XMC"
                /end XCP_ON_TCP_IP

            /end IF_DATA
        /end MODULE
    /end PROJECT
    """

    with Parser() as p:
        ast = p.tree_from_a2l(a2l_string.encode())
        assert ast.PROJECT.MODULE[0].MOD_PAR.MEMORY_SEGMENT[0].IF_DATA[0].Name.Value == 'XCPplus'


def test_issue_17():
    a2l_string = """
    /begin PROJECT project_name "example project"
        /begin MODULE first_module "first module long identifier"
            /begin CHARACTERISTIC SFB_R_FFO_DE.Properties.1.Qly "" VALUE 36453 _UBYTE 0 NO_COMPU_METHOD 0 255
                /begin ANNOTATION
                    /begin ANNOTATION_TEXT
                        "Factor 1.0"
                        "Offset 0"
                    /end ANNOTATION_TEXT
                    ANNOTATION_LABEL "CalInPatcher Additional Attributes"
                /end ANNOTATION
                SYMBOL_LINK "SFB_R_FFO_DE.Properties.1.Qly" 0
            /end CHARACTERISTIC
        /end MODULE
    /end PROJECT"""

    with Parser() as p:
        ast = p.tree_from_a2l(a2l_string.encode())
        assert ast.PROJECT.MODULE[0].CHARACTERISTIC[0].Name.Value == 'SFB_R_FFO_DE.Properties.1.Qly'
        assert ast.PROJECT.MODULE[0].CHARACTERISTIC[0].SYMBOL_LINK.SymbolName.Value == 'SFB_R_FFO_DE.Properties.1.Qly'
        assert ast.PROJECT.MODULE[0].CHARACTERISTIC[0].SYMBOL_LINK.Offset.Value == 0
