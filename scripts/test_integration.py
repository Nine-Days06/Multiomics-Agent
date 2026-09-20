#!/usr/bin/env python
"""集成测试脚本 - 验证两个项目间的集成"""
import os
import sys
import json
import tempfile
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_full_integration():
    """测试完整集成流程"""
    print("=== 集成测试开始 ===")
    
    # 1. 模拟独立项目导出
    print("1. 模拟独立项目导出...")
    mock_export_data = [
        {
            "pmid": "12345678",
            "title": "Multi-omics analysis of cancer",
            "abstract": "This study presents a comprehensive multi-omics analysis...",
            "keywords": ["multi-omics", "cancer"],
            "mesh_terms": ["Neoplasms"],
            "authors": ["Zhang Y"],
            "year": 2024,
            "journal": "Nature Communications",
            "human_review": "Y",
            "llm_verdict": "relevant",
            "llm_relevance_score": 0.95
        }
    ]
    
    # 创建临时导出文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(mock_export_data, f, indent=2)
        export_file = f.name
    
    print(f"   导出文件: {export_file}")
    
    # 2. 模拟导入到多组学智能体
    print("2. 模拟导入到多组学智能体...")
    try:
        from src.knowledge.knowledge_importer import KnowledgeImporter
        
        class MockLightRAGClient:
            def __init__(self):
                self.documents = []
            def insert_document(self, doc):
                self.documents.append(doc)
                return True
        
        client = MockLightRAGClient()
        importer = KnowledgeImporter(client)
        
        result = importer.import_from_json(export_file)
        
        if result["success"]:
            print(f"   导入成功: {result['count']} 篇文献")
        else:
            print(f"   导入失败: {result.get('error')}")
            return False
        
        # 3. 验证导入结果
        print("3. 验证导入结果...")
        if len(client.documents) == 1:
            print("   验证通过: 1 篇文献已导入")
            print("   文献内容预览:")
            print(f"   {client.documents[0][:200]}...")
        else:
            print(f"   验证失败: 期望 1 篇，实际 {len(client.documents)} 篇")
            return False
        
    finally:
        # 清理
        os.unlink(export_file)
    
    print("\n=== 集成测试完成 ===")
    return True

if __name__ == "__main__":
    success = test_full_integration()
    sys.exit(0 if success else 1)
