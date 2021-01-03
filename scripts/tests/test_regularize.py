# coding:utf-8

import unittest
from unittest import TestCase
import textwrap
from layout_optimizer.layout_optimizer import (
    regularize_text,
    extract_vailed_texts,
    text2score,
    devide_strokes_side,
    char2stroke,
    text2keystrokes,
    keystrokes2score,
    char2stroke,
)


class TestGeneration(TestCase):
    def test_regularize_text(self):
        self.assertEqual("このこうかは1たーんに1ど.", regularize_text("この効果は１ターンに１度。"))
        self.assertEqual(
            "ちゅうしんに,じどう・せいしょうねんしりょうさーびす", regularize_text("中心に、児童・青少年資料サービス")
        )

    def test_extract_vailed_texts(self):
        tin1 = textwrap.dedent(
            """\
            # A-ID:w201106-0002400375
            1 配糖体の一種アミグダリンが含まれる。
            2 日本には古代に中国から伝えられ、"""
        )

        tout1 = ["配糖体の一種アミグダリンが含まれる。", "日本には古代に中国から伝えられ、"]

        tin2 = textwrap.dedent(
            """\
            2-3 関係なしまたは弱い関係:0.999968 対比:1.1e-05 原因・理由:5e-06

            # A-ID:w201106-0002400376
            1 古い文献には「今春」とも。"""
        )

        tout2 = ["関係なしまたは弱い関係:0.999968 対比:1.1e-05 原因・理由:5e-06", "古い文献には「今春」とも。"]
        self.assertEqual(tout1, extract_vailed_texts(tin1))
        self.assertEqual(tout2, extract_vailed_texts(tin2))

    def test_score_from_text(self):
        # self.assertTrue(1 > 0)
        self.assertGreater(text2score(u"あいうえお"), text2score(u"あいう"))
        self.assertEqual(text2score(u"ぎゃぎゅぎょ"), text2score(u"ぎぎぎ"))
        # self.assertGreater(text2score(u"ぎぎぎ"), text2score(u"あこす"))
        self.assertGreater(text2score(u"じょぃぎゃぅ"), text2score(u"ぎょぎょう"))
        # print(str(text2score(u"じょぃぎゃぅ"))+" "+str(text2score(u"ぎょぎょう")))
        self.assertNotEqual(text2score(u"ぎゃぐり"), text2score(u"べぼば"))

    def test_devide_stroke_side(self):
        self.assertEqual(devide_strokes_side("asdfghjkl;")[0], "asdfg")
        self.assertEqual(devide_strokes_side("asdfghjkl;")[1], "hjkl;")
        self.assertEqual(devide_strokes_side("zxcvbnm,./")[0], "zxcvb")
        self.assertEqual(devide_strokes_side("zxcvbnm,./")[1], "nm,./")

    def test_char2stroke(self):
        self.assertEqual(char2stroke("あ"), "al")
        self.assertEqual(char2stroke("い"), "a;")
        self.assertEqual(char2stroke("あい"), None)
        self.assertEqual(char2stroke("き"), "s;")
        self.assertEqual(char2stroke("きゃ"), "so")
        self.assertEqual(char2stroke("ぎゃ"), "wo")
        self.assertEqual(char2stroke("わ"), "zl")
        self.assertEqual(char2stroke(","), ",")
        self.assertEqual(char2stroke("."), ".")

    def test_keystrokes_from_text(self):
        self.assertEqual(text2keystrokes("あ"), "al")
        self.assertEqual(text2keystrokes("あい"), "ala;")
        self.assertEqual(text2keystrokes("あいう"), "ala;aj")
        self.assertEqual(text2keystrokes("わぎゃ"), "zlwo")
        self.assertNotEqual(text2keystrokes("ぎ"), "ぎゃ")

    def test_score_from_keystrokes(self):
        self.assertIsInstance(keystrokes2score("a"), float)
        self.assertLess(keystrokes2score("a"), keystrokes2score("as"))
        self.assertLess(keystrokes2score("as"), keystrokes2score("asd"))
        self.assertLess(keystrokes2score("asd"), keystrokes2score("asdf"))
        self.assertLess(keystrokes2score("j"), keystrokes2score("jk"))
        self.assertNotEqual(keystrokes2score("wo"), keystrokes2score("wi"))
        self.assertLess(keystrokes2score("jk"), 1.0)
        self.assertGreater(keystrokes2score("jk"), 0.01)
        self.assertEqual(keystrokes2score(""), 0.0)


if __name__ == "__main__":
    unittest.main()
