# -*- coding: utf-8 -*-
"""Tests for market strategy blueprints."""

import unittest

from src.core.market_strategy import get_market_strategy_blueprint
from src.market_analyzer import MarketAnalyzer, MarketOverview


class TestMarketStrategyBlueprint(unittest.TestCase):
    """Validate CN/US strategy blueprint basics."""

    def test_cn_blueprint_contains_action_framework(self):
        blueprint = get_market_strategy_blueprint("cn")
        block = blueprint.to_prompt_block()

        self.assertIn("A股市场三段式复盘策略", block)
        self.assertIn("Action Framework", block)
        self.assertIn("进攻", block)

    def test_us_blueprint_contains_regime_strategy(self):
        blueprint = get_market_strategy_blueprint("us")
        block = blueprint.to_prompt_block()

        self.assertIn("US Market Regime Strategy", block)
        self.assertIn("Risk-on", block)
        self.assertIn("Macro & Flows", block)


class TestMarketAnalyzerStrategyPrompt(unittest.TestCase):
    """Validate strategy section is injected into prompt/report."""

    def test_cn_prompt_contains_strategy_plan_section(self):
        analyzer = MarketAnalyzer(region="cn")
        prompt = analyzer._build_review_prompt(MarketOverview(date="2026-02-24"), [])

        self.assertIn("策略计划", prompt)
        self.assertIn("A股市场三段式复盘策略", prompt)
        self.assertIn("建议仅供参考，不构成投资建议", prompt)

    def test_us_prompt_contains_strategy_plan_section(self):
        analyzer = MarketAnalyzer(region="us")
        prompt = analyzer._build_review_prompt(MarketOverview(date="2026-02-24"), [])

        self.assertIn("Strategy Plan", prompt)
        self.assertIn("US Market Regime Strategy", prompt)
        self.assertIn("For reference only, not investment advice", prompt)


class TestMarkdownStrategyBlock(unittest.TestCase):
    """Validate markdown rendering by region."""

    def test_cn_markdown_heading_is_chinese(self):
        block = get_market_strategy_blueprint("cn").to_markdown_block()
        self.assertIn("### 六、策略框架", block)
        self.assertIn("趋势结构", block)

    def test_us_markdown_heading_is_english_and_consistent(self):
        block = get_market_strategy_blueprint("us").to_markdown_block()
        self.assertIn("### 6. Strategy Framework", block)
        self.assertIn("Trend Regime", block)
        self.assertIn("Macro & Flows", block)
        self.assertIn("Sector Themes", block)


if __name__ == "__main__":
    unittest.main()
