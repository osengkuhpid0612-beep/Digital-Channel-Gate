#!/usr/bin/env python3
import json
import os
from datetime import datetime

class TruthShanRenValidator:
    """真善忍驗證器 - 整合第五步優化"""
    
    def __init__(self, rules_path="config/truth-rules.json"):
        with open(rules_path, 'r', encoding='utf-8') as f:
            self.rules = json.load(f)
        self.violation_log = []
    
    def validate_truth(self, content, source=""):
        """檢查『真』- 虛假信息"""
        truth_score = 100
        issues = []
        
        for keyword in self.rules['truth_filters']['fake_news_keywords']:
            if keyword.lower() in content.lower():
                truth_score -= 20
                issues.append({
                    'type': 'fake_news',
                    'keyword': keyword,
                    'severity': 'high'
                })
        
        for pattern in self.rules['truth_filters']['clickbait_patterns']:
            if pattern in content:
                truth_score -= 15
                issues.append({
                    'type': 'clickbait',
                    'pattern': pattern,
                    'severity': 'medium'
                })
        
        return max(0, truth_score), issues
    
    def validate_goodness(self, content):
        """檢查『善』- 惡意內容"""
        goodness_score = 100
        issues = []
        
        for keyword in self.rules['goodness_filters']['hate_speech_keywords']:
            if keyword in content:
                goodness_score -= 30
                issues.append({
                    'type': 'hate_speech',
                    'keyword': keyword,
                    'severity': 'critical'
                })
        
        for keyword in self.rules['goodness_filters']['violent_content']:
            if keyword in content:
                goodness_score -= 40
                issues.append({
                    'type': 'violent_content',
                    'keyword': keyword,
                    'severity': 'critical'
                })
        
        return max(0, goodness_score), issues
    
    def validate_patience(self, content):
        """檢查『忍』- 極端偏激"""
        patience_score = 100
        issues = []
        
        for keyword in self.rules['patience_filters']['extreme_keywords']:
            if keyword in content:
                patience_score -= 15
                issues.append({
                    'type': 'extreme_language',
                    'keyword': keyword,
                    'severity': 'medium'
                })
        
        for keyword in self.rules['patience_filters']['conspiracy_keywords']:
            if keyword in content:
                patience_score -= 20
                issues.append({
                    'type': 'conspiracy_theory',
                    'keyword': keyword,
                    'severity': 'high'
                })
        
        return max(0, patience_score), issues
    
    def validate(self, content, source="unknown"):
        """進行完整驗證"""
        truth_score, truth_issues = self.validate_truth(content, source)
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
            'issue_count': len(all_issues),
            'critical_issues': len([i for i in all_issues if i.get('severity') == 'critical'])
        }
        
        if all_issues:
            self.violation_log.append(result)
        
        return result
    
    def get_violation_report(self):
        """獲取違規報告"""
        if not self.violation_log:
            return None
        
        return {
            'total_violations': len(self.violation_log),
            'critical_count': sum(1 for v in self.violation_log if v['critical_issues'] > 0),
            'average_score': sum(v['overall_score'] for v in self.violation_log) / len(self.violation_log),
            'violations': self.violation_log
        }

if __name__ == "__main__":
    validator = TruthShanRenValidator()
    
    test_cases = [
        "這是一個正常的新聞報導",
        "震驚！你不會相信發生了什麼",
        "我們應該攻擊那些人",
        "這個陰謀論很有趣"
    ]
    
    for test in test_cases:
        result = validator.validate(test)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print("---")
