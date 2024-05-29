from comfy.model_patcher import ModelPatcher


class ModelTilt:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL", ),
                "target": ("STRING", {
                    "default": "transformer_block"
                }),
                "tilt_strength": ("FLOAT", {
                    "default": 0.1,
                    "min": 0.0,
                    "max": 10.0,
                    "step": 0.0001,
                    "round": 0.0000001,
                    "display": "number"}),
                "tilt_seed": ("INT", {
                    "default": 0
                }),
                "mask_strength": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "round": False,
                    "display": "number"}),
                "mask_seed": ("INT", {
                    "default": 0
                })
            }
        }

    RETURN_TYPES = ("MODEL", )

    FUNCTION = "tilt"

    CATEGORY = "model_patches"

    def tilt(self, model: ModelPatcher, target: str, tilt_strength: float, tilt_seed: int, mask_strength: float, mask_seed: int):
        if model is None:
            return (None, )

        new_model = model.clone()
        seed_offset = 0
        for key in model.model_keys:
            if key.find(target) < 0:
                continue
            new_model.add_patches({
                key: ("tilt", (tilt_seed + seed_offset, mask_strength, mask_seed + seed_offset))
            }, strength_model=1.0, strength_patch=tilt_strength)
            seed_offset += 1

        return (new_model, )

NODE_CLASS_MAPPINGS = {
    "ModelTilt": ModelTilt,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ModelTilt": "Model Tilt",
}