from .Types import PriceUpdate, ExchangeRateRequest
import dateutil.parser


class InputParser:
    """
    Converts from strings to program instructions.
    """
    PRICE_UPDATE_FIELD_COUNT = 6
    EXCHANGE_RATE_REQUEST_FIELD_COUNT = 5
    EXCHANGE_RATE_REQUEST_PREFIX = "EXCHANGE_RATE_REQUEST"

    def __init__(self):
        pass

    def parse(self, line):
        try:
            fields = line.split()
            if len(fields) == self.PRICE_UPDATE_FIELD_COUNT:
                return PriceUpdate(timestamp = dateutil.parser.parse(fields[0]),
                                   exchange = fields[1],
                                   source_currency = fields[2],
                                   destination_currency = fields[3],
                                   forward_factor = fields[4],
                                   backward_factor = fields[5])

            elif len(fields) == self.EXCHANGE_RATE_REQUEST_FIELD_COUNT \
                    and fields[0] == self.EXCHANGE_RATE_REQUEST_PREFIX:
                return ExchangeRateRequest(source_exchange=fields[1],
                                           source_currency=fields[2],
                                           destination_exchange=fields[3],
                                           destination_currency=fields[4])

            else:
                return None

        except Exception as exc:
            raise ParseException("Invalid input: {}".format(line)) from exc


class ParseException(Exception):
    def __init__(self, message):
        super().__init__(message)
