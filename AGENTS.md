# AGENTS.md

This repository is a learning workspace for "Accelerated Rotation-Invariant Convolution for UAV Image Segmentation".

## Project Overview

```text
.
├── code/
├── docs/
├── src/
```

- `docs/` is the study reference layer.
- `code/` is the C++ implementation layer: each phase turns one part of the paper or learning plan into small, standalone C++ programs. Keep examples focused and runnable rather than building a reusable framework.
- `src/` is the Python reproduction layer: keep modules educational, focused, and runnable through standalone examples.

## Environment Configuration

- Target runtime environment: WSL2 Ubuntu 24.04.
  - The assistant runs on Windows, not inside WSL2. Do not execute WSL2-only commands directly from the assistant environment.
  - When a command must run in WSL2, stop and tell the user the exact command to run in WSL2, then continue after the user provides the result.
  - Exception: `uv` commands for Python environment management and Python examples may run on the Windows host when they do not depend on WSL2-only tools.

- C++ standard: C++17.
- Python: use `uv` with Python 3.11.
- CUDA: configure only when reaching the CUDA learning phase. Version TBD.

## Build and Test Command

- Run these commands in WSL2 Ubuntu 24.04, not from the Windows assistant environment:

```bash
cmake -S code -B code/build
cmake --build code/build

./code/build/2d_convolution
./code/build/im2col
```

- There is no dedicated test suite yet. Treat each standalone executable as a smoke test for its topic.
- After adding a new source file, update `code/CMakeLists.txt`, rebuild, and ask the user to run the new executable in WSL2.

## Teaching Style

- The user is a beginner in this area. Explain concepts with both rigorous academic language and beginner-friendly intuition.
- For mathematical topics, use precise terminology, symbols, and formula derivations. Show why an equation or algorithm is correct when it matters.
- Pair formal explanations with simple analogies or small numerical examples.
- For paper concepts, connect theory to the corresponding code file and learning phase.
- Keep explanations concise. Do not dilute technical accuracy.

## Code Style

- Strictly follow Google C++ Style Guide.
- Do not add project-specific style deviations.

## Git Rules

- Use atomic commits. Commit one logical change at a time instead of batching unrelated work.
- Write commit messages in Conventional Commits format: `<type>(<scope>): <subject>`.
- Prefer scopes such as `docs`, `code`, `phase1`, `cmake`, or the specific learning phase.
- Examples: `docs(agents): add project workflow rules`, `feat(phase2): add scatter convolution demo`, `build(cmake): add phase executable`.

## Output

- Return code first. Explanation after, only if non-obvious.
- No inline prose. Use comments sparingly - only where logic is unclear.
- No boilerplate unless explicitly requested.

## Code Rules

- Simplest working solution. No over-engineering.
- No abstractions for single-use operations.
- No speculative features or "you might also want..."
- Read the file before modifying it. Never edit blind.
- No docstrings or type annotations on code not being changed.
- No error handling for scenarios that cannot happen.
- Three similar lines is better than a premature abstraction.

## Review Rules

- State the bug. Show the fix. Stop.
- No suggestions beyond the scope of the review.
- No compliments on the code before or after the review.

## Debugging Rules

- Never speculate about a bug without reading the relevant code first.
- State what you found, where, and the fix. One pass.
- If cause is unclear: say so. Do not guess.

## Simple Formatting

- No em dashes, smart quotes, or decorative Unicode symbols.
- Plain hyphens and straight quotes only.
- Natural language characters (accented letters, CJK, etc.) are fine when the content requires them.
- Code output must be copy-paste safe.
