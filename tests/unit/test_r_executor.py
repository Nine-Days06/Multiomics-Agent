import pytest
import tempfile
import os
import subprocess

def is_r_available():
    """检查R是否可用"""
    try:
        result = subprocess.run(["Rscript", "--version"], capture_output=True, timeout=5)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False

@pytest.mark.skipif(not is_r_available(), reason="R not installed")
def test_execute_r_script():
    """Test executing R scripts"""
    # 创建临时 R 脚本
    with tempfile.NamedTemporaryFile(mode='w', suffix='.R', delete=False) as f:
        f.write("args <- commandArgs(trailingOnly=TRUE)\n")
        f.write("cat('Hello from R:', args[1], '\\n')\n")
        temp_script = f.name
    
    try:
        from src.analysis.r_executor import RExecutor
        executor = RExecutor()
        result = executor.execute_script(temp_script, ["world"])
        
        assert result.returncode == 0
        assert "Hello from R: world" in result.stdout
    finally:
        os.unlink(temp_script)

@pytest.mark.skipif(not is_r_available(), reason="R not installed")
def test_execute_r_code():
    """Test executing R code directly"""
    from src.analysis.r_executor import RExecutor
    executor = RExecutor()
    result = executor.execute_code("print(1 + 1)")
    
    assert result.returncode == 0
    assert "[1] 2" in result.stdout

def test_r_executor_initialization():
    """Test R executor initialization"""
    from src.analysis.r_executor import RExecutor
    executor = RExecutor()
    
    assert executor.rscript_path is not None
    assert executor.r_home is not None

def test_execute_script_file_not_found():
    """Test executing non-existent R script"""
    from src.analysis.r_executor import RExecutor
    executor = RExecutor()
    
    with pytest.raises(FileNotFoundError):
        executor.execute_script("nonexistent_script.R")