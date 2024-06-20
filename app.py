import os
from nr_graphql import nr_graphql


account_id = os.getenv('NEWRELIC_ACCOUNT_ID')
newrelic_user_key = os.getenv('NEWRELIC_USER_KEY') 

current_configurations = {}
env_vars_checked = False

def check_env_vars():
    global env_vars_checked
    keys = ("NEWRELIC_ACCOUNT_ID","NEWRELIC_USER_KEY")
    keys_not_set = []

    for key in keys:
        if key not in os.environ:
            keys_not_set.append(key)
    else:
        pass

    if len(keys_not_set) > 0: 
        for key in keys_not_set:
            print(key + " not set")
        exit(1)
    else:
        env_vars_checked = True
        print("All REQUIRED environment variables set, starting...")

def query(nrql_query):
    query_result = nr_graphql.run_query(newrelic_user_key,account_id,nrql_query)
    return query_result


if not env_vars_checked:
    check_env_vars()
    
# Grab entities that match
nrql_query_1="""
            {
            actor {
                entitySearch(
                    queryBuilder: {tags: {key: "k8s.deployment.name", value: "newrelic-otel-accountingservice"}} ) {
                results {
                    entities {
                    name
                    entityType
                    guid
                    }
                }
                }
            }
            }
        """

entities=query(nrql_query_1)
entities_json=entities['actor']['entitySearch']['results']['entities']
entityone=entities_json[0]['guid']

       
# Grab entities that match
nrql_query_2="""
            {
            actor {
                entitySearch(
                    queryBuilder: {tags: {key: "k8s.deployment.name", value: "newrelic-otel-cartservice"}} ) {
                results {
                    entities {
                    name
                    entityType
                    guid
                    }
                }
                }
            }
            }
        """
entities=query(nrql_query_2)
entities_json=entities['actor']['entitySearch']['results']['entities']
entitytwo=entities_json[0]['guid']


# Create relationship
nrql_query_3="""
            mutation {
            entityRelationshipUserDefinedCreateOrReplace(
                sourceEntityGuid: """+"\""+str(entityone)+"\""+"""
                targetEntityGuid:  """+"\""+str(entitytwo)+"\""+"""
                type: CALLS
            ){
            errors {
            message
            type
            }
            }
            }
        """

relationship_response=query(nrql_query_3)
relationship_response_json=relationship_response
print(relationship_response_json)