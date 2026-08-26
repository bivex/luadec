Overview
========

**LuaDec** is a high-performance, memory-safe Lua decompiler and disassembler supporting **Lua 5.1**, **Lua 5.2**, **Lua 5.3**, **Lua 5.4**, and **Lua 5.5**.

It reconstructs readable Lua source code from compiled bytecode chunks (`.luac`), with advanced control-flow analysis, local variable recovery, and short-circuit expression rebuilding.

Originally created by Hisham Muhammad (Lua 5.0) and ported to Lua 5.1 by Zsolt Sz. Sztupak (`luadec51`), with comprehensive Lua 5.2–5.5 architecture support by VirusCamp and contributors.


Key Features
------------
* **Universal Lua Support**: Lua 5.1, 5.2, 5.3, 5.4, and 5.5.
* **Stripped Bytecode Support**: Full reconstruction of chunks stripped with `luac -s` (dynamic `_ENV` resolution, local name inference, and upvalue inheritance).
* **Advanced Expression Engine**: Accurate short-circuit expressions (`return a or b`, `arr[idx] or arr[#arr]`, nested boolean logic chains).
* **Memory Safety & Robustness**: Zero-leak architecture verified under Clang UBSan, ASan, and macOS `leaks` / `MallocGuardEdges`.
* **Zero Compiler Warnings**: Clean `-Wall` compilation on macOS (Apple Silicon / Intel) and Linux.
* **Specialized Tools**: Includes `popcap_converter.py` for decompiling PopCap (e.g. *Plants vs. Zombies*) custom Lua 5.0 bytecode.


Supported Versions
------------------
| Version | Status | Highlights |
| :--- | :---: | :--- |
| **Lua 5.1** | ✅ Full | Standard 5.1 bytecode, vararg parameters, OP_CLOSE / TFORLOOP |
| **Lua 5.2** | ✅ Full | Goto/labels, `_ENV` lexical scoping, `OP_TFORCALL` + `OP_TFORLOOP` |
| **Lua 5.3** | ✅ Full | Bitwise/integer operators (`//`, `&`, `\|`, `~`, `<<`, `>>`), safe upvalue tables |
| **Lua 5.4** | ✅ Full | 83 opcodes, `isJ`/`k` instruction formats, to-be-closed (`<close>`) variables, `OP_TFORPREP` |
| **Lua 5.5** | ✅ Full | `ivABC` format, `OP_GETVARG`, `OP_ERRNNIL`, updated TFOR register mappings |


Compiling
---------

### macOS / Linux

Build `luadec` for your target Lua version:

```bash
# 1. Compile the respective Lua core library (e.g., 5.4)
cd lua-5.4       # or lua-5.1, lua-5.2, lua-5.3, lua-5.5
make macosx      # or: make linux

# 2. Compile LuaDec utilities (luadec, luareplace, luaopswap)
cd ../luadec
make LUAVER=5.4  # or: LUAVER=5.1, LUAVER=5.2, LUAVER=5.3, LUAVER=5.5
```

To build and test all versions in batch:
```bash
for v in 5.1 5.2 5.3 5.4 5.5; do
    make -C lua-$v macosx  # or linux
    make -C luadec LUAVER=$v clean
    make -C luadec LUAVER=$v
done
```

### Windows (Visual Studio)
Project files are provided for Visual Studio (`vcproj-5.1`, `vcproj-5.2`, `vcproj-5.3`).


Tools Included
--------------
* **`luadec`** — Bytecode decompiler and disassembler.
* **`luareplace`** — Injects or replaces function prototypes inside compiled `.luac` binaries.
* **`luaopswap`** — Swaps opcode order in precompiled Lua chunks for obfuscated binaries.
* **`tools/popcap_converter.py`** — Converts PopCap modified Lua 5.0 bytecode (used in *Plants vs. Zombies*) into standard Lua 5.1 bytecode for direct decompilation.


Usage
-----

### Basic Decompilation

* **Decompile a compiled binary chunk (`.luac` ➔ `.lua`):**
  ```bash
  ./luadec/luadec script.luac > script_decompiled.lua
  ```

* **Decompile a Lua source file directly (compiles on the fly):**
  ```bash
  ./luadec/luadec script.lua
  ```

* **Disassemble bytecode to human-readable assembly instructions:**
  ```bash
  ./luadec/luadec -dis script.luac
  ```

### Advanced Options

* **Print function hierarchy tree:**
  ```bash
  ./luadec/luadec -pn script.luac
  # 0
  #   0_0
  #     0_0_0
  #   0_1
  ```

* **Decompile only a specific sub-function:**
  ```bash
  ./luadec/luadec -f 0_1 script.luac
  ```

* **Disable processing sub-functions:**
  ```bash
  ./luadec/luadec -ns -f 0_1 script.luac
  ```

* **Compare decompiled output against original bytecode:**
  ```bash
  ./luadec/luadec -fc script.luac
  ```

* **Disable local variable guessing (use debug symbols only):**
  ```bash
  ./luadec/luadec -dg script.luac
  ```

### PopCap / PvZ Bytecode Decompilation

To decompile PopCap `.luac` files:
```bash
# 1. Convert PopCap Lua 5.0 format to Lua 5.1
python3 tools/popcap_converter.py /path/to/game.luac /tmp/converted_51.luac

# 2. Decompile with luadec (LUAVER=5.1)
./luadec/luadec /tmp/converted_51.luac
```


Credits & License
-----------------
* Original LuaDec by **Hisham Muhammad** (http://luadec.luaforge.net)
* Lua 5.1 port by **Zsolt Sz. Sztupak** (https://github.com/sztupy/luadec51/)
* Lua 5.2, 5.3, 5.4, 5.5 support and memory safety enhancements by **VirusCamp** and contributors.
* Licensed under the same MIT-style license as Lua and the original LuaDec.
