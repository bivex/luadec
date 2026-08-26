Overview
========

LuaDec is a Lua decompiler for **Lua 5.1**, **Lua 5.2**, **Lua 5.3**, **Lua 5.4**, and **Lua 5.5**.

It is based on Hisham Muhammad's luadec which targeted Lua 5.0.x and LuaDec51 by Zsolt Sz. Sztupak.

LuaDec is free software and uses the same license as the original LuaDec.


Supported Versions
------------------
* **Lua 5.1** (Full support)
* **Lua 5.2** (Full support)
* **Lua 5.3** (Full support)
* **Lua 5.4** (Full support: 83 opcodes, `TFORPREP`/`TFORCALL`/`TFORLOOP`, `sJ`/`k` formats, to-be-closed variables)
* **Lua 5.5** (Full support: `ivABC` format, `OP_GETVARG`, `OP_ERRNNIL`, updated `TFOR` register layouts)


Compiling
---------

### macOS / Linux

To build `luadec` for a specific Lua version:

```bash
# 1. Compile the respective Lua engine (e.g., 5.4 or 5.5)
cd lua-5.4       # or lua-5.1, lua-5.2, lua-5.3, lua-5.5
make macosx      # or make linux

# 2. Compile LuaDec utilities (luadec, luareplace, luaopswap)
cd ../luadec
make LUAVER=5.4  # or LUAVER=5.1, LUAVER=5.2, LUAVER=5.3, LUAVER=5.5
```

### Windows (Visual Studio)
Project files are provided for Visual Studio (`vcproj-5.1`, `vcproj-5.2`, `vcproj-5.3`).


Tools Included
--------------
* **`luadec`** — Bytecode decompiler & disassembler.
* **`luareplace`** — Tool to replace functions inside compiled `.luac` files.
* **`luaopswap`** — Tool to swap opcode order in Lua chunks.


Usage
-----

* **Decompile a compiled binary chunk (`.luac` ➔ `.lua`):**
  ```bash
  luadec script.luac > script_decompiled.lua
  ```

* **Decompile a Lua source file directly:**
  ```bash
  luadec script.lua
  ```

* **Disassemble bytecode to human-readable assembly:**
  ```bash
  luadec -dis script.luac
  ```

* **Print nested function hierarchy:**
  ```bash
  luadec -pn script.luac
  # 0
  #   0_0
  #     0_0_0
  #   0_1
  ```

* **Decompile only a specific nested function:**
  ```bash
  luadec -f 0_1 script.luac
  ```

* **Disable processing sub-functions:**
  ```bash
  luadec -ns -f 0_1 script.luac
  ```

* **Compare decompiled output against original bytecode:**
  ```bash
  luadec -fc script.luac
  ```

* **Disable built-in local variable guessing (use debug symbols):**
  ```bash
  luadec -dg script.luac
  ```


Credits
-------

* Original by **Hisham Muhammad** (http://luadec.luaforge.net)
* Ongoing port to Lua 5.1 by **Zsolt Sz. Sztupak** (https://github.com/sztupy/luadec51/)
* Lua 5.2, 5.3, 5.4, and 5.5 enhancements by **VirusCamp** and contributors.
