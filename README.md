# Exchange Rate
Solution to the Exchange Rate Path Problem.

This is an implementation of a modified Floyd-Warshall algorithm to find:
 * the most favorable exchange rate, between any 2 (exchange,currency) pairs. 
 * and the sequence of conversions to attain that rate,

## Running the program 
Simply run using python3.  
```bash
python3 main.py
```
Input data can be from pipes, file redirection, or interactive.

To stop the program, send EOF character.


## Testing
### Unit Tests
```bash
python3 -m rates.test.test_ExchangeGraph
```

### Command line test with file input
```
python3 main.py < rates/test/input1.txt
cat rates/test/input2.txt | python3 main.py 
```

### Sample Output
Run the Unit Tests!
```bash
$ python3 -m rates.test.test_ExchangeGraph
BEST_RATES_BEGIN
KRAKEN USD GDAX BTC 0.0009
KRAKEN, USD
KRAKEN, BTC
GDAX, BTC
BEST_RATES_END

.BEST_RATES_BEGIN
GDAX USD KRAKEN BTC 0.0009
GDAX, USD
KRAKEN, USD
KRAKEN, BTC
BEST_RATES_END

.BEST_RATES_BEGIN
KRAKEN USD GDAX BTC 0.0009
KRAKEN, USD
KRAKEN, BTC
GDAX, BTC
BEST_RATES_END

.BEST_RATES_BEGIN
GDAX USD KRAKEN BTC 0.0009
GDAX, USD
KRAKEN, USD
KRAKEN, BTC
BEST_RATES_END

BEST_RATES_BEGIN
KRAKEN USD GDAX BTC 0.0007
KRAKEN, USD
GDAX, USD
GDAX, BTC
BEST_RATES_END

.
----------------------------------------------------------------------
Ran 4 tests in 0.003s

OK
```
Run the Integration Test on command line! 

Redirect input instructions into the program from a data file.
```bash
$ python3 main.py < rates/test/input1.txt 
Exchange Rate Optimization Pathfinder solution.
Copyright © 2018 Frank Ang https://www.linkedin.com/in/frankang/
--------------------------------------------------
BEST_RATES_BEGIN
KRAKEN USD GDAX BTC 0.0009
KRAKEN, USD
KRAKEN, BTC
GDAX, BTC
BEST_RATES_END
End of program. Thank you for trading.
```



## Exchange Rate Path Problem
The following section was excerpted from the Technical Exercise document.
Reproduced here for reference.

### Input Data
Receive a stream of price updates and exchange rate requests on stdin.
Each price update or exchange rate request will be separated by a newline.

#### Price Updates
The price updates will be of the form:
```
<timestamp> <exchange> <source_currency> <destination_currency> <forward_factor> <backward_factor>
```
E.g.
```
2017-11-01T09:42:23+00:00 KRAKEN BTC USD 1000.0 0.0009
```
I.e. price update was received from Kraken on November 1, 2017 at 9:42am. 
The update says that 1 BTC is worth $1000 USD and that $1 USD is worth
0.0009 BTC.

The forward_factor and backward_factor will always multiply to a number 
that is less than or equal to 1

Price updates are not guaranteed to arrive in chronological order. 

You should only consider the most recent price update for each 
`(source_currency, destination_currency)` pair 
when responding to an exchange rate request.

#### Exchange Rate Requests 

```
EXCHANGE_RATE_REQUEST <source_exchange> <source_currency> <destination_exchange> <destination_currency>
```
I.e., the question: What is the best exchange rate 
for converting source_currency on source_exchange 
into destination_currency on destination_exchange, 
and what trades and transfers need to be made to achieve that rate?

### The Exchange Rate Graph
Each `(exchange, currency)` pair can be considered as a vertex in a graph. Vertices
are created the first time a price update appears that references them.

### Finding the Best Exchange Rate
When you receive an exchange rate request, your job is to return the best possible
exchange rate as well as the trades and transfers needed to achieve that rate.

