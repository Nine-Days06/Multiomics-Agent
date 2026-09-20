import logging
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

logger = logging.getLogger(__name__)

class Visualizer:
    """可视化模块，生成图表"""
    
    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}
        self._set_matplotlib_style()
    
    def _set_matplotlib_style(self):
        """设置 matplotlib 样式，兼容不同版本"""
        try:
            # 尝试使用新版样式
            plt.style.use('seaborn-v0_8')
        except OSError:
            try:
                # 尝试使用旧版样式
                plt.style.use('seaborn')
            except OSError:
                # 如果都找不到，使用默认样式
                logger.warning("Could not find seaborn styles, using default matplotlib style")
    
    def plot_volcano(self, data: pd.DataFrame, 
                    log2fc_col: str = 'log2FC', 
                    pval_col: str = 'padj',
                    title: str = 'Volcano Plot') -> plt.Figure:
        """绘制火山图"""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # 简化实现
        significant = data[data[pval_col] < 0.05]
        non_significant = data[data[pval_col] >= 0.05]
        
        ax.scatter(non_significant[log2fc_col], -np.log10(non_significant[pval_col]), 
                  alpha=0.5, color='gray', label='Non-significant')
        ax.scatter(significant[log2fc_col], -np.log10(significant[pval_col]), 
                  alpha=0.7, color='red', label='Significant')
        
        ax.set_xlabel('Log2 Fold Change')
        ax.set_ylabel('-Log10 Adjusted P-value')
        ax.set_title(title)
        ax.legend()
        
        return fig
    
    def plot_heatmap(self, data: pd.DataFrame, 
                    title: str = 'Heatmap') -> plt.Figure:
        """绘制热图"""
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(data, ax=ax, cmap='viridis')
        ax.set_title(title)
        return fig
    
    def plot_pathway(self, pathway_data: dict[str, Any]) -> plt.Figure:
        """绘制通路图（简化版）"""
        # 实际需要更复杂的通路可视化
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, 'Pathway Visualization\n(Placeholder)', 
                ha='center', va='center', fontsize=14)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        return fig