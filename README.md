# Model Tilt for Comfy UI

## What is this?
"Model tilt" is a process of adding noise to a subset of the model weights to produce potentially interesting results. I see this as a parallel to cartrigde tilting, hence the name.

## How do I use this?
- Copy `model_tilt.py` to custom nodes directory in Comfy UI
- Apply the patch using `git am model_patcher_add_tilt.patch`

If done correctly, you will now see a "Model Tilt" node available under "model_patches". This node takes a model as an input and outputs a model with applied noise.

You can tune the following parameters:
- `target`: a substring of a model key; all the weights which names include this substring will be affected. I personally like to tilt `1.norm` or `1.attn`.
- `tilt_strength`: amount of noise to add; the noise will be generated in the `[-tilt_strength .. tilt_strength]` range.
- `tilt_seed`: seed to use for tilt noise generation; each subsequent weight tensor will have this seed incremented internally.
- `mask_strength`: threshold for the mask; the formula is basically `weight = weight + noise * mask`, where `mask` is a noise tensor with values less than `1 - mask_strength` mapped to 0 and other values mapped to 1.
- `mask_seed`: seed to use for mask noise generation; each subsequent weight tensor will have this seed incremented internally.

## Can you show me some examples?

![Demo 1](examples/tilt_demo_1.jpg)

![Demo 2](examples/tilt_demo_5.jpg)

![Demo 3](examples/tilt_demo_2.jpg)

![Demo 4](examples/tilt_demo_4.jpg)