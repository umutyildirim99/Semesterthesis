import json
from pathlib import Path

from nastran_to_kratos.nastran.bulk_data import BulkDataSection
from nastran_to_kratos.translation_layer import RBE2Connector

# Define the input file path as a Path object
input_bdf_path = Path("example_rbe2.bdf")

# Read the BDF file
with input_bdf_path.open("r") as f:
    lines = f.readlines()

# Filter out empty lines and comment lines starting with $
filtered_lines = [line for line in lines if line.strip() and not line.strip().startswith("$")]

# Parse the bulk data from filtered lines
bulk_data = BulkDataSection.from_file_content(filtered_lines)

# Extract RBE2 connectors
connectors = RBE2Connector.rbe2_connectors_from_nastran(bulk_data)

# Convert to Kratos format
kratos_constraints = []
for rbe2 in connectors:
    kratos_constraints.extend(rbe2.to_kratos())

# Export to JSON
output_json_path = Path("rbe2_output.json")
with output_json_path.open("w") as f:
    json.dump(kratos_constraints, f, indent=2)

print("Exported RBE2 constraints to:", output_json_path)
