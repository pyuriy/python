# Subprocess Module Explanation

## Overview
This document explains the usage of Python's `subprocess` module in the `get_table_id()` function from `backup.py`. The subprocess module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes.

## Code Context

The code executes a CQL (Cassandra Query Language) command to retrieve table metadata from ScyllaDB's system schema:

```python
cmd = [
    'cqlsh',
    '-u', USER,
    '-p', PASSWORD,
    '-e', cql_query
]

try:
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        check=True
    )
    output = result.stdout

    match = re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', output)
    if match:
        table_id = match.group(1).replace("-", "")
        logger.info(f"Table ID for {table_name}: {table_id}")
        return table_id
    else:
        logger.error(f"Table ID not found for {table_name}")
        return None

except subprocess.CalledProcessError as e:
    logger.error(f"Error getting table ID for {table_name}: {e.stderr}")
    return None
```

## Detailed Breakdown

### 1. Command Construction

```python
cmd = [
    'cqlsh',           # The CQL shell executable
    '-u', USER,        # Username flag and value
    '-p', PASSWORD,    # Password flag and value
    '-e', cql_query    # Execute flag with the query to run
]
```

**Purpose**: Creates a list representing the command and its arguments. Using a list (instead of a single string) is the **recommended approach** because:
- It's safer - no shell injection vulnerabilities
- Arguments are automatically escaped
- More portable across platforms

### 2. subprocess.run() Method

```python
result = subprocess.run(
    cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    universal_newlines=True,
    check=True
)
```

#### Parameters Explained:

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `cmd` | Command list | The command to execute |
| `stdout=subprocess.PIPE` | Capture standard output | Redirects the command's output so it can be read in Python |
| `stderr=subprocess.PIPE` | Capture standard error | Redirects error messages so they can be read in Python |
| `universal_newlines=True` | Text mode | Returns output as strings (not bytes), handles line endings automatically |
| `check=True` | Exception on failure | Raises `CalledProcessError` if the command returns non-zero exit code |

#### Alternative Naming:
In Python 3.7+, `universal_newlines=True` can also be written as `text=True` (more intuitive).

### 3. Return Value

```python
result = subprocess.run(...)
```

Returns a `CompletedProcess` object with these attributes:

- **`result.stdout`** - The captured standard output (string)
- **`result.stderr`** - The captured standard error (string)
- **`result.returncode`** - The exit code (0 for success)
- **`result.args`** - The command that was run

### 4. Output Processing

```python
output = result.stdout

match = re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', output)
if match:
    table_id = match.group(1).replace("-", "")
```

**Steps**:
1. Store the captured stdout in `output` variable
2. Use regex to find a UUID pattern (e.g., `550e8400-e29b-41d4-a716-446655440000`)
3. Extract the UUID and remove dashes to get the table ID

**Regex Pattern Breakdown**:
- `[0-9a-f]{8}` - 8 hexadecimal characters
- `-` - Literal dash
- `[0-9a-f]{4}` - 4 hexadecimal characters (repeated 3 times)
- `[0-9a-f]{12}` - 12 hexadecimal characters

### 5. Error Handling

```python
except subprocess.CalledProcessError as e:
    logger.error(f"Error getting table ID for {table_name}: {e.stderr}")
    return None
```

**CalledProcessError** is raised when:
- The command exits with a non-zero return code
- Only happens because we set `check=True`

**Benefits of this approach**:
- Automatic error detection
- Access to error output via `e.stderr`
- Clean separation of success and failure paths

## Why Use subprocess.run()?

### Advantages:

1. **Recommended Modern API** (Python 3.5+)
   - Replaces older `subprocess.call()`, `subprocess.check_output()`
   - Single function for most use cases

2. **Secure by Default**
   - No shell parsing (when passing list)
   - No command injection vulnerabilities

3. **Easy Output Capture**
   - Both stdout and stderr
   - Can be processed as text or bytes

4. **Built-in Error Handling**
   - `check=True` provides automatic exception on failure
   - Access to error messages via exception

### Alternative: subprocess.Popen()

For more complex scenarios (used elsewhere in `backup.py`):

```python
proc = subprocess.Popen(
    ['nodetool', 'snapshot', f'alternator_{table_name}'],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
stdout, stderr = proc.communicate()
```

**Use Popen when**:
- You need more control over process execution
- Want to interact with process while it's running
- Need to handle long-running processes

## Real-World Example

Given this CQL query:
```sql
SELECT id, keyspace_name, table_name 
FROM system_schema.tables 
WHERE keyspace_name = 'alternator_my_test_table' 
AND table_name = 'my_test_table';
```

**Expected Output**:
```
 id                                   | keyspace_name              | table_name
--------------------------------------+----------------------------+------------------
 550e8400-e29b-41d4-a716-446655440000 | alternator_my_test_table   | my_test_table
```

**Processing**:
1. Regex finds: `550e8400-e29b-41d4-a716-446655440000`
2. Dashes removed: `550e8400e29b41d4a716446655440000`
3. Returns: `550e8400e29b41d4a716446655440000` as the table ID

## Security Considerations

### ✅ Good Practices (used in this code):

1. **Command as List** - Prevents shell injection
2. **No shell=True** - Doesn't invoke shell interpreter
3. **Credentials from Variables** - Not hardcoded in command string
4. **Error Logging** - Captures and logs errors for debugging

### ⚠️ Potential Improvements:

1. **Credential Management** - Consider using environment variables or secure vaults instead of module-level constants
2. **Input Validation** - Validate `table_name` before constructing query to prevent CQL injection
3. **Timeout** - Add `timeout=30` parameter to prevent hanging on network issues

Example with timeout:
```python
result = subprocess.run(
    cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    universal_newlines=True,
    check=True,
    timeout=30  # Raise TimeoutExpired after 30 seconds
)
```

## Common Issues and Solutions

### Issue 1: Command Not Found
```python
FileNotFoundError: [Errno 2] No such file or directory: 'cqlsh'
```
**Solution**: Ensure `cqlsh` is in system PATH or use full path:
```python
cmd = ['/usr/local/bin/cqlsh', '-u', USER, ...]
```

### Issue 2: Authentication Failure
```python
CalledProcessError: Command returned non-zero exit status 1
stderr: "Authentication failed"
```
**Solution**: Verify credentials are correct and user has permissions

### Issue 3: Regex Doesn't Match
```python
Table ID not found for my_test_table
```
**Solution**: 
- Check if table exists in keyspace
- Verify CQL query returns expected format
- Print raw output for debugging:
  ```python
  logger.debug(f"CQL output: {output}")
  ```

## Summary

The subprocess module provides a powerful and secure way to execute external commands in Python. This code demonstrates best practices:

- ✅ Using `subprocess.run()` for simple command execution
- ✅ Capturing both stdout and stderr
- ✅ Automatic error handling with `check=True`
- ✅ Text mode for easier string processing
- ✅ Proper exception handling
- ✅ Command as list (not string) for security

This pattern is ideal for integrating Python scripts with command-line tools like `cqlsh`, `nodetool`, and other database utilities.
