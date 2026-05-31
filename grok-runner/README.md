# Grok Runner

A persistent external runner for the **Grok CLI** (Grok Build TUI) on Windows.

This tool solves a common limitation: when Grok tries to run batch files or commands, the spawned CMD windows often get terminated when the agent's command finishes due to Windows Job Objects.

## How It Works

1. You start `grok_runner.py` once in its own window.
2. The runner stays alive and watches a **command queue folder**.
3. When you ask Grok to run a batch file (e.g. "run hello.bat"), Grok adds the command to the queue.
4. The runner processes commands **one by one in order** and launches each one in a **new, independent visible CMD window** that stays open until you close it.

This system now supports sending multiple commands safely — they will be executed sequentially.

## Setup

### 1. Start the Runner

Run this command once (keep the window open):

```cmd
python grok_runner.py
```

You should see a window titled **"Grok Persistent Runner"**.

### 2. Use It With Grok

Just tell Grok things like:

- `run hello.bat`
- `run W:\scripts\deploy.bat`
- `run C:\path\to\my-script.bat`

You can send multiple commands in a row. The runner will process them in the order they were received.

## How the Queue Works

- Commands are stored as individual files inside `W:\__grok_queue\`
- The runner processes them in **FIFO order** (first in, first out)
- Each command file is automatically deleted after it has been executed
- This makes it safe to send many commands quickly without losing any

## Files

| File                  | Description                                      |
|-----------------------|--------------------------------------------------|
| `grok_runner.py`      | The persistent runner (start this)               |
| `grok-runner.ico`     | Windows icon for runner shortcuts or packaging   |
| `.gitignore`          | Ignores runtime queue files and Python artifacts |

## Requirements

- Windows
- Python 3
- Grok CLI (xAI)

## Notes

- This tool is specifically designed for use with the Grok CLI agent.
- The runner must be running for "run *.bat" commands to work.
- Each run opens in its own new CMD window.
- You can safely send multiple run commands — they will queue up automatically.

## License

MIT (or as specified in original standalone repository)

---

> **Note:** This project has been moved into the [AI-TOOLS](..) collection repository for better organization.  
> The canonical location is now: https://github.com/Orffyrus-Qc/AI-TOOLS/tree/main/grok-runner  
> This standalone repository may be archived.


