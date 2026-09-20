import pickle
import hashlib
from pathlib import Path
from typing import Any, Optional, Union
import logging

logger = logging.getLogger(__name__)

class Cache:
    """简单的文件缓存机制"""
    
    def __init__(self, cache_dir: Union[str, Path] = None):
        self.cache_dir = Path(cache_dir) if cache_dir else Path("cache")
        self.cache_dir.mkdir(exist_ok=True)
    
    def _get_cache_key(self, key: str) -> Path:
        """生成缓存文件路径"""
        hash_key = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{hash_key}.pkl"
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存数据"""
        cache_path = self._get_cache_key(key)
        if cache_path.exists():
            try:
                with open(cache_path, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                logger.warning(f"Failed to load cache for key {key}: {e}")
        return None
    
    def set(self, key: str, value: Any):
        """设置缓存数据"""
        cache_path = self._get_cache_key(key)
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(value, f)
        except Exception as e:
            logger.warning(f"Failed to save cache for key {key}: {e}")
    
    def clear(self):
        """清空缓存"""
        for cache_file in self.cache_dir.glob("*.pkl"):
            cache_file.unlink()