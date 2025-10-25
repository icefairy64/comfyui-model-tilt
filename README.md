# Model Tilt for Comfy UI

## What is this?
"Model tilt" is a process of adding noise to a subset of the model weights to produce potentially interesting results. I see this as a parallel to cartrigde tilting, hence the name.

## How do I use this?
- Copy `model_tilt.py` to custom nodes directory in Comfy UI
- Experiment away!

If done correctly, you will now see a "Model Tilt" node available under "model_tilt". This node takes a model as an input and outputs a model with applied noise.

You can tune the following parameters:
- `key_re`: a regex for matching model keys. I personally like to tilt `1.norm` or `1.attn`.
- `strength`: amount of noise to add; the noise will be generated in the `[-tilt_strength .. tilt_strength]` range.
- `noise_seed`: seed to use for tilt noise generation; each subsequent weight tensor will have this seed incremented internally.
- `dropout`: threshold for the mask; 1 means no effect and 0 means full effect.
- `dropout_seed`: seed to use for mask noise generation.

## Can you show me some examples?

![Demo 1](examples/tilt_example_1.png)

![Demo 2](examples/stitched_example_1.png)

![Demo 3](examples/stitched_example_2.png)
