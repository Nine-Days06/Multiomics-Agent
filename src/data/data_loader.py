import pandas as pd
from pathlib import Path
from typing import Union, Dict, Any
import logging

logger = logging.getLogger(__name__)

class DataLoader:
    """统一的数据加载器，支持多组学数据格式"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.supported_formats = {
            'csv': self._load_csv,
            'tsv': self._load_tsv,
            'fastq': self._load_fastq,
            'vcf': self._load_vcf,
            'fasta': self._load_fasta,
        }
    
    def load_csv(self, file_path: Union[str, Path]) -> pd.DataFrame:
        """加载 CSV 文件"""
        return self._load_csv(file_path)
    
    def _load_csv(self, file_path: Union[str, Path]) -> pd.DataFrame:
        """内部 CSV 加载方法"""
        try:
            df = pd.read_csv(file_path)
            logger.info(f"Loaded CSV file: {file_path}, shape: {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Failed to load CSV file {file_path}: {e}")
            raise
    
    def _load_tsv(self, file_path: Union[str, Path]) -> pd.DataFrame:
        """加载 TSV 文件"""
        return pd.read_csv(file_path, sep='\t')
    
    def _load_fastq(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """加载 FASTQ 文件（简化版）"""
        # 实际实现需要解析 FASTQ 格式
        return {"format": "fastq", "file": str(file_path)}
    
    def _load_vcf(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """加载 VCF 文件（简化版）"""
        return {"format": "vcf", "file": str(file_path)}
    
    def _load_fasta(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """加载 FASTA 文件（简化版）"""
        return {"format": "fasta", "file": str(file_path)}
    
    def auto_detect_format(self, file_path: Union[str, Path]) -> str:
        """自动检测文件格式"""
        suffix = Path(file_path).suffix.lower()
        format_map = {
            '.csv': 'csv',
            '.tsv': 'tsv',
            '.fastq': 'fastq',
            '.fq': 'fastq',
            '.vcf': 'vcf',
            '.fasta': 'fasta',
            '.fa': 'fasta',
        }
        return format_map.get(suffix, 'unknown')