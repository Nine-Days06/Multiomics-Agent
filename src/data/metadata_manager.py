import json
from pathlib import Path
from typing import Dict, Any, List, Union
import logging

logger = logging.getLogger(__name__)

class MetadataManager:
    """管理样本元数据和实验设计"""
    
    def __init__(self, metadata_dir: Union[str, Path] = None):
        self.metadata_dir = Path(metadata_dir) if metadata_dir else Path("metadata")
        self.metadata_dir.mkdir(exist_ok=True)
    
    def add_sample_metadata(self, sample_id: str, metadata: Dict[str, Any]):
        """添加样本元数据"""
        metadata_file = self.metadata_dir / f"{sample_id}.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        logger.info(f"Added metadata for sample: {sample_id}")
    
    def get_sample_metadata(self, sample_id: str) -> Dict[str, Any]:
        """获取样本元数据"""
        metadata_file = self.metadata_dir / f"{sample_id}.json"
        if metadata_file.exists():
            with open(metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def list_samples(self) -> List[str]:
        """列出所有样本"""
        return [f.stem for f in self.metadata_dir.glob("*.json")]