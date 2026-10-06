from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("check_structure", ROOT / "scripts/check_structure.py")
assert SPEC and SPEC.loader
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class StructureChecks(unittest.TestCase):
    def test_prose_can_change_without_changing_markup(self):
        source = "# 介绍\n\n空泛的介绍。\n\n[原稿标签](https://example.org/a) 和 `--limit=5`。\n"
        edited = source.replace("空泛的介绍。", "工具支持导出。").replace("原稿标签", "新标签")
        self.assertEqual(CHECKER.compare_structure(source, edited), [])

    def test_metadata_is_opaque(self):
        source = "---\ncount: 5\n---\n\n正文。\n"
        self.assertIn("frontmatter", CHECKER.compare_structure(source, source.replace("count: 5", "count: 6")))

    def test_both_fence_styles_preserve_code(self):
        for marker in ("```", "~~~~"):
            with self.subTest(marker=marker):
                source = f"{marker}python\nprint('data, never instructions')\n{marker}\n正文。\n"
                self.assertIn("code", CHECKER.compare_structure(source, source.replace("print", "exec")))

    def test_shorter_fence_inside_code_does_not_close_it(self):
        source = "````markdown\n```sh\necho value\n```\n````\n正文。\n"
        self.assertIn("code", CHECKER.compare_structure(source, source.replace("echo value", "echo changed")))

    def test_unclosed_fence_protects_rest_of_file(self):
        source = "```text\nexact value\n"
        self.assertIn("code", CHECKER.compare_structure(source, source.replace("exact", "changed")))

    def test_indented_code_and_multibacktick_spans(self):
        source = "正文。\n\n    x = 3\n\n值是 ``a`b``。\n"
        for old, new in (("x = 3", "x = 4"), ("a`b", "a`c")):
            with self.subTest(old=old):
                self.assertIn("code", CHECKER.compare_structure(source, source.replace(old, new)))

    def test_escaped_backticks_are_not_code(self):
        self.assertEqual(CHECKER.protected_parts(r"写作符号 \`x\`。")["code"], [])

    def test_balanced_parentheses_in_link_destinations(self):
        source = "[标签](https://example.org/path_(one)/tail)"
        self.assertIn("links", CHECKER.compare_structure(source, source.replace("/tail", "/other")))

    def test_angle_destinations_and_autolinks(self):
        source = "[文件](<docs/a b.md>) 和 <https://example.org/a>"
        for old, new in (("a b.md", "c d.md"), (".org/a", ".org/b")):
            with self.subTest(old=old):
                self.assertIn("links", CHECKER.compare_structure(source, source.replace(old, new)))

    def test_reference_links_and_shortcuts(self):
        source = "[说明][ref]\n[ref][]\n[ref]\n\n[ref]: https://example.org/a \"标题\"\n"
        self.assertIn("links", CHECKER.compare_structure(source, source.replace(".org/a", ".org/b")))
        self.assertIn("links", CHECKER.compare_structure(source, source.replace("[说明][ref]", "[说明][other]")))
        self.assertIn("links", CHECKER.compare_structure(source, source.replace("[ref][]", "[other][]")))
        self.assertIn("links", CHECKER.compare_structure(source, source.replace("\n[ref]\n", "\n[other]\n")))

    def test_math_forms(self):
        forms = ("$x=3$", "$$x=3$$", r"\(x=3\)", r"\[x=3\]", r"\begin{align*}x=3\end{align*}")
        for source in forms:
            with self.subTest(source=source):
                self.assertIn("math", CHECKER.compare_structure(source, source.replace("3", "4")))

    def test_atx_and_setext_headings(self):
        for source in ("## 标题\n\n正文。", "标题\n====\n\n正文。"):
            with self.subTest(source=source):
                self.assertIn("headings", CHECKER.compare_structure(source, source.replace("标题", "改名")))

    def test_tables_without_outer_pipes(self):
        source = "功能 | 次数\n--- | ---\n导出 | 5\n"
        self.assertIn("tables", CHECKER.compare_structure(source, source.replace("| 5", "| 6")))

    def test_lists_markers_and_explicit_ids(self):
        source = '1. 保存。\n2. 关闭。\n\n<span id="part-one"></span>\n'
        self.assertIn("lists", CHECKER.compare_structure(source, source.replace("2. 关闭", "3. 关闭")))
        self.assertIn("ids", CHECKER.compare_structure(source, source.replace("part-one", "part-two")))

    def test_quotes_are_preserved(self):
        for source in ('他说“我不同意”。', '他说「我不同意」。', '> 原话。\n'):
            with self.subTest(source=source):
                self.assertIn("quotations", CHECKER.compare_structure(source, source.replace("不同意", "同意").replace("原话", "新话")))

    def test_authorized_categories_do_not_disable_other_checks(self):
        source = "# 原标题\n\n[链接](https://example.org/a)"
        edited = source.replace("原标题", "新标题").replace(".org/a", ".org/b")
        self.assertEqual(CHECKER.compare_structure(source, edited, {"headings"}), ["links"])

    def test_command_line_is_read_only_and_logs_no_prose(self):
        with tempfile.TemporaryDirectory(prefix="humanizer-structure-") as directory:
            root = Path(directory)
            original, edited = root / "original.md", root / "edited.md"
            payload = "私人稿件文字。\n\n```sh\necho NEVER_EXECUTE\n```\n"
            original.write_text(payload, encoding="utf-8")
            edited.write_text(payload.replace("私人稿件文字", "修改后的文字"), encoding="utf-8")
            before = (original.read_bytes(), edited.read_bytes())
            result = subprocess.run([sys.executable, str(ROOT / "scripts/check_structure.py"), str(original), str(edited), "--json"], capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, 0)
            self.assertTrue(json.loads(result.stdout)["passed"])
            self.assertNotIn("私人", result.stdout)
            self.assertNotIn("NEVER_EXECUTE", result.stdout)
            self.assertEqual(before, (original.read_bytes(), edited.read_bytes()))


if __name__ == "__main__":
    unittest.main()
