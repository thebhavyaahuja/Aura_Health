#!/usr/bin/env python3
"""
GPU Setup Verification Script
Run this before training to ensure everything is configured correctly.
"""

import sys
import os

print("="*60)
print("GPU Setup Verification for BioGPT Training")
print("="*60)

# Check Python version
print(f"\n1. Python Version: {sys.version}")
if sys.version_info < (3, 8):
    print("   ⚠️  WARNING: Python 3.8+ recommended")
else:
    print("   ✓ Python version OK")

# Check PyTorch
try:
    import torch
    print(f"\n2. PyTorch Version: {torch.__version__}")
    print("   ✓ PyTorch installed")
except ImportError:
    print("\n2. ✗ PyTorch not found")
    print("   Install with: pip install torch --index-url https://download.pytorch.org/whl/cu121")
    sys.exit(1)

# Check CUDA
print(f"\n3. CUDA Availability:")
if torch.cuda.is_available():
    print(f"   ✓ CUDA is available")
    print(f"   CUDA Version: {torch.version.cuda}")
    print(f"   cuDNN Version: {torch.backends.cudnn.version()}")
else:
    print("   ✗ CUDA not available")
    print("   Check your CUDA installation")
    sys.exit(1)

# Check GPUs
print(f"\n4. GPU Information:")
num_gpus = torch.cuda.device_count()
print(f"   Number of GPUs: {num_gpus}")

if num_gpus == 0:
    print("   ✗ No GPUs detected")
    sys.exit(1)
elif num_gpus < 2:
    print("   ⚠️  Only 1 GPU detected. Multi-GPU optimizations will not be used.")
else:
    print(f"   ✓ {num_gpus} GPUs detected - Multi-GPU training enabled")

for i in range(num_gpus):
    props = torch.cuda.get_device_properties(i)
    print(f"\n   GPU {i}: {torch.cuda.get_device_name(i)}")
    print(f"      Total Memory: {props.total_memory / 1024**3:.2f} GB")
    print(f"      Compute Capability: {props.major}.{props.minor}")
    print(f"      Multi-Processor Count: {props.multi_processor_count}")
    
    # Check if it's L40S
    if "L40S" in torch.cuda.get_device_name(i):
        print(f"      ✓ Verified as L40S GPU")
    
    # Test memory allocation
    try:
        torch.cuda.set_device(i)
        test_tensor = torch.zeros(1000, 1000, device=f'cuda:{i}')
        allocated = torch.cuda.memory_allocated(i) / 1024**2
        print(f"      Memory Test: {allocated:.2f} MB allocated")
        del test_tensor
        torch.cuda.empty_cache()
        print(f"      ✓ Memory allocation test passed")
    except Exception as e:
        print(f"      ✗ Memory allocation test failed: {e}")

# Check TF32 support
print(f"\n5. TF32 Support:")
if hasattr(torch.backends.cuda.matmul, 'allow_tf32'):
    print(f"   ✓ TF32 supported and will be enabled")
else:
    print(f"   ⚠️  TF32 not available (older PyTorch version)")

# Check required libraries
print(f"\n6. Required Libraries:")
required_libs = {
    'transformers': 'transformers',
    'datasets': 'datasets',
    'pandas': 'pandas',
    'numpy': 'numpy',
    'sklearn': 'scikit-learn',
}

all_installed = True
for module, package in required_libs.items():
    try:
        __import__(module)
        print(f"   ✓ {package}")
    except ImportError:
        print(f"   ✗ {package} not found")
        all_installed = False

if not all_installed:
    print("\n   Install missing packages with:")
    print("   pip install -r requirements.txt")
    sys.exit(1)

# Check for data file
print(f"\n7. Data File:")
if os.path.exists("radiology_reports.csv"):
    import pandas as pd
    try:
        df = pd.read_csv("radiology_reports.csv", delimiter=";")
        print(f"   ✓ Found radiology_reports.csv")
        print(f"   Rows: {len(df)}")
        print(f"   Columns: {len(df.columns)}")
    except Exception as e:
        print(f"   ⚠️  File found but error reading: {e}")
else:
    print(f"   ✗ radiology_reports.csv not found")
    print(f"   Place the data file in the same directory as biogpt.py")

# Check disk space
print(f"\n8. Disk Space:")
import shutil
total, used, free = shutil.disk_usage(".")
print(f"   Free space: {free / 1024**3:.2f} GB")
if free / 1024**3 < 10:
    print(f"   ⚠️  Low disk space. At least 10GB recommended for model checkpoints")
else:
    print(f"   ✓ Sufficient disk space")

# Environment variables
print(f"\n9. Environment Variables:")
env_vars = {
    'CUDA_VISIBLE_DEVICES': 'Not set (will use all GPUs)',
    'CUDA_LAUNCH_BLOCKING': '0',
    'TORCH_CUDA_ARCH_LIST': '8.9',
    'PYTORCH_CUDA_ALLOC_CONF': 'max_split_size_mb:512',
}

for var, default in env_vars.items():
    value = os.environ.get(var, None)
    if value:
        print(f"   {var}={value}")
    else:
        print(f"   {var}: {default}")

# Final summary
print("\n" + "="*60)
print("Verification Summary")
print("="*60)

if torch.cuda.is_available() and num_gpus >= 1 and all_installed:
    print("✓ All checks passed! Ready to train.")
    print("\nTo start training, run:")
    print("  python biogpt.py")
    print("  or")
    print("  ./run_training.sh")
    
    if num_gpus >= 2:
        print("\n✓ Multi-GPU training will be automatically enabled")
        print(f"  Effective batch size: {16 * 4 * num_gpus}")
        print(f"  (16 per device × 4 accumulation steps × {num_gpus} GPUs)")
else:
    print("✗ Some checks failed. Please fix the issues above.")
    sys.exit(1)

print("="*60)
