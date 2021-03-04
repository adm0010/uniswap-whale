from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from coinmarketcapapi import CoinMarketCapAPI, CoinMarketCapAPIError

from datetime import datetime

sample_transport=RequestsHTTPTransport(
    url='https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2',
    verify=True,
    retries=3,
)
client = Client(
    transport=sample_transport
)


large_amount = 1000
first_amount = 1000
token_tx_id = ""
token_name = "BOND"

cmc = CoinMarketCapAPI('6c43df37-3c8e-4875-8b24-bb98bd3e21dd') # Sandbox environnement

try:
    r = cmc.cryptocurrency_quotes_latest(symbol=token_name)
except CoinMarketCapAPIError as e:
    r = e.rep




print("Current price: $" + (repr (r.data[token_name]['quote']['USD']['price'])))

token_price = (r.data[token_name]['quote']['USD']['price'])


#Important!!! PAIR
pair = "0x6591c4bcd6d7a1eb4e537da8b78676c1576ba244"



query = gql('''
query {
  swaps(first: ''' + str(first_amount) + ''', where: { pair: "''' + pair + '''" } orderBy: timestamp, orderDirection: desc) {
      transaction {
        timestamp
      }
      
      amount0In
      amount0Out
      amount1In
      amount1Out
      amountUSD
      to
    }
}
''')

response = client.execute(query)

i = first_amount-1
while i > 0:
    inflow = response['swaps'][i]
    inflow_select = response['swaps'][i]['amount0In']
    #print (inflow_select + " "+ token_name )
    if int((float(inflow_select))) > large_amount:
        ts = (int(response['swaps'][i]['transaction']['timestamp']))
        print (str(int((float(inflow_select)))) + " "+ "$" + token_name + " ---------> "
               + str(int(float(response['swaps'][i]['amountUSD'])))
               + " USD" +
               " @ " + (str(int(float(response['swaps'][i]['amountUSD']) / (float(inflow_select))))) + " USD" 

               + " | " +
               (datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))
        
    i = i-1

#print(response)

