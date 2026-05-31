# miditxt_converter

🕹️ ■ □ ■ Standard MIDI File ⇄ Raw Text Dual-Way Independent Converter ■ □ ■ 👾

An 8-bit utility bridging LLMs and DAWs by converting MIDI to raw text and back. It filters complex MIDI into clean `note`, `vel`, `time` strings for LLMs. For MIDI reconstruction, it locks the timebase at **480 Ticks/Beat** and injects a **120 BPM** tempo tag, preventing missing bars or grid drift in DAWs. Standalone .exe with ZH/EN/JA UI.

---

## ❖ 核心痛点解决 / Problem Solved

### 中文 (ZH)
标准 MIDI 文件为二进制格式，包含复杂的底层 Tick 时钟和 Meta 指令，直接转换为文本时极其臃肿，大模型无法稳定理解与输出。而直接将 AI 导出的文本写入新 MIDI 时，又经常由于时钟分辨率不匹配导致数字音频工作站（DAW，如 Cubase、FL Studio）中出现“漏拍、错位、快进”等严重断流现象。该工具通过底层时基归一化彻底扬了此 Bug。

### English (EN)
Standard MIDI files are encoded in binary and packed with low-level Tick clocks, making raw data too bloated for LLMs to interpret or generate reliably. Conversely, when reassembling AI-generated text back into a MIDI file, subtle mismatches in timebase resolution frequently trigger severe timing bugs, such as skipped beats or grid drift within the DAW timeline. This utility completely resolves the issue via underlying normalization.

---

## ❖ 技术机制 / Technical Mechanism

1. **数据语料化 (MIDI ➔ TEXT)** 精简并过滤单轨 MIDI 中的冗余控制信息，将其解构为纯粹、高可读性的文本指令（包含音高 `note`、力度 `vel` 与相对时值 `time`），完美对齐大模型上下文。
   *Filters and condenses MIDI streams into human-and-model-readable text strings, making it ideal for LLM prompt training and parsing.*

2. **时基归一化 (TEXT ➔ MIDI)** 强制将新建 MIDI 轨道的时基锁死在标准的 **480 Ticks/Beat**，并自动在音轨头部注入 **120 BPM** 的标准速度元数据（`set_tempo`）。
   *Forces the newly constructed MIDI track to lock at a standard **480 Ticks/Beat** resolution and dynamically injects a standard **120 BPM** tempo meta-tag.*

---

## ❖ 项目结构 / Repository Structure

```text
├── .gitignore          # 自动隔离打包缓存与临时编译文件 (Excludes build artifacts)
├── README.md           # 双语技术概述文档 (This documentation)
└── miditxt.py          # 核心源码：冷酷像素风多语言 UI 转换引擎 (Core source code)
