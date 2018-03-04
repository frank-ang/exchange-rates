"""
The Main processor loop for ExchangeRates
Waits for and parses PriceUpdate and ExchangeRateRequest inputs by line.
Prints BestRate responses to stdout.
"""
__author__ = "Frank Ang"


import sys
from rates.data.InputParser import InputParser, ParseException
from rates.data.Types import PriceUpdate, ExchangeRateRequest
from rates.graph.ExchangeGraph import ExchangeGraph

class ExchangeRatesProcessor:

    exchange_graph = None
    parser = InputParser()

    def __init__(self):
        print("Exchange Rate Optimization Pathfinder solution.")
        print("Copyright © 2018 Frank Ang https://www.linkedin.com/in/frankang/")
        print("--------------------------------------------------")
        self.exchange_graph = ExchangeGraph()

    def execute(self):
        while True:
            try:
                line = input()
                instruction = self.parser.parse(line)
                # this is either a PriceUpdate or ExchangeRateRequest.
                # if PriceUpdate, update the graph
                if isinstance(instruction, PriceUpdate):
                    self.exchange_graph.update_currency_pair(instruction)
                # else, compute rate path.
                elif isinstance(instruction, ExchangeRateRequest):
                    best_rate = self.exchange_graph.find_optimal_exchange_rate(instruction)
                    print(best_rate.to_string())

                else:
                    pass

            except ParseException:
                print("ParseException: {}".format(sys.exc_info()[0]))

            except EOFError:
                print("End of program. Thank you for trading.")
                break

            except Exception:
                print("Unknown exception: {}".format(sys.exc_info()[0]))


if __name__== "__main__":
    processor = ExchangeRatesProcessor()
    processor.execute()