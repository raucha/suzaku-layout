# coding:utf-8

import unittest
from unittest import TestCase
import textwrap
from layout_optimizer.layout_optimizer import regularize_text, extract_vailed_texts, get_score


class TestGeneration(TestCase):
    def test_regularize_text(self):
        self.assertEqual("コノコウカハ1ターンニ1ド.", regularize_text("この効果は１ターンに１度。"))
        self.assertEqual("チュウシンニ,ジドウ・セイショウネンシリョウサービス", 
            regularize_text("中心に、児童・青少年資料サービス"))
    
    def test_extract_vailed_texts(self):
        tin1 = textwrap.dedent("""\
            # A-ID:w201106-0002400375
            1 配糖体の一種アミグダリンが含まれる。
            2 日本には古代に中国から伝えられ、""")

        tout1 = [
            "配糖体の一種アミグダリンが含まれる。",
            "日本には古代に中国から伝えられ、"]

        tin2 = textwrap.dedent("""\
            2-3 関係なしまたは弱い関係:0.999968 対比:1.1e-05 原因・理由:5e-06

            # A-ID:w201106-0002400376
            1 古い文献には「今春」とも。""")

        tout2 = [
            "関係なしまたは弱い関係:0.999968 対比:1.1e-05 原因・理由:5e-06",
            "古い文献には「今春」とも。"]
        self.assertEqual(tout1, extract_vailed_texts(tin1))
        self.assertEqual(tout2, extract_vailed_texts(tin2))

    def test_regularize_text(self):
        # self.assertTrue(1 > 0)
        self.assertTrue(get_score(u"アイウエオ") > get_score(u"アイウ"))
        self.assertTrue(get_score(u"ギョギョウ") > get_score(u"あいうえお"))
        self.assertTrue(get_score(u"ジョィギャ") > get_score(u"あいうえお"))


if __name__ == "__main__":
    unittest.main()
