# Auto-Loading Environment Variables in VS Code Terminal

This guide explains how to automatically load environment variables from a `.env` file when opening a terminal in VS Code.

## Overview

Instead of manually running `. .envrc` or `source .envrc` every time you open a terminal, VS Code can automatically load your environment variables using the `BASH_ENV` mechanism.

## Setup Instructions

### 1. Create the `.envrc` File

Create a `.envrc` file in your project root:

```bash
# filepath: /app/alternator/.envrc
#!/bin/bash
# Auto-load environment variables from .env file
if [ -f "${BASH_SOURCE%/*}/.env" ]; then
    set -a
    source "${BASH_SOURCE%/*}/.env"
    set +a
    echo "✅ Loaded credentials from .env"
fi
```

**What this script does:**
- Checks if `.env` file exists in the same directory
- `set -a` - Exports all variables automatically
- `source .env` - Loads the environment variables
- `set +a` - Stops auto-exporting
- Prints confirmation message

### 2. Create the `.env` File

Create a `.env` file with your credentials (same directory as `.envrc`):

```bash
# filepath: /app/alternator/.env
export ACCESS_KEY_ID='your_access_key'
export SECRET_ACCESS_KEY='your_secret_key'
export ALTERNATOR_ENDPOINT='http://localhost:8000'
```

**Important:** Add `.env` to `.gitignore` to prevent committing secrets!

```bash
echo ".env" >> .gitignore
```

### 3. Configure VS Code Settings

Add this configuration to your VS Code settings:

**For Linux:**

Open VS Code settings (`Cmd/Ctrl + ,`) → Search for "settings.json" → Click "Edit in settings.json"

Add:

```json
{
    "terminal.integrated.env.linux": {
        "BASH_ENV": "${workspaceFolder}/.envrc"
    }
}
```

**For macOS:**

```json
{
    "terminal.integrated.env.osx": {
        "BASH_ENV": "${workspaceFolder}/.envrc"
    }
}
```

**For Windows (Git Bash/WSL):**

```json
{
    "terminal.integrated.env.windows": {
        "BASH_ENV": "${workspaceFolder}/.envrc"
    }
}
```

**All platforms:**

```json
{
    "terminal.integrated.env.linux": {
        "BASH_ENV": "${workspaceFolder}/.envrc"
    },
    "terminal.integrated.env.osx": {
        "BASH_ENV": "${workspaceFolder}/.envrc"
    },
    "terminal.integrated.env.windows": {
        "BASH_ENV": "${workspaceFolder}/.envrc"
    }
}
```

### 4. Reload VS Code

After adding the configuration:

1. Close all terminal windows in VS Code
2. Open a new terminal (`Ctrl + `` ` `` or `Cmd + `` ` ``)
3. You should see: `✅ Loaded credentials from .env`

## How It Works

```
┌─────────────────────────────────────────────────────────┐
│ 1. You open a new terminal in VS Code                  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ 2. VS Code sets: BASH_ENV=/app/alternator/.envrc       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ 3. Bash automatically executes .envrc before prompt     │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ 4. .envrc sources .env file and exports all variables   │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ 5. Environment variables are available to all commands  │
└─────────────────────────────────────────────────────────┘
```

## Key Variables Explained

### `BASH_ENV`
- A special Bash variable that points to a script file
- Bash executes this script **before** running any command in non-interactive shells
- Perfect for auto-loading environment variables

### `${workspaceFolder}`
- VS Code variable that resolves to your workspace root directory
- Example: `/app/alternator`
- Ensures `.envrc` is always found regardless of subdirectory

### `set -a` and `set +a`
- `set -a` - Automatically export all variables that are created/modified
- `set +a` - Turn off automatic exporting
- Ensures all variables in `.env` become environment variables

## Verification

Test that variables are loaded:

```bash
# Open a new terminal in VS Code
echo $ACCESS_KEY_ID
echo $SECRET_ACCESS_KEY
echo $ALTERNATOR_ENDPOINT
```

You should see your values printed.

## Troubleshooting

### Variables not loading?

1. **Check `.envrc` is executable:**
   ```bash
   chmod +x .envrc
   ```

2. **Verify `.env` file exists:**
   ```bash
   ls -la .env
   ```

3. **Check VS Code settings:**
   - Open Command Palette (`Cmd/Ctrl + Shift + P`)
   - Search "Preferences: Open Settings (JSON)"
   - Verify `terminal.integrated.env.*` entries exist

4. **Restart VS Code completely:**
   - Close all terminals
   - Quit VS Code
   - Reopen VS Code and project

5. **Test `.envrc` manually:**
   ```bash
   bash .envrc
   echo $ACCESS_KEY_ID
   ```

### Still not working?

Check the terminal shell:
```bash
echo $SHELL
```

If not using Bash, `BASH_ENV` won't work. Consider:
- Using Bash as your default shell
- Or create similar mechanism for your shell (e.g., `.zshenv` for Zsh)

## Benefits

✅ **No manual sourcing** - Variables load automatically  
✅ **Consistent environment** - Same setup for all team members  
✅ **Secure** - `.env` stays in `.gitignore`  
✅ **Convenient** - Works across all terminals in VS Code  
✅ **Per-project** - Different variables for different projects  

## Security Best Practices

1. **Never commit `.env`:**
   ```bash
   echo ".env" >> .gitignore
   ```

2. **Provide `.env.example`:**
   ```bash
   # filepath: .env.example
   export ACCESS_KEY_ID='your_access_key_here'
   export SECRET_ACCESS_KEY='your_secret_key_here'
   export ALTERNATOR_ENDPOINT='http://localhost:8000'
   ```

3. **Document required variables** in your README

4. **Use strong credentials** in production

## Alternative: direnv

For more advanced environment management, consider using [`direnv`](https://direnv.net/):

```bash
# Install direnv
sudo apt install direnv  # Linux
brew install direnv      # macOS

# Add to ~/.bashrc
eval "$(direnv hook bash)"

# Allow .envrc
direnv allow .
```

This provides additional security and flexibility for environment variable management.

## References

- [VS Code Terminal Environment Variables](https://code.visualstudio.com/docs/terminal/profiles#_configuring-the-task-and-debug-terminals-environment)
- [Bash BASH_ENV Variable](https://www.gnu.org/software/bash/manual/html_node/Bash-Variables.html)
- [direnv - unclutter your .profile](https://direnv.net/)

---

**Last Updated:** January 10, 2026  
**Tested On:** Rocky Linux 8, VS Code 1.95+
