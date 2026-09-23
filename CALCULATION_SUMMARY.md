# Ethanol combustion Gibbs-energy calculation

## Status

The calculation is in progress on Slurm. It uses one ORCA core per job at
B3LYP/6-31G(d), 298.15 K, and 1 bar for the gas-phase reaction

`C2H5OH + 3 O2 -> 2 CO2 + 3 H2O`.

At the latest health check, ethanol geometry optimization was running. Its
maximum gradient decreased from 0.155946 to 0.064998, and MAESTRO classified
the trajectory as progressing. The Hessian/thermochemistry step has not yet
completed, so individual Gibbs energies and the combustion Gibbs energy are
not available yet.

## Planned result

Once all four species finish, the workflow reports

`ΔGcomb = 2G(CO2) + 3G(H2O) - G(C2H5OH) - 3G(O2)`.

The requested O2 spin state is singlet (`spin = 0`); consequently, the final
value corresponds to that specified electronic state rather than triplet
ground-state oxygen.
