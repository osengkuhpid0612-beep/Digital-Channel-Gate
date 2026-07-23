#!/usr/bin/env python3
import json
import os
from datetime import datetime

class TruthValidator:
    def __init__(self, rules_path="config/truth-rules.json"):
        with open(rules_path, 'r', encoding='utf-8') as f:
            self.rules = json.load(f)
    
    def validate_truth(self, content):
        """檢查『真』- 虛假信息"""
        truth_score = 100
        issues = []
        
        for keyword in self.rules['truth_filters']['fake_news_keywords']:
            if keyword.lower() in content.lower():
                truth_score -= 20
                issues.append(f"檢測到虛假信息關鍵詞: {keyword}")
        
        for pattern in self.rules['truth_filters']['clickbait_patterns']:
            if pattern in content:
                truth_score -= 15
                issues.append(f"檢測到標題黨模式: {pattern}")
        
        return max(0, truth_score), issues
    
    def validate_goodness(self, content):
        """檢查『善』- 惡意內容"""
        goodness_score = 100
        issues = []
        
        for keyword in self.rules['goodness_filters']['hate_speech_keywords']:
            if keyword in content:
                goodness_score -= 30
                issues.append(f"檢測到仇恨言論: {keyword}")
        
        for keyword in self.rules['goodness_filters']['violent_content']:
            if keyword in content:
                goodness_score -= 40
                issues.append(f"檢測到暴力內容: {keyword}")
        
        return max(0, goodness_score), issues
    
    def validate_patience(self, content):
        """檢查『忍』- 極端偏激"""
        patience_score = 100
        issues = []
        
        for keyword in self.rules['patience_filters']['extreme_keywords']:
            if keyword in content:
                patience_score -= 15
                issues.append(f"檢測到極端用詞: {keyword}")
        
        for keyword in self.rules['patience_filters']['conspiracy_keywords']:
            if keyword in content:
                patience_score -= 20
                issues.append(f"檢測到陰謀論: {keyword}")
        
        return max(0, patience_score), issues
    
    def validate(self, content):
        """進行完整驗證"""
        truth_score, truth_issues = self.validate_truth(content)
        goodness_score, goodness_issues = self.validate_goodness(content)
        patience_score, patience_issues = self.validate_patience(content)
        
        overall_score = (truth_score + goodness_score + patience_score) / 3
        
        return {
            'overall_score': overall_score,
            'truth_score': truth_score,
            'goodness_score': goodness_score,
            'patience_score': patience_score,
            'passed': overall_score >= 70,
            'issues': truth_issues + goodness_issues + patience_issues,
            'timestamp': datetime.now().isoformat()
        }

if __name__ == "__main__":
    validator = TruthValidator()
    
    test_content = "這是一個測試內容"
    result = validator.validate(test_content)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
