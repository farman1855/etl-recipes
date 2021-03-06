import os
import shutil
import helpers
import unittest
from models import Matchable, Recipe
import spark


class MatchableTest(unittest.TestCase):
    def fuzzy_match(self, left, right):
        return Matchable(left).fuzzy_match(right)

    def test_match_same_string(self):
        self.assertTrue(self.fuzzy_match("chilie", "chilie"))

    def test_match_singular_plural(self):
        self.assertTrue(self.fuzzy_match("chilie", "chillies"))

    def test_match_small_mispell(self):
        self.assertTrue(self.fuzzy_match("chilie", "chiliee"))

    def test_does_not_match_huge_mispell(self):
        self.assertFalse(self.fuzzy_match("chilie", "chilean"))


class TestRecipe(unittest.TestCase):
    def recipe_attrs(self, override_attrs):
        recipe_attrs = {"ingredients": "", "description": ""}
        recipe_attrs.update(override_attrs)
        return recipe_attrs

    def test_has_chili(self):
        recipe = Recipe(self.recipe_attrs({"ingredients":
                                           "salt sugar sour chili"}))
        self.assertTrue(recipe.has_chili())

    def test_has_no_chili(self):
        recipe = Recipe(self.recipe_attrs({"ingredients":
                                           "salt sugar sour spice"}))
        self.assertFalse(recipe.has_chili())

    def test_is_unkown(self):
        recipe = Recipe(self.recipe_attrs({"prepTime": ""}))
        self.assertEqual("Unkown", recipe.difficulty())

    def test_is_easy(self):
        recipe = Recipe(self.recipe_attrs({"prepTime": "PT1M",
                                           "cookTime": "PT1M"}))
        self.assertEqual("Easy", recipe.difficulty())

    def test_is_medium(self):
        recipe = Recipe(self.recipe_attrs({"prepTime": "PT15M",
                                           "cookTime": "PT16M"}))
        self.assertEqual("Medium", recipe.difficulty())

    def test_is_hard(self):
        recipe = Recipe(self.recipe_attrs({"prepTime": "PT30M",
                                           "cookTime": "PT31M"}))
        self.assertEqual("Hard", recipe.difficulty())


class TestSpark(unittest.TestCase):
    sc, sql_context = spark.configure_spark("SkillUpExerciseTest", "local")
    output = "tests/output.test"

    @classmethod
    def delete_output_if_exist(cls):
        if os.path.exists(cls.output):
            shutil.rmtree(cls.output)

    setUpClass = delete_output_if_exist
    tearDownClass = delete_output_if_exist

    def test_create_success_file(self):
        spark.run(self.sc, self.sql_context, self.output)
        self.assertTrue(os.path.exists(self.output + "/_SUCCESS"))


if __name__ == '__main__':
    unittest.main()
