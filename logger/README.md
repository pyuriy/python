# Python Logging Configuration Guide
## ScyllaDB Alternator Backup Tool

## Overview

This document explains the logging configuration used in the ScyllaDB Alternator Backup Tool. The logging system provides comprehensive tracking of all backup operations, errors, and events for debugging, auditing, and monitoring purposes.

---

## Table of Contents

- [Introduction](#introduction)
- [Logging Configuration Breakdown](#logging-configuration-breakdown)
- [Log Levels Explained](#log-levels-explained)
- [Log Format](#log-format)
- [Handlers: Dual Logging System](#handlers-dual-logging-system)
- [Logger Instance Creation](#logger-instance-creation)
- [Usage Examples](#usage-examples)
- [Alternative Configurations](#alternative-configurations)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

---

## Introduction

The logging configuration is a critical component that enables:

✅ **Real-time monitoring** - See what's happening during backup operations  
✅ **Permanent audit trail** - Keep records for compliance and debugging  
✅ **Error tracking** - Identify and diagnose issues quickly  
✅ **Performance analysis** - Track backup duration and success rates  
✅ **User feedback** - Provide clear status updates during operations  

---

## Logging Configuration Breakdown

### Complete Code Block

```python
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('alternator_backup.log'),
        logging.StreamHandler()  # Also print to console
    ]
)
logger = logging.getLogger(__name__)
```

### Line-by-Line Analysis

#### Line 25: `logging.basicConfig(`

**Purpose:** Initializes Python's built-in logging framework with custom settings.

**What it does:**
- Configures the **root logger** (top-level logger for the entire application)
- Must be called before any logging operations
- Can only be effectively called once per program execution

**Technical Details:**
```python
logging.basicConfig(
    # Accepts multiple keyword arguments for configuration
)
```

---

#### Line 26: `level=logging.INFO,`

**Purpose:** Sets the minimum severity threshold for log messages.

**Value:** `logging.INFO` (severity level 20)

### Log Levels Reference Table

| Level | Numeric Value | When to Use | Visibility |
|-------|---------------|-------------|------------|
| **DEBUG** | 10 | Detailed diagnostic information | ❌ Hidden with INFO level |
| **INFO** | 20 | General informational messages | ✅ Shown |
| **WARNING** | 30 | Warning messages (non-critical issues) | ✅ Shown |
| **ERROR** | 40 | Error messages (operation failed) | ✅ Shown |
| **CRITICAL** | 50 | Critical errors (system failure) | ✅ Shown |

**Configuration Impact:**

```python
level=logging.INFO  # Shows: INFO, WARNING, ERROR, CRITICAL
                    # Hides: DEBUG
```

**Example Messages by Level:**

```python
logger.debug("Detailed table metadata: {...}")        # ❌ Not shown
logger.info("Backup started for users")               # ✅ Shown
logger.warning("No tables found in database")         # ✅ Shown
logger.error("Failed to create schema file")          # ✅ Shown
logger.critical("Database connection lost")           # ✅ Shown
```

**Why INFO Level?**

- ✅ **Balanced:** Not too verbose (like DEBUG), not too sparse (like WARNING)
- ✅ **Production-friendly:** Captures important events without overwhelming logs
- ✅ **Debugging-capable:** Provides enough information for troubleshooting
- ✅ **Performance:** Minimal overhead compared to DEBUG level

---

#### Line 27: `format='%(asctime)s - %(levelname)s - %(message)s',`

**Purpose:** Defines the structure and appearance of each log message.

**Format String Breakdown:**

```python
format='%(asctime)s - %(levelname)s - %(message)s'
```

### Format Placeholders

| Placeholder | Description | Example Output |
|-------------|-------------|----------------|
| `%(asctime)s` | Timestamp when log was created | `2024-12-06 14:30:15,123` |
| `%(levelname)s` | Severity level name | `INFO`, `ERROR`, `WARNING` |
| `%(message)s` | The actual log message content | `Backup started for users` |
| `-` | Separator character | `-` |

**Complete Example:**

```
Input:  logger.info("Backup started for users")
Output: 2024-12-06 14:30:15,123 - INFO - Backup started for users
        └─────────────────────┘   └──┘   └──────────────────────┘
              asctime          levelname        message
```

### Available Format Attributes (Extended)

Beyond the basic three, Python logging supports many other placeholders:

| Attribute | Description | Example |
|-----------|-------------|---------|
| `%(name)s` | Logger name | `__main__` or `backup` |
| `%(filename)s` | Source file name | `backup.py` |
| `%(lineno)d` | Line number where logged | `123` |
| `%(funcName)s` | Function name | `backup_table` |
| `%(pathname)s` | Full file path | `/app/alternator/backup.py` |
| `%(process)d` | Process ID | `12345` |
| `%(thread)d` | Thread ID | `67890` |
| `%(levelno)d` | Numeric log level | `20` (for INFO) |

**Example with Extended Format:**

```python
format='%(asctime)s - [%(filename)s:%(lineno)d] - %(levelname)s - %(message)s'

# Output:
# 2024-12-06 14:30:15,123 - [backup.py:182] - INFO - Backup started for users
```

---

#### Lines 28-31: `handlers=[...]`

**Purpose:** Specifies where log messages should be sent (output destinations).

```python
handlers=[
    logging.FileHandler('alternator_backup.log'),
    logging.StreamHandler()  # Also print to console
]
```

**Why Multiple Handlers?**

This configuration implements **dual logging** - sending messages to two destinations simultaneously:

1. **File** - Persistent storage for audit trail
2. **Console** - Real-time user feedback

### Handler 1: FileHandler

```python
logging.FileHandler('alternator_backup.log')
```

**Configuration Details:**

| Property | Value | Description |
|----------|-------|-------------|
| **Filename** | `alternator_backup.log` | Stored in current working directory |
| **Mode** | `'a'` (append) | Adds to existing file, doesn't overwrite |
| **Encoding** | Default (UTF-8) | Supports international characters |
| **Delay** | `False` | File opened immediately |

**File Contents Example:**

```
2024-12-06 14:30:15,123 - INFO - ===== Backup process started =====
2024-12-06 14:30:15,456 - INFO - Found 3 tables
2024-12-06 14:30:15,789 - INFO - Available tables (3 total):
2024-12-06 14:30:16,012 - INFO -   1. users
2024-12-06 14:30:16,234 - INFO -   2. orders
2024-12-06 14:30:16,567 - INFO -   3. products
2024-12-06 14:30:17,890 - INFO - ===== Start backup process for users =====
2024-12-06 14:30:18,123 - INFO - Table ID for users: 220f8fd0aca211f0af61efb5703633f5
2024-12-06 14:30:18,456 - INFO - Creating schema file for users at ./backups/users/schema.cql
2024-12-06 14:30:18,789 - INFO - Created backup folder: ./backups/users
2024-12-06 14:30:19,012 - INFO - Schema file created at ./backups/users/schema.cql
2024-12-06 14:30:19,345 - INFO - Taking snapshot for alternator_users
2024-12-06 14:30:20,678 - INFO - Snapshot created for users with ID: 1733493020
2024-12-06 14:30:20,901 - INFO - Snapshot directory verified: /var/lib/scylla/data/alternator_users/users-220f8fd0aca211f0af61efb5703633f5/snapshots/1733493020/
2024-12-06 14:30:21,234 - INFO - Creating backup archive: ./backups/users/users_backup.tar.gz
2024-12-06 14:30:22,567 - INFO - Backup created at ./backups/users/users_backup.tar.gz
2024-12-06 14:30:22,890 - INFO - ===== Backup completed for users =====
```

**Benefits of File Logging:**

✅ **Persistence** - Logs survive terminal closure and system reboots  
✅ **Audit Trail** - Complete history of all operations  
✅ **Debugging** - Review logs long after operations complete  
✅ **Monitoring** - Automated tools can parse log files  
✅ **Compliance** - Meet regulatory requirements for record-keeping  
✅ **Analysis** - Identify patterns and trends over time  

**File Location:**

```bash
# In the same directory as the script
/app/alternator/alternator_backup.log

# Check file size
ls -lh alternator_backup.log

# View last 50 lines
tail -n 50 alternator_backup.log

# Search for errors
grep "ERROR" alternator_backup.log

# Follow logs in real-time
tail -f alternator_backup.log
```

### Handler 2: StreamHandler

```python
logging.StreamHandler()  # Also print to console
```

**Configuration Details:**

| Property | Value | Description |
|----------|-------|-------------|
| **Stream** | `sys.stderr` (default) | Outputs to standard error |
| **Purpose** | User feedback | Real-time progress updates |
| **Format** | Same as FileHandler | Consistent formatting |

**Console Output Example:**

```bash
$ python3 backup.py

============================================================
ScyllaDB Alternator Table Backup Tool
============================================================

Fetching list of all available tables...
2024-12-06 14:30:15,123 - INFO - Found 3 tables

Available tables (3 total):
  1. users
  2. orders
  3. products

Options:
1. Backup a specific table
2. Backup all tables
3. Exit

Enter your choice (1, 2, or 3): 1
Enter table name: users

2024-12-06 14:30:17,890 - INFO - ===== Start backup process for users =====
2024-12-06 14:30:18,123 - INFO - Table ID for users: 220f8fd0aca211f0af61efb5703633f5
2024-12-06 14:30:18,456 - INFO - Creating schema file for users at ./backups/users/schema.cql
2024-12-06 14:30:19,012 - INFO - Schema file created at ./backups/users/schema.cql
2024-12-06 14:30:19,345 - INFO - Taking snapshot for alternator_users
2024-12-06 14:30:20,678 - INFO - Snapshot created for users with ID: 1733493020
2024-12-06 14:30:22,890 - INFO - ===== Backup completed for users =====

✅ Backup completed successfully for users
```

**Benefits of Console Logging:**

✅ **Immediate Feedback** - See progress in real-time  
✅ **User Experience** - Know the script is working  
✅ **Quick Debugging** - Spot issues immediately  
✅ **Interactive** - Combined with user input prompts  
✅ **Development** - Essential during script development  

---

## Logger Instance Creation

#### Line 32: `logger = logging.getLogger(__name__)`

**Purpose:** Creates a logger instance specific to this module.

```python
logger = logging.getLogger(__name__)
```

### Component Breakdown

#### `__name__` Variable

**What is `__name__`?**

- Special Python built-in variable
- Contains the name of the current module
- Value depends on how the script is executed

**Value Examples:**

| Execution Method | `__name__` Value | Description |
|------------------|------------------|-------------|
| `python3 backup.py` | `'__main__'` | Script run directly |
| `import backup` | `'backup'` | Imported as module |
| `from backup import ...` | `'backup'` | Imported from module |

**Code Example:**

```python
# In backup.py
print(f"__name__ = {__name__}")

# When run directly:
$ python3 backup.py
__name__ = __main__

# When imported:
$ python3
>>> import backup
__name__ = backup
```

#### `logging.getLogger(__name__)`

**What it does:**

1. **Creates logger** - If it doesn't exist
2. **Retrieves logger** - If it already exists
3. **Inherits config** - Uses settings from `basicConfig()`
4. **Names logger** - Uses module name for identification

**Technical Details:**

```python
logger = logging.getLogger(__name__)
# Returns: <Logger __main__ (INFO)>
#          └────┘  └──────┘ └──┘
#          Type    Name     Level
```

**Why Use `__name__`?**

✅ **Traceability** - Know which module generated each log  
✅ **Modularity** - Different log levels per module  
✅ **Best Practice** - Standard Python convention  
✅ **Flexibility** - Easy to filter logs by module  

**Example with Module Names:**

```python
# backup.py
logger = logging.getLogger(__name__)
logger.info("Backup started")
# Output: 2024-12-06 14:30:15,123 - INFO - Backup started

# If we used a literal string:
logger = logging.getLogger('backup_module')
logger.info("Backup started")
# Output: 2024-12-06 14:30:15,123 - INFO - Backup started

# But __name__ is better because it's automatic and consistent
```

---

## Usage Examples

### Throughout the Backup Script

#### Example 1: Process Start/End

```python
logger.info('===== Backup process started =====')
# ... operations ...
logger.info('===== Backup process completed =====')
```

**Output:**
```
2024-12-06 14:30:15,123 - INFO - ===== Backup process started =====
2024-12-06 14:35:42,789 - INFO - ===== Backup process completed =====
```

#### Example 2: Informational Messages

```python
logger.info(f"Found {len(tables)} tables")
logger.info(f"Table ID for {table_name}: {table_id}")
logger.info(f"Schema file created at {SCHEMA_FILE}")
```

**Output:**
```
2024-12-06 14:30:15,456 - INFO - Found 3 tables
2024-12-06 14:30:18,123 - INFO - Table ID for users: 220f8fd0aca211f0af61efb5703633f5
2024-12-06 14:30:19,012 - INFO - Schema file created at ./backups/users/schema.cql
```

#### Example 3: Error Messages

```python
logger.error(f"Backup failed for {table_name}: Could not retrieve table ID")
logger.error(f"Failed to create backup folder {BACKUP_FOLDER}: {e}")
logger.error(f"Snapshot directory {snapshot_dir} does not exist")
```

**Output:**
```
2024-12-06 14:30:18,123 - ERROR - Backup failed for users: Could not retrieve table ID
2024-12-06 14:30:19,456 - ERROR - Failed to create backup folder ./backups/users: Permission denied
2024-12-06 14:30:20,789 - ERROR - Snapshot directory /var/lib/scylla/data/.../snapshots/1234/ does not exist
```

#### Example 4: Warning Messages

```python
logger.warning("No tables found in database")
logger.warning(f"User entered non-existent table: {table_name}")
logger.warning(f"Invalid menu choice: {choice}")
```

**Output:**
```
2024-12-06 14:30:15,123 - WARNING - No tables found in database
2024-12-06 14:30:16,456 - WARNING - User entered non-existent table: invalid_table
2024-12-06 14:30:17,789 - WARNING - Invalid menu choice: 5
```

#### Example 5: Exception Logging with Traceback

```python
try:
    subprocess.check_call(tar_cmd)
except subprocess.CalledProcessError as e:
    logger.error(f"Failed to create backup archive for {table_name}: {e}")
except Exception as e:
    logger.exception(f"Unexpected error during backup: {e}")
```

**Output (using `.exception()`):**
```
2024-12-06 14:30:22,123 - ERROR - Unexpected error during backup: division by zero
Traceback (most recent call last):
  File "/app/alternator/backup.py", line 234, in backup_table
    result = 10 / 0
ZeroDivisionError: division by zero
```

**Note:** `logger.exception()` automatically includes the full traceback.

---

## Alternative Configurations

### Configuration 1: File Only (No Console)

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='alternator_backup.log'  # Simplified - no handlers list
)
```

**Use Case:** Automated scripts running via cron where console output isn't needed.

### Configuration 2: Console Only (No File)

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
    # No filename, no handlers - defaults to console
)
```

**Use Case:** Interactive development where you don't need persistent logs.

### Configuration 3: More Detailed Format

```python
logging.basicConfig(
    level=logging.DEBUG,  # More verbose
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.FileHandler('alternator_backup.log'),
        logging.StreamHandler()
    ]
)
```

**Example Output:**
```
2024-12-06 14:30:15,123 - __main__ - INFO - [backup.py:182] - Backup started for users
```

**Use Case:** Debugging complex issues where you need to know exact file and line numbers.

### Configuration 4: Different Formats for Different Handlers

```python
# Create handlers with different formats
file_handler = logging.FileHandler('alternator_backup.log')
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
))

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(
    '%(levelname)s - %(message)s'  # Simpler for console
))

# Configure logging with both handlers
logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler, console_handler]
)
```

**Result:**
- **File:** `2024-12-06 14:30:15,123 - INFO - [backup.py:182] - Backup started`
- **Console:** `INFO - Backup started` (cleaner, less clutter)

**Use Case:** Detailed logs in file, clean output on console for better UX.

### Configuration 5: Rotating File Handler (For Production)

```python
from logging.handlers import RotatingFileHandler

file_handler = RotatingFileHandler(
    'alternator_backup.log',
    maxBytes=10*1024*1024,  # 10 MB
    backupCount=5            # Keep 5 backup files
)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'
))

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        file_handler,
        logging.StreamHandler()
    ]
)
```

**How it works:**
- When `alternator_backup.log` reaches 10 MB, it's renamed to `alternator_backup.log.1`
- New logs start in a fresh `alternator_backup.log`
- Keeps up to 5 old files: `.log.1`, `.log.2`, `.log.3`, `.log.4`, `.log.5`
- Oldest file is deleted when limit is reached

**Use Case:** Production environments where log files grow large over time.

### Configuration 6: Time-Based Rotation

```python
from logging.handlers import TimedRotatingFileHandler

file_handler = TimedRotatingFileHandler(
    'alternator_backup.log',
    when='midnight',  # Rotate daily at midnight
    interval=1,
    backupCount=30    # Keep 30 days of logs
)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'
))

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        file_handler,
        logging.StreamHandler()
    ]
)
```

**How it works:**
- Creates new log file at midnight
- Old file renamed with date: `alternator_backup.log.2024-12-06`
- Keeps 30 days of history

**Use Case:** Daily backup operations where you want one log file per day.

---

## Best Practices

### 1. Always Use Named Loggers

```python
# ✅ Good
logger = logging.getLogger(__name__)

# ❌ Bad
logger = logging.getLogger()  # Uses root logger
```

### 2. Use Appropriate Log Levels

```python
# ✅ Good - Appropriate levels
logger.debug("Detailed variable values: {data}")     # Development only
logger.info("Backup completed successfully")         # Normal operations
logger.warning("Table not found, skipping")          # Non-critical issues
logger.error("Failed to create backup")              # Operation failures
logger.critical("Database connection lost")          # System failures

# ❌ Bad - Wrong levels
logger.error("Backup started")                       # Too severe
logger.info("Critical database failure")             # Not severe enough
```

### 3. Include Context in Messages

```python
# ✅ Good - Includes context
logger.error(f"Failed to backup table '{table_name}': {e}")
logger.info(f"Snapshot created for {table_name} with ID: {snapshot_id}")

# ❌ Bad - Vague
logger.error("Backup failed")
logger.info("Snapshot created")
```

### 4. Use f-strings for Formatting

```python
# ✅ Good - Modern f-strings (Python 3.6+)
logger.info(f"Processing {count} tables")

# ❌ Outdated - Old string formatting
logger.info("Processing %d tables" % count)
logger.info("Processing {} tables".format(count))
```

### 5. Log Before and After Important Operations

```python
# ✅ Good
logger.info(f"Starting backup for {table_name}")
success = backup_table(table_name)
if success:
    logger.info(f"Backup completed for {table_name}")
else:
    logger.error(f"Backup failed for {table_name}")
```

### 6. Use `.exception()` for Exception Handling

```python
# ✅ Good - Includes traceback
try:
    operation()
except Exception as e:
    logger.exception(f"Unexpected error: {e}")

# ❌ Bad - No traceback
try:
    operation()
except Exception as e:
    logger.error(f"Unexpected error: {e}")
```

### 7. Configure Logging Early

```python
# ✅ Good - Configure before any operations
logging.basicConfig(...)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting...")

# ❌ Bad - Configure inside functions
def main():
    logging.basicConfig(...)  # Too late if already used elsewhere
```

### 8. Don't Log Sensitive Data

```python
# ✅ Good - No sensitive data
logger.info(f"User authenticated: {username}")

# ❌ Bad - Logs password
logger.info(f"Login attempt: {username}:{password}")
```

---

## Troubleshooting

### Issue 1: Logs Not Appearing

**Symptoms:**
```python
logger.info("This doesn't appear")
```

**Diagnosis:**

```python
# Check if logging is configured
print(logging.getLogger().handlers)  # Should show handlers

# Check log level
print(logging.getLogger().level)  # Should be 20 (INFO) or lower
```

**Solutions:**

1. **Ensure `basicConfig()` is called:**
```python
logging.basicConfig(level=logging.INFO, ...)
```

2. **Check log level:**
```python
# If set to WARNING, INFO messages won't show
logging.basicConfig(level=logging.INFO)  # ✅ Shows INFO
logging.basicConfig(level=logging.WARNING)  # ❌ Hides INFO
```

3. **Verify logger name:**
```python
# Use __name__ for module-specific loggers
logger = logging.getLogger(__name__)
```

### Issue 2: Duplicate Log Messages

**Symptoms:**
```
2024-12-06 14:30:15,123 - INFO - Backup started
2024-12-06 14:30:15,123 - INFO - Backup started
```

**Causes:**

1. **Multiple calls to `basicConfig()`**
2. **Adding handlers multiple times**

**Solution:**

```python
# ✅ Good - Configure once at module level
logging.basicConfig(...)
logger = logging.getLogger(__name__)

# ❌ Bad - Configuring in functions
def backup():
    logging.basicConfig(...)  # Called every time function runs
```

### Issue 3: Logs Not Writing to File

**Symptoms:**
- Console output works
- File is empty or doesn't exist

**Diagnosis:**

```bash
# Check if file exists
ls -la alternator_backup.log

# Check permissions
ls -l alternator_backup.log

# Check if process has write access
touch alternator_backup.log
```

**Solutions:**

1. **Check file path:**
```python
# Use absolute path
logging.FileHandler('/var/log/alternator_backup.log')

# Or check current directory
import os
print(f"Current directory: {os.getcwd()}")
```

2. **Verify permissions:**
```bash
# Make directory writable
chmod 755 ./
chmod 644 alternator_backup.log
```

3. **Check disk space:**
```bash
df -h
```

### Issue 4: Log File Growing Too Large

**Symptoms:**
- `alternator_backup.log` is hundreds of MB
- Disk space running out

**Solution: Use Rotating File Handler**

```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    'alternator_backup.log',
    maxBytes=10*1024*1024,  # 10 MB
    backupCount=5
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[handler, logging.StreamHandler()]
)
```

### Issue 5: Timestamps Not Showing

**Symptoms:**
```
INFO - Backup started  # Missing timestamp
```

**Cause:** Format string doesn't include `%(asctime)s`

**Solution:**

```python
# ✅ Include asctime
format='%(asctime)s - %(levelname)s - %(message)s'

# ❌ Missing asctime
format='%(levelname)s - %(message)s'
```

### Issue 6: Logger Not Using Configuration

**Symptoms:**
```python
logger.debug("This doesn't show even with DEBUG level")
```

**Cause:** Logger created before `basicConfig()` was called

**Solution:**

```python
# ✅ Good order
logging.basicConfig(level=logging.DEBUG, ...)  # Configure first
logger = logging.getLogger(__name__)           # Then create logger

# ❌ Bad order
logger = logging.getLogger(__name__)           # Created first
logging.basicConfig(level=logging.DEBUG, ...)  # Configuration ignored
```

---

## Summary

The logging configuration in the ScyllaDB Alternator Backup Tool provides:

✅ **Dual Output** - File for persistence, console for real-time feedback  
✅ **Appropriate Level** - INFO level balances detail and clarity  
✅ **Consistent Format** - Timestamp, level, and message in every log  
✅ **Production-Ready** - Handles errors, provides audit trail  
✅ **Easy Debugging** - Clear messages with context  
✅ **Modular Design** - Uses `__name__` for module-specific loggers  
✅ **Comprehensive Coverage** - Logs all important operations and errors  

### Key Takeaways

1. **`logging.basicConfig()`** - Configures the logging system
2. **`level=logging.INFO`** - Sets minimum severity to INFO
3. **`format='...'`** - Defines log message structure
4. **`handlers=[...]`** - Specifies output destinations (file + console)
5. **`logging.getLogger(__name__)`** - Creates module-specific logger
6. **Best Practice** - Configure once, log everywhere

### Recommended Reading

- [Python Logging Documentation](https://docs.python.org/3/library/logging.html)
- [Logging HOWTO](https://docs.python.org/3/howto/logging.html)
- [Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html)

---

**Note:** This logging configuration is suitable for production use and provides comprehensive tracking of all backup operations. Always test logging in your specific environment to ensure it meets your requirements.
