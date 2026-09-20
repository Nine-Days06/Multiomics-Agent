import subprocess
import tempfile
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class RExecutor:
    """R 脚本执行器"""
    
    def __init__(self, r_home: Optional[str] = None):
        self.r_home = r_home or os.getenv("R_HOME", "/usr/lib/R")
        self.rscript_path = self._find_rscript()
    
    def _find_rscript(self) -> str:
        """查找 Rscript 可执行文件"""
        # 简化实现，实际需要更复杂的路径查找
        return "Rscript"
    
    def execute_script(self, script_path: str, args: List[str] = None) -> subprocess.CompletedProcess:
        """执行 R 脚本"""
        cmd = [self.rscript_path, str(script_path)] + (args or [])
        logger.info(f"Executing R script: {cmd}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5分钟超时
        )
        
        if result.returncode != 0:
            logger.error(f"R script failed: {result.stderr}")
        
        return result
    
    def execute_code(self, code: str) -> subprocess.CompletedProcess:
        """执行 R 代码"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.R', delete=False) as f:
            f.write(code)
            temp_script = f.name
        
        try:
            return self.execute_script(temp_script)
        finally:
            os.unlink(temp_script)
    
    def install_package(self, package_name: str) -> subprocess.CompletedProcess:
        """安装 R 包"""
        code = f"if (!requireNamespace('{package_name}', quietly = TRUE)) {{ install.packages('{package_name}') }}"
        return self.execute_code(code)