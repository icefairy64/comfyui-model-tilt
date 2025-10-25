from comfy.model_patcher import ModelPatcher


class ModelTilt:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "model": ("MODEL",),
                              "key_re": ("STRING",),
                              "strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.000001}),
                              "noise_seed": ("INT", {"default": 0, "min": 0, "max": 9999999999}),
                              "dropout": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.000001}),
                              "dropout_seed": ("INT", {"default": 0, "min": 0, "max": 9999999999}),
                              }}
    RETURN_TYPES = ("MODEL",)
    FUNCTION = "tilt"

    CATEGORY = "model_tilt"

    def tilt(self, model: ModelPatcher, key_re: str, strength: float, noise_seed: int, dropout: float, dropout_seed: int):
        import re
        import torch
        import numpy as np

        # Create a clone of the model
        new_model = model.clone()

        # Compile regex pattern
        pattern = re.compile(key_re)

        # Setup random generators for noise and dropout
        noise_rng = np.random.RandomState(noise_seed)
        dropout_rng = np.random.RandomState(dropout_seed)

        # Create a list to store patches
        patches = {}

        # Count modified keys for logging
        modified_count = 0

        # Iterate through model's state dict to find matching parameters
        for key, param in model.model.state_dict().items():
            # Check if this parameter matches the pattern
            if pattern.search(key) and isinstance(param, torch.Tensor) and param.numel() > 0:
                # Generate noise with same shape as the parameter
                noise = torch.tensor(
                    np.clip(noise_rng.normal(0, 0.33, size=param.shape), -1, 1),
                    dtype=param.dtype,
                    device=param.device
                )

                # Apply dropout if specified
                if dropout > 0:
                    dropout_mask = torch.tensor(
                        dropout_rng.random(size=param.shape) > dropout,
                        dtype=torch.float32,
                        device=param.device
                    )
                    noise.mul_(dropout_mask)

                # Add to patches list
                patches[key] = (noise * strength, )
                modified_count += 1

        # Add all patches to the model at once
        new_model.add_patches(patches)

        if modified_count == 0:
            print(f"Warning: No keys matched the pattern '{key_re}'")
        else:
            print(f"Applied tilt to {modified_count} keys matching '{key_re}'")

        return (new_model,)


NODE_CLASS_MAPPINGS = {
    "ModelTilt": ModelTilt
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ModelTilt": "Model Tilt"
}
