import json  # noqa: INP001

from nastran_to_kratos.translation_layer.connector import RBE2Connector


# Fake Rbe2 class for testing without pyNastran
class Rbe2:
    def __init__(self, eid, gn, cm, gmi, alpha=None, tref=None):
        self.eid = eid
        self.gn = gn
        self.cm = cm
        self.gmi = gmi
        self.alpha = alpha
        self.tref = tref


rbe2_entry = Rbe2(eid=1, gn=10, cm=123, gmi=[20, 30, 40])

# Convert to RBE2Connector
connector = RBE2Connector.from_nastran(rbe2_entry)

# Convert to Kratos constraints (or process)
kratos_process = connector.to_kratos_process("Structure")

# Print result
print(json.dumps(kratos_process, indent=2))  # noqa: T201
