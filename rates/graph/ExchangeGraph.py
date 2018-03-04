"""
Implementation as a modified Floyd-Warshall algorithm to find:
 * the most favorable exchange rate,
 * and the sequence of conversions to attain that rate,
between any 2 (exchange,currency) pairs.

:return:
   rates 2-dimensional dictionary of optimal rates
   preds 2-dimensional dictionary of predecessors in route
"""
__author__ = "Frank Ang"


from rates.data.Types import BestRate
import pprint


class ExchangeGraph:

    STARTING_USDBTC = 0.0009
    STARTING_BTCUSD = 1000

    # Available exchange,currency pairs.
    # Currently does not permit adding new pairs.
    # TODO: add feature request to sprint backlog.
    exchange_currency = [("KRAKEN", "USD"),
                         ("KRAKEN", "BTC"),
                         ("GDAX", "USD"),
                         ("GDAX", "BTC")]

    # dictionary of pairs -> timestamps
    exchange_currency_last_updated = {}

    # Adjacency matrix of optimal rates
    rates = {0: {}, 1: {}, 2: {}, 3: {}}

    pp = pprint.PrettyPrinter()

    def __init__(self):
        self.init_adjacency_matrix()

    def init_adjacency_matrix(self, exchange_currency=exchange_currency):
        rates = self.rates
        for row, rTuple in enumerate(exchange_currency):
            for col, cTuple in enumerate(exchange_currency):
                if row == col:
                    rates[row][col] = 0
                elif rTuple[0] == cTuple[0]:  # same exchange
                    if rTuple[1] == "USD" and cTuple[1] == "BTC":
                        self.rates[row][col] = self.STARTING_USDBTC
                    elif rTuple[1] == "BTC" and cTuple[1] == "USD":
                        self.rates[row][col] = self.STARTING_BTCUSD
                elif rTuple[1] == cTuple[1]:  # same currency
                    self.rates[row][col] = 1
        #print("Initialized starting matrix:")
        #self.pp.pprint(self.rates)

    def update_currency_pair(self, price_update):
        """
        updates the rates matrix.
        out-of-sequence timestamped updates are ignored.
        :param price_update: PriceUpdate data object
        """
        if not self.is_latest_update(price_update):
            return
        p = price_update
        src = self.exchange_currency.index((p.exchange, p.source_currency))
        tgt = self.exchange_currency.index((p.exchange, p.destination_currency))
        self.rates[src][tgt] = float(p.forward_factor)   # TODO consider using Decimal type instead of float
        self.rates[tgt][src] = float(p.backward_factor)  #
        self.exchange_currency_last_updated[(p.exchange, p.source_currency)] = p.timestamp
        self.exchange_currency_last_updated[(p.exchange, p.destination_currency)] = p.timestamp

    def is_latest_update(self, price_update):
        """boolean check if the price_update is the latest available"""
        key = (price_update.exchange, price_update.source_currency)
        try:
            if self.exchange_currency_last_updated[key] > price_update.timestamp:
                return False
        except KeyError as err:
            pass
        return True

    def _find_optimal_paths(self, rates=rates):
        # Initialize dist and pred
        # copy graph into dist
        # set None where there is no edge
        dist = {}
        pred = {}
        for u in rates:
            dist[u] = {}
            pred[u] = {}
            for v in rates:
                dist[u][v] = 0
                pred[u][v] = None
            for neighbor in rates[u]:
                dist[u][neighbor] = rates[u][neighbor]
                pred[u][neighbor] = u

        for t in rates:
            # given dist u to v, check if path u - t - v is a better rate
            for u in rates:
                for v in rates:
                    newdist = dist[u][t] * dist[t][v]
                    if newdist > dist[u][v]:
                        dist[u][v] = newdist
                        pred[u][v] = pred[t][v]  # route new path through t

        return dist, pred

    def find_optimal_exchange_rate(self, exchange_rate_request):
        """
        find best exchange rate for converting source_currency on source_exchange
        into destination_currency on destination_exchange,
        and what trades and transfers need to be made to achieve that rate
        :return: BestRate object
        """
        dist, pred = self._find_optimal_paths()
        rq = exchange_rate_request
        src = self.exchange_currency.index((rq.source_exchange, rq.source_currency))
        dst = self.exchange_currency.index((rq.destination_exchange, rq.destination_currency))
        rate = dist[src][dst]
        path = [self.exchange_currency[src]]
        row = pred[src]
        cursor = row[dst]
        while cursor != src:
            path.append(self.exchange_currency[cursor])
            cursor = row[cursor]
        path.append(self.exchange_currency[dst])
        best_rate = BestRate(rq.source_exchange, rq.source_currency, rq.destination_exchange, rq.destination_currency, rate, path)
        return best_rate
