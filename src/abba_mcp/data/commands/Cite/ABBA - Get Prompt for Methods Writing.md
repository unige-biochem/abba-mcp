# ABBA - Get Prompt for Methods Writing

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Cite > ABBA - Get Prompt for Methods Writing`  
Class: `ch.epfl.biop.atlas.aligner.command.ABBAGenerateMethodsPrompt`

Generates a prompt describing how the selected slices were registered (atlas, slicing angles, positions, registration steps), to paste in a large language model to draft the methods section of a publication.

## Inputs

- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.

## Outputs

- `llm_prompt_for_methods` (String): Text to copy into a large language model. Review the generated methods carefully.

