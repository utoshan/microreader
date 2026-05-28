Import("env")
import os
import sys

_TOOLS_DIR = os.path.join(env.subst("$PROJECT_DIR"), "tools")
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)
import build_assets  # noqa: E402

project_dir = env.subst("$PROJECT_DIR")
esp32_dir = os.path.join(project_dir, "platforms", "esp32")
bin_path = os.path.join(esp32_dir, "assets.bin")
asm_path = os.path.join(esp32_dir, "assets_embedded.S")

build_assets.build(project_dir, bin_path)
print(f"[generate_assets] assets.bin written ({os.path.getsize(bin_path):,} bytes)")

# Generate a minimal assembly file that uses .incbin to embed the binary.
# This is exactly what ESP-IDF's EMBED_FILES does internally, but done here
# so CMake never needs to find or generate it itself.
bin_path_escaped = bin_path.replace("\\", "/")
asm = f"""\
    .section .rodata
    .global _binary_assets_bin_start
    .global _binary_assets_bin_end
_binary_assets_bin_start:
    .incbin \"{bin_path_escaped}\"
_binary_assets_bin_end:
"""
with open(asm_path, "w") as f:
    f.write(asm)
print(f"[generate_assets] assets_embedded.S written")
