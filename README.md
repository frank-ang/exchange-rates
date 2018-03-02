# Exchange Rate
## Input Data
Receive a stream of price updates and exchange rate requests on stdin.
Each price update or exchange rate request will be separated by a newline.

### Price Updates
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

### Exchange Rate Requests 

```
EXCHANGE_RATE_REQUEST <source_exchange> <source_currency> <destination_exchange> <destination_currency>
```
I.e., the question: What is the best exchange rate 
for converting source_currency on source_exchange 
into destination_currency on destination_exchange, 
and what trades and transfers need to be made to achieve that rate?

## The Exchange Rate Graph
Each `(exchange, currency)` pair can be considered as a vertex in a graph. Vertices
are created the first time a price update appears that references them.

## Finding the Best Exchange Rate
When you receive an exchange rate request, your job is to return the best possible
exchange rate as well as the trades and transfers needed to achieve that rate.

## Output Format
For each exchange rate request line you receive on stdin, you should output to
stdout:

```
BEST_RATES_BEGIN <source_exchange> <source_currency> <destination_exchange>
<destination_currency> <rate>
<source_exchange, source_currency>
<exchange, currency>
<exchange, currency>
...
<destination_exchange, destination_currency>
BEST_RATES_END
```