from __future__ import annotations

from dataclasses import dataclass

from .constraint import KratosConstraint
from .load import KratosLoad


@dataclass
class SimulationParameters:
    """Main container of information about the kratos simulation."""

    constraints: list[KratosConstraint]
    loads: list[KratosLoad]

    @classmethod
    def from_json(cls, json: dict) -> SimulationParameters:
        """Construct this class from Kratos json content."""
        return SimulationParameters(
            constraints=[
                KratosConstraint.from_json(c) for c in json["processes"]["constraints_process_list"]
            ],
            loads=[KratosLoad.from_json(load) for load in json["processes"]["loads_process_list"]],
        )

    def to_json(self) -> dict:
        """Export this class to a dictionary in a Kratos compatible format."""
        return {
            "problem_data": {
                "parallel_type": "OpenMP",
                "echo_level": 1,
                "start_time": 0.0,
                "end_time": 1.0,
            },
            "solver_settings": {
                "time_stepping": {"time_step": 1.1},
                "solver_type": "Static",
                "model_part_name": "Structure",
                "domain_size": 3,
                "echo_level": 0,
                "analysis_type": "linear",
                "model_import_settings": {"input_type": "mdpa", "input_filename": "model"},
                "material_import_settings": {"materials_filename": "materials.json"},
                "line_search": False,
                "convergence_criterion": "residual_criterion",
                "displacement_relative_tolerance": 1.0e-4,
                "displacement_absolute_tolerance": 1.0e-9,
                "residual_relative_tolerance": 1.0e-4,
                "residual_absolute_tolerance": 1.0e-9,
                "max_iteration": 10,
                "rotation_dofs": False,
                "volumetric_strain_dofs": False,
            },
            "processes": {
                "constraints_process_list": [c.to_json() for c in self.constraints],
                "loads_process_list": [load.to_json() for load in self.loads],
                "list_other_processes": [],
            },
            "output_processes": {
                "vtk_output": [
                    {
                        "python_module": "vtk_output_process",
                        "kratos_module": "KratosMultiphysics",
                        "process_name": "VtkOutputProcess",
                        "Parameters": {
                            "model_part_name": "Structure",
                            "output_control_type": "step",
                            "output_interval": 1,
                            "file_format": "ascii",
                            "output_precision": 7,
                            "output_sub_model_parts": False,
                            "output_path": "vtk_output",
                            "save_output_files_in_folder": True,
                            "nodal_solution_step_data_variables": ["DISPLACEMENT", "REACTION"],
                            "nodal_data_value_variables": [],
                            "element_data_value_variables": [],
                            "condition_data_value_variables": [],
                            "gauss_point_variables_extrapolated_to_nodes": [],
                        },
                    }
                ]
            },
            "analysis_stage": (
                "KratosMultiphysics"
                ".StructuralMechanicsApplication"
                ".structural_mechanics_analysis"
            ),
        }
