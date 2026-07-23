#!/usr/bin/env python3
"""
竹泊爾王國 - 中繼站隔離驗證器
小蜥蜴在隔離沙盒中工作，不保存任何記憶
每次執行都是乾淨的小蜥蜴
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Tuple

class IsolatedLizardValidator:
    """隔離沙盒模式的小蜥蜴驗證器"""
    
    def __init__(self, rules_path="config/truth-rules.json"):
        """初始化時載入規則，但不保存任何狀態"""
        self.rules = self._load_rules(rules_path)
        # 重要：不保存任何記憶或狀態
        self.session_id = f"isolated_{datetime.now().isoformat()}"
        self.is_isolated = True
    
    def _load_rules(self, rules_path: str) -> Dict:
        """載入真善忍規則"""
        if os.path.exists(rules_path):
            with open(rules_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def validate_truth(self, content: str) -> Tuple[int, List[str]]:
        """檢查『真』- 虛假信息"""
        truth_score = 100
        issues = []
        
        for keyword in self.rules.get('truth_filters', {}).get('fake_news_keywords', []):
            if keyword.lower() in content.lower():
                truth_score -= 20
                issues.append(f"虛假信息: {keyword}")
        
        for pattern in self.rules.get('truth_filters', {}).get('clickbait_patterns', []):
            if pattern in content:
                truth_score -= 15
                issues.append(f"標題黨: {pattern}")
        
        return max(0, truth_score), issues
    
    def validate_goodness(self, content: str) -> Tuple[int, List[str]]:
        """檢查『善』- 惡意內容"""
        goodness_score = 100
        issues = []
        
        for keyword in self.rules.get('goodness_filters', {}).get('hate_speech_keywords', []):
            if keyword in content:
                goodness_score -= 30
                issues.append(f"仇恨言論: {keyword}")
        
        for keyword in self.rules.get('goodness_filters', {}).get('violent_content', []):
            if keyword in content:
                goodness_score -= 40
                issues.append(f"暴力內容: {keyword}")
        
        return max(0, goodness_score), issues
    
    def validate_patience(self, content: str) -> Tuple[int, List[str]]:
        """檢查『忍』- 極端偏激"""
        patience_score = 100
        issues = []
        
        for keyword in self.rules.get('patience_filters', {}).get('extreme_keywords', []):
            if keyword in content:
                patience_score -= 15
                issues.append(f"極端用詞: {keyword}")
        
        for keyword in self.rules.get('patience_filters', {}).get('conspiracy_keywords', []):
            if keyword in content:
                patience_score -= 20
                issues.append(f"陰謀論: {keyword}")
        
        return max(0, patience_score), issues
    
    def validate(self, content: str, source: str = "unknown") -> Dict:
        """
        進行完整驗證
        
        返回：驗證結果（不保存到記憶）
        """
        truth_score, truth_issues = self.validate_truth(content)
        goodness_score, goodness_issues = self.validate_goodness(content)
        patience_score, patience_issues = self.validate_patience(content)
        
        overall_score = (truth_score + goodness_score + patience_score) / 3
        all_issues = truth_issues + goodness_issues + patience_issues
        
        result = {
            'overall_score': round(overall_score, 2),
            'truth_score': truth_score,
            'goodness_score': goodness_score,
            'patience_score': patience_score,
            'passed': overall_score >= 70,
            'issues': all_issues,
            'source': source,
            'timestamp': datetime.now().isoformat(),
            'session_id': self.session_id,
            'is_isolated': True
        }
        
        # 重要：不保存到任何記憶中
        return result
    
    def cleanup(self):
        """清理所有臨時狀態"""
        self.rules = {}
        self.session_id = None
        print("✅ 隔離驗證器已清理，小蜥蜴恢復純淨")


def batch_validate_data(input_file: str, output_file: str) -> None:
    """
    批量驗證資料
    
    參數：
    - input_file: 原始資料檔案
    - output_file: 驗證結果檔案
    """
    validator = IsolatedLizardValidator()
    
    try:
        # 讀取原始資料
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        results = {
            'validation_timestamp': datetime.now().isoformat(),
            'session_id': validator.session_id,
            'is_isolated': True,
            'validated_items': []
        }
        
        # 驗證每一項
        items = data if isinstance(data, list) else data.get('items', [])
        for item in items:
            content = item.get('content', '') or item.get('title', '')
            source = item.get('source', 'unknown')
            
            validation_result = validator.validate(content, source)
            results['validated_items'].append({
                'source': source,
                'content_preview': content[:100],
                'validation': validation_result
            })
        
        # 寫入結果
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 驗證完成: {len(results['validated_items'])} 項")
    
    finally:
        # 清理
        validator.cleanup()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 2:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        batch_validate_data(input_file, output_file)
    else:
        print("用法: python isolated_validator.py <input_file> <output_file>")
