import os
from dotenv import load_dotenv
import requests
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

load_dotenv()


client_id = os.environ.get("TNID_CLIENT_ID")
client_secret = os.environ.get("TNID_SECRET")


class TNID:

    def __init__(self):
        self.token = self.get_bearer_token(client_id, client_secret)

    def get_bearer_token(self, client_id, client_secret):
        url = "https://api.staging.v2.tnid.com/auth/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"client_id": client_id, "client_secret": client_secret}

        # Make the POST request to the token endpoint
        response = requests.post(url, headers=headers, data=data)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response and extract the access token
            token_data = response.json()
            return token_data.get("access_token")
        else:
            raise Exception(
                f"Failed to retrieve token: {response.status_code} {response.text}"
            )

    def invite_user(self, user_email, user_role, connection_type):
        # Initialize transport with the authorization header
        transport = AIOHTTPTransport(
            url="https://api.staging.v2.tnid.com/company",
            headers={"Authorization": f"Bearer {self.token}"},
        )

        # Create a GraphQL client using the defined transport
        client = Client(transport=transport, fetch_schema_from_transport=True)

        # Define the mutation for inviting a user
        mutation = gql(
            """
            mutation (
                $user: InviteUserInput!
                $connectionType: B2cConnectionType!
            ) {
                createB2cInvite(
                    user: $user
                    connectionType: $connectionType
                ) {
                    id
                    status
                    type
                    insertedAt
                    respondedAt
                    updatedAt
                    company {
                        id
                    }
                    user {
                        id
                    }
                    invitedUser {
                        id
                        firstName
                        lastName
                    }
                }
            }
            """
        )

        # Set parameters for the mutation
        params = {
            "user": {"email": user_email},
            "connectionType": connection_type,
        }

        try:
            # Execute the mutation
            response = client.execute(mutation, variable_values=params)
            return response
        except Exception as e:
            print(f"Exception when inviting user: {e}")
            return None


# Example usage:

tnid = TNID()
# response = tnid.invite_user(
#     user_email="muhdabdullahi36@gmail.com",
#     user_role="member",
#     connection_type="CUSTOMER",
# )
# print("Invite response:", response)
