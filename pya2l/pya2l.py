"""
@project: pya2l
@file: pya2l.py
@author: Guillaume Sottas
@date: 20.03.2018
"""

from grammar import A2lParser


class PyA2l(A2lParser):
    def __init__(self, string):
        super(PyA2l, self).__init__(string)


if __name__ == '__main__':
    parser = PyA2l(r"""
    ASAP2_VERSION 1 61
    A2ML_VERSION 2 36
    /begin PROJECT ASAP2_Example ""
        /begin HEADER "ASAP2 Example File"
            VERSION "V1.61"
            PROJECT_NO MCD_P12_08
        /end HEADER
        /begin MODULE Example ""
            /begin IF_DATA module_if_datas
            /begin CHECKSUM "crc16.dll" /end CHECKSUM
            /begin SEED_KEY "access.dll" "access.dll" "access.dll" /end SEED_KEY
            /begin RASTER "Segment synchronous cylinder" "CYL1" 1 103 1 /end RASTER
            /begin EVENT_GROUP "group of events" "G1" 2 5 8 9 /end EVENT_GROUP
            /end IF_DATA
            /begin A2ML
                block "IF_DATA" taggedunion if_data {


/*  ==============================================================================================  */
/*                                                                                                  */
/*  ASAM XCP AML                                                                                    */
/*                                                                                                  */
/*  ==============================================================================================  */

        "XCP" struct {
          taggedstruct {
            block "PROTOCOL_LAYER" struct {
              uint;
              uint;
              uint;
              uint;
              uint;
              uint;
              uint;
              uint;
              uchar;
              uint;
              enum {
                "BYTE_ORDER_MSB_LAST" = 0,
                "BYTE_ORDER_MSB_FIRST" = 1
              };
              enum {
                "ADDRESS_GRANULARITY_BYTE" = 1,
                "ADDRESS_GRANULARITY_WORD" = 2,
                "ADDRESS_GRANULARITY_DWORD" = 4
              };
              taggedstruct {
                ("OPTIONAL_CMD" enum {
                  "GET_COMM_MODE_INFO" = 251,
                  "GET_ID" = 250,
                  "SET_REQUEST" = 249,
                  "GET_SEED" = 248,
                  "UNLOCK" = 247,
                  "SET_MTA" = 246,
                  "UPLOAD" = 245,
                  "SHORT_UPLOAD" = 244,
                  "BUILD_CHECKSUM" = 243,
                  "TRANSPORT_LAYER_CMD" = 242,
                  "USER_CMD" = 241,
                  "DOWNLOAD" = 240,
                  "DOWNLOAD_NEXT" = 239,
                  "DOWNLOAD_MAX" = 238,
                  "SHORT_DOWNLOAD" = 237,
                  "MODIFY_BITS" = 236,
                  "SET_CAL_PAGE" = 235,
                  "GET_CAL_PAGE" = 234,
                  "GET_PAG_PROCESSOR_INFO" = 233,
                  "GET_SEGMENT_INFO" = 232,
                  "GET_PAGE_INFO" = 231,
                  "SET_SEGMENT_MODE" = 230,
                  "GET_SEGMENT_MODE" = 229,
                  "COPY_CAL_PAGE" = 228,
                  "CLEAR_DAQ_LIST" = 227,
                  "SET_DAQ_PTR" = 226,
                  "WRITE_DAQ" = 225,
                  "SET_DAQ_LIST_MODE" = 224,
                  "GET_DAQ_LIST_MODE" = 223,
                  "START_STOP_DAQ_LIST" = 222,
                  "START_STOP_SYNCH" = 221,
                  "GET_DAQ_CLOCK" = 220,
                  "READ_DAQ" = 219,
                  "GET_DAQ_PROCESSOR_INFO" = 218,
                  "GET_DAQ_RESOLUTION_INFO" = 217,
                  "GET_DAQ_LIST_INFO" = 216,
                  "GET_DAQ_EVENT_INFO" = 215,
                  "FREE_DAQ" = 214,
                  "ALLOC_DAQ" = 213,
                  "ALLOC_ODT" = 212,
                  "ALLOC_ODT_ENTRY" = 211,
                  "PROGRAM_START" = 210,
                  "PROGRAM_CLEAR" = 209,
                  "PROGRAM" = 208,
                  "PROGRAM_RESET" = 207,
                  "GET_PGM_PROCESSOR_INFO" = 206,
                  "GET_SECTOR_INFO" = 205,
                  "PROGRAM_PREPARE" = 204,
                  "PROGRAM_FORMAT" = 203,
                  "PROGRAM_NEXT" = 202,
                  "PROGRAM_MAX" = 201,
                  "PROGRAM_VERIFY" = 200
                })*;
                "COMMUNICATION_MODE_SUPPORTED" taggedunion {
                  "BLOCK" taggedstruct {
                    "SLAVE" ;
                    "MASTER" struct {
                      uchar;
                      uchar;
                    };
                  };
                  "INTERLEAVED" uchar;
                };
                "SEED_AND_KEY_EXTERNAL_FUNCTION" char[256];
              };
            };
            block "SEGMENT" struct {
              uchar;
              uchar;
              uchar;
              uchar;
              uchar;
              taggedstruct {
                block "CHECKSUM" struct {
                  enum {
                    "XCP_ADD_11" = 1,
                    "XCP_ADD_12" = 2,
                    "XCP_ADD_14" = 3,
                    "XCP_ADD_22" = 4,
                    "XCP_ADD_24" = 5,
                    "XCP_ADD_44" = 6,
                    "XCP_CRC_16" = 7,
                    "XCP_CRC_16_CITT" = 8,
                    "XCP_CRC_32" = 9,
                    "XCP_USER_DEFINED" = 255
                  };
                  taggedstruct {
                    "MAX_BLOCK_SIZE" ulong;
                    "EXTERNAL_FUNCTION" char[256];
                  };
                };
                (block "PAGE" struct {
                  uchar;
                  enum {
                    "ECU_ACCESS_NOT_ALLOWED" = 0,
                    "ECU_ACCESS_WITHOUT_XCP_ONLY" = 1,
                    "ECU_ACCESS_WITH_XCP_ONLY" = 2,
                    "ECU_ACCESS_DONT_CARE" = 3
                  };
                  enum {
                    "XCP_READ_ACCESS_NOT_ALLOWED" = 0,
                    "XCP_READ_ACCESS_WITHOUT_ECU_ONLY" = 1,
                    "XCP_READ_ACCESS_WITH_ECU_ONLY" = 2,
                    "XCP_READ_ACCESS_DONT_CARE" = 3
                  };
                  enum {
                    "XCP_WRITE_ACCESS_NOT_ALLOWED" = 0,
                    "XCP_WRITE_ACCESS_WITHOUT_ECU_ONLY" = 1,
                    "XCP_WRITE_ACCESS_WITH_ECU_ONLY" = 2,
                    "XCP_WRITE_ACCESS_DONT_CARE" = 3
                  };
                  taggedstruct {
                    "INIT_SEGMENT" uchar;
                  };
                })*;
                (block "ADDRESS_MAPPING" struct {
                  ulong;
                  ulong;
                  ulong;
                })*;
                "PGM_VERIFY" ulong;
              };
            };
            block "DAQ" struct {
              enum {
                "STATIC" = 0,
                "DYNAMIC" = 1
              };
              uint;
              uint;
              uchar;
              enum {
                "OPTIMISATION_TYPE_DEFAULT" = 0,
                "OPTIMISATION_TYPE_ODT_TYPE_16" = 1,
                "OPTIMISATION_TYPE_ODT_TYPE_32" = 2,
                "OPTIMISATION_TYPE_ODT_TYPE_64" = 3,
                "OPTIMISATION_TYPE_ODT_TYPE_ALIGNMENT" = 4,
                "OPTIMISATION_TYPE_MAX_ENTRY_SIZE" = 5
              };
              enum {
                "ADDRESS_EXTENSION_FREE" = 0,
                "ADDRESS_EXTENSION_ODT" = 1,
                "ADDRESS_EXTENSION_DAQ" = 3
              };
              enum {
                "IDENTIFICATION_FIELD_TYPE_ABSOLUTE" = 0,
                "IDENTIFICATION_FIELD_TYPE_RELATIVE_BYTE" = 1,
                "IDENTIFICATION_FIELD_TYPE_RELATIVE_WORD" = 2,
                "IDENTIFICATION_FIELD_TYPE_RELATIVE_WORD_ALIGNED" = 3
              };
              enum {
                "GRANULARITY_ODT_ENTRY_SIZE_DAQ_BYTE" = 1,
                "GRANULARITY_ODT_ENTRY_SIZE_DAQ_WORD" = 2,
                "GRANULARITY_ODT_ENTRY_SIZE_DAQ_DWORD" = 4,
                "GRANULARITY_ODT_ENTRY_SIZE_DAQ_DLONG" = 8
              };
              uchar;
              enum {
                "NO_OVERLOAD_INDICATION" = 0,
                "OVERLOAD_INDICATION_PID" = 1,
                "OVERLOAD_INDICATION_EVENT" = 2
              };
              taggedstruct {
                "PRESCALER_SUPPORTED" ;
                "RESUME_SUPPORTED" ;
                block "STIM" struct {
                  enum {
                    "GRANULARITY_ODT_ENTRY_SIZE_STIM_BYTE" = 1,
                    "GRANULARITY_ODT_ENTRY_SIZE_STIM_WORD" = 2,
                    "GRANULARITY_ODT_ENTRY_SIZE_STIM_DWORD" = 4,
                    "GRANULARITY_ODT_ENTRY_SIZE_STIM_DLONG" = 8
                  };
                  uchar;
                  taggedstruct {
                    "BIT_STIM_SUPPORTED" ;
                  };
                };
                block "TIMESTAMP_SUPPORTED" struct {
                  uint;
                  enum {
                    "NO_TIME_STAMP" = 0,
                    "SIZE_BYTE" = 1,
                    "SIZE_WORD" = 2,
                    "SIZE_DWORD" = 4
                  };
                  enum {
                    "UNIT_1NS" = 0,
                    "UNIT_10NS" = 1,
                    "UNIT_100NS" = 2,
                    "UNIT_1US" = 3,
                    "UNIT_10US" = 4,
                    "UNIT_100US" = 5,
                    "UNIT_1MS" = 6,
                    "UNIT_10MS" = 7,
                    "UNIT_100MS" = 8,
                    "UNIT_1S" = 9
                  };
                  taggedstruct {
                    "TIMESTAMP_FIXED" ;
                  };
                };
                "PID_OFF_SUPPORTED" ;
                (block "DAQ_LIST" struct {
                  uint;
                  taggedstruct {
                    "DAQ_LIST_TYPE" enum {
                      "DAQ" = 1,
                      "STIM" = 2,
                      "DAQ_STIM" = 3
                    };
                    "MAX_ODT" uchar;
                    "MAX_ODT_ENTRIES" uchar;
                    "FIRST_PID" uchar;
                    "EVENT_FIXED" uint;
                    block "PREDEFINED" taggedstruct {
                      (block "ODT" struct {
                        uchar;
                        taggedstruct {
                          ("ODT_ENTRY" struct {
                            uchar;
                            ulong;
                            uchar;
                            uchar;
                            uchar;
                          })*;
                        };
                      })*;
                    };
                  };
                })*;
                (block "EVENT" struct {
                  char[101];
                  char[9];
                  uint;
                  enum {
                    "DAQ" = 1,
                    "STIM" = 2,
                    "DAQ_STIM" = 3
                  };
                  uchar;
                  uchar;
                  uchar;
                  uchar;
                })*;
              };
            };
            block "PAG" struct {
              uchar;
              taggedstruct {
                "FREEZE_SUPPORTED" ;
              };
            };
            block "PGM" struct {
              enum {
                "PGM_MODE_ABSOLUTE" = 1,
                "PGM_MODE_FUNCTIONAL" = 2,
                "PGM_MODE_ABSOLUTE_AND_FUNCTIONAL" = 3
              };
              uchar;
              uchar;
              taggedstruct {
                (block "SECTOR" struct {
                  char[101];
                  uchar;
                  ulong;
                  ulong;
                  uchar;
                  uchar;
                  uchar;
                })*;
                "COMMUNICATION_MODE_SUPPORTED" taggedunion {
                  "BLOCK" taggedstruct {
                    "SLAVE" ;
                    "MASTER" struct {
                      uchar;
                      uchar;
                    };
                  };
                  "INTERLEAVED" uchar;
                };
              };
            };
            block "DAQ_EVENT" taggedunion {
              "FIXED_EVENT_LIST" taggedstruct {
                ("EVENT" uint)*;
              };
              "VARIABLE" taggedstruct {
                block "AVAILABLE_EVENT_LIST" taggedstruct {
                  ("EVENT" uint)*;
                };
                block "DEFAULT_EVENT_LIST" taggedstruct {
                  ("EVENT" uint)*;
                };
              };
            };
            block "XCP_ON_CAN" struct {
              uint;
              taggedstruct {
                "CAN_ID_BROADCAST" ulong;
                "CAN_ID_MASTER" ulong;
                "CAN_ID_SLAVE" ulong;
                "BAUDRATE" ulong;
                "SAMPLE_POINT" uchar;
                "SAMPLE_RATE" enum {
                  "SINGLE" = 1,
                  "TRIPLE" = 3
                };
                "BTL_CYCLES" uchar;
                "SJW" uchar;
                "SYNC_EDGE" enum {
                  "SINGLE" = 1,
                  "DUAL" = 2
                };
                "MAX_DLC_REQUIRED" ;
                (block "DAQ_LIST_CAN_ID" struct {
                  uint;
                  taggedstruct {
                    "VARIABLE" ;
                    "FIXED" ulong;
                  };
                })*;
                block "PROTOCOL_LAYER" struct {
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uchar;
                  uint;
                  enum {
                    "BYTE_ORDER_MSB_LAST" = 0,
                    "BYTE_ORDER_MSB_FIRST" = 1
                  };
                  enum {
                    "ADDRESS_GRANULARITY_BYTE" = 1,
                    "ADDRESS_GRANULARITY_WORD" = 2,
                    "ADDRESS_GRANULARITY_DWORD" = 4
                  };
                  taggedstruct {
                    ("OPTIONAL_CMD" enum {
                      "GET_COMM_MODE_INFO" = 251,
                      "GET_ID" = 250,
                      "SET_REQUEST" = 249,
                      "GET_SEED" = 248,
                      "UNLOCK" = 247,
                      "SET_MTA" = 246,
                      "UPLOAD" = 245,
                      "SHORT_UPLOAD" = 244,
                      "BUILD_CHECKSUM" = 243,
                      "TRANSPORT_LAYER_CMD" = 242,
                      "USER_CMD" = 241,
                      "DOWNLOAD" = 240,
                      "DOWNLOAD_NEXT" = 239,
                      "DOWNLOAD_MAX" = 238,
                      "SHORT_DOWNLOAD" = 237,
                      "MODIFY_BITS" = 236,
                      "SET_CAL_PAGE" = 235,
                      "GET_CAL_PAGE" = 234,
                      "GET_PAG_PROCESSOR_INFO" = 233,
                      "GET_SEGMENT_INFO" = 232,
                      "GET_PAGE_INFO" = 231,
                      "SET_SEGMENT_MODE" = 230,
                      "GET_SEGMENT_MODE" = 229,
                      "COPY_CAL_PAGE" = 228,
                      "CLEAR_DAQ_LIST" = 227,
                      "SET_DAQ_PTR" = 226,
                      "WRITE_DAQ" = 225,
                      "SET_DAQ_LIST_MODE" = 224,
                      "GET_DAQ_LIST_MODE" = 223,
                      "START_STOP_DAQ_LIST" = 222,
                      "START_STOP_SYNCH" = 221,
                      "GET_DAQ_CLOCK" = 220,
                      "READ_DAQ" = 219,
                      "GET_DAQ_PROCESSOR_INFO" = 218,
                      "GET_DAQ_RESOLUTION_INFO" = 217,
                      "GET_DAQ_LIST_INFO" = 216,
                      "GET_DAQ_EVENT_INFO" = 215,
                      "FREE_DAQ" = 214,
                      "ALLOC_DAQ" = 213,
                      "ALLOC_ODT" = 212,
                      "ALLOC_ODT_ENTRY" = 211,
                      "PROGRAM_START" = 210,
                      "PROGRAM_CLEAR" = 209,
                      "PROGRAM" = 208,
                      "PROGRAM_RESET" = 207,
                      "GET_PGM_PROCESSOR_INFO" = 206,
                      "GET_SECTOR_INFO" = 205,
                      "PROGRAM_PREPARE" = 204,
                      "PROGRAM_FORMAT" = 203,
                      "PROGRAM_NEXT" = 202,
                      "PROGRAM_MAX" = 201,
                      "PROGRAM_VERIFY" = 200
                    })*;
                    "COMMUNICATION_MODE_SUPPORTED" taggedunion {
                      "BLOCK" taggedstruct {
                        "SLAVE" ;
                        "MASTER" struct {
                          uchar;
                          uchar;
                        };
                      };
                      "INTERLEAVED" uchar;
                    };
                    "SEED_AND_KEY_EXTERNAL_FUNCTION" char[256];
                  };
                };
                block "SEGMENT" struct {
                  uchar;
                  uchar;
                  uchar;
                  uchar;
                  uchar;
                  taggedstruct {
                    block "CHECKSUM" struct {
                      enum {
                        "XCP_ADD_11" = 1,
                        "XCP_ADD_12" = 2,
                        "XCP_ADD_14" = 3,
                        "XCP_ADD_22" = 4,
                        "XCP_ADD_24" = 5,
                        "XCP_ADD_44" = 6,
                        "XCP_CRC_16" = 7,
                        "XCP_CRC_16_CITT" = 8,
                        "XCP_CRC_32" = 9,
                        "XCP_USER_DEFINED" = 255
                      };
                      taggedstruct {
                        "MAX_BLOCK_SIZE" ulong;
                        "EXTERNAL_FUNCTION" char[256];
                      };
                    };
                    (block "PAGE" struct {
                      uchar;
                      enum {
                        "ECU_ACCESS_NOT_ALLOWED" = 0,
                        "ECU_ACCESS_WITHOUT_XCP_ONLY" = 1,
                        "ECU_ACCESS_WITH_XCP_ONLY" = 2,
                        "ECU_ACCESS_DONT_CARE" = 3
                      };
                      enum {
                        "XCP_READ_ACCESS_NOT_ALLOWED" = 0,
                        "XCP_READ_ACCESS_WITHOUT_ECU_ONLY" = 1,
                        "XCP_READ_ACCESS_WITH_ECU_ONLY" = 2,
                        "XCP_READ_ACCESS_DONT_CARE" = 3
                      };
                      enum {
                        "XCP_WRITE_ACCESS_NOT_ALLOWED" = 0,
                        "XCP_WRITE_ACCESS_WITHOUT_ECU_ONLY" = 1,
                        "XCP_WRITE_ACCESS_WITH_ECU_ONLY" = 2,
                        "XCP_WRITE_ACCESS_DONT_CARE" = 3
                      };
                      taggedstruct {
                        "INIT_SEGMENT" uchar;
                      };
                    })*;
                    (block "ADDRESS_MAPPING" struct {
                      ulong;
                      ulong;
                      ulong;
                    })*;
                    "PGM_VERIFY" ulong;
                  };
                };
                block "DAQ" struct {
                  enum {
                    "STATIC" = 0,
                    "DYNAMIC" = 1
                  };
                  uint;
                  uint;
                  uchar;
                  enum {
                    "OPTIMISATION_TYPE_DEFAULT" = 0,
                    "OPTIMISATION_TYPE_ODT_TYPE_16" = 1,
                    "OPTIMISATION_TYPE_ODT_TYPE_32" = 2,
                    "OPTIMISATION_TYPE_ODT_TYPE_64" = 3,
                    "OPTIMISATION_TYPE_ODT_TYPE_ALIGNMENT" = 4,
                    "OPTIMISATION_TYPE_MAX_ENTRY_SIZE" = 5
                  };
                  enum {
                    "ADDRESS_EXTENSION_FREE" = 0,
                    "ADDRESS_EXTENSION_ODT" = 1,
                    "ADDRESS_EXTENSION_DAQ" = 3
                  };
                  enum {
                    "IDENTIFICATION_FIELD_TYPE_ABSOLUTE" = 0,
                    "IDENTIFICATION_FIELD_TYPE_RELATIVE_BYTE" = 1,
                    "IDENTIFICATION_FIELD_TYPE_RELATIVE_WORD" = 2,
                    "IDENTIFICATION_FIELD_TYPE_RELATIVE_WORD_ALIGNED" = 3
                  };
                  enum {
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_BYTE" = 1,
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_WORD" = 2,
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_DWORD" = 4,
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_DLONG" = 8
                  };
                  uchar;
                  enum {
                    "NO_OVERLOAD_INDICATION" = 0,
                    "OVERLOAD_INDICATION_PID" = 1,
                    "OVERLOAD_INDICATION_EVENT" = 2
                  };
                  taggedstruct {
                    "PRESCALER_SUPPORTED" ;
                    "RESUME_SUPPORTED" ;
                    block "STIM" struct {
                      enum {
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_BYTE" = 1,
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_WORD" = 2,
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_DWORD" = 4,
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_DLONG" = 8
                      };
                      uchar;
                      taggedstruct {
                        "BIT_STIM_SUPPORTED" ;
                      };
                    };
                    block "TIMESTAMP_SUPPORTED" struct {
                      uint;
                      enum {
                        "NO_TIME_STAMP" = 0,
                        "SIZE_BYTE" = 1,
                        "SIZE_WORD" = 2,
                        "SIZE_DWORD" = 4
                      };
                      enum {
                        "UNIT_1NS" = 0,
                        "UNIT_10NS" = 1,
                        "UNIT_100NS" = 2,
                        "UNIT_1US" = 3,
                        "UNIT_10US" = 4,
                        "UNIT_100US" = 5,
                        "UNIT_1MS" = 6,
                        "UNIT_10MS" = 7,
                        "UNIT_100MS" = 8,
                        "UNIT_1S" = 9
                      };
                      taggedstruct {
                        "TIMESTAMP_FIXED" ;
                      };
                    };
                    "PID_OFF_SUPPORTED" ;
                    (block "DAQ_LIST" struct {
                      uint;
                      taggedstruct {
                        "DAQ_LIST_TYPE" enum {
                          "DAQ" = 1,
                          "STIM" = 2,
                          "DAQ_STIM" = 3
                        };
                        "MAX_ODT" uchar;
                        "MAX_ODT_ENTRIES" uchar;
                        "FIRST_PID" uchar;
                        "EVENT_FIXED" uint;
                        block "PREDEFINED" taggedstruct {
                          (block "ODT" struct {
                            uchar;
                            taggedstruct {
                              ("ODT_ENTRY" struct {
                                uchar;
                                ulong;
                                uchar;
                                uchar;
                                uchar;
                              })*;
                            };
                          })*;
                        };
                      };
                    })*;
                    (block "EVENT" struct {
                      char[101];
                      char[9];
                      uint;
                      enum {
                        "DAQ" = 1,
                        "STIM" = 2,
                        "DAQ_STIM" = 3
                      };
                      uchar;
                      uchar;
                      uchar;
                      uchar;
                    })*;
                  };
                };
                block "PAG" struct {
                  uchar;
                  taggedstruct {
                    "FREEZE_SUPPORTED" ;
                  };
                };
                block "PGM" struct {
                  enum {
                    "PGM_MODE_ABSOLUTE" = 1,
                    "PGM_MODE_FUNCTIONAL" = 2,
                    "PGM_MODE_ABSOLUTE_AND_FUNCTIONAL" = 3
                  };
                  uchar;
                  uchar;
                  taggedstruct {
                    (block "SECTOR" struct {
                      char[101];
                      uchar;
                      ulong;
                      ulong;
                      uchar;
                      uchar;
                      uchar;
                    })*;
                    "COMMUNICATION_MODE_SUPPORTED" taggedunion {
                      "BLOCK" taggedstruct {
                        "SLAVE" ;
                        "MASTER" struct {
                          uchar;
                          uchar;
                        };
                      };
                      "INTERLEAVED" uchar;
                    };
                  };
                };
                block "DAQ_EVENT" taggedunion {
                  "FIXED_EVENT_LIST" taggedstruct {
                    ("EVENT" uint)*;
                  };
                  "VARIABLE" taggedstruct {
                    block "AVAILABLE_EVENT_LIST" taggedstruct {
                      ("EVENT" uint)*;
                    };
                    block "DEFAULT_EVENT_LIST" taggedstruct {
                      ("EVENT" uint)*;
                    };
                  };
                };
              };
            };
            block "XCP_ON_SxI" struct {
              uint;
              ulong;
              taggedstruct {
                "ASYNCH_FULL_DUPLEX_MODE" struct {
                  enum {
                    "PARITY_NONE" = 0,
                    "PARITY_ODD" = 1,
                    "PARITY_EVEN" = 2
                  };
                  enum {
                    "ONE_STOP_BIT" = 1,
                    "TWO_STOP_BITS" = 2
                  };
                };
                "SYNCH_FULL_DUPLEX_MODE_BYTE" ;
                "SYNCH_FULL_DUPLEX_MODE_WORD" ;
                "SYNCH_FULL_DUPLEX_MODE_DWORD" ;
                "SYNCH_MASTER_SLAVE_MODE_BYTE" ;
                "SYNCH_MASTER_SLAVE_MODE_WORD" ;
                "SYNCH_MASTER_SLAVE_MODE_DWORD" ;
              };
              enum {
                "HEADER_LEN_BYTE" = 0,
                "HEADER_LEN_CTR_BYTE" = 1,
                "HEADER_LEN_WORD" = 2,
                "HEADER_LEN_CTR_WORD" = 3
              };
              enum {
                "NO_CHECKSUM" = 0,
                "CHECKSUM_BYTE" = 1,
                "CHECKSUM_WORD" = 2
              };
              taggedstruct {
                block "PROTOCOL_LAYER" struct {
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uchar;
                  uint;
                  enum {
                    "BYTE_ORDER_MSB_LAST" = 0,
                    "BYTE_ORDER_MSB_FIRST" = 1
                  };
                  enum {
                    "ADDRESS_GRANULARITY_BYTE" = 1,
                    "ADDRESS_GRANULARITY_WORD" = 2,
                    "ADDRESS_GRANULARITY_DWORD" = 4
                  };
                  taggedstruct {
                    ("OPTIONAL_CMD" enum {
                      "GET_COMM_MODE_INFO" = 251,
                      "GET_ID" = 250,
                      "SET_REQUEST" = 249,
                      "GET_SEED" = 248,
                      "UNLOCK" = 247,
                      "SET_MTA" = 246,
                      "UPLOAD" = 245,
                      "SHORT_UPLOAD" = 244,
                      "BUILD_CHECKSUM" = 243,
                      "TRANSPORT_LAYER_CMD" = 242,
                      "USER_CMD" = 241,
                      "DOWNLOAD" = 240,
                      "DOWNLOAD_NEXT" = 239,
                      "DOWNLOAD_MAX" = 238,
                      "SHORT_DOWNLOAD" = 237,
                      "MODIFY_BITS" = 236,
                      "SET_CAL_PAGE" = 235,
                      "GET_CAL_PAGE" = 234,
                      "GET_PAG_PROCESSOR_INFO" = 233,
                      "GET_SEGMENT_INFO" = 232,
                      "GET_PAGE_INFO" = 231,
                      "SET_SEGMENT_MODE" = 230,
                      "GET_SEGMENT_MODE" = 229,
                      "COPY_CAL_PAGE" = 228,
                      "CLEAR_DAQ_LIST" = 227,
                      "SET_DAQ_PTR" = 226,
                      "WRITE_DAQ" = 225,
                      "SET_DAQ_LIST_MODE" = 224,
                      "GET_DAQ_LIST_MODE" = 223,
                      "START_STOP_DAQ_LIST" = 222,
                      "START_STOP_SYNCH" = 221,
                      "GET_DAQ_CLOCK" = 220,
                      "READ_DAQ" = 219,
                      "GET_DAQ_PROCESSOR_INFO" = 218,
                      "GET_DAQ_RESOLUTION_INFO" = 217,
                      "GET_DAQ_LIST_INFO" = 216,
                      "GET_DAQ_EVENT_INFO" = 215,
                      "FREE_DAQ" = 214,
                      "ALLOC_DAQ" = 213,
                      "ALLOC_ODT" = 212,
                      "ALLOC_ODT_ENTRY" = 211,
                      "PROGRAM_START" = 210,
                      "PROGRAM_CLEAR" = 209,
                      "PROGRAM" = 208,
                      "PROGRAM_RESET" = 207,
                      "GET_PGM_PROCESSOR_INFO" = 206,
                      "GET_SECTOR_INFO" = 205,
                      "PROGRAM_PREPARE" = 204,
                      "PROGRAM_FORMAT" = 203,
                      "PROGRAM_NEXT" = 202,
                      "PROGRAM_MAX" = 201,
                      "PROGRAM_VERIFY" = 200
                    })*;
                    "COMMUNICATION_MODE_SUPPORTED" taggedunion {
                      "BLOCK" taggedstruct {
                        "SLAVE" ;
                        "MASTER" struct {
                          uchar;
                          uchar;
                        };
                      };
                      "INTERLEAVED" uchar;
                    };
                    "SEED_AND_KEY_EXTERNAL_FUNCTION" char[256];
                  };
                };
                block "SEGMENT" struct {
                  uchar;
                  uchar;
                  uchar;
                  uchar;
                  uchar;
                  taggedstruct {
                    block "CHECKSUM" struct {
                      enum {
                        "XCP_ADD_11" = 1,
                        "XCP_ADD_12" = 2,
                        "XCP_ADD_14" = 3,
                        "XCP_ADD_22" = 4,
                        "XCP_ADD_24" = 5,
                        "XCP_ADD_44" = 6,
                        "XCP_CRC_16" = 7,
                        "XCP_CRC_16_CITT" = 8,
                        "XCP_CRC_32" = 9,
                        "XCP_USER_DEFINED" = 255
                      };
                      taggedstruct {
                        "MAX_BLOCK_SIZE" ulong;
                        "EXTERNAL_FUNCTION" char[256];
                      };
                    };
                    (block "PAGE" struct {
                      uchar;
                      enum {
                        "ECU_ACCESS_NOT_ALLOWED" = 0,
                        "ECU_ACCESS_WITHOUT_XCP_ONLY" = 1,
                        "ECU_ACCESS_WITH_XCP_ONLY" = 2,
                        "ECU_ACCESS_DONT_CARE" = 3
                      };
                      enum {
                        "XCP_READ_ACCESS_NOT_ALLOWED" = 0,
                        "XCP_READ_ACCESS_WITHOUT_ECU_ONLY" = 1,
                        "XCP_READ_ACCESS_WITH_ECU_ONLY" = 2,
                        "XCP_READ_ACCESS_DONT_CARE" = 3
                      };
                      enum {
                        "XCP_WRITE_ACCESS_NOT_ALLOWED" = 0,
                        "XCP_WRITE_ACCESS_WITHOUT_ECU_ONLY" = 1,
                        "XCP_WRITE_ACCESS_WITH_ECU_ONLY" = 2,
                        "XCP_WRITE_ACCESS_DONT_CARE" = 3
                      };
                      taggedstruct {
                        "INIT_SEGMENT" uchar;
                      };
                    })*;
                    (block "ADDRESS_MAPPING" struct {
                      ulong;
                      ulong;
                      ulong;
                    })*;
                    "PGM_VERIFY" ulong;
                  };
                };
                block "DAQ" struct {
                  enum {
                    "STATIC" = 0,
                    "DYNAMIC" = 1
                  };
                  uint;
                  uint;
                  uchar;
                  enum {
                    "OPTIMISATION_TYPE_DEFAULT" = 0,
                    "OPTIMISATION_TYPE_ODT_TYPE_16" = 1,
                    "OPTIMISATION_TYPE_ODT_TYPE_32" = 2,
                    "OPTIMISATION_TYPE_ODT_TYPE_64" = 3,
                    "OPTIMISATION_TYPE_ODT_TYPE_ALIGNMENT" = 4,
                    "OPTIMISATION_TYPE_MAX_ENTRY_SIZE" = 5
                  };
                  enum {
                    "ADDRESS_EXTENSION_FREE" = 0,
                    "ADDRESS_EXTENSION_ODT" = 1,
                    "ADDRESS_EXTENSION_DAQ" = 3
                  };
                  enum {
                    "IDENTIFICATION_FIELD_TYPE_ABSOLUTE" = 0,
                    "IDENTIFICATION_FIELD_TYPE_RELATIVE_BYTE" = 1,
                    "IDENTIFICATION_FIELD_TYPE_RELATIVE_WORD" = 2,
                    "IDENTIFICATION_FIELD_TYPE_RELATIVE_WORD_ALIGNED" = 3
                  };
                  enum {
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_BYTE" = 1,
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_WORD" = 2,
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_DWORD" = 4,
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_DLONG" = 8
                  };
                  uchar;
                  enum {
                    "NO_OVERLOAD_INDICATION" = 0,
                    "OVERLOAD_INDICATION_PID" = 1,
                    "OVERLOAD_INDICATION_EVENT" = 2
                  };
                  taggedstruct {
                    "PRESCALER_SUPPORTED" ;
                    "RESUME_SUPPORTED" ;
                    block "STIM" struct {
                      enum {
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_BYTE" = 1,
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_WORD" = 2,
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_DWORD" = 4,
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_DLONG" = 8
                      };
                      uchar;
                      taggedstruct {
                        "BIT_STIM_SUPPORTED" ;
                      };
                    };
                    block "TIMESTAMP_SUPPORTED" struct {
                      uint;
                      enum {
                        "NO_TIME_STAMP" = 0,
                        "SIZE_BYTE" = 1,
                        "SIZE_WORD" = 2,
                        "SIZE_DWORD" = 4
                      };
                      enum {
                        "UNIT_1NS" = 0,
                        "UNIT_10NS" = 1,
                        "UNIT_100NS" = 2,
                        "UNIT_1US" = 3,
                        "UNIT_10US" = 4,
                        "UNIT_100US" = 5,
                        "UNIT_1MS" = 6,
                        "UNIT_10MS" = 7,
                        "UNIT_100MS" = 8,
                        "UNIT_1S" = 9
                      };
                      taggedstruct {
                        "TIMESTAMP_FIXED" ;
                      };
                    };
                    "PID_OFF_SUPPORTED" ;
                    (block "DAQ_LIST" struct {
                      uint;
                      taggedstruct {
                        "DAQ_LIST_TYPE" enum {
                          "DAQ" = 1,
                          "STIM" = 2,
                          "DAQ_STIM" = 3
                        };
                        "MAX_ODT" uchar;
                        "MAX_ODT_ENTRIES" uchar;
                        "FIRST_PID" uchar;
                        "EVENT_FIXED" uint;
                        block "PREDEFINED" taggedstruct {
                          (block "ODT" struct {
                            uchar;
                            taggedstruct {
                              ("ODT_ENTRY" struct {
                                uchar;
                                ulong;
                                uchar;
                                uchar;
                                uchar;
                              })*;
                            };
                          })*;
                        };
                      };
                    })*;
                    (block "EVENT" struct {
                      char[101];
                      char[9];
                      uint;
                      enum {
                        "DAQ" = 1,
                        "STIM" = 2,
                        "DAQ_STIM" = 3
                      };
                      uchar;
                      uchar;
                      uchar;
                      uchar;
                    })*;
                  };
                };
                block "PAG" struct {
                  uchar;
                  taggedstruct {
                    "FREEZE_SUPPORTED" ;
                  };
                };
                block "PGM" struct {
                  enum {
                    "PGM_MODE_ABSOLUTE" = 1,
                    "PGM_MODE_FUNCTIONAL" = 2,
                    "PGM_MODE_ABSOLUTE_AND_FUNCTIONAL" = 3
                  };
                  uchar;
                  uchar;
                  taggedstruct {
                    (block "SECTOR" struct {
                      char[101];
                      uchar;
                      ulong;
                      ulong;
                      uchar;
                      uchar;
                      uchar;
                    })*;
                    "COMMUNICATION_MODE_SUPPORTED" taggedunion {
                      "BLOCK" taggedstruct {
                        "SLAVE" ;
                        "MASTER" struct {
                          uchar;
                          uchar;
                        };
                      };
                      "INTERLEAVED" uchar;
                    };
                  };
                };
                block "DAQ_EVENT" taggedunion {
                  "FIXED_EVENT_LIST" taggedstruct {
                    ("EVENT" uint)*;
                  };
                  "VARIABLE" taggedstruct {
                    block "AVAILABLE_EVENT_LIST" taggedstruct {
                      ("EVENT" uint)*;
                    };
                    block "DEFAULT_EVENT_LIST" taggedstruct {
                      ("EVENT" uint)*;
                    };
                  };
                };
              };
            };
            block "XCP_ON_TCP_IP" struct {
              uint;
              uint;
              taggedunion {
                "HOST_NAME" char[256];
                "ADDRESS" char[15];
              };
              taggedstruct {
                block "PROTOCOL_LAYER" struct {
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uchar;
                  uint;
                  enum {
                    "BYTE_ORDER_MSB_LAST" = 0,
                    "BYTE_ORDER_MSB_FIRST" = 1
                  };
                  enum {
                    "ADDRESS_GRANULARITY_BYTE" = 1,
                    "ADDRESS_GRANULARITY_WORD" = 2,
                    "ADDRESS_GRANULARITY_DWORD" = 4
                  };
                  taggedstruct {
                    ("OPTIONAL_CMD" enum {
                      "GET_COMM_MODE_INFO" = 251,
                      "GET_ID" = 250,
                      "SET_REQUEST" = 249,
                      "GET_SEED" = 248,
                      "UNLOCK" = 247,
                      "SET_MTA" = 246,
                      "UPLOAD" = 245,
                      "SHORT_UPLOAD" = 244,
                      "BUILD_CHECKSUM" = 243,
                      "TRANSPORT_LAYER_CMD" = 242,
                      "USER_CMD" = 241,
                      "DOWNLOAD" = 240,
                      "DOWNLOAD_NEXT" = 239,
                      "DOWNLOAD_MAX" = 238,
                      "SHORT_DOWNLOAD" = 237,
                      "MODIFY_BITS" = 236,
                      "SET_CAL_PAGE" = 235,
                      "GET_CAL_PAGE" = 234,
                      "GET_PAG_PROCESSOR_INFO" = 233,
                      "GET_SEGMENT_INFO" = 232,
                      "GET_PAGE_INFO" = 231,
                      "SET_SEGMENT_MODE" = 230,
                      "GET_SEGMENT_MODE" = 229,
                      "COPY_CAL_PAGE" = 228,
                      "CLEAR_DAQ_LIST" = 227,
                      "SET_DAQ_PTR" = 226,
                      "WRITE_DAQ" = 225,
                      "SET_DAQ_LIST_MODE" = 224,
                      "GET_DAQ_LIST_MODE" = 223,
                      "START_STOP_DAQ_LIST" = 222,
                      "START_STOP_SYNCH" = 221,
                      "GET_DAQ_CLOCK" = 220,
                      "READ_DAQ" = 219,
                      "GET_DAQ_PROCESSOR_INFO" = 218,
                      "GET_DAQ_RESOLUTION_INFO" = 217,
                      "GET_DAQ_LIST_INFO" = 216,
                      "GET_DAQ_EVENT_INFO" = 215,
                      "FREE_DAQ" = 214,
                      "ALLOC_DAQ" = 213,
                      "ALLOC_ODT" = 212,
                      "ALLOC_ODT_ENTRY" = 211,
                      "PROGRAM_START" = 210,
                      "PROGRAM_CLEAR" = 209,
                      "PROGRAM" = 208,
                      "PROGRAM_RESET" = 207,
                      "GET_PGM_PROCESSOR_INFO" = 206,
                      "GET_SECTOR_INFO" = 205,
                      "PROGRAM_PREPARE" = 204,
                      "PROGRAM_FORMAT" = 203,
                      "PROGRAM_NEXT" = 202,
                      "PROGRAM_MAX" = 201,
                      "PROGRAM_VERIFY" = 200
                    })*;
                    "COMMUNICATION_MODE_SUPPORTED" taggedunion {
                      "BLOCK" taggedstruct {
                        "SLAVE" ;
                        "MASTER" struct {
                          uchar;
                          uchar;
                        };
                      };
                      "INTERLEAVED" uchar;
                    };
                    "SEED_AND_KEY_EXTERNAL_FUNCTION" char[256];
                  };
                };
                block "SEGMENT" struct {
                  uchar;
                  uchar;
                  uchar;
                  uchar;
                  uchar;
                  taggedstruct {
                    block "CHECKSUM" struct {
                      enum {
                        "XCP_ADD_11" = 1,
                        "XCP_ADD_12" = 2,
                        "XCP_ADD_14" = 3,
                        "XCP_ADD_22" = 4,
                        "XCP_ADD_24" = 5,
                        "XCP_ADD_44" = 6,
                        "XCP_CRC_16" = 7,
                        "XCP_CRC_16_CITT" = 8,
                        "XCP_CRC_32" = 9,
                        "XCP_USER_DEFINED" = 255
                      };
                      taggedstruct {
                        "MAX_BLOCK_SIZE" ulong;
                        "EXTERNAL_FUNCTION" char[256];
                      };
                    };
                    (block "PAGE" struct {
                      uchar;
                      enum {
                        "ECU_ACCESS_NOT_ALLOWED" = 0,
                        "ECU_ACCESS_WITHOUT_XCP_ONLY" = 1,
                        "ECU_ACCESS_WITH_XCP_ONLY" = 2,
                        "ECU_ACCESS_DONT_CARE" = 3
                      };
                      enum {
                        "XCP_READ_ACCESS_NOT_ALLOWED" = 0,
                        "XCP_READ_ACCESS_WITHOUT_ECU_ONLY" = 1,
                        "XCP_READ_ACCESS_WITH_ECU_ONLY" = 2,
                        "XCP_READ_ACCESS_DONT_CARE" = 3
                      };
                      enum {
                        "XCP_WRITE_ACCESS_NOT_ALLOWED" = 0,
                        "XCP_WRITE_ACCESS_WITHOUT_ECU_ONLY" = 1,
                        "XCP_WRITE_ACCESS_WITH_ECU_ONLY" = 2,
                        "XCP_WRITE_ACCESS_DONT_CARE" = 3
                      };
                      taggedstruct {
                        "INIT_SEGMENT" uchar;
                      };
                    })*;
                    (block "ADDRESS_MAPPING" struct {
                      ulong;
                      ulong;
                      ulong;
                    })*;
                    "PGM_VERIFY" ulong;
                  };
                };
                block "DAQ" struct {
                  enum {
                    "STATIC" = 0,
                    "DYNAMIC" = 1
                  };
                  uint;
                  uint;
                  uchar;
                  enum {
                    "OPTIMISATION_TYPE_DEFAULT" = 0,
                    "OPTIMISATION_TYPE_ODT_TYPE_16" = 1,
                    "OPTIMISATION_TYPE_ODT_TYPE_32" = 2,
                    "OPTIMISATION_TYPE_ODT_TYPE_64" = 3,
                    "OPTIMISATION_TYPE_ODT_TYPE_ALIGNMENT" = 4,
                    "OPTIMISATION_TYPE_MAX_ENTRY_SIZE" = 5
                  };
                  enum {
                    "ADDRESS_EXTENSION_FREE" = 0,
                    "ADDRESS_EXTENSION_ODT" = 1,
                    "ADDRESS_EXTENSION_DAQ" = 3
                  };
                  enum {
                    "IDENTIFICATION_FIELD_TYPE_ABSOLUTE" = 0,
                    "IDENTIFICATION_FIELD_TYPE_RELATIVE_BYTE" = 1,
                    "IDENTIFICATION_FIELD_TYPE_RELATIVE_WORD" = 2,
                    "IDENTIFICATION_FIELD_TYPE_RELATIVE_WORD_ALIGNED" = 3
                  };
                  enum {
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_BYTE" = 1,
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_WORD" = 2,
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_DWORD" = 4,
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_DLONG" = 8
                  };
                  uchar;
                  enum {
                    "NO_OVERLOAD_INDICATION" = 0,
                    "OVERLOAD_INDICATION_PID" = 1,
                    "OVERLOAD_INDICATION_EVENT" = 2
                  };
                  taggedstruct {
                    "PRESCALER_SUPPORTED" ;
                    "RESUME_SUPPORTED" ;
                    block "STIM" struct {
                      enum {
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_BYTE" = 1,
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_WORD" = 2,
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_DWORD" = 4,
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_DLONG" = 8
                      };
                      uchar;
                      taggedstruct {
                        "BIT_STIM_SUPPORTED" ;
                      };
                    };
                    block "TIMESTAMP_SUPPORTED" struct {
                      uint;
                      enum {
                        "NO_TIME_STAMP" = 0,
                        "SIZE_BYTE" = 1,
                        "SIZE_WORD" = 2,
                        "SIZE_DWORD" = 4
                      };
                      enum {
                        "UNIT_1NS" = 0,
                        "UNIT_10NS" = 1,
                        "UNIT_100NS" = 2,
                        "UNIT_1US" = 3,
                        "UNIT_10US" = 4,
                        "UNIT_100US" = 5,
                        "UNIT_1MS" = 6,
                        "UNIT_10MS" = 7,
                        "UNIT_100MS" = 8,
                        "UNIT_1S" = 9
                      };
                      taggedstruct {
                        "TIMESTAMP_FIXED" ;
                      };
                    };
                    "PID_OFF_SUPPORTED" ;
                    (block "DAQ_LIST" struct {
                      uint;
                      taggedstruct {
                        "DAQ_LIST_TYPE" enum {
                          "DAQ" = 1,
                          "STIM" = 2,
                          "DAQ_STIM" = 3
                        };
                        "MAX_ODT" uchar;
                        "MAX_ODT_ENTRIES" uchar;
                        "FIRST_PID" uchar;
                        "EVENT_FIXED" uint;
                        block "PREDEFINED" taggedstruct {
                          (block "ODT" struct {
                            uchar;
                            taggedstruct {
                              ("ODT_ENTRY" struct {
                                uchar;
                                ulong;
                                uchar;
                                uchar;
                                uchar;
                              })*;
                            };
                          })*;
                        };
                      };
                    })*;
                    (block "EVENT" struct {
                      char[101];
                      char[9];
                      uint;
                      enum {
                        "DAQ" = 1,
                        "STIM" = 2,
                        "DAQ_STIM" = 3
                      };
                      uchar;
                      uchar;
                      uchar;
                      uchar;
                    })*;
                  };
                };
                block "PAG" struct {
                  uchar;
                  taggedstruct {
                    "FREEZE_SUPPORTED" ;
                  };
                };
                block "PGM" struct {
                  enum {
                    "PGM_MODE_ABSOLUTE" = 1,
                    "PGM_MODE_FUNCTIONAL" = 2,
                    "PGM_MODE_ABSOLUTE_AND_FUNCTIONAL" = 3
                  };
                  uchar;
                  uchar;
                  taggedstruct {
                    (block "SECTOR" struct {
                      char[101];
                      uchar;
                      ulong;
                      ulong;
                      uchar;
                      uchar;
                      uchar;
                    })*;
                    "COMMUNICATION_MODE_SUPPORTED" taggedunion {
                      "BLOCK" taggedstruct {
                        "SLAVE" ;
                        "MASTER" struct {
                          uchar;
                          uchar;
                        };
                      };
                      "INTERLEAVED" uchar;
                    };
                  };
                };
                block "DAQ_EVENT" taggedunion {
                  "FIXED_EVENT_LIST" taggedstruct {
                    ("EVENT" uint)*;
                  };
                  "VARIABLE" taggedstruct {
                    block "AVAILABLE_EVENT_LIST" taggedstruct {
                      ("EVENT" uint)*;
                    };
                    block "DEFAULT_EVENT_LIST" taggedstruct {
                      ("EVENT" uint)*;
                    };
                  };
                };
              };
            };
            block "XCP_ON_UDP_IP" struct {
              uint;
              uint;
              taggedunion {
                "HOST_NAME" char[256];
                "ADDRESS" char[15];
              };
              taggedstruct {
                block "PROTOCOL_LAYER" struct {
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uchar;
                  uint;
                  enum {
                    "BYTE_ORDER_MSB_LAST" = 0,
                    "BYTE_ORDER_MSB_FIRST" = 1
                  };
                  enum {
                    "ADDRESS_GRANULARITY_BYTE" = 1,
                    "ADDRESS_GRANULARITY_WORD" = 2,
                    "ADDRESS_GRANULARITY_DWORD" = 4
                  };
                  taggedstruct {
                    ("OPTIONAL_CMD" enum {
                      "GET_COMM_MODE_INFO" = 251,
                      "GET_ID" = 250,
                      "SET_REQUEST" = 249,
                      "GET_SEED" = 248,
                      "UNLOCK" = 247,
                      "SET_MTA" = 246,
                      "UPLOAD" = 245,
                      "SHORT_UPLOAD" = 244,
                      "BUILD_CHECKSUM" = 243,
                      "TRANSPORT_LAYER_CMD" = 242,
                      "USER_CMD" = 241,
                      "DOWNLOAD" = 240,
                      "DOWNLOAD_NEXT" = 239,
                      "DOWNLOAD_MAX" = 238,
                      "SHORT_DOWNLOAD" = 237,
                      "MODIFY_BITS" = 236,
                      "SET_CAL_PAGE" = 235,
                      "GET_CAL_PAGE" = 234,
                      "GET_PAG_PROCESSOR_INFO" = 233,
                      "GET_SEGMENT_INFO" = 232,
                      "GET_PAGE_INFO" = 231,
                      "SET_SEGMENT_MODE" = 230,
                      "GET_SEGMENT_MODE" = 229,
                      "COPY_CAL_PAGE" = 228,
                      "CLEAR_DAQ_LIST" = 227,
                      "SET_DAQ_PTR" = 226,
                      "WRITE_DAQ" = 225,
                      "SET_DAQ_LIST_MODE" = 224,
                      "GET_DAQ_LIST_MODE" = 223,
                      "START_STOP_DAQ_LIST" = 222,
                      "START_STOP_SYNCH" = 221,
                      "GET_DAQ_CLOCK" = 220,
                      "READ_DAQ" = 219,
                      "GET_DAQ_PROCESSOR_INFO" = 218,
                      "GET_DAQ_RESOLUTION_INFO" = 217,
                      "GET_DAQ_LIST_INFO" = 216,
                      "GET_DAQ_EVENT_INFO" = 215,
                      "FREE_DAQ" = 214,
                      "ALLOC_DAQ" = 213,
                      "ALLOC_ODT" = 212,
                      "ALLOC_ODT_ENTRY" = 211,
                      "PROGRAM_START" = 210,
                      "PROGRAM_CLEAR" = 209,
                      "PROGRAM" = 208,
                      "PROGRAM_RESET" = 207,
                      "GET_PGM_PROCESSOR_INFO" = 206,
                      "GET_SECTOR_INFO" = 205,
                      "PROGRAM_PREPARE" = 204,
                      "PROGRAM_FORMAT" = 203,
                      "PROGRAM_NEXT" = 202,
                      "PROGRAM_MAX" = 201,
                      "PROGRAM_VERIFY" = 200
                    })*;
                    "COMMUNICATION_MODE_SUPPORTED" taggedunion {
                      "BLOCK" taggedstruct {
                        "SLAVE" ;
                        "MASTER" struct {
                          uchar;
                          uchar;
                        };
                      };
                      "INTERLEAVED" uchar;
                    };
                    "SEED_AND_KEY_EXTERNAL_FUNCTION" char[256];
                  };
                };
                block "SEGMENT" struct {
                  uchar;
                  uchar;
                  uchar;
                  uchar;
                  uchar;
                  taggedstruct {
                    block "CHECKSUM" struct {
                      enum {
                        "XCP_ADD_11" = 1,
                        "XCP_ADD_12" = 2,
                        "XCP_ADD_14" = 3,
                        "XCP_ADD_22" = 4,
                        "XCP_ADD_24" = 5,
                        "XCP_ADD_44" = 6,
                        "XCP_CRC_16" = 7,
                        "XCP_CRC_16_CITT" = 8,
                        "XCP_CRC_32" = 9,
                        "XCP_USER_DEFINED" = 255
                      };
                      taggedstruct {
                        "MAX_BLOCK_SIZE" ulong;
                        "EXTERNAL_FUNCTION" char[256];
                      };
                    };
                    (block "PAGE" struct {
                      uchar;
                      enum {
                        "ECU_ACCESS_NOT_ALLOWED" = 0,
                        "ECU_ACCESS_WITHOUT_XCP_ONLY" = 1,
                        "ECU_ACCESS_WITH_XCP_ONLY" = 2,
                        "ECU_ACCESS_DONT_CARE" = 3
                      };
                      enum {
                        "XCP_READ_ACCESS_NOT_ALLOWED" = 0,
                        "XCP_READ_ACCESS_WITHOUT_ECU_ONLY" = 1,
                        "XCP_READ_ACCESS_WITH_ECU_ONLY" = 2,
                        "XCP_READ_ACCESS_DONT_CARE" = 3
                      };
                      enum {
                        "XCP_WRITE_ACCESS_NOT_ALLOWED" = 0,
                        "XCP_WRITE_ACCESS_WITHOUT_ECU_ONLY" = 1,
                        "XCP_WRITE_ACCESS_WITH_ECU_ONLY" = 2,
                        "XCP_WRITE_ACCESS_DONT_CARE" = 3
                      };
                      taggedstruct {
                        "INIT_SEGMENT" uchar;
                      };
                    })*;
                    (block "ADDRESS_MAPPING" struct {
                      ulong;
                      ulong;
                      ulong;
                    })*;
                    "PGM_VERIFY" ulong;
                  };
                };
                block "DAQ" struct {
                  enum {
                    "STATIC" = 0,
                    "DYNAMIC" = 1
                  };
                  uint;
                  uint;
                  uchar;
                  enum {
                    "OPTIMISATION_TYPE_DEFAULT" = 0,
                    "OPTIMISATION_TYPE_ODT_TYPE_16" = 1,
                    "OPTIMISATION_TYPE_ODT_TYPE_32" = 2,
                    "OPTIMISATION_TYPE_ODT_TYPE_64" = 3,
                    "OPTIMISATION_TYPE_ODT_TYPE_ALIGNMENT" = 4,
                    "OPTIMISATION_TYPE_MAX_ENTRY_SIZE" = 5
                  };
                  enum {
                    "ADDRESS_EXTENSION_FREE" = 0,
                    "ADDRESS_EXTENSION_ODT" = 1,
                    "ADDRESS_EXTENSION_DAQ" = 3
                  };
                  enum {
                    "IDENTIFICATION_FIELD_TYPE_ABSOLUTE" = 0,
                    "IDENTIFICATION_FIELD_TYPE_RELATIVE_BYTE" = 1,
                    "IDENTIFICATION_FIELD_TYPE_RELATIVE_WORD" = 2,
                    "IDENTIFICATION_FIELD_TYPE_RELATIVE_WORD_ALIGNED" = 3
                  };
                  enum {
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_BYTE" = 1,
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_WORD" = 2,
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_DWORD" = 4,
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_DLONG" = 8
                  };
                  uchar;
                  enum {
                    "NO_OVERLOAD_INDICATION" = 0,
                    "OVERLOAD_INDICATION_PID" = 1,
                    "OVERLOAD_INDICATION_EVENT" = 2
                  };
                  taggedstruct {
                    "PRESCALER_SUPPORTED" ;
                    "RESUME_SUPPORTED" ;
                    block "STIM" struct {
                      enum {
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_BYTE" = 1,
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_WORD" = 2,
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_DWORD" = 4,
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_DLONG" = 8
                      };
                      uchar;
                      taggedstruct {
                        "BIT_STIM_SUPPORTED" ;
                      };
                    };
                    block "TIMESTAMP_SUPPORTED" struct {
                      uint;
                      enum {
                        "NO_TIME_STAMP" = 0,
                        "SIZE_BYTE" = 1,
                        "SIZE_WORD" = 2,
                        "SIZE_DWORD" = 4
                      };
                      enum {
                        "UNIT_1NS" = 0,
                        "UNIT_10NS" = 1,
                        "UNIT_100NS" = 2,
                        "UNIT_1US" = 3,
                        "UNIT_10US" = 4,
                        "UNIT_100US" = 5,
                        "UNIT_1MS" = 6,
                        "UNIT_10MS" = 7,
                        "UNIT_100MS" = 8,
                        "UNIT_1S" = 9
                      };
                      taggedstruct {
                        "TIMESTAMP_FIXED" ;
                      };
                    };
                    "PID_OFF_SUPPORTED" ;
                    (block "DAQ_LIST" struct {
                      uint;
                      taggedstruct {
                        "DAQ_LIST_TYPE" enum {
                          "DAQ" = 1,
                          "STIM" = 2,
                          "DAQ_STIM" = 3
                        };
                        "MAX_ODT" uchar;
                        "MAX_ODT_ENTRIES" uchar;
                        "FIRST_PID" uchar;
                        "EVENT_FIXED" uint;
                        block "PREDEFINED" taggedstruct {
                          (block "ODT" struct {
                            uchar;
                            taggedstruct {
                              ("ODT_ENTRY" struct {
                                uchar;
                                ulong;
                                uchar;
                                uchar;
                                uchar;
                              })*;
                            };
                          })*;
                        };
                      };
                    })*;
                    (block "EVENT" struct {
                      char[101];
                      char[9];
                      uint;
                      enum {
                        "DAQ" = 1,
                        "STIM" = 2,
                        "DAQ_STIM" = 3
                      };
                      uchar;
                      uchar;
                      uchar;
                      uchar;
                    })*;
                  };
                };
                block "PAG" struct {
                  uchar;
                  taggedstruct {
                    "FREEZE_SUPPORTED" ;
                  };
                };
                block "PGM" struct {
                  enum {
                    "PGM_MODE_ABSOLUTE" = 1,
                    "PGM_MODE_FUNCTIONAL" = 2,
                    "PGM_MODE_ABSOLUTE_AND_FUNCTIONAL" = 3
                  };
                  uchar;
                  uchar;
                  taggedstruct {
                    (block "SECTOR" struct {
                      char[101];
                      uchar;
                      ulong;
                      ulong;
                      uchar;
                      uchar;
                      uchar;
                    })*;
                    "COMMUNICATION_MODE_SUPPORTED" taggedunion {
                      "BLOCK" taggedstruct {
                        "SLAVE" ;
                        "MASTER" struct {
                          uchar;
                          uchar;
                        };
                      };
                      "INTERLEAVED" uchar;
                    };
                  };
                };
                block "DAQ_EVENT" taggedunion {
                  "FIXED_EVENT_LIST" taggedstruct {
                    ("EVENT" uint)*;
                  };
                  "VARIABLE" taggedstruct {
                    block "AVAILABLE_EVENT_LIST" taggedstruct {
                      ("EVENT" uint)*;
                    };
                    block "DEFAULT_EVENT_LIST" taggedstruct {
                      ("EVENT" uint)*;
                    };
                  };
                };
              };
            };
            block "XCP_ON_USB" struct {
              uint;
              uint;
              uint;
              uchar;
              enum {
                "HEADER_LEN_BYTE" = 0,
                "HEADER_LEN_CTR_BYTE" = 1,
                "HEADER_LEN_FILL_BYTE" = 2,
                "HEADER_LEN_WORD" = 3,
                "HEADER_LEN_CTR_WORD" = 4,
                "HEADER_LEN_FILL_WORD" = 5
              };
              taggedunion {
                block "OUT_EP_CMD_STIM" struct {
                  uchar;
                  enum {
                    "BULK_TRANSFER" = 2,
                    "INTERRUPT_TRANSFER" = 3
                  };
                  uint;
                  uchar;
                  enum {
                    "MESSAGE_PACKING_SINGLE" = 0,
                    "MESSAGE_PACKING_MULTIPLE" = 1,
                    "MESSAGE_PACKING_STREAMING" = 2
                  };
                  enum {
                    "ALIGNMENT_8_BIT" = 0,
                    "ALIGNMENT_16_BIT" = 1,
                    "ALIGNMENT_32_BIT" = 2,
                    "ALIGNMENT_64_BIT" = 3
                  };
                  taggedstruct {
                    "RECOMMENDED_HOST_BUFSIZE" uint;
                  };
                };
              };
              taggedunion {
                block "IN_EP_RESERR_DAQ_EVSERV" struct {
                  uchar;
                  enum {
                    "BULK_TRANSFER" = 2,
                    "INTERRUPT_TRANSFER" = 3
                  };
                  uint;
                  uchar;
                  enum {
                    "MESSAGE_PACKING_SINGLE" = 0,
                    "MESSAGE_PACKING_MULTIPLE" = 1,
                    "MESSAGE_PACKING_STREAMING" = 2
                  };
                  enum {
                    "ALIGNMENT_8_BIT" = 0,
                    "ALIGNMENT_16_BIT" = 1,
                    "ALIGNMENT_32_BIT" = 2,
                    "ALIGNMENT_64_BIT" = 3
                  };
                  taggedstruct {
                    "RECOMMENDED_HOST_BUFSIZE" uint;
                  };
                };
              };
              taggedstruct {
                "ALTERNATE_SETTING_NO" uchar;
                "INTERFACE_STRING_DESCRIPTOR" char[101];
                (block "OUT_EP_ONLY_STIM" struct {
                  uchar;
                  enum {
                    "BULK_TRANSFER" = 2,
                    "INTERRUPT_TRANSFER" = 3
                  };
                  uint;
                  uchar;
                  enum {
                    "MESSAGE_PACKING_SINGLE" = 0,
                    "MESSAGE_PACKING_MULTIPLE" = 1,
                    "MESSAGE_PACKING_STREAMING" = 2
                  };
                  enum {
                    "ALIGNMENT_8_BIT" = 0,
                    "ALIGNMENT_16_BIT" = 1,
                    "ALIGNMENT_32_BIT" = 2,
                    "ALIGNMENT_64_BIT" = 3
                  };
                  taggedstruct {
                    "RECOMMENDED_HOST_BUFSIZE" uint;
                  };
                })*;
                (block "IN_EP_ONLY_DAQ" struct {
                  uchar;
                  enum {
                    "BULK_TRANSFER" = 2,
                    "INTERRUPT_TRANSFER" = 3
                  };
                  uint;
                  uchar;
                  enum {
                    "MESSAGE_PACKING_SINGLE" = 0,
                    "MESSAGE_PACKING_MULTIPLE" = 1,
                    "MESSAGE_PACKING_STREAMING" = 2
                  };
                  enum {
                    "ALIGNMENT_8_BIT" = 0,
                    "ALIGNMENT_16_BIT" = 1,
                    "ALIGNMENT_32_BIT" = 2,
                    "ALIGNMENT_64_BIT" = 3
                  };
                  taggedstruct {
                    "RECOMMENDED_HOST_BUFSIZE" uint;
                  };
                })*;
                block "IN_EP_ONLY_EVSERV" struct {
                  uchar;
                  enum {
                    "BULK_TRANSFER" = 2,
                    "INTERRUPT_TRANSFER" = 3
                  };
                  uint;
                  uchar;
                  enum {
                    "MESSAGE_PACKING_SINGLE" = 0,
                    "MESSAGE_PACKING_MULTIPLE" = 1,
                    "MESSAGE_PACKING_STREAMING" = 2
                  };
                  enum {
                    "ALIGNMENT_8_BIT" = 0,
                    "ALIGNMENT_16_BIT" = 1,
                    "ALIGNMENT_32_BIT" = 2,
                    "ALIGNMENT_64_BIT" = 3
                  };
                  taggedstruct {
                    "RECOMMENDED_HOST_BUFSIZE" uint;
                  };
                };
                (block "DAQ_LIST_USB_ENDPOINT" struct {
                  uint;
                  taggedstruct {
                    "FIXED_IN" uchar;
                    "FIXED_OUT" uchar;
                  };
                })*;
                block "PROTOCOL_LAYER" struct {
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uchar;
                  uint;
                  enum {
                    "BYTE_ORDER_MSB_LAST" = 0,
                    "BYTE_ORDER_MSB_FIRST" = 1
                  };
                  enum {
                    "ADDRESS_GRANULARITY_BYTE" = 1,
                    "ADDRESS_GRANULARITY_WORD" = 2,
                    "ADDRESS_GRANULARITY_DWORD" = 4
                  };
                  taggedstruct {
                    ("OPTIONAL_CMD" enum {
                      "GET_COMM_MODE_INFO" = 251,
                      "GET_ID" = 250,
                      "SET_REQUEST" = 249,
                      "GET_SEED" = 248,
                      "UNLOCK" = 247,
                      "SET_MTA" = 246,
                      "UPLOAD" = 245,
                      "SHORT_UPLOAD" = 244,
                      "BUILD_CHECKSUM" = 243,
                      "TRANSPORT_LAYER_CMD" = 242,
                      "USER_CMD" = 241,
                      "DOWNLOAD" = 240,
                      "DOWNLOAD_NEXT" = 239,
                      "DOWNLOAD_MAX" = 238,
                      "SHORT_DOWNLOAD" = 237,
                      "MODIFY_BITS" = 236,
                      "SET_CAL_PAGE" = 235,
                      "GET_CAL_PAGE" = 234,
                      "GET_PAG_PROCESSOR_INFO" = 233,
                      "GET_SEGMENT_INFO" = 232,
                      "GET_PAGE_INFO" = 231,
                      "SET_SEGMENT_MODE" = 230,
                      "GET_SEGMENT_MODE" = 229,
                      "COPY_CAL_PAGE" = 228,
                      "CLEAR_DAQ_LIST" = 227,
                      "SET_DAQ_PTR" = 226,
                      "WRITE_DAQ" = 225,
                      "SET_DAQ_LIST_MODE" = 224,
                      "GET_DAQ_LIST_MODE" = 223,
                      "START_STOP_DAQ_LIST" = 222,
                      "START_STOP_SYNCH" = 221,
                      "GET_DAQ_CLOCK" = 220,
                      "READ_DAQ" = 219,
                      "GET_DAQ_PROCESSOR_INFO" = 218,
                      "GET_DAQ_RESOLUTION_INFO" = 217,
                      "GET_DAQ_LIST_INFO" = 216,
                      "GET_DAQ_EVENT_INFO" = 215,
                      "FREE_DAQ" = 214,
                      "ALLOC_DAQ" = 213,
                      "ALLOC_ODT" = 212,
                      "ALLOC_ODT_ENTRY" = 211,
                      "PROGRAM_START" = 210,
                      "PROGRAM_CLEAR" = 209,
                      "PROGRAM" = 208,
                      "PROGRAM_RESET" = 207,
                      "GET_PGM_PROCESSOR_INFO" = 206,
                      "GET_SECTOR_INFO" = 205,
                      "PROGRAM_PREPARE" = 204,
                      "PROGRAM_FORMAT" = 203,
                      "PROGRAM_NEXT" = 202,
                      "PROGRAM_MAX" = 201,
                      "PROGRAM_VERIFY" = 200
                    })*;
                    "COMMUNICATION_MODE_SUPPORTED" taggedunion {
                      "BLOCK" taggedstruct {
                        "SLAVE" ;
                        "MASTER" struct {
                          uchar;
                          uchar;
                        };
                      };
                      "INTERLEAVED" uchar;
                    };
                    "SEED_AND_KEY_EXTERNAL_FUNCTION" char[256];
                  };
                };
                block "SEGMENT" struct {
                  uchar;
                  uchar;
                  uchar;
                  uchar;
                  uchar;
                  taggedstruct {
                    block "CHECKSUM" struct {
                      enum {
                        "XCP_ADD_11" = 1,
                        "XCP_ADD_12" = 2,
                        "XCP_ADD_14" = 3,
                        "XCP_ADD_22" = 4,
                        "XCP_ADD_24" = 5,
                        "XCP_ADD_44" = 6,
                        "XCP_CRC_16" = 7,
                        "XCP_CRC_16_CITT" = 8,
                        "XCP_CRC_32" = 9,
                        "XCP_USER_DEFINED" = 255
                      };
                      taggedstruct {
                        "MAX_BLOCK_SIZE" ulong;
                        "EXTERNAL_FUNCTION" char[256];
                      };
                    };
                    (block "PAGE" struct {
                      uchar;
                      enum {
                        "ECU_ACCESS_NOT_ALLOWED" = 0,
                        "ECU_ACCESS_WITHOUT_XCP_ONLY" = 1,
                        "ECU_ACCESS_WITH_XCP_ONLY" = 2,
                        "ECU_ACCESS_DONT_CARE" = 3
                      };
                      enum {
                        "XCP_READ_ACCESS_NOT_ALLOWED" = 0,
                        "XCP_READ_ACCESS_WITHOUT_ECU_ONLY" = 1,
                        "XCP_READ_ACCESS_WITH_ECU_ONLY" = 2,
                        "XCP_READ_ACCESS_DONT_CARE" = 3
                      };
                      enum {
                        "XCP_WRITE_ACCESS_NOT_ALLOWED" = 0,
                        "XCP_WRITE_ACCESS_WITHOUT_ECU_ONLY" = 1,
                        "XCP_WRITE_ACCESS_WITH_ECU_ONLY" = 2,
                        "XCP_WRITE_ACCESS_DONT_CARE" = 3
                      };
                      taggedstruct {
                        "INIT_SEGMENT" uchar;
                      };
                    })*;
                    (block "ADDRESS_MAPPING" struct {
                      ulong;
                      ulong;
                      ulong;
                    })*;
                    "PGM_VERIFY" ulong;
                  };
                };
                block "DAQ" struct {
                  enum {
                    "STATIC" = 0,
                    "DYNAMIC" = 1
                  };
                  uint;
                  uint;
                  uchar;
                  enum {
                    "OPTIMISATION_TYPE_DEFAULT" = 0,
                    "OPTIMISATION_TYPE_ODT_TYPE_16" = 1,
                    "OPTIMISATION_TYPE_ODT_TYPE_32" = 2,
                    "OPTIMISATION_TYPE_ODT_TYPE_64" = 3,
                    "OPTIMISATION_TYPE_ODT_TYPE_ALIGNMENT" = 4,
                    "OPTIMISATION_TYPE_MAX_ENTRY_SIZE" = 5
                  };
                  enum {
                    "ADDRESS_EXTENSION_FREE" = 0,
                    "ADDRESS_EXTENSION_ODT" = 1,
                    "ADDRESS_EXTENSION_DAQ" = 3
                  };
                  enum {
                    "IDENTIFICATION_FIELD_TYPE_ABSOLUTE" = 0,
                    "IDENTIFICATION_FIELD_TYPE_RELATIVE_BYTE" = 1,
                    "IDENTIFICATION_FIELD_TYPE_RELATIVE_WORD" = 2,
                    "IDENTIFICATION_FIELD_TYPE_RELATIVE_WORD_ALIGNED" = 3
                  };
                  enum {
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_BYTE" = 1,
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_WORD" = 2,
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_DWORD" = 4,
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_DLONG" = 8
                  };
                  uchar;
                  enum {
                    "NO_OVERLOAD_INDICATION" = 0,
                    "OVERLOAD_INDICATION_PID" = 1,
                    "OVERLOAD_INDICATION_EVENT" = 2
                  };
                  taggedstruct {
                    "PRESCALER_SUPPORTED" ;
                    "RESUME_SUPPORTED" ;
                    block "STIM" struct {
                      enum {
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_BYTE" = 1,
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_WORD" = 2,
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_DWORD" = 4,
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_DLONG" = 8
                      };
                      uchar;
                      taggedstruct {
                        "BIT_STIM_SUPPORTED" ;
                      };
                    };
                    block "TIMESTAMP_SUPPORTED" struct {
                      uint;
                      enum {
                        "NO_TIME_STAMP" = 0,
                        "SIZE_BYTE" = 1,
                        "SIZE_WORD" = 2,
                        "SIZE_DWORD" = 4
                      };
                      enum {
                        "UNIT_1NS" = 0,
                        "UNIT_10NS" = 1,
                        "UNIT_100NS" = 2,
                        "UNIT_1US" = 3,
                        "UNIT_10US" = 4,
                        "UNIT_100US" = 5,
                        "UNIT_1MS" = 6,
                        "UNIT_10MS" = 7,
                        "UNIT_100MS" = 8,
                        "UNIT_1S" = 9
                      };
                      taggedstruct {
                        "TIMESTAMP_FIXED" ;
                      };
                    };
                    "PID_OFF_SUPPORTED" ;
                    (block "DAQ_LIST" struct {
                      uint;
                      taggedstruct {
                        "DAQ_LIST_TYPE" enum {
                          "DAQ" = 1,
                          "STIM" = 2,
                          "DAQ_STIM" = 3
                        };
                        "MAX_ODT" uchar;
                        "MAX_ODT_ENTRIES" uchar;
                        "FIRST_PID" uchar;
                        "EVENT_FIXED" uint;
                        block "PREDEFINED" taggedstruct {
                          (block "ODT" struct {
                            uchar;
                            taggedstruct {
                              ("ODT_ENTRY" struct {
                                uchar;
                                ulong;
                                uchar;
                                uchar;
                                uchar;
                              })*;
                            };
                          })*;
                        };
                      };
                    })*;
                    (block "EVENT" struct {
                      char[101];
                      char[9];
                      uint;
                      enum {
                        "DAQ" = 1,
                        "STIM" = 2,
                        "DAQ_STIM" = 3
                      };
                      uchar;
                      uchar;
                      uchar;
                      uchar;
                    })*;
                  };
                };
                block "PAG" struct {
                  uchar;
                  taggedstruct {
                    "FREEZE_SUPPORTED" ;
                  };
                };
                block "PGM" struct {
                  enum {
                    "PGM_MODE_ABSOLUTE" = 1,
                    "PGM_MODE_FUNCTIONAL" = 2,
                    "PGM_MODE_ABSOLUTE_AND_FUNCTIONAL" = 3
                  };
                  uchar;
                  uchar;
                  taggedstruct {
                    (block "SECTOR" struct {
                      char[101];
                      uchar;
                      ulong;
                      ulong;
                      uchar;
                      uchar;
                      uchar;
                    })*;
                    "COMMUNICATION_MODE_SUPPORTED" taggedunion {
                      "BLOCK" taggedstruct {
                        "SLAVE" ;
                        "MASTER" struct {
                          uchar;
                          uchar;
                        };
                      };
                      "INTERLEAVED" uchar;
                    };
                  };
                };
                block "DAQ_EVENT" taggedunion {
                  "FIXED_EVENT_LIST" taggedstruct {
                    ("EVENT" uint)*;
                  };
                  "VARIABLE" taggedstruct {
                    block "AVAILABLE_EVENT_LIST" taggedstruct {
                      ("EVENT" uint)*;
                    };
                    block "DEFAULT_EVENT_LIST" taggedstruct {
                      ("EVENT" uint)*;
                    };
                  };
                };
              };
            };
          };
        };


      };
            /end A2ML


            /begin MOD_PAR ""
      NO_OF_INTERFACES 1

      /begin MEMORY_SEGMENT ECU_Code
        "Memory segment for code part of the ECU"
        DATA FLASH EXTERN 0x16000 0x86C -1 -1 -1 -1 -1
        /begin IF_DATA XCP
          ADDRESS_MAPPING 0x4000 0x8000 0x0200
          ADDRESS_MAPPING 0x5000 0x9000 0x0300
          /begin SEGMENT
            0x0 0x2 0x0 0x0 0x0
            /begin PAGE
              0x0 ECU_ACCESS_DONT_CARE XCP_READ_ACCESS_WITH_ECU_ONLY XCP_WRITE_ACCESS_NOT_ALLOWED
            /end PAGE
            /begin PAGE
              0x1 ECU_ACCESS_DONT_CARE XCP_READ_ACCESS_WITH_ECU_ONLY XCP_WRITE_ACCESS_WITH_ECU_ONLY
            /end PAGE
          /end SEGMENT
        /end IF_DATA
      /end MEMORY_SEGMENT

      /begin MEMORY_SEGMENT ECU_Data
        "Memory segment for parameters"
        DATA FLASH EXTERN 0x810000 0x10000 -1 -1 -1 -1 -1
      /end MEMORY_SEGMENT

      SYSTEM_CONSTANT "System_Constant_1" "-3.45"
      SYSTEM_CONSTANT "System_Constant_2" "5.67"
      SYSTEM_CONSTANT "System_Constant_3" "Text in System Constant"

    /end MOD_PAR

            /begin MOD_COMMON ""
      DEPOSIT ABSOLUTE
      BYTE_ORDER MSB_LAST
      ALIGNMENT_BYTE 1
      ALIGNMENT_WORD 2
      ALIGNMENT_LONG 4
      ALIGNMENT_FLOAT32_IEEE 4
      ALIGNMENT_FLOAT64_IEEE 4
    /end MOD_COMMON
            /begin AXIS_PTS 
            AirChrgrMdlHi_CmprSpdCorrd_MAPX 
            "Air Charger Model _ Compressor Speed Corrected _ Map X Axis"
      0x50002DF2 
      AirChrgrMdlHi_CmprPRat 
      _REC_A2AXS_60_LMB_s2 
      15.9997558594 
      Fryuynd_aryqffa_FmndnDc_n_aoo45 
      16 
      -8 
      7.99975585938

        DISPLAY_IDENTIFIER DI.ASAM.C.SCALAR.SBYTE.IDENTICAL 
        READ_ONLY
                BYTE_ORDER MSB_FIRST
      ECU_ADDRESS_EXTENSION 0x0
      EXTENDED_LIMITS -8 7.99975585938
      DEPOSIT ABSOLUTE
                /begin FUNCTION_LIST
                    FunctionVirtualMeasurements
                    FunctionVirtualMeasurements
                    FunctionVirtualMeasurements
                /end FUNCTION_LIST
                /begin ANNOTATION
                    ANNOTATION_LABEL "ASAM Workinggroup"
                    ANNOTATION_ORIGIN ""
                    /begin ANNOTATION_TEXT
                        "Test the A2L annotation 3 "
                        "Test the A2L annotation 4 "
                    /end ANNOTATION_TEXT
                /end ANNOTATION
                REF_MEMORY_SEGMENT CAL_asd
                GUARD_RAILS
      FORMAT "%6.3"
      EXTENDED_LIMITS -8 7.99975585938
            /begin IF_DATA asd
            /end IF_DATA
            CALIBRATION_ACCESS CALIBRATION
    /end AXIS_PTS
            /begin IF_DATA asd
            /end IF_DATA
            /begin CHARACTERISTIC AirChrgrCoorr_SpdRefForCmprHi_C "Air Charger Coordinator _ Speed Reference For Compressor High _ Calibration Value"
      VALUE 0x50002D3A _REC_S1VAL_60_LMB_s2 524280 lAagFra_pBustdb_cAsAEha_1nR_oa0 -262144 262136
      ECU_ADDRESS_EXTENSION 0x0
      EXTENDED_LIMITS -262144 262136
      FORMAT "%6.3"
    /end CHARACTERISTIC
    /begin CHARACTERISTIC AirChrgrMdl_TestSubOfCmprTOutl_C "Air Charger Model _ Test Substitute Of Compressor Temperature Outlet _ Calibration Value"
      VALUE 0x50002DF0 _REC_S1VAL_60_LMB_s2 1123.96875 fzyBCrc_bErjugb_Fgjzexb_qR0ao3e -100 1023.96875
      ECU_ADDRESS_EXTENSION 0x0
      EXTENDED_LIMITS -100 1023.96875
      FORMAT "%6.3"
    /end CHARACTERISTIC
            /begin CHARACTERISTIC ASAM.C.SCALAR.UBYTE.IDENTICAL
                "Scalar FW U16 and CDF20 as name"
                VALUE
                0x7140
                RL.FNC.SBYTE.ROW_DIR
                0
                CM.IDENTICAL
                10 200
                EXTENDED_LIMITS 0 256
                NUMBER 42
                READ_ONLY
                DISPLAY_IDENTIFIER DI.ASAM.C.SCALAR.SBYTE.IDENTICAL
                FORMAT "%6.1"
                REF_MEMORY_SEGMENT SEC_CONST.UNSPECIFIED
                /begin VIRTUAL_CHARACTERISTIC
                    "X1 - 9"
                    ASAM.C.SCALAR.SBYTE.IDENTICAL                     /* used as input X1 variable in teh dependent formula */
                /end VIRTUAL_CHARACTERISTIC
                BIT_MASK 0x0FF0
                /begin DEPENDENT_CHARACTERISTIC
                    "X1 + 5"
                    ASAM.C.SCALAR.SBYTE.IDENTICAL                     /* used as input X1 variable in teh dependent formula */
                /end DEPENDENT_CHARACTERISTIC
                BYTE_ORDER MSB_LAST
                CALIBRATION_ACCESS CALIBRATION
                /begin ANNOTATION
                    ANNOTATION_LABEL "ASAM Workinggroup"
                    ANNOTATION_ORIGIN ""
                    /begin ANNOTATION_TEXT
                        "Test the A2L annotation 1 "
                        "Test the A2L annotation 2 "
                    /end ANNOTATION_TEXT
                /end ANNOTATION
                /begin AXIS_DESCR /* description of X-axis points */
COM_AXIS N /* common axis points, input quantity
*/
CONV_N 14 /* conversion, max. no. of axis p.*/
0.0 5800.0 /* lower limit, upper limit */
/end AXIS_DESCR
                /begin IF_DATA XCP
                /end IF_DATA
                MAX_REFRESH 3 15
                MATRIX_DIM 2 4 3
                /begin FUNCTION_LIST
                    FunctionVirtualMeasurements
                    FunctionVirtualMeasurements
                    FunctionVirtualMeasurements
                /end FUNCTION_LIST
                /begin ANNOTATION
                    ANNOTATION_LABEL "ASAM Workinggroup"
                    ANNOTATION_ORIGIN ""
                    /begin ANNOTATION_TEXT
                        "Test the A2L annotation 3 "
                        "Test the A2L annotation 4 "
                    /end ANNOTATION_TEXT
                /end ANNOTATION
                /begin MAP_LIST
                    FunctionVirtualMeasurements
                    FunctionVirtualMeasurements
                    FunctionVirtualMeasurements
                /end MAP_LIST
                COMPARISON_QUANTITY blah.blah.blah__
                ECU_ADDRESS_EXTENSION 1
            /end CHARACTERISTIC
            /begin IF_DATA asd
            /end IF_DATA
            /begin MEASUREMENT N /* name */
                "Engine speed" /* long identifier */
                UWORD /* datatype */
                R_SPEED_3 /* conversion */
                2 /* resolution */
                2.5 /* accuracy */
                120.0 /* lower limit */
                8400.0 /* upper limit */
                /begin BIT_OPERATION
                    RIGHT_SHIFT 4 /*4 positions*/
                    SIGN_EXTEND
                /end BIT_OPERATION
            /begin IF_DATA asd
            /end IF_DATA
                BIT_MASK 0x0FF0
                /begin ANNOTATION
                    ANNOTATION_LABEL "ASAM Workinggroup"
                    ANNOTATION_ORIGIN ""
                    /begin ANNOTATION_TEXT
                        "Test the A2L annotation 3 "
                        "Test the A2L annotation 4 "
                    /end ANNOTATION_TEXT
                /end ANNOTATION
                MAX_REFRESH 3 15
                BYTE_ORDER MSB_FIRST
                /begin FUNCTION_LIST
                    FunctionVirtualMeasurements
                    FunctionVirtualMeasurements
                    FunctionVirtualMeasurements
                /end FUNCTION_LIST
      FORMAT "%5.0"
      READ_WRITE
                DISPLAY_IDENTIFIER DI.ASAM.C.SCALAR.SBYTE.IDENTICAL
                /begin ANNOTATION
                    ANNOTATION_LABEL "ASAM Workinggroup"
                    ANNOTATION_ORIGIN ""
                    /begin ANNOTATION_TEXT
                        "Test the A2L annotation 3 "
                        "Test the A2L annotation 4 "
                    /end ANNOTATION_TEXT
                /end ANNOTATION
                ECU_ADDRESS 0x12FE
                ERROR_MASK 0x00000001
                ECU_ADDRESS_EXTENSION 0x0
                MATRIX_DIM 2 4 3
                REF_MEMORY_SEGMENT SEC_VAR.FAST
                /begin VIRTUAL PHI_BASIS PHI_CORR
/end VIRTUAL
             ARRAY_SIZE 16                                        /* Note: ARRAY_SIZE allows only 1 dimension. For more dimensions use MATRIX_DIM */
     /end MEASUREMENT
            /begin COMPU_METHOD CM.IDENTICAL
      "conversion that delivers always phys = int"
      IDENTICAL "%3.0" "hours"
      COEFFS -0 +1 -0.2 +0.4 123123.123 -1
      REF_UNIT kms_per_hour
      COMPU_TAB_REF TMPCON1

      /begin FORMULA "a * x + b" /end FORMULA
            /end COMPU_METHOD
            /begin COMPU_TAB
            TT /* name */
"conversion table for oil temperatures"
 TAB_NOINTP /* convers_type */
7 /* number_value_pairs */ 
1 4.3 2 4.7 3 5.8 4 14.2 
5 16.8 6 17.2 7 19.4
DEFAULT_VALUE "out of range..."
            /end COMPU_TAB
            /begin COMPU_VTAB
            TT /* name */ "engine status conversion"
TAB_VERB 4
0 "engine off"
1 "idling"
2 "partial load"
3 "full load"
DEFAULT_VALUE "i'm the default..."
            /end COMPU_VTAB
            /begin COMPU_VTAB_RANGE
            TT
            "engine conversion"
            5
            0 0 "ONE"
            1 2 "fist section"
            3 3 "THREE"
            4 5 "second section"
            6 500 "usual_case"
            DEFAULT_VALUE "value_out_of.range"
            /end COMPU_VTAB_RANGE




            /begin FUNCTION ID_ADJUSTM /* name */
                "function group idling adjustment"
                /begin DEF_CHARACTERISTIC
                    INJECTION_CURVE
                /end DEF_CHARACTERISTIC 
                /begin REF_CHARACTERISTIC 
                    FACTOR_1                    
                /end REF_CHARACTERISTIC 
                /begin IN_MEASUREMENT
                    WHEEL_REVOLUTIONS ENGINE_SPEED
                /end IN_MEASUREMENT 
                /begin OUT_MEASUREMENT 
                    OK_FLAG SENSOR_FLAG
                /end OUT_MEASUREMENT 
                /begin LOC_MEASUREMENT
                    LOOP_COUNTER TEMPORARY_1
                /end LOC_MEASUREMENT 
                /begin SUB_FUNCTION
                    ID_ADJUSTM_SUB
                /end SUB_FUNCTION 
            /end FUNCTION




            /begin GROUP SOFTWARE_COMPONENTS "assignment of the definitions to C files"
            /begin REF_CHARACTERISTIC INJECTION_CURVE /end REF_CHARACTERISTIC
/begin REF_MEASUREMENT LOOP_COUNTER TEMPORARY_1 /end REF_MEASUREMENT
ROOT
/begin SUB_GROUP INJE C6TD
/end SUB_GROUP /end GROUP
            /begin RECORD_LAYOUT DAMOS_KF
FNC_VALUES 7 SWORD COLUMN_DIR DIRECT
AXIS_PTS_X 3 SWORD INDEX_INCR DIRECT
AXIS_PTS_Y 6 UBYTE INDEX_INCR DIRECT
NO_AXIS_PTS_X 2 UBYTE
NO_AXIS_PTS_Y 5 UBYTE
SRC_ADDR_X 1
SRC_ADDR_Y 4
ALIGNMENT_BYTE 2
IDENTIFICATION 1 UWORD
/end RECORD_LAYOUT
            /begin VARIANT_CODING
VAR_SEPARATOR "." /* PUMKF.1 */
VAR_NAMING NUMERIC 
/* variant criterion "Car body" with three variants */
/begin VAR_CRITERION Car "Car body" Limousine Kombi Cabrio
/end VAR_CRITERION
/* variant criterion "Type of gear box" with two variants */
/begin VAR_CRITERION Gear "Type of gear box" Manual Automatic
/end VAR_CRITERION
/begin VAR_FORBIDDEN_COMB /* forbidden: Limousine - Manual */
Car Limousine
Gear Manual
/end VAR_FORBIDDEN_COMB
/begin VAR_FORBIDDEN_COMB /* forbidden: Cabrio - Automatic */
Car Cabrio
Gear Automatic
/end VAR_FORBIDDEN_COMB
/begin VAR_CHARACTERISTIC PUMKF /* define PUMKF as variant coded */
Gear /* Gear box variants */
/begin VAR_ADDRESS
0x7140 0x7168
/end VAR_ADDRESS
/end VAR_CHARACTERISTIC
/begin VAR_CHARACTERISTIC NLLM /* define NLLM as variant coded */
Gear Car /* car body and gear box variants */
/begin VAR_ADDRESS
0x8840 0x8858 0x8870 0x8888
/end VAR_ADDRESS
/end VAR_CHARACTERISTIC
/* forbidden variant combination (doesn't exist in control unit software): */
/begin VAR_FORBIDDEN_COMB
Car Limousine /* variant value 'Limousine' of criterion 'Car' */
Gear Manual /* variant value 'Manual' of criterion 'Gear' */
/end VAR_FORBIDDEN_COMB
/* variant criterion "Car body" with three variants */
/begin VAR_CRITERION Car "Car body"
/* Enumeration of criterion values */
Limousine Kombi Cabrio
VAR_MEASUREMENT S_CAR
VAR_SELECTION_CHARACTERISTIC V_CAR
/end VAR_CRITERION
VAR_SEPARATOR "." /* example: "PUMKF.1" */
/* three parts of variant coded adjustable objects name: */
/* 1.) Identifier of adjustable object: "PUMKF" */
/* 2.) Separator: "." (decimal point) */
/* 3.) Variants extension: "1" */
VAR_NAMING NUMERIC
/end VARIANT_CODING
/begin FRAME ABS_ADJUSTM
"function group ABS adjustment"
3
2 /* 2 msec. */
FRAME_MEASUREMENT LOOP_COUNTER TEMPORARY_1
/end FRAME


/begin USER_RIGHTS application_engineers
/begin REF_GROUP group_1 /end REF_GROUP
/end USER_RIGHTS
/begin USER_RIGHTS measurement_engineers
/begin REF_GROUP group_1 group_2 /end REF_GROUP
READ_ONLY
/end USER_RIGHTS
/begin UNIT
metres_per_second
"extended SI unit for velocity"
            "[m/s]"
EXTENDED_SI
SI_EXPONENTS 1 0 -1 0 0 0 0 /* [m] * [s]-1 */
/end UNIT
/begin UNIT
kms_per_hour
"derived unit for velocity: kilometres per hour"
"[km/h]"
EXTENDED_SI
SI_EXPONENTS 0 0 0 0 1 0 0
REF_UNIT metres_per_second
UNIT_CONVERSION 3.6 0.0 /* y [km/h] = (60*60/1000) * x [m/s] + 0.0
*/
/end UNIT
/begin UNIT
miles_per_hour
"derived unit for velocity: miles per hour"
"[mph]"
DERIVED
REF_UNIT metres_per_second
UNIT_CONVERSION 2.237 0.0 /* y [mph] = (60*60/1609) * x [m/s] + 0.0
*/
/end UNIT
        /end MODULE
    /end PROJECT""")

    a = parser
    print a
