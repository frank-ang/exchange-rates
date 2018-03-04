"""
Unit tests.
"""
__author__ = "Frank Ang"


import unittest
from rates.graph.ExchangeGraph import ExchangeGraph
from rates.data.Types import PriceUpdate, ExchangeRateRequest
from rates.data.InputParser import InputParser


class TestExchangeGraph(unittest.TestCase):

    exchange_graph = ExchangeGraph()
    parser = InputParser()

    def test_KRAKENUSD_GDAXBTC(self):
        test_input = ["2017-11-01T09:00:00+00:00 KRAKEN BTC USD 1000.0 0.0009",
                      "2017-11-01T09:00:00+00:00 GDAX BTC USD 1001.0 0.0008",
                      "EXCHANGE_RATE_REQUEST KRAKEN USD GDAX BTC"]
        result = self.helper_send_instructions(test_input)
        self.assertEqual(1, len(result))
        self.assertEqual("BEST_RATES_BEGIN\nKRAKEN USD GDAX BTC 0.0009\nKRAKEN, USD\nKRAKEN, BTC\nGDAX, BTC\nBEST_RATES_END",
                         result[0].to_string())

    def test_GDAXUSD_KRAKENBTC(self):
        test_input = ["2017-11-01T09:10:00+00:00 KRAKEN BTC USD 1000.0 0.0009",
                      "2017-11-01T09:10:00+00:00 GDAX BTC USD 1001.0 0.0008",
                      "EXCHANGE_RATE_REQUEST GDAX USD KRAKEN BTC"]
        result = self.helper_send_instructions(test_input)
        self.assertEqual(1, len(result))
        self.assertEqual("BEST_RATES_BEGIN\nGDAX USD KRAKEN BTC 0.0009\nGDAX, USD\nKRAKEN, USD\nKRAKEN, BTC\nBEST_RATES_END",
                         result[0].to_string())

    def test_out_of_sequence_update(self):
        test_input = ["2017-11-01T09:20:10+00:00 KRAKEN BTC USD 1000.0 0.0009",
                      "2017-11-01T09:20:09+00:00 KRAKEN BTC USD 1001.0 0.0010",
                      "2017-11-01T09:20:08+00:00 KRAKEN USD BTC 0.0010 1001.0",
                      "2017-11-01T09:20:09+00:00 KRAKEN BTC USD 1001.0 0.0010",
                      "2017-11-01T09:20:10+00:00 GDAX BTC USD 1001.0 0.0008",
                      "EXCHANGE_RATE_REQUEST KRAKEN USD GDAX BTC"]
        result = self.helper_send_instructions(test_input)
        self.assertEqual(1, len(result))
        self.assertEqual("BEST_RATES_BEGIN\nKRAKEN USD GDAX BTC 0.0009\nKRAKEN, USD\nKRAKEN, BTC\nGDAX, BTC\nBEST_RATES_END",
                         result[0].to_string())

    def test_multiple_rate_requests(self):
        test_input = ["2017-11-01T09:30:10+00:00 KRAKEN BTC USD 1000.0 0.0009",
                      "2017-11-01T09:30:10+00:00 GDAX BTC USD 1001.0 0.0008",
                      "EXCHANGE_RATE_REQUEST GDAX USD KRAKEN BTC",
                      "2017-11-01T09:30:11+00:00 KRAKEN BTC USD 1009.0 0.0006",
                      "2017-11-01T09:30:11+00:00 GDAX BTC USD 1002.0 0.0007",
                      "EXCHANGE_RATE_REQUEST KRAKEN USD GDAX BTC"]
        result = self.helper_send_instructions(test_input)
        self.assertEqual(2, len(result))
        self.assertEqual(0.0009, result[0].rate)
        self.assertEqual(0.0007, result[1].rate)
        self.assertTrue("KRAKEN, USD\nGDAX, USD\nGDAX, BTC" in result[1].to_string())

    def helper_send_instructions(self, test_input):
        best_rate_list = []
        for s in test_input:
            instruction = self.parser.parse(s)
            if isinstance(instruction, PriceUpdate):
                self.exchange_graph.update_currency_pair(instruction)
            elif isinstance(instruction, ExchangeRateRequest):
                best_rate = self.exchange_graph.find_optimal_exchange_rate(instruction)
                best_rate_list.append(best_rate)
                print("{}\n".format(best_rate.to_string()))
        return best_rate_list


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestExchangeGraph('test_KRAKENUSD_GDAXBTC'))
    suite.addTest(TestExchangeGraph('test_GDAXUSD_KRAKENBTC'))
    suite.addTest(TestExchangeGraph('test_out_of_sequence_update'))
    suite.addTest(TestExchangeGraph('test_multiple_rate_requests'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())

