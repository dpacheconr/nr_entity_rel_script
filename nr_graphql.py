from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

class nr_graphql():
    def run_query(newrelic_user_key,nrql_query):
        nr_headers = {'Content-Type': 'application/json', 'Api-Key': str(newrelic_user_key)}
        transport = AIOHTTPTransport(url="https://api.newrelic.com/graphql", headers=nr_headers)
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql(nrql_query)
        vars = {}
        result = client.execute(query, variable_values=vars)
        return result

if __name__ == "__main__":
    nr_graphql.run_query()