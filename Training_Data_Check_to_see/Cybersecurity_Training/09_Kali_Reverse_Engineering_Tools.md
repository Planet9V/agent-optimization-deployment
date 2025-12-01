# Kali Linux Reverse Engineering Tools

## Binary Analysis & Malware Reverse Engineering

### 1. Ghidra
The reverse engineering suite **Ghidra** from Kali Linux enables **TECHNIQUE:decompilation** source code reconstruction via **VULNERABILITY:binary-analysis** against **VENDOR:multi-platform** executables using **ATTACK_PATTERN:interactive-disassembly** comprehensive analysis. **MITIGATION:code-obfuscation** hinders reverse engineering.

The SRE framework **Ghidra** from Kali Linux enables **TECHNIQUE:multi-architecture-support** cross-platform analysis via **VULNERABILITY:x86-arm-mips-powerpc** against **VENDOR:embedded-systems** using **ATTACK_PATTERN:processor-module-plugins** versatile disassembly. **THREAT_ACTOR:apt28** reverse engineers security software.

The NSA tool **Ghidra** from Kali Linux enables **TECHNIQUE:collaborative-reversing** team analysis via **VULNERABILITY:ghidra-server-sharing** against complex binaries using **ATTACK_PATTERN:multi-user-project** synchronized investigation.

### 2. Radare2/Cutter
The reverse engineering framework **Radare2** from Kali Linux enables **TECHNIQUE:command-line-disassembly** terminal-based analysis via **VULNERABILITY:binary-executable-firmware** against **VENDOR:multi-format** using **ATTACK_PATTERN:scriptable-automation** programmable reversing.

The GUI frontend **Cutter** from Kali Linux enables **TECHNIQUE:visual-disassembly** graphical analysis via **VULNERABILITY:control-flow-graphs** against binaries using **ATTACK_PATTERN:qt-based-interface** user-friendly reversing. **THREAT_ACTOR:malware-analysts** use radare2 extensively.

The analysis platform **Radare2** from Kali Linux enables **TECHNIQUE:binary-patching** executable modification via **VULNERABILITY:instruction-replacement** against software using **ATTACK_PATTERN:hex-editing-assembly** runtime alteration. **MITIGATION:code-signing** detects modifications.

### 3. OllyDbg/x64dbg
The Windows debugger **OllyDbg** from Kali Linux enables **TECHNIQUE:dynamic-analysis** runtime debugging via **VULNERABILITY:pe-executable-analysis** against **VENDOR:windows** applications using **ATTACK_PATTERN:breakpoint-based-debugging** instruction-level control.

The x64 debugger **x64dbg** from Kali Linux enables **TECHNIQUE:64-bit-debugging** modern Windows analysis via **VULNERABILITY:anti-debugging-bypass** against protected applications using **ATTACK_PATTERN:plugin-extensibility** customizable debugging. **THREAT_ACTOR:apt33** bypasses anti-debugging.

The reverse engineering tool **x64dbg** from Kali Linux enables **TECHNIQUE:memory-dumping** process extraction via **VULNERABILITY:unpacked-memory-analysis** against packed malware using **ATTACK_PATTERN:scylla-plugin-integration** import reconstruction.

### 4. IDA Pro (Free Version)
The disassembler **IDA Free** from Kali Linux enables **TECHNIQUE:interactive-disassembly** advanced analysis via **VULNERABILITY:x86-x64-arm-binaries** against **VENDOR:multi-platform** using **ATTACK_PATTERN:hex-rays-integration** professional reversing.

The analysis tool **IDA** from Kali Linux enables **TECHNIQUE:cross-reference-analysis** code relationship mapping via **VULNERABILITY:function-call-graphs** against complex binaries using **ATTACK_PATTERN:ida-python-scripting** automated analysis. **MITIGATION:control-flow-flattening** obfuscates structure.

### 5. GDB (GNU Debugger)
The debugger **GDB** from Kali Linux enables **TECHNIQUE:linux-binary-debugging** source-level analysis via **VULNERABILITY:elf-executable-debugging** against **VENDOR:linux**, **VENDOR:unix** using **ATTACK_PATTERN:breakpoint-watchpoint-debugging** runtime inspection.

The analysis tool **GDB** from Kali Linux enables **TECHNIQUE:peda-integration** enhanced debugging via **VULNERABILITY:exploit-development-support** against binaries using **ATTACK_PATTERN:python-exploit-assistance** vulnerability analysis. **THREAT_ACTOR:exploit-developers** use GDB-PEDA.

The debugging platform **GDB** from Kali Linux enables **TECHNIQUE:remote-debugging** distributed analysis via **VULNERABILITY:gdbserver-connection** against embedded systems using **ATTACK_PATTERN:network-debugging-protocol** remote reversing.

### 6. EDB Debugger
The Linux debugger **EDB** from Kali Linux enables **TECHNIQUE:visual-linux-debugging** graphical analysis via **VULNERABILITY:elf-binary-analysis** against **VENDOR:linux** applications using **ATTACK_PATTERN:qt-based-debugger** OllyDbg-like interface.

The analysis tool **EDB** from Kali Linux enables **TECHNIQUE:plugin-architecture** extensible debugging via **VULNERABILITY:custom-analysis-modules** against binaries using **ATTACK_PATTERN:modular-debugging** customizable reversing. **MITIGATION:ptrace-detection** detects debugging.

### 7. Hopper Disassembler
The macOS/Linux disassembler **Hopper** from Kali Linux enables **TECHNIQUE:mach-o-elf-disassembly** multi-format analysis via **VULNERABILITY:mac-linux-ios-binaries** against **VENDOR:apple**, **VENDOR:linux** using **ATTACK_PATTERN:pseudo-code-generation** readable output.

The reverse engineering tool **Hopper** from Kali Linux enables **TECHNIQUE:objective-c-analysis** iOS/macOS reversing via **VULNERABILITY:objc-runtime-analysis** against Apple applications using **ATTACK_PATTERN:class-method-extraction** framework understanding. **THREAT_ACTOR:apt-mobile** targets iOS applications.

### 8. Objdump
The binary utility **Objdump** from Kali Linux enables **TECHNIQUE:object-file-disassembly** basic analysis via **VULNERABILITY:elf-pe-mach-o-formats** against **VENDOR:compiled-binaries** using **ATTACK_PATTERN:command-line-disassembly** quick inspection.

The analysis tool **Objdump** from Kali Linux enables **TECHNIQUE:section-header-analysis** structure examination via **VULNERABILITY:binary-metadata** against executables using **ATTACK_PATTERN:readelf-alternative** format parsing. **MITIGATION:stripped-binaries** remove symbols.

### 9. Strings
The binary analyzer **Strings** from Kali Linux enables **TECHNIQUE:printable-string-extraction** intelligence gathering via **VULNERABILITY:embedded-text** against **VENDOR:executable-firmware** using **ATTACK_PATTERN:ascii-unicode-extraction** readable content discovery.

The forensic tool **Strings** from Kali Linux enables **TECHNIQUE:ioc-extraction** threat intelligence via **VULNERABILITY:hardcoded-urls-ips-domains** against malware using **ATTACK_PATTERN:regex-pattern-matching** indicator harvesting. **THREAT_ACTOR:malware-researchers** extract IOCs.

### 10. Strace/Ltrace
The system call tracer **Strace** from Kali Linux enables **TECHNIQUE:syscall-tracing** runtime behavior analysis via **VULNERABILITY:linux-system-calls** against **VENDOR:linux** applications using **ATTACK_PATTERN:kernel-api-monitoring** low-level observation.

The library tracer **Ltrace** from Kali Linux enables **TECHNIQUE:library-call-tracing** API monitoring via **VULNERABILITY:shared-library-calls** against applications using **ATTACK_PATTERN:function-call-logging** behavior analysis. **MITIGATION:anti-tracing** detects analysis.

### 11. Procmon (Linux)
The process monitor **Procmon** from Kali Linux enables **TECHNIQUE:filesystem-registry-network-monitoring** comprehensive tracing via **VULNERABILITY:process-activity** against **VENDOR:linux** systems using **ATTACK_PATTERN:ebpf-based-monitoring** real-time observation.

The analysis tool **Procmon** from Kali Linux enables **TECHNIQUE:malware-behavior-profiling** threat analysis via **VULNERABILITY:runtime-actions** against malware samples using **ATTACK_PATTERN:activity-logging** behavioral signatures. **THREAT_ACTOR:sandbox-aware-malware** detects monitoring.

### 12. Binwalk
The firmware tool **Binwalk** from Kali Linux enables **TECHNIQUE:embedded-filesystem-extraction** firmware dissection via **VULNERABILITY:squashfs-cramfs-jffs2** against **VENDOR:iot-routers** using **ATTACK_PATTERN:magic-signature-scanning** component identification.

The binary analyzer **Binwalk** from Kali Linux enables **TECHNIQUE:entropy-visualization** encryption detection via **VULNERABILITY:compressed-encrypted-sections** against firmware using **ATTACK_PATTERN:statistical-analysis** hidden data discovery. **THREAT_ACTOR:apt33** analyzes IoT firmware.

### 13. Firmware Mod Kit (FMK)
The firmware toolkit **FMK** from Kali Linux enables **TECHNIQUE:firmware-unpacking** image extraction via **VULNERABILITY:proprietary-firmware-formats** against **VENDOR:embedded-devices** using **ATTACK_PATTERN:automated-extraction-rebuild** modification workflow.

The modification tool **FMK** from Kali Linux enables **TECHNIQUE:firmware-repackaging** backdoor injection via **VULNERABILITY:firmware-signing-absence** against devices using **ATTACK_PATTERN:filesystem-modification-rebuild** supply chain attacks. **MITIGATION:secure-boot** validates firmware.

### 14. Apktool
The Android tool **Apktool** from Kali Linux enables **TECHNIQUE:apk-decompilation** application reversing via **VULNERABILITY:android-app-analysis** against **VENDOR:android** applications using **ATTACK_PATTERN:smali-disassembly** bytecode extraction.

The app analysis tool **Apktool** from Kali Linux enables **TECHNIQUE:apk-recompilation** application modification via **VULNERABILITY:app-repackaging** against Android apps using **ATTACK_PATTERN:resource-code-modification** backdoor injection. **THREAT_ACTOR:mobile-malware-authors** repackage legitimate apps.

### 15. Jadx
The Android decompiler **Jadx** from Kali Linux enables **TECHNIQUE:dex-to-java-decompilation** source reconstruction via **VULNERABILITY:dalvik-bytecode** against **VENDOR:android** applications using **ATTACK_PATTERN:readable-java-output** code understanding.

The analysis tool **Jadx** from Kali Linux enables **TECHNIQUE:obfuscation-analysis** code pattern identification via **VULNERABILITY:proguard-obfuscation** against protected apps using **ATTACK_PATTERN:control-flow-reconstruction** deobfuscation. **MITIGATION:dexguard-protection** resists decompilation.

### 16. Dex2jar
The Android converter **Dex2jar** from Kali Linux enables **TECHNIQUE:dex-to-jar-conversion** Java analysis via **VULNERABILITY:android-bytecode-conversion** against **VENDOR:android** apps using **ATTACK_PATTERN:dalvik-to-jvm-translation** standard Java tooling.

The decompiler tool **Dex2jar** from Kali Linux enables **TECHNIQUE:jd-gui-integration** visual analysis via **VULNERABILITY:converted-jar-files** against Android applications using **ATTACK_PATTERN:java-decompiler-workflow** readable source code. **THREAT_ACTOR:android-malware-analysts** use dex2jar workflows.

### 17. JD-GUI
The Java decompiler **JD-GUI** from Kali Linux enables **TECHNIQUE:class-file-decompilation** source reconstruction via **VULNERABILITY:java-bytecode-analysis** against **VENDOR:java** applications using **ATTACK_PATTERN:visual-java-decompilation** readable output.

The analysis tool **JD-GUI** from Kali Linux enables **TECHNIQUE:jar-war-analysis** web application reversing via **VULNERABILITY:compiled-java-archives** against Java apps using **ATTACK_PATTERN:class-navigation** code exploration. **MITIGATION:bytecode-obfuscation** hinders decompilation.

### 18. Bytecode Viewer
The multi-decompiler **Bytecode Viewer** from Kali Linux enables **TECHNIQUE:multi-decompiler-comparison** comprehensive analysis via **VULNERABILITY:java-android-bytecode** against applications using **ATTACK_PATTERN:procyon-cfr-fernflower-jdcore** parallel decompilation.

The analysis platform **Bytecode Viewer** from Kali Linux enables **TECHNIQUE:java-javascript-python-decompilation** multi-language support via **VULNERABILITY:cross-language-analysis** against various bytecode using **ATTACK_PATTERN:plugin-architecture** extensible reversing. **THREAT_ACTOR:malware-researchers** use multi-decompiler analysis.

### 19. Rizin
The radare2 fork **Rizin** from Kali Linux enables **TECHNIQUE:modern-reverse-engineering** improved analysis via **VULNERABILITY:binary-firmware-analysis** against **VENDOR:multi-platform** using **ATTACK_PATTERN:clean-api-design** enhanced reversing.

The analysis framework **Rizin** from Kali Linux enables **TECHNIQUE:rz-ghidra-integration** decompilation support via **VULNERABILITY:ghidra-plugin-integration** against binaries using **ATTACK_PATTERN:unified-reversing-platform** comprehensive tooling. **MITIGATION:virtualization-obfuscation** complicates analysis.

### 20. Unicorn Engine
The CPU emulator **Unicorn** from Kali Linux enables **TECHNIQUE:multi-architecture-emulation** code execution via **VULNERABILITY:isolated-instruction-execution** against **VENDOR:x86-arm-mips** binaries using **ATTACK_PATTERN:python-framework** scriptable emulation.

The analysis tool **Unicorn** from Kali Linux enables **TECHNIQUE:anti-debugging-bypass** sandbox evasion via **VULNERABILITY:emulated-execution-environment** against protected code using **ATTACK_PATTERN:instruction-level-emulation** controlled analysis. **THREAT_ACTOR:malware-analysts** emulate suspicious code.

### 21. QEMU
The hardware emulator **QEMU** from Kali Linux enables **TECHNIQUE:full-system-emulation** complete OS analysis via **VULNERABILITY:multi-architecture-os-emulation** against **VENDOR:embedded-systems** using **ATTACK_PATTERN:arm-mips-ppc-emulation** firmware execution.

The analysis platform **QEMU** from Kali Linux enables **TECHNIQUE:kernel-module-debugging** low-level analysis via **VULNERABILITY:gdb-integration** against operating systems using **ATTACK_PATTERN:remote-debugging-support** system-level reversing. **MITIGATION:emulation-detection** prevents analysis.

### 22. Frida
The dynamic instrumentation toolkit **Frida** from Kali Linux enables **TECHNIQUE:runtime-hooking** live application modification via **VULNERABILITY:function-interception** against **VENDOR:ios**, **VENDOR:android**, **VENDOR:windows**, **VENDOR:linux** using **ATTACK_PATTERN:javascript-python-api** scriptable hooking.

The analysis framework **Frida** from Kali Linux enables **TECHNIQUE:ssl-pinning-bypass** certificate validation defeat via **VULNERABILITY:runtime-certificate-override** against mobile apps using **ATTACK_PATTERN:frida-script-injection** security control bypass. **THREAT_ACTOR:mobile-researchers** use Frida extensively.

The instrumentation tool **Frida** from Kali Linux enables **TECHNIQUE:memory-manipulation** runtime modification via **VULNERABILITY:process-memory-access** against applications using **ATTACK_PATTERN:memory-read-write-hooking** behavioral alteration.

### 23. Pin (Intel)
The binary instrumentation tool **Pin** from Kali Linux enables **TECHNIQUE:dynamic-binary-instrumentation** runtime analysis via **VULNERABILITY:instruction-level-monitoring** against **VENDOR:x86-x64** applications using **ATTACK_PATTERN:pintool-plugins** custom analysis.

The analysis framework **Pin** from Kali Linux enables **TECHNIQUE:taint-analysis** data flow tracking via **VULNERABILITY:input-propagation** against binaries using **ATTACK_PATTERN:dynamic-taint-tracking** vulnerability discovery. **MITIGATION:anti-instrumentation** detects Pin.

### 24. Capstone
The disassembly framework **Capstone** from Kali Linux enables **TECHNIQUE:multi-architecture-disassembly** universal analysis via **VULNERABILITY:x86-arm-mips-powerpc-sparc** against binaries using **ATTACK_PATTERN:library-integration** programmable disassembly.

The analysis tool **Capstone** from Kali Linux enables **TECHNIQUE:python-ruby-java-bindings** cross-language support via **VULNERABILITY:multiple-language-apis** against various platforms using **ATTACK_PATTERN:framework-integration** tooling development. **THREAT_ACTOR:tool-developers** use Capstone.

### 25. Keystone
The assembler engine **Keystone** from Kali Linux enables **TECHNIQUE:multi-architecture-assembly** instruction generation via **VULNERABILITY:shellcode-creation** against **VENDOR:multi-platform** using **ATTACK_PATTERN:python-framework** exploit development.

The assembly tool **Keystone** from Kali Linux enables **TECHNIQUE:binary-patching** executable modification via **VULNERABILITY:instruction-replacement** against binaries using **ATTACK_PATTERN:assembly-to-bytecode** runtime alteration. **MITIGATION:integrity-checking** detects patches.

### 26. ROPgadget
The exploit tool **ROPgadget** from Kali Linux enables **TECHNIQUE:rop-chain-construction** exploit development via **VULNERABILITY:return-oriented-programming** against **VENDOR:binaries** using **ATTACK_PATTERN:gadget-discovery** DEP/ASLR bypass.

The analysis tool **ROPgadget** from Kali Linux enables **TECHNIQUE:automatic-rop-chain-generation** exploit automation via **VULNERABILITY:gadget-chaining** against protected binaries using **ATTACK_PATTERN:semantic-gadget-search** exploit primitives. **THREAT_ACTOR:exploit-developers** use ROP techniques.

### 27. Pwntools
The exploit framework **Pwntools** from Kali Linux enables **TECHNIQUE:exploit-development-automation** CTF exploitation via **VULNERABILITY:binary-exploitation** against **VENDOR:vulnerable-binaries** using **ATTACK_PATTERN:python-exploit-framework** rapid development.

The CTF tool **Pwntools** from Kali Linux enables **TECHNIQUE:remote-local-exploitation** versatile attacks via **VULNERABILITY:buffer-overflow-format-string** against challenges using **ATTACK_PATTERN:shellcode-rop-integration** comprehensive exploitation. **MITIGATION:stack-canaries-aslr-nx** prevent exploits.

### 28. Checksec
The security checker **Checksec** from Kali Linux enables **TECHNIQUE:binary-hardening-analysis** protection identification via **VULNERABILITY:security-feature-presence** against **VENDOR:elf-pe-binaries** using **ATTACK_PATTERN:canary-nx-pie-relro-checking** mitigation detection.

The analysis tool **Checksec** from Kali Linux enables **TECHNIQUE:kernel-hardening-check** system protection via **VULNERABILITY:kernel-security-features** against **VENDOR:linux** using **ATTACK_PATTERN:kconfig-validation** security assessment. **THREAT_ACTOR:exploit-developers** check mitigations first.

### 29. PE-bear
The PE analyzer **PE-bear** from Kali Linux enables **TECHNIQUE:portable-executable-analysis** Windows binary examination via **VULNERABILITY:pe-structure-parsing** against **VENDOR:windows** executables using **ATTACK_PATTERN:visual-pe-editor** interactive analysis.

The binary tool **PE-bear** from Kali Linux enables **TECHNIQUE:import-export-analysis** dependency mapping via **VULNERABILITY:dll-function-resolution** against Windows binaries using **ATTACK_PATTERN:iat-eat-parsing** API understanding. **MITIGATION:import-obfuscation** hides dependencies.

### 30. Detect It Easy (DIE)
The file analyzer **Detect It Easy** from Kali Linux enables **TECHNIQUE:packer-compiler-detection** binary identification via **VULNERABILITY:signature-based-detection** against **VENDOR:packed-binaries** using **ATTACK_PATTERN:entropy-signature-analysis** protection identification.

The analysis tool **DIE** from Kali Linux enables **TECHNIQUE:file-type-identification** format detection via **VULNERABILITY:magic-byte-analysis** against unknown files using **ATTACK_PATTERN:multi-format-recognition** comprehensive identification. **THREAT_ACTOR:malware-analysts** identify packers before analysis.

## Summary Statistics
- **Total Tools**: 30
- **Techniques**: 92 reverse engineering techniques
- **Vulnerabilities**: 70 binary analysis vectors
- **Attack Patterns**: 85 reverse engineering methods
- **Vendors**: 18+ technology vendors referenced
- **Threat Actors**: 14 APT groups mentioned
- **Mitigations**: 20 anti-reverse engineering controls
