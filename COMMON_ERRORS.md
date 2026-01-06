# 🐛 Common Errors & Solutions

## Python Syntax Errors

### Error: `NameError: name 'MODE' is not defined`

**Problem:**
```python
# ❌ Wrong
python -c "import os; print(f'Mode: {os.environ.get(MODE)}')"
```

**Solution:**
```python
# ✅ Correct
python -c "import os; print(f'Mode: {os.environ.get(\"MODE\")}')"
```

**Explanation:** Environment variable names must be in quotes (strings) when using `os.environ.get()`.

---

### Error: `SyntaxError: unterminated string literal`

**Problem:**
Incorrect quote escaping in commands.

**Solution:**
Use proper quote escaping:
```python
# ✅ Correct
python -c "import os; print(f'Mode: {os.environ.get(\"MODE\")}')"
```

---

## Container Errors

### Error: "rootfs not found"

**Problem:** Container rootfs directory doesn't exist.

**Solution:**
- Rootfs is automatically created when you create a container
- If error persists, delete and recreate the container
- In Windows simulation mode, rootfs is created but not actively used

---

### Error: "Container failed to start"

**Possible Causes:**
1. **Command syntax error** - Check your command for typos
2. **Missing quotes** - Ensure environment variables are quoted
3. **Invalid command** - Verify the command works in terminal first

**Solution:**
- Test your command in terminal first
- Check logs for detailed error messages
- Verify environment variables are set correctly

---

## Environment Variable Errors

### Variables Not Working

**Problem:** Environment variables not accessible in container.

**Solution:**
1. **Check format:** Must be `KEY=VALUE` (no spaces around `=`)
2. **Access correctly:** Use `os.environ.get('KEY')` with quotes
3. **Verify in logs:** Check container logs to see if variables are set

**Example:**
```
Env Var: MODE=production
Command: python -c "import os; print(os.environ.get('MODE'))"
```

---

## Quick Fixes

### Fix Command Syntax
```python
# ❌ Wrong
python -c "print(os.environ.get(MODE))"

# ✅ Correct  
python -c "print(os.environ.get('MODE'))"
```

### Fix Quote Escaping
```python
# ❌ Wrong
python -c "print('Hello')"

# ✅ Correct (for web UI)
python -c "print('Hello')"  # Single quotes inside double quotes
```

---

*For more examples, see [USAGE_GUIDE.md](USAGE_GUIDE.md)*

