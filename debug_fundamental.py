#!/usr/bin/env python3
"""Debug growth data parsing."""

import sys
import os
import warnings
warnings.filterwarnings('ignore')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import akshare as ak

code = "600519"

print("=== Testing stock_financial_abstract ===")
df = ak.stock_financial_abstract(symbol=code)
print(f"Shape: {df.shape}")
print(f"Columns: {list(df.columns[:10])}")
print()
print("First 3 rows (key columns):")
if '指标' in df.columns:
    print(df[['指标', '20250331', '20241231']].head(10))

print()
print("=== Testing stock_gdfx_top_10_em ValueError ===")
import traceback
try:
    df = ak.stock_gdfx_top_10_em(symbol='sh600519', date='20250331')
    print(f"Shape: {df.shape}")
except Exception as e:
    traceback.print_exc()