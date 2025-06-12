import KratosMultiphysics as Kratos


def Factory(settings: Kratos.Parameters, model: Kratos.Model) -> Kratos.Process:
    return ImposeRBE2Process(model, settings["Parameters"])


class ImposeRBE2Process(Kratos.Process):
    def __init__(self, model: Kratos.Model, parameters: Kratos.Parameters):
        super().__init__()

        default_parameters = Kratos.Parameters("""{
            "main_model_part_name" : "Structure",
            "model_part_name"      : "please_specify_model_part_name",
            "master_node_id"       : 1,
            "interval"             : [0.0, 1e30]
        }""")

        parameters.ValidateAndAssignDefaults(default_parameters)

        self.main_model_part = model[parameters["main_model_part_name"].GetString()]
        self.rigid_body_model_part = self.main_model_part.GetSubModelPart(
            parameters["model_part_name"].GetString()
        )

        self.master_node = self.main_model_part.GetNode(parameters["master_node_id"].GetInt())

        self.interval = Kratos.IntervalUtility(parameters)

        self.__CreateConstraints()

    def ExecuteInitializeSolutionStep(self):
        current_time = self.main_model_part.ProcessInfo[Kratos.TIME]

        if self.interval.IsInInterval(current_time):
            Kratos.VariableUtils().SetFlag(
                Kratos.ACTIVE, True, self.rigid_body_model_part.MasterSlaveConstraints
            )
        else:
            Kratos.VariableUtils().SetFlag(
                Kratos.ACTIVE, False, self.rigid_body_model_part.MasterSlaveConstraints
            )

    def __CreateConstraints(self):
        master_node = self.master_node
        model_part = self.main_model_part
        rbe_part = self.rigid_body_model_part

        print(f"[RBE2] Master node ID: {master_node.Id}")
        print(
            f"[RBE2] Slave nodes in submodel part '{rbe_part.Name}': {[node.Id for node in rbe_part.Nodes]}"
        )

        # Check DOFs on master node
        dof_check = []
        for dir in "XYZ":
            disp_var = Kratos.KratosGlobals.GetVariable(f"DISPLACEMENT_{dir}")
            rot_var = Kratos.KratosGlobals.GetVariable(f"ROTATION_{dir}")
            has_disp_dof = master_node.HasDofFor(disp_var)
            has_rot_dof = master_node.HasDofFor(rot_var)
            dof_check.append((dir, has_disp_dof, has_rot_dof))
        print(f"[RBE2] Master node DOFs (DISPLACEMENT, ROTATION): {dof_check}")

        master_slave_constraint_id = (
            model_part.GetCommunicator().GlobalNumberOfMasterSlaveConstraints() + 1
        )
        constraints_created = 0

        for slave_node in rbe_part.Nodes:
            if slave_node.Id == master_node.Id:
                continue  # Skip the master node

            r = [
                slave_node.X0 - master_node.X0,
                slave_node.Y0 - master_node.Y0,
                slave_node.Z0 - master_node.Z0,
            ]

            print(
                f"[RBE2] Creating constraints for slave node {slave_node.Id} at relative position {r}"
            )

            for i, dir in enumerate("XYZ"):
                slave_dof = Kratos.KratosGlobals.GetVariable(f"DISPLACEMENT_{dir}")
                master_disp = Kratos.KratosGlobals.GetVariable(f"DISPLACEMENT_{dir}")

                if not slave_node.HasDofFor(slave_dof):
                    print(
                        f"[RBE2] Warning: Slave node {slave_node.Id} does NOT have DOF for DISPLACEMENT_{dir}, skipping"
                    )
                    continue
                if not master_node.HasDofFor(master_disp):
                    print(
                        f"[RBE2] Warning: Master node does NOT have DOF for DISPLACEMENT_{dir}, skipping"
                    )
                    continue

                # 1. Direct translation constraint
                constraint = model_part.CreateNewMasterSlaveConstraint(
                    "LinearMasterSlaveConstraint",
                    master_slave_constraint_id,
                    master_node,
                    master_disp,
                    slave_node,
                    slave_dof,
                    1.0,
                    0.0,
                )
                rbe_part.AddMasterSlaveConstraint(constraint)
                print(
                    f"[RBE2] Added translation constraint: Master node {master_node.Id} DISPLACEMENT_{dir} -> Slave node {slave_node.Id} DISPLACEMENT_{dir}"
                )
                master_slave_constraint_id += 1
                constraints_created += 1

                # 2. Rotational coupling via cross product
                for j, rot_dir in enumerate("XYZ"):
                    rot_var = Kratos.KratosGlobals.GetVariable(f"ROTATION_{rot_dir}")

                    if not slave_node.HasDofFor(slave_dof):
                        continue
                    if not master_node.HasDofFor(rot_var):
                        continue

                    coeff = self.__GetCrossProductCoeff(dir, rot_dir, r)
                    if abs(coeff) > 1e-12:
                        constraint = model_part.CreateNewMasterSlaveConstraint(
                            "LinearMasterSlaveConstraint",
                            master_slave_constraint_id,
                            master_node,
                            rot_var,
                            slave_node,
                            slave_dof,
                            coeff,
                            0.0,
                        )
                        rbe_part.AddMasterSlaveConstraint(constraint)
                        print(
                            f"[RBE2] Added rotational constraint: Master node {master_node.Id} ROTATION_{rot_dir} (coeff {coeff:.3e}) -> Slave node {slave_node.Id} DISPLACEMENT_{dir}"
                        )
                        master_slave_constraint_id += 1
                        constraints_created += 1

            # ✅ ADD THIS BLOCK to synchronize ROTATION DOFs directly
            for dir in "XYZ":
                rot_var = Kratos.KratosGlobals.GetVariable(f"ROTATION_{dir}")
                if not master_node.HasDofFor(rot_var) or not slave_node.HasDofFor(rot_var):
                    continue
                constraint = model_part.CreateNewMasterSlaveConstraint(
                    "LinearMasterSlaveConstraint",
                    master_slave_constraint_id,
                    master_node,
                    rot_var,
                    slave_node,
                    rot_var,
                    1.0,
                    0.0,
                )
                rbe_part.AddMasterSlaveConstraint(constraint)
                print(
                    f"[RBE2] Added rotation constraint: Master node {master_node.Id} ROTATION_{dir} -> Slave node {slave_node.Id} ROTATION_{dir}"
                )
                master_slave_constraint_id += 1
                constraints_created += 1

        print(f"[RBE2] Total master-slave constraints created: {constraints_created}")

    @staticmethod
    def __GetCrossProductCoeff(slave_dir, rot_dir, r):
        """Returns the coefficient from r x theta for a given displacement direction and rotation direction."""
        if slave_dir == "X":
            if rot_dir == "Y":
                return -r[2]
            if rot_dir == "Z":
                return r[1]
        elif slave_dir == "Y":
            if rot_dir == "Z":
                return -r[0]
            if rot_dir == "X":
                return r[2]
        elif slave_dir == "Z":
            if rot_dir == "X":
                return -r[1]
            if rot_dir == "Y":
                return r[0]
        return 0.0
