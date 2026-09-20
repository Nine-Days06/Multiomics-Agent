import pytest
import pandas as pd
import tempfile
import os
from pathlib import Path

def test_load_csv_data():
    """Test loading CSV data files"""
    # 创建临时 CSV 文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("gene,sample1,sample2,condition\n")
        f.write("TP53,10.2,11.5,treatment\n")
        f.write("BRCA1,8.7,9.2,control\n")
        temp_path = f.name
    
    try:
        from src.data.data_loader import DataLoader
        loader = DataLoader()
        data = loader.load_csv(temp_path)
        
        assert isinstance(data, pd.DataFrame)
        assert data.shape == (2, 4)
        assert 'gene' in data.columns
    finally:
        os.unlink(temp_path)

def test_load_fastq_file():
    """Test loading FASTQ format files"""
    # 此测试验证 FASTQ 文件解析
    pass  # 将在后续实现

def test_auto_detect_format():
    """Test automatic format detection"""
    pass  # 将在后续实现