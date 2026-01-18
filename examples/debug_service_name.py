"""Debug script to verify service name is being sent to Phoenix."""
import os
import subprocess
from custom.evals import initialize_tracing, shutdown_tracing, get_tracer

# Load environment variables
command = "source ~/.zprofile && env"
proc = subprocess.Popen(
    command,
    stdout=subprocess.PIPE,
    shell=True,
    executable="/bin/zsh"
)
for line in proc.stdout:
    key, _, value = line.decode().partition("=")
    os.environ[key] = value.strip()

print("=" * 80)
print("Service Name Debug Test")
print("=" * 80)

# Initialize with explicit service name
SERVICE_NAME = "custom-evals-test-123"
print(f"\nInitializing with service_name: {SERVICE_NAME}")

initialize_tracing(
    service_name=SERVICE_NAME,
    phoenix_endpoint="http://localhost:4317",
    metrics_enabled=False,
    protocol="grpc",
    console_export=True  # Enable console export to see what's being sent
)

# Get tracer and check config
tracer = get_tracer()
print(f"Tracer config service_name: {tracer.config.service_name}")

# Create a simple span to test
print("\nCreating test span...")
with tracer.span("test_span", attributes={"test": "value"}):
    print("  → Span created with service name:", SERVICE_NAME)

print("\n" + "=" * 80)
print("Flushing traces...")
print("=" * 80)

# Force flush to ensure data is sent
shutdown_tracing()

print("\n✓ Done!")
print(f"\nNow check Phoenix UI:")
print(f"  1. Go to: http://localhost:6006/projects")
print(f"  2. Look for project: '{SERVICE_NAME}'")
print(f"  3. Click on it to see the test_span")
print(f"\nIf you see the console export above, traces ARE being sent.")
print(f"If you don't see '{SERVICE_NAME}' in Phoenix, the issue is with Phoenix itself.")
