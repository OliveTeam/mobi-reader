import struct
import sys

# Reference for the format available here: https://wiki.mobileread.com/wiki/PDB#Palm_Database_Format
PALM_DB_HEADERS_FMT = '>32shhIIIIII4s4sIIH'
PALM_DB_RECORDS_FMT = '>II'
PALM_DB_INFO = {
    'headersInfo': {
        'fmt': PALM_DB_HEADERS_FMT,
        'len': struct.calcsize(PALM_DB_HEADERS_FMT),
        'fields': [
            'name',
            'attributes',
            'version',
            'createdDate',
            'modifiedDate',
            'lastBackupDate',
            'modificationNumber',
            'appInfoID',
            'sortInfoID',
            'type',
            'creator',
            'uniqueIDseed',
            'nextRecordListID',
            'numberOfRecords'
        ]
    },
    'recordsInfo': {
        'fmt': PALM_DB_RECORDS_FMT,
        'len': struct.calcsize(PALM_DB_RECORDS_FMT),
        'fields': [
            'recordDataOffset',
            'UniqueID'
        ]
    }
}


class PalmDBParser:
    def __init__(self):
        pass

    @staticmethod
    def parse(file_name):
        try:
            file = None
            offset = 0
            if isinstance(file_name, str):
                file = open(file_name, "rb")
            else:
                file = file_name

            content = file.read()

            headers = PalmDBParser.extract_headers(content, offset)
            records = PalmDBParser.extract_records(
                content,
                PalmDBParser.get_offset_record(offset),
                headers['numberOfRecords'])
            return {
                'headers': headers,
                'records': records
            }
        except IOError as error:
            sys.stderr.write("Unable to open %s! " % file_name)
            raise error

    @staticmethod
    def extract_headers(content, offset):
        """

        :type content: bytes
        :type offset: int
        :param content: 
        :param offset: 
        :return.
        :rtype: dict
        """
        return PalmDBParser.to_dict(
            zip(
                PALM_DB_INFO['headersInfo']['fields'],
                struct.unpack(
                    PALM_DB_INFO['headersInfo']['fmt'],
                    content[offset:offset + PALM_DB_INFO['headersInfo']['len']]
                )
            )
        )

    @staticmethod
    def extract_records(content, offset, number_of_records):
        """

        :type content: bytes
        :type offset: int
        :type number_of_records: int
        :param content:
        :param offset:
        :param number_of_records:
        :return:
        :rtype: list of dict
        """
        return [
            PalmDBParser.extract_single_record(
                content,
                offset + record_index * PALM_DB_INFO['recordsInfo']['len']
            ) for record_index in range(number_of_records)
        ]

    @staticmethod
    def extract_single_record(content, offset):
        record = PalmDBParser.to_dict(
            zip(
                PALM_DB_INFO['recordsInfo']['fields'],
                struct.unpack(
                    PALM_DB_INFO['recordsInfo']['fmt'],
                    content[offset:offset + PALM_DB_INFO['recordsInfo']['len']]
                )
            )
        )
        # TODO: do this directly with fmt ?
        record['recordAttributes'] = (record['UniqueID'] & 0xFF000000) >> 24
        record['UniqueID'] = record['UniqueID'] & 0x00FFFFFF
        return record

    @staticmethod
    def get_offset_record(initial_offset):
        return initial_offset + PALM_DB_INFO['headersInfo']['len']

    @staticmethod
    def to_dict(tuples):
        results_dict = {}
        for field, value in tuples:
            if len(field) > 0 and field[0] != "-":
                results_dict[field] = value
        return results_dict
