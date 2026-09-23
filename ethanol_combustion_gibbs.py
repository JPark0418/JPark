"""Gas-phase combustion Gibbs energy at 298.15 K and 1 bar.

Reaction: C2H5OH + 3 O2 -> 2 CO2 + 3 H2O.
All species use B3LYP/6-31G(d) thermochemistry through MAESTRO/ORCA.
"""

from maestro import DFT, Maestro, OrcaEngine, SystemQM, ThermoTask
from maestro.engines.jobspec import EnvInfo, ExecInfo, Resources

HARTREE_TO_KJMOL = 2625.49962

mae = Maestro(
    mode="slurm",
    workdir=".",
    runinfo_path="combustion_orca_runinfo.toml",
)
theory = DFT(functional="B3LYP", basis="6-31G(d)")
engine = OrcaEngine(
    env=EnvInfo(kind="module", modules=["orca/v6.0.1"]),
    exec=ExecInfo(
        exec_cmd="orca",
        exec_dir="/appl/share/orca_6_0_1_linux_x86-64_shared_openmpi416",
    ),
    resources=Resources(cores=1),
)

species = {
    "ethanol": ("ethanol.xyz", 0, 0),
    "oxygen": ("oxygen.xyz", 0, 0),
    "carbon_dioxide": ("carbon_dioxide.xyz", 0, 0),
    "water": ("water.xyz", 0, 0),
}

gibbs = {}
for name, (geometry, charge, spin) in species.items():
    system = SystemQM(geometry=geometry, charge=charge, spin=spin)
    task = ThermoTask(
        system=system,
        theory=theory,
        temperature=298.15,
        pressure=1.0,
    )
    result = mae.run(
        rundir=f"combustion_gibbs_work/{name}",
        task=task,
        engines=engine,
    )
    gibbs[name] = result.load("gibbs_free_energy")
    print(f"{name} Gibbs free energy ({result.unit('gibbs_free_energy')}): "
          f"{gibbs[name]}")

delta_g_hartree = (
    2 * gibbs["carbon_dioxide"]
    + 3 * gibbs["water"]
    - gibbs["ethanol"]
    - 3 * gibbs["oxygen"]
)
print(f"Delta G_combustion (Hartree/mol): {delta_g_hartree}")
print(f"Delta G_combustion (kJ/mol): {delta_g_hartree * HARTREE_TO_KJMOL}")
