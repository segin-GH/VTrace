# VTrace - Git Version Trace Generator

**VTrace** is a lightweight, developer-friendly version tracking utility that generates source-compatible and human-readable files containing Git metadata about the current commit. It's ideal for embedding version info in firmware, binaries, or build logs to ensure traceability and reproducibility of builds.

---

## 🔧 What Does VTrace Do?

On execution, `vtrace.py`:
- Runs a series of Git commands to collect metadata about the current commit.
- Captures the Git tag, SHA, branch, `git describe` output, and current timestamp.
- Outputs the metadata to:
  - A `version.h` C header file (for embedding in code)
  - A `version.yml` file (for CI logs, release packaging, etc.)

---

## 📦 What Information Is Collected?

| Field              | Description                                  |
|-------------------|----------------------------------------------|
| `Git Describe`     | Output of `git describe --tags --long`      |
| `Git Branch`       | Active branch name                          |
| `Git Sha`          | Full commit hash                            |
| `Git Sha-short`    | Abbreviated short SHA                       |
| `Git Tag`          | Most recent tag                             |
| `Commit Timestamp` | UTC timestamp when the file was generated   |

---

## 🖥 Example Output

### 🔹 `version.h`

```c
/* This file was auto generated from VTrace. */

#pragma once

#define TIMESTAMP         "2025-05-01 14:32:11.230176"
#define GIT_BRANCH        "main"
#define GIT_DESCRIBE      "v1.0.3-5-g3f8a2cd-dirty"
#define GIT_SHA           "3f8a2cd123456789abcdefabcdef123456789abc"
#define GIT_SHA_SHORT     "3f8a2cd"
#define GIT_TAG           "v1.0.3"
```

---

### 🔸 `version.yml`

```yaml
# This file was auto generated from VTrace.

Commit Timestamp: '2025-05-01 14:32:11.230176'
Git Branch: main
Git Describe: v1.0.3-5-g3f8a2cd-dirty
Git Sha: 3f8a2cd123456789abcdefabcdef123456789abc
Git Sha-short: 3f8a2cd
Git Tag: v1.0.3
```

---

## 🚀 Use Cases

- Embed version info in firmware via `version.h`
- Generate reproducible build metadata for CI/CD pipelines
- Package build artifacts with `version.yml` for traceability
- Quickly identify the exact commit and tag of a deployed version

---

## 🏗 How to Run

Simply execute the script from your Git repository:

```bash
python3 vtrace.py
```

Output files (`version.h` and `version.yml`) will be generated in the current directory.

---

## 📌 Requirements

- Python 3.6+
- Git must be installed and available in `PATH`
- Script must be run inside a Git repository

---

## 📁 File Output Options

Currently supports generating:
- C header file (`version.h`)
- YAML metadata (`version.yml`)

Future support planned for:
- `version.json`
- `version.txt`

---

## 🧪 Example Integration

In CMakeLists.txt:
```cmake
# Find Python3
find_package(Python3 REQUIRED)

set(VTRACE_SCRIPT ${CMAKE_CURRENT_SOURCE_DIR}/scripts/vtrace.py)
set(VTRACE_OUT_H ${CMAKE_CURRENT_BINARY_DIR}/version.h)
set(VTRACE_OUT_YML ${CMAKE_CURRENT_BINARY_DIR}/version.yml)

# Custom command to generate version files
add_custom_command(
    OUTPUT ${VTRACE_OUT_H} ${VTRACE_OUT_YML}
    COMMAND ${Python3_EXECUTABLE} ${VTRACE_SCRIPT}
    DEPENDS ${VTRACE_SCRIPT} ${CMAKE_SOURCE_DIR}/.git/index
    COMMENT "Running VTrace to generate version info"
    VERBATIM
)

# Custom target that depends on the output files
add_custom_target(generate_version ALL
    DEPENDS ${VTRACE_OUT_H} ${VTRACE_OUT_YML}
)

# Your application target depends on version generation
add_dependencies(app generate_version)

# Add header include path
include_directories(${CMAKE_CURRENT_BINARY_DIR})
```
---

In source file:
```c
#include "version.h"
printf("Firmware built from commit: %s\n", GIT_DESCRIBE);
```
## 📝 License

MIT License. Use it, modify it, ship it.
