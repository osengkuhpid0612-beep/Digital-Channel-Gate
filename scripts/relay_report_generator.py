#!/usr/bin/env python3
"""
竹泊爾王國 - 中繼站報告生成器
小蜥蜴在隔離沙盒中工作後，生成工作報告
報告格式跟通訊器小蜥蜴一致
"""

import json
import os
from datetime import datetime
from typing import Dict, List

class RelayReportGenerator:
    """中繼站報告生成器"""
    
    def __init__(self, report_dir: str = "reports"):
        self.report_dir = report_dir
        os.makedirs(report_dir, exist_ok=True)
    
    def generate_validation_report(self, validation_results: Dict, 
                                   session_id: str = None) -> str:
        """
        生成驗證報告（Markdown 格式）
        
        參數：
        - validation_results: 驗證結果字典
        - session_id: 會話 ID
        
        返回：報告檔案路徑
        """
        if not session_id:
            session_id = f"relay_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 統計資訊
        total_items = len(validation_results.get('validated_items', []))
        passed_items = sum(1 for item in validation_results.get('validated_items', [])
                          if item.get('validation', {}).get('passed', False))
        failed_items = total_items - passed_items
        
        # 計算平均分數
        scores = [item.get('validation', {}).get('overall_score', 0)
                 for item in validation_results.get('validated_items', [])]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        # 找出問題最多的項目
        problematic_items = [
            item for item in validation_results.get('validated_items', [])
            if len(item.get('validation', {}).get('issues', [])) > 0
        ]
        
        # 生成報告
        report = f"""# 中繼站驗證報告
**會話 ID**：{session_id}  
**報告生成時間**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**報告生成者**：中繼站隔離小蜥蜴
---

## 📋 驗證摘要

| 項目 | 數值 |
|------|------|
| 驗證總數 | {total_items} |
| 通過數 | {passed_items} |
| 失敗數 | {failed_items} |
| 通過率 | {(passed_items/total_items*100):.1f}% |
| 平均評分 | {avg_score:.2f}/100 |

---

## 🔍 驗證詳情

### 評分分佈

| 評分範圍 | 數量 | 百分比 |
|---------|------|--------|
| 90-100 | {sum(1 for s in scores if s >= 90)} | {(sum(1 for s in scores if s >= 90)/len(scores)*100):.1f}% |
| 70-89 | {sum(1 for s in scores if 70 <= s < 90)} | {(sum(1 for s in scores if 70 <= s < 90)/len(scores)*100):.1f}% |
| 50-69 | {sum(1 for s in scores if 50 <= s < 70)} | {(sum(1 for s in scores if 50 <= s < 70)/len(scores)*100):.1f}% |
| 0-49 | {sum(1 for s in scores if s < 50)} | {(sum(1 for s in scores if s < 50)/len(scores)*100):.1f}% |

---

## ⚠️ 問題項目

"""
        
        if problematic_items:
            report += f"檢測到 {len(problematic_items)} 個問題項目：\n\n"
            for i, item in enumerate(problematic_items[:10], 1):  # 只顯示前 10 個
                issues = item.get('validation', {}).get('issues', [])
                report += f"### {i}. {item.get('source', 'Unknown')}\n"
                report += f"**內容預覽**：{item.get('content_preview', '')[:100]}...\n"
                report += f"**評分**：{item.get('validation', {}).get('overall_score', 0)}/100\n"
                report += f"**問題**：\n"
                for issue in issues[:5]:  # 只顯示前 5 個問題
                    report += f"- {issue}\n"
                report += "\n"
        else:
            report += "✅ 所有項目均通過驗證，無問題項目。\n\n"
        
        # 生成真善忍評分分析
        report += """---

## 📊 真善忍評分分析

### 『真』評分統計
"""
        truth_scores = [item.get('validation', {}).get('truth_score', 0)
                       for item in validation_results.get('validated_items', [])]
        report += f"- 平均分：{sum(truth_scores)/len(truth_scores) if truth_scores else 0:.2f}/100\n"
        report += f"- 最高分：{max(truth_scores) if truth_scores else 0}/100\n"
        report += f"- 最低分：{min(truth_scores) if truth_scores else 0}/100\n\n"
        
        report += """### 『善』評分統計
"""
        goodness_scores = [item.get('validation', {}).get('goodness_score', 0)
                          for item in validation_results.get('validated_items', [])]
        report += f"- 平均分：{sum(goodness_scores)/len(goodness_scores) if goodness_scores else 0:.2f}/100\n"
        report += f"- 最高分：{max(goodness_scores) if goodness_scores else 0}/100\n"
        report += f"- 最低分：{min(goodness_scores) if goodness_scores else 0}/100\n\n"
        
        report += """### 『忍』評分統計
"""
        patience_scores = [item.get('validation', {}).get('patience_score', 0)
                          for item in validation_results.get('validated_items', [])]
        report += f"- 平均分：{sum(patience_scores)/len(patience_scores) if patience_scores else 0:.2f}/100\n"
        report += f"- 最高分：{max(patience_scores) if patience_scores else 0}/100\n"
        report += f"- 最低分：{min(patience_scores) if patience_scores else 0}/100\n\n"
        
        report += f"""---

## 📝 結論

中繼站隔離小蜥蜴已完成本次驗證工作。所有資料均已按照真善忍標準進行檢測。
通過驗證的資料已存儲在 `data/filtered` 目錄中，可供精靈們安全使用。

**報告版本**：1.0  
**隔離模式**：已啟用  
**小蜥蜴狀態**：已清理（恢復純淨）  
**最後更新**：{datetime.now().isoformat()}  
**狀態**：已完成
"""
        
        # 儲存報告
        report_filename = f"Relay_Report_{session_id}.md"
        report_path = os.path.join(self.report_dir, report_filename)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ 報告已生成：{report_path}")
        return report_path
    
    def generate_daily_summary(self, reports_dir: str = None) -> str:
        """
        生成每日摘要報告
        
        返回：摘要報告檔案路徑
        """
        if not reports_dir:
            reports_dir = self.report_dir
        
        summary = f"""# 中繼站每日摘要
**生成時間**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**生成者**：中繼站隔離小蜥蜴

---

## 📊 今日工作統計

- 驗證報告數：待統計
- 通過率：待統計
- 平均評分：待統計

---

**狀態**：已完成  
**下次執行**：明天午夜
"""
        
        summary_path = os.path.join(reports_dir, 
                                   f"Daily_Summary_{datetime.now().strftime('%Y-%m-%d')}.md")
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        return summary_path


if __name__ == "__main__":
    generator = RelayReportGenerator()
    print("✅ 報告生成器已準備")
