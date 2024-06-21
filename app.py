import os
from nr_graphql import nr_graphql


newrelic_user_key = os.getenv('NEW_RELIC_USER_KEY') 

current_configurations = {}
env_vars_checked = False

def check_env_vars():
    global env_vars_checked
    keys = ("NEW_RELIC_USER_KEY",)
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
    query_result = nr_graphql.run_query(newrelic_user_key,nrql_query)
    return query_result


if not env_vars_checked:
    check_env_vars()

def create_relationship(sourceEntityGuid,targetEntityGuid):
    nrql_query="""
            mutation {
            entityRelationshipUserDefinedCreateOrReplace(
                sourceEntityGuid: """+"\""+str(sourceEntityGuid)+"\""+"""
                targetEntityGuid:  """+"\""+str(targetEntityGuid)+"\""+"""
                type: CONSUMES
            ){
            errors {
            message
            type
            }
            }
            }
        """
    print(nrql_query)


# Grab GCP_PUB_SUB_TOPICS
nrql_query_1="""
            {
            actor {
                entitySearch(queryBuilder: {infrastructureIntegrationType: GCP_PUB_SUB_TOPIC}) {
                results {
                    entities {
                    name
                    entityType
                    guid
                    tags {
                        key
                        values
                    }
                    }
                }
                }
            }
            }
        """
parsed_entities1={}
entities1=query(nrql_query_1)
entities1_json=entities1['actor']['entitySearch']['results']['entities']
for entity in entities1_json:
    for tag in entity['tags']:
        if tag ['key'] == 'gcp.topicId':
            parsed_entities1[tag['values'][0]] = {"guid": entity['guid'],"name": entity['name']}
            
    
# Grab GCP_PUB_SUB_SUBSCRIPTION
nrql_query_2="""
            {
            actor {
                entitySearch(
                queryBuilder: {infrastructureIntegrationType: GCP_PUB_SUB_SUBSCRIPTION}
                ) {
                results {
                    entities {
                    name
                    entityType
                    guid
                    tags {
                        key
                        values
                    }
                    }
                }
                }
            }
        }
        """
parsed_entities2={}
entities2=query(nrql_query_2)
entities2_json=entities2['actor']['entitySearch']['results']['entities']
for entity in entities2_json:
    for tag in entity['tags']:
        if tag ['key'] == 'gcp.topicId':
            parsed_entities2[str(tag['values'][0]).split("/")[3]] = {"guid": entity['guid'],"name": entity['name']}

# Check each subscription topicId for matching topic
for entity in parsed_entities2:
    if entity in parsed_entities1:
        print(parsed_entities2[entity],parsed_entities2[entity])

