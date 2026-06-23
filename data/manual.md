# Plant Equipment Maintenance Manual

## Haas VF-2 CNC Mill (CNC-7) — Spindle System

The spindle runs on a matched pair of precision angular-contact bearings,
part number BRG-6207. Normal spindle temperature is 35-55 C under load.

Fault E-214 (spindle bearing over-temperature): the spindle has exceeded its
thermal limit. Stop the spindle immediately to avoid bearing seizure and
permanent spindle damage.

Repair procedure for E-214:
1. Lock out / tag out the machine and confirm zero energy state.
2. Allow the spindle to cool to ambient before disassembly.
3. Remove the spindle cartridge per section 7 of the OEM service guide.
4. Replace both BRG-6207 bearings as a matched set — never reuse one.
5. Re-lubricate with the specified high-speed spindle grease.
6. Torque the retaining nut to 25 Nm.
7. Run the spindle warm-up cycle and verify temperature stays under 55 C.

Recurring E-214 almost always means the lubrication interval is too long.
Shorten the greasing schedule and log it.

## Grundfos Hydraulic Power Unit (PUMP-3)

Fault E-091 (hydraulic pressure below threshold): system pressure has dropped
below the 1800 psi minimum. The usual cause is a failed pump shaft seal
(part SEAL-HP12) or an internal leak.

Repair procedure for E-091:
1. Lock out / tag out and relieve hydraulic pressure to zero.
2. Inspect for external leaks at fittings first — the cheapest fix.
3. If no external leak, replace the pump shaft seal SEAL-HP12.
4. Refill with the specified hydraulic fluid and bleed air from the system.
5. Restart and confirm pressure holds at 1800-2200 psi.

## Dorner 2200 Conveyor (CONV-2)

Fault E-330 (drive motor overload trip): the conveyor drive motor drew
excess current and tripped. IMPORTANT: check for a mechanical belt jam BEFORE
condemning the motor — most E-330 events are jams, not motor failures.

Repair procedure for E-330:
1. Lock out / tag out.
2. Clear any belt jam or foreign object; inspect the belt for damage.
3. Manually rotate the drive — if it turns freely, the motor is likely fine.
4. Only if the motor is seized or burnt, replace drive motor MTR-CV3.
5. Reset the overload relay and run an unloaded test cycle.
