import logging

logger = logging.getLogger(__name__)

async def run(code: str) -> str:
    """Execute a Python code snippet and return the output."""
    try:
        allowed_builtins = {'abs', 'min', 'max', 'sum', 'len', 'range'}
        safe_globals = {"__builtins__": {k: __builtins__[k] for k in allowed_builtins}}
        logger.info(f"Executing code: {code}")
        result = eval(code, safe_globals)
        logger.info(f"Execution result: {result}")
        return str(result)
    except Exception as e:
        logger.error(f"Error executing code '{code}': {e}")
        return f"Error: {e}" 