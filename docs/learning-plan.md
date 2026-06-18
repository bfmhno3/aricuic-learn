# Learning Plan: Accelerated Rotation-Invariant Convolution for UAV Image Segmentation

## Paper

**Title**: Accelerated Rotation-Invariant Convolution for UAV Image Segmentation

**Source**: `docs/aricuir_tex_src/revised_version_1.tex`

**PDF**: `docs/Accelerated_Rotation-Invariant_Convolution_for_UAV_Image_Segmentation.pdf`

## Environment

- WSL2 Ubuntu 24.04, g++, VS Code remote
- OpenCV via `apt install libopencv-dev`
- NVIDIA RTX 4050 (for Day 5 CUDA)

---

## Day 1: Convolution Foundations

| Block | Content | Output |
|-------|---------|--------|
| AM Theory | 1D conv definition, 2D conv, im2col | Read paper sec 3.1 |
| PM Practice | `2d_convolution.cpp` -- hand-written conv vs `cv::filter2D` | Verified output |
| PM Practice | `im2col.cpp` -- see data duplication in column matrix | Printed matrix |
| EVE Theory | Scatter convolution (Eq.3, Algo.1) | Read paper sec 3.1 cont. |

---

## Day 2: Scatter + Rotation Basics

| Block | Content | Output |
|-------|---------|--------|
| AM Practice | `scatter_convolution.cpp` -- Algorithm 1 implementation | Matches gather output |
| AM Practice | `benchmark.cpp` -- gather vs scatter timing | Timing comparison |
| PM Theory | Rotation matrix, kernel rotation, equivariance vs invariance | Read paper sec 3.2 |
| EVE Practice | `rotate_kernel.cpp` -- 4 rotations of Sobel, directional edges | Visual output |
| EVE Practice | `equivariance_demo.cpp` -- rotated input, same kernel | Feature maps shown |

---

## Day 3: p4 Group + Scatter Acceleration

| Block | Content | Output |
|-------|---------|--------|
| AM Theory | p4 group, data reuse (Fig.4), orientation pooling | Read paper sec 3.2 cont. |
| PM Practice | `p4_naive.cpp` -- 4 separate convs + pool | Verified output |
| PM Practice | `p4_scatter.cpp` -- multiply once, scatter to 4 maps + pool | Same output, faster |
| EVE Theory | Steerable filters, quadrant symmetry | Read paper sec 3.4 |

---

## Day 4: Steerable Filters + Segmentation

| Block | Content | Output |
|-------|---------|--------|
| AM Practice | `steerable_filter.cpp` -- base filter combination at various angles | Directional responses |
| AM Practice | `quadrant_mapping.cpp` -- 16 angles, Q1 mapping | Mapping table |
| PM Theory | GPU implementation concepts, U-Net architecture | Read paper sec 4-5 |
| EVE Practice | `simple_segmentation.cpp` -- threshold segmentation on UAV image | Segmentation result |

---

## Day 5: CUDA + Review

| Block | Content | Output |
|-------|---------|--------|
| AM Theory+Practice | CUDA basics, simple kernel, gather-GEMM-scatter concepts | CUDA hello world |
| PM Review | Re-read key paper sections, review all code | Notes document |

---

## Project Structure

```
code/
  CMakeLists.txt
  phase1/
    2d_convolution.cpp
    im2col.cpp
  phase2/
    scatter_convolution.cpp
    benchmark.cpp
  phase3/
    rotate_kernel.cpp
    equivariance_demo.cpp
    p4_naive.cpp
    p4_scatter.cpp
  phase4/
    steerable_filter.cpp
    quadrant_mapping.cpp
  phase5/
    simple_segmentation.cpp
  phase6/
    cuda_basics.cu
```

## Key Design Decisions

- Every practice file is standalone (own `main()`)
- Verify against OpenCV built-in where possible
- No over-engineering -- minimal CMake, minimal abstractions
- Paper's .tex source is the primary reference for math notation
