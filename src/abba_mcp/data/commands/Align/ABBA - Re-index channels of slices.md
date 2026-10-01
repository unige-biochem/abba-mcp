# ABBA - Re-index channels of slices

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Align > ABBA - Re-index channels of slices`  
Class: `ch.epfl.biop.atlas.aligner.command.ReindexSlicesCommand`

Reorders, removes or duplicates the channels of the selected slices. Each selected slice is replaced by a new slice with the new channels, at the same position and with the same registrations. The same channel order is applied to all selected slices.

## Inputs

- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `new_channel_order_csv` (String) **New channel order**
  Comma separated 0-based indices of the original channels, in their new order: '0,2' keeps the first and third channels, '1,0' swaps the first two channels.

