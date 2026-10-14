# ABBA - Wait

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Inspect > ABBA - Wait`  
Class: `ch.epfl.biop.atlas.aligner.command.WaitCommand`

Waits until the actions queued on the slices are done, at most 'timeout_s' seconds, then tells how many are still pending and what failed since the previous 'ABBA - Wait'. Registration and DeepSlice commands return as soon as their actions are queued, and their failures come later: follow them with this command, and call it again while 'pending_actions' is above 0.

## Inputs

- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session to wait for.
- `timeout_s` (double) **Timeout (s)**, default `30.0`
  Longest wait, in seconds. Clients usually give up on a call after about 60 s: keep it under 45, and call again while actions are pending.

## Outputs

- `failures` (String): The failures recorded since the previous 'ABBA - Wait' on this session, one per line ('#index hh:mm:ss action on slices: reason'), or empty.
- `pending_actions` (int): Number of actions still queued or running, 0 once all are done.
- `summary` (String): One line, for instance 'done: no pending action, no new failure' or '3 actions pending after 30 s; 1 new failure'.

