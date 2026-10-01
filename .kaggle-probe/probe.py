import subprocess, sys, torch
print("torch:", torch.__version__, flush=True)
print("cuda available:", torch.cuda.is_available(), flush=True)
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0), flush=True)
    print("VRAM:", round(torch.cuda.get_device_properties(0).total_memory/1e9, 1), "GB", flush=True)
else:
    print("NO GPU ACCESS — account likely lacks phone verification", flush=True)
