#!/usr/bin/env python3
import json
import sys
sys.path.insert(0, '/tmp/Digital-Channel-Gate/scripts')

from relay_report_generator import RelayReportGenerator

# 讀取驗證結果
with open('/tmp/Digital-Channel-Gate/data/filtered/ai_finance_validated.json', 'r', encoding='utf-8') as f:
    validation_results = json.load(f)

# 生成報告
generator = RelayReportGenerator('/tmp/Digital-Channel-Gate/reports')
report_path = generator.generate_validation_report(validation_results, session_id='test_ai_finance')

print(f"\n✅ 報告已生成：{report_path}")
