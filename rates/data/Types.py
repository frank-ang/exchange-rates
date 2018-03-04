"""
Defines data value classes
"""
__author__ = "Frank Ang"


class PriceUpdate:
    """
    <timestamp> <exchange> <source_currency> <destination_currency> <forward_factor> <backward_factor>
    E.g.: 2017-11-01T09:42:23+00:00 KRAKEN BTC USD 1000.0 0.0009
    """

    def __init__(self, timestamp, exchange, source_currency, destination_currency, forward_factor, backward_factor):
        self.timestamp = timestamp
        self.exchange = exchange
        self.source_currency = source_currency
        self.destination_currency = destination_currency
        self.forward_factor = forward_factor
        self.backward_factor = backward_factor


class ExchangeRateRequest:
    """
    EXCHANGE_RATE_REQUEST <source_exchange> <source_currency> <destination_exchange> <destination_currency>
    E.g.: EXCHANGE_RATE_REQUEST KRAKEN USD GDAX BTC
    """

    def __init__(self, source_exchange, source_currency, destination_exchange, destination_currency):
        self.source_exchange = source_exchange
        self.source_currency = source_currency
        self.destination_exchange = destination_exchange
        self.destination_currency = destination_currency


class BestRate(ExchangeRateRequest):
    """
    The response to an ExchangeRateRequest. Formatted into text as:
    BEST_RATES_BEGIN
    <source_exchange> <source_currency> <destination_exchange> <destination_currency> <rate>
    <source_exchange, source_currency>
    <exchange, currency>
    <exchange, currency>
    ...
    <destination_exchange, destination_currency>
    BEST_RATES_END
    """

    def __init__(self, source_exchange, source_currency, destination_exchange, destination_currency, rate, path):
        self.rate = rate
        self.path = path
        super(BestRate, self).__init__(source_exchange, source_currency, destination_exchange, destination_currency)

    def to_string(self):
        s = "BEST_RATES_BEGIN\n{} {} {} {} {}\n".format(self.source_exchange, self.source_currency,
                                                           self.destination_exchange, self.destination_currency,
                                                           self.rate)
        for v in self.path:
            s += "{}, {}\n".format(v[0], v[1])
        s += "BEST_RATES_END"
        return s



