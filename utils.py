from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def get_user_votes(user):
    # Select your transport with a defined url endpoint
    transport = RequestsHTTPTransport(url="https://hub.snapshot.org/graphql")

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Provide a GraphQL query
    query = gql("""
    query Votes {
      votes (
        first: 1000
        skip: 0
        where: {
          voter: "user_address"
          space: "gitcoindao.eth"
        }
        orderBy: "created",
        orderDirection: desc
      ) {
        id
        voter
        created
        choice
        proposal {
          id
          title
          body
          choices
          start
          end
          snapshot
          state
          author 
        }
        space {
          id
        }
      }
    }
    """.replace('user_address', user)
    )

    # Execute the query on the transport
    return client.execute(query)['votes']
    

def get_proposals():
    client = Client(transport=transport, fetch_schema_from_transport=True)
    query = gql("""
query Proposals {
  proposals (
    where: {
      space_in: ["gitcoindao.eth"],
      state: "closed"
    },
    orderBy: "created",
    orderDirection: desc
  ) {
    id
    title
    body
    choices
    start
    end
    snapshot
    state
    author
    space {
      id
      name
    }
  }
}
    """)

    return client.execute(query)['proposals']
    

def final_result_for_proposal(proposal):
    transport = RequestsHTTPTransport(url="https://hub.snapshot.org/graphql", verify=True, retries=3,)

    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql("""
query Votes {
  votes (
    first: 1000
    skip: 0
    where: {
      proposal: "proposal_id"
      space: "gitcoindao.eth"
    }
    orderBy: "created",
    orderDirection: desc
  ) {
    id
    voter
    created
    choice
  }
}
""".replace('proposal_id', proposal['id']))
    votes = client.execute(query)['votes']
    choices = { x: 0 for x in range(1, len(proposal['choices'])+ 1) }
    for vote in votes:
        choices[vote['choice']] += 1
        
    
    return choices


def calculate_gtc_reputation(user):
    votes = get_user_votes(user)
    score = 0
    for vote in votes:
        choices = final_result_for_proposal(vote['proposal'])
        score += 1 + (choices[vote['choice']]/1000)
        
    return score

