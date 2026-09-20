import logging
from typing import Any

logger = logging.getLogger(__name__)

class ResultExplainer:
    """将统计结果转化为自然语言解释"""
    
    def __init__(self, llm_client=None):
        self.llm_client = llm_client
    
    def explain_differential_expression(self, results: dict[str, Any]) -> str:
        """解释差异表达分析结果"""
        total_genes = results.get('total_genes', 0)
        significant_genes = results.get('significant_genes', 0)
        
        # 防止零除错误
        percentage = (significant_genes / total_genes * 100) if total_genes > 0 else 0.0
        
        explanation = f"""
差异表达分析完成。

统计摘要：
- 总基因数：{total_genes}
- 显著差异基因（调整后p值 < 0.05）：{significant_genes}
- 显著比例：{percentage:.1f}%

主要发现：
1. 识别出 {significant_genes} 个在不同条件下表达水平显著变化的基因。
2. 这些基因可能与研究的生物学过程密切相关。

建议下一步：
- 对显著差异基因进行功能富集分析。
- 验证关键基因的表达变化。
- 结合文献进一步解读生物学意义。
"""
        return explanation
    
    def explain_pathway_analysis(self, pathways: list[dict[str, Any]]) -> str:
        """解释通路分析结果"""
        if not pathways:
            return "未发现显著富集的通路。"
        
        explanation = "通路富集分析结果：\n\n"
        for i, pathway in enumerate(pathways[:5], 1):  # 只显示前5个
            explanation += f"{i}. {pathway.get('name', 'Unknown')}\n"
            explanation += f"   - 富集分数：{pathway.get('score', 'N/A')}\n"
            explanation += f"   - p值：{pathway.get('pvalue', 'N/A')}\n\n"
        
        return explanation
    
    def generate_llm_explanation(self, data: dict[str, Any], question: str) -> str:
        """使用 LLM 生成更详细的解释"""
        if not self.llm_client:
            return "LLM 客户端未配置，无法生成详细解释。"
        
        # 实际实现需要调用 LLM API
        # 这里将调用 LLM 客户端
        return "LLM 解释功能待实现。"