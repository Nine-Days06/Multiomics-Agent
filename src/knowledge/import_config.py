"""知识库导入配置"""
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ImportConfig:
    """导入配置"""
    import_dir: str = "data/import"
    supported_types: list[str] = None
    default_sql_query: str = """
        SELECT * FROM articles 
        WHERE human_review = 'Y' 
        OR (human_review IS NULL AND llm_verdict = 'relevant')
    """
    auto_import: bool = False
    cleanup_after_import: bool = False
    
    def __post_init__(self):
        if self.supported_types is None:
            self.supported_types = ['json', 'csv', 'sqlite']
        Path(self.import_dir).mkdir(parents=True, exist_ok=True)

# 全局配置实例
import_config = ImportConfig()
