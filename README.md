# VoxControl AI - Advanced Voice-Controlled PC Assistant

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![OS](https://img.shields.io/badge/Windows-10%20%7C%2011-0078D6.svg)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-20%20passed-success.svg)](tests/)

**VoxControl AI** is a fully functional, offline-first Windows desktop voice assistant that enables users to operate their computer through natural spoken voice commands.

Unlike simple launchers that merely open or close programs, VoxControl AI interacts deeply **inside** supported applications: searching for content, playing/pausing media, scrolling, focusing input fields, typing Unicode text, navigating files, and executing multi-step sequential workflows.

---

## 1. System Architecture

VoxControl AI is engineered with a modular, decoupled architecture:

```
voxcontrol1/
├── main.py                     # Application startup entry point
├── requirements.txt            # Dependency definitions
├── config.json                 # Speech recognition, audio, and safety settings
├── apps.json                   # Application aliases and path resolution rules
├── README.md                   # Complete documentation and demo guide
├── assistant/
│   ├── __init__.py             # Package initializer
│   ├── action_executor.py      # Background execution coordinator and pacing
│   ├── action_planner.py       # Decomposes multi-step voice commands into plans
│   ├── app_controller.py       # Application lifecycle and window switching
│   ├── browser_controller.py   # Chrome & Edge controls (shortcuts + Playwright)
│   ├── command_parser.py       # Natural language intent & entity parsing
│   ├── command_router.py       # Context-aware dispatch to subsystems
│   ├── context_manager.py      # Session state and window tracking
│   ├── dictation_engine.py     # Punctuation formatting, typing, and editing
│   ├── editor_controller.py    # Notepad, VS Code, and Word automation
│   ├── file_explorer_controller.py # Windows File Explorer navigation & actions
│   ├── safety.py               # Destructive command blocker & confirmation manager
│   ├── speech_input.py         # faster-whisper local STT + level metering
│   ├── speech_output.py        # Asynchronous non-blocking pyttsx3 TTS
│   ├── system_controller.py    # pycaw volume, window focus, scrolling, hotkeys
│   ├── verification.py         # State change verification engine
│   ├── whatsapp_controller.py  # WhatsApp Desktop & Web automation
│   ├── windows_ui_controller.py# Accessible UI Automation (pywinauto UIA)
│   └── youtube_controller.py   # YouTube search and video player controls
├── ui/
│   ├── __init__.py             # UI package initializer
│   └── dashboard.py            # Modern CustomTkinter dark-themed desktop GUI
└── tests/
    ├── __init__.py             # Test suite initializer
    ├── test_command_parser.py  # Intent recognition and compound command parsing
    ├── test_context_manager.py # Action planning, step tracking, and cancellation
    ├── test_controllers.py     # Volume clamping, app resolution, and routing
    ├── test_dictation.py       # Spoken punctuation formatting and editing rules
    └── test_safety.py          # Dangerous command blocking and confirmation
```

---

## 2. Core Capabilities

### 🎙️ Dual Voice Engines
- **Speech-to-Text (STT):** Local, private speech recognition using `faster-whisper` (`tiny.en` on CPU `int8`) with automatic fallback to `speech_recognition`.
- **Text-to-Speech (TTS):** Non-blocking, offline voice responses using `pyttsx3` in an asynchronous background queue (GUI remains 100% fluid).
- **Listening Modes:** Push-to-Talk and Continuous Listening with ambient voice activity detection.
- **Microphone Visualizer:** Real-time audio VU meter in the dashboard.

### 📝 Command Mode vs. Dictation Mode
- **Command Mode:** Spoken input is interpreted as operational computer instructions.
- **Dictation Mode:** Natural speech is formatted and typed directly into the active field:
  - Spoken punctuation translation: *"period"* ➔ `.`, *"comma"* ➔ `,`, *"question mark"* ➔ `?`, *"exclamation mark"* ➔ `!`, *"new line"* ➔ `\n`, *"new paragraph"* ➔ `\n\n`.
  - Inline voice editing: *"backspace"*, *"delete"*, *"select all"*, *"copy"*, *"paste"*, *"undo"*, *"redo"*.
  - Safe Unicode insertion via clipboard paste with **automatic clipboard preservation and restoration**.

### 🛡️ Safety & Confirmation Protection
- Ordinary navigation executes directly.
- **High-impact operations** (sending WhatsApp messages, deleting files, overwriting documents) require **explicit user confirmation** via voice (*"yes, send it"*) or the UI **Approve** button.
- Dangerous destructive shell commands (*"format c:"*, *"rmdir /s"*, *"del /f"*, arbitrary bash/powershell executions) are blocked automatically.
- **Emergency Stop:** Instant cancellation of active workflows via the red UI button, voice command (*"stop"* / *"cancel"*), or hotkey.

---

## 3. Supported Voice Commands

| Category | Spoken Command Examples | Action Performed |
| :--- | :--- | :--- |
| **System Volume** | *"Set volume to 40 percent"*<br>*"Increase volume"* / *"Volume up"*<br>*"Decrease volume"* / *"Turn it down"*<br>*"Mute"* / *"Unmute"* | Adjusts master volume via `pycaw`<br>Increases volume by 10%<br>Decreases volume by 10%<br>Toggles master mute |
| **Window Management** | *"Minimize window"*<br>*"Maximize window"*<br>*"Restore window"*<br>*"Switch window"*<br>*"Switch to Notepad"*<br>*"Close the current window"* | Minimizes foreground window<br>Maximizes foreground window<br>Restores window size<br>Alt+Tab window switch<br>Brings Notepad to focus<br>Safely closes active window |
| **Scrolling & Navigation** | *"Scroll down"* / *"Scroll down a lot"*<br>*"Scroll up"* / *"Scroll up a little"*<br>*"Scroll to top"* / *"Scroll to bottom"*<br>*"Go back"* / *"Go forward"* | Scrolls active document/page down<br>Scrolls active document/page up<br>Jumps to top or bottom (Ctrl+Home/End)<br>Navigates history backward/forward |
| **Applications** | *"Open Chrome"*<br>*"Open Notepad"*<br>*"Open Calculator"*<br>*"Open File Explorer"*<br>*"Open VS Code"*<br>*"Close Chrome"* | Resolves and opens application<br>Brings running window forward<br>Safely closes app without killing arbitrary tasks |
| **Browser Control** | *"Search for Arduino tutorials"*<br>*"Go to python.org"*<br>*"Open a new tab"* / *"Close tab"*<br>*"Next tab"* / *"Previous tab"*<br>*"Refresh page"*<br>*"Zoom in"* / *"Zoom out"*<br>*"Focus address bar"* | Performs Google search<br>Navigates to URL<br>Ctrl+T / Ctrl+W<br>Ctrl+Tab / Ctrl+Shift+Tab<br>F5 refresh<br>Ctrl++ / Ctrl+-<br>Ctrl+L address focus |
| **YouTube Control** | *"Open YouTube"*<br>*"Search YouTube for ESP32 projects"*<br>*"Play the first video"*<br>*"Pause the video"* / *"Resume"*<br>*"Skip forward ten seconds"*<br>*"Go back ten seconds"*<br>*"Enter fullscreen"* / *"Exit fullscreen"*<br>*"Set playback speed to 1.5 times"*<br>*"Scroll down to the comments"* | Opens YouTube homepage<br>Opens YouTube search results<br>Selects first video result<br>Toggles playback ('k'/space)<br>Skips forward 10s ('l')<br>Rewinds 10s ('j')<br>Toggles fullscreen ('f'/Esc)<br>Adjusts playback speed (Shift+>)<br>Scrolls down to comments |
| **WhatsApp** | *"Open WhatsApp"*<br>*"Search for Rahul"*<br>*"Open the first Rahul"*<br>*"Type hello Rahul, I will reach in ten minutes"*<br>*"Yes, send it"* / *"Cancel"* | Focuses/opens WhatsApp<br>Searches contact in chat list<br>Opens chat conversation<br>Drafts text into message box<br>**Sends message after explicit confirmation** |
| **Dictation & Text** | *"Start dictation"*<br>*"Welcome to our presentation period"*<br>*"New line"*<br>*"Select all"* / *"Copy"* / *"Paste"*<br>*"Stop dictation"* | Activates Dictation Mode<br>Types: "Welcome to our presentation."<br>Inserts newline (`\n`)<br>Executes hotkeys<br>Returns to Command Mode |
| **Multi-Step Tasks** | *"Open Chrome, go to YouTube, search for Arduino Uno, and play the first result"* | Parses, verifies, and executes all 4 steps in order |

---

## 4. Installation & Setup

### Prerequisites
- Windows 10 or Windows 11 (64-bit)
- Python 3.10, 3.11, or 3.12 installed
- Microphone and speakers/headphones connected

### Installation Steps

1. **Clone or navigate to the project directory:**
   ```powershell
   cd d:\voxcontrol1
   ```

2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Verify installation with tests:**
   ```powershell
   python -m pytest -v
   ```

---

## 5. Starting VoxControl AI

Launch the desktop assistant by running:

```powershell
python main.py
```

The dark-themed **VoxControl AI Dashboard** will appear:
- Click **PUSH TO TALK** (or toggle **Continuous Listening**).
- Speak naturally into your microphone.
- Or type commands into the quick execution bar at the bottom.

---

## 6. Live Demonstration Guide

Follow this step-by-step walkthrough to demonstrate VoxControl AI's full capabilities:

### Demo Scenario 1: System Control
1. Click **PUSH TO TALK** (or use the bottom text bar).
2. Say: `"Set volume to 40 percent"`
   - *Result:* Windows master volume adjusts to 40% and VoxControl responds: *"Master volume set to 40%."*
3. Say: `"Mute"` ➔ Audio mutes.
4. Say: `"Unmute"` ➔ Audio unmutes.

### Demo Scenario 2: Multi-Step Browser & YouTube Automation
1. Say: `"Open Chrome, go to YouTube, and play the first result"`
   - *Result:*
     1. Chrome launches and is brought to the foreground.
     2. YouTube opens.
     3. The first video is selected and playback starts.
2. Say: `"Pause the video"` ➔ Video pauses.
3. Say: `"Resume"` ➔ Video resumes.
4. Say: `"Skip forward ten seconds"` ➔ Playhead skips forward.
5. Say: `"Scroll down to the comments"` ➔ Page scrolls to the comments section.

### Demo Scenario 3: Dictation Mode in Notepad
1. Say: `"Open Notepad"` ➔ Notepad opens.
2. Say: `"Start dictation"` ➔ Voice prompt: *"Dictation mode activated."*
3. Say: `"Hello team comma welcome to VoxControl AI period new line testing voice typing exclamation mark"`
   - *Result:* Types into Notepad:
     ```
     Hello team, welcome to VoxControl AI.
     testing voice typing!
     ```
4. Say: `"Select all"` ➔ Selects all text.
5. Say: `"Stop dictation"` ➔ Voice prompt: *"Dictation mode stopped. Switched to command mode."*

### Demo Scenario 4: WhatsApp with Safety Confirmation
1. Say: `"Open WhatsApp"` ➔ Brings WhatsApp window forward.
2. Say: `"Search for Rahul"` ➔ Enters Rahul into the WhatsApp search bar.
3. Say: `"Open the first Rahul"` ➔ Opens conversation with Rahul.
4. Say: `"Type hello Rahul, I will reach in ten minutes"` ➔ Types draft into the input field.
   - *Safety Guard:* A high-visibility confirmation banner appears on the dashboard with **Approve** and **Cancel** buttons, and the assistant asks for confirmation.
5. Say: `"Yes, send it"` (or click **Approve Action**) ➔ Message sends.

---

## 7. Automated Test Suite Results

VoxControl AI includes a comprehensive test suite covering command parsing, compound splitting, safety policies, context tracking, volume bounds, and dictation rules:

```
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1
rootdir: D:\voxcontrol1
collected 20 items

tests/test_command_parser.py::test_volume_commands PASSED                [  5%]
tests/test_command_parser.py::test_youtube_commands PASSED               [ 10%]
tests/test_command_parser.py::test_whatsapp_commands PASSED              [ 15%]
tests/test_command_parser.py::test_application_and_window_commands PASSED [ 20%]
tests/test_command_parser.py::test_scrolling_and_navigation PASSED       [ 25%]
tests/test_command_parser.py::test_compound_command_splitting PASSED     [ 30%]
tests/test_context_manager.py::test_action_planner_generates_ordered_plan PASSED [ 35%]
tests/test_context_manager.py::test_context_manager_state PASSED         [ 40%]
tests/test_controllers.py::test_app_controller_resolution PASSED         [ 45%]
tests/test_controllers.py::test_system_volume_clamping PASSED            [ 50%]
tests/test_controllers.py::test_action_executor_volume_execution PASSED  [ 55%]
tests/test_controllers.py::test_action_executor_unknown_command PASSED   [ 60%]
tests/test_dictation.py::test_spoken_punctuation_formatting PASSED       [ 65%]
tests/test_dictation.py::test_dictation_mode_transitions PASSED          [ 70%]
tests/test_dictation.py::test_editing_command_detection PASSED           [ 75%]
tests/test_safety.py::test_destructive_patterns_blocked PASSED           [ 80%]
tests/test_safety.py::test_sensitive_action_classification PASSED        [ 85%]
tests/test_safety.py::test_confirmation_lifecycle PASSED                 [ 90%]
tests/test_safety.py::test_confirmation_rejection PASSED                 [ 95%]
tests/test_safety.py::test_confirmation_timeout PASSED                   [100%]

======================== 20 passed in 1.33s =========================
```

---

## 8. Technical Limitations & Fallback Protections

1. **Accessibility Element Availability:**
   - Some legacy or non-standard Win32/DirectX interfaces do not expose full UI Automation trees. When accessible elements cannot be identified, VoxControl AI gracefully falls back to standard keyboard navigation (Tab, Enter, hotkeys) and informs the user rather than clicking random coordinates.
2. **Packaged UWP Store Apps:**
   - On Windows 11, certain packaged applications (such as Store-based Notepad or Settings) are hosted under `ApplicationFrameHost.exe`. VoxControl AI inspects both standard HWNDs and UIA hierarchies to interact with modern AppX windows.
3. **Browser Security Protections:**
   - VoxControl AI adheres to browser sandbox security: it does not bypass CAPTCHAs, two-factor authentication, or financial transaction screens. For sensitive web actions, user intervention is requested.
4. **Microphone Device Disconnection:**
   - If the microphone is disconnected or muted, the speech engine reports a clear status message on the dashboard, and users can continue operating via the manual text command bar.
