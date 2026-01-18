"""Verify Phoenix is receiving traces and metrics."""
import requests
import json

PHOENIX_URL = "http://localhost:6006"

print("=" * 80)
print("Phoenix Verification")
print("=" * 80)

# Check Phoenix is running
try:
    response = requests.get(PHOENIX_URL, timeout=5)
    if response.status_code == 200:
        print("✓ Phoenix server is running")
    else:
        print(f"✗ Phoenix returned status {response.status_code}")
except Exception as e:
    print(f"✗ Cannot connect to Phoenix: {e}")
    exit(1)

# Check GraphQL endpoint for traces
graphql_url = f"{PHOENIX_URL}/graphql"
query = """
{
  spans(first: 10) {
    edges {
      span {
        name
        spanKind
        statusCode
        startTime
        attributes
      }
    }
  }
}
"""

try:
    response = requests.post(
        graphql_url,
        json={"query": query},
        headers={"Content-Type": "application/json"},
        timeout=10
    )

    if response.status_code == 200:
        data = response.json()
        print(f"\nGraphQL Response: {json.dumps(data, indent=2)[:500]}")

        if "data" in data and data["data"] and "spans" in data["data"]:
            spans = data["data"]["spans"]["edges"] if data["data"]["spans"] else []
            print(f"\n✓ Found {len(spans)} traces in Phoenix")

            if spans:
                print("\nRecent traces:")
                for i, edge in enumerate(spans[:5], 1):
                    span = edge["span"]
                    print(f"  {i}. {span['name']}")
                    print(f"     Status: {span['statusCode']}")
                    print(f"     Time: {span['startTime']}")
                    attrs = span.get('attributes')
                    if attrs and isinstance(attrs, str) and 'evaluator.name' in attrs:
                        print(f"     Attributes: {attrs[:100]}")
                print("\n✓ Traces are being received by Phoenix!")
                print(f"✓ View them at: {PHOENIX_URL}/projects")
            else:
                print("\n✗ No traces found in Phoenix yet")
                print("   This could mean:")
                print("   1. Traces haven't been flushed yet (call shutdown_tracing())")
                print("   2. The endpoint is incorrect")
                print("   3. There's a network issue")
        else:
            print(f"✗ Unexpected GraphQL response: {data}")
    else:
        print(f"✗ GraphQL query failed with status {response.status_code}")
        print(f"   Response: {response.text[:200]}")

except Exception as e:
    print(f"✗ Error querying Phoenix: {e}")

print("=" * 80)
