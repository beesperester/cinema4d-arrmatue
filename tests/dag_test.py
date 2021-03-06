import c4d
import unittest

from typing import List

from armature import dag
from tests import utilities


class TestDagAtom(unittest.TestCase):
    def test_GetName(self):
        asset_object = utilities.create_example_dagatom()

        # assert resulting name
        result = asset_object.GetName()
        result_expected = "Asset_Grp"

        self.assertEqual(result, result_expected)

    def test_GetType(self):
        asset_object = utilities.create_example_dagatom()

        # assert resulting type
        result = asset_object.GetType()
        result_expected = c4d.Onull

        self.assertEqual(result, result_expected)

    def test_IsAlive(self):
        asset_object = utilities.create_example_dagatom()

        self.assertTrue(asset_object.IsAlive())

        asset_object.Remove()

        self.assertFalse(asset_object.IsAlive())


class TestDagBaseObject(unittest.TestCase):
    def test_GetChildren(self):
        asset_object = utilities.create_example_dagbaseobject()

        # assert resulting instance
        self.assertIsInstance(asset_object.GetChildren(), dag.DagAtomList)

        # assert list of resulting names
        result = [x.GetName() for x in asset_object.GetChildren()]
        result_expected = ["Geo_Grp", "Rig_Grp"]

        self.assertListEqual(result, result_expected)

    def test_GetChild(self):
        asset_object = utilities.create_example_dagbaseobject()

        child = asset_object.GetChild("Rig_Grp/Joints_Grp")

        # assert resulting instance
        self.assertIsInstance(child, dag.DagBaseObject)

        # assert name of resulting child
        result = child.GetName()
        result_expected = "Joints_Grp"

        self.assertEqual(result, result_expected)

    def test_GetParent(self):
        asset_object = utilities.create_example_dagbaseobject()

        child = asset_object.GetChild("Geo_Grp")

        parent = child.GetParent()

        # assert resulting instance
        self.assertIsInstance(parent, dag.DagBaseObject)

        # assert name of resulting parent
        result = parent.GetName()
        result_expected = "Asset_Grp"

        self.assertEqual(result, result_expected)

    def test_GetTags(self):
        asset_object = utilities.create_example_dagbaseobject()

        tags = asset_object.GetTags()

        # assert resulting instance
        self.assertIsInstance(tags, dag.DagAtomList)

        # assert resulting names
        result = [x.GetName() for x in tags]
        result_excpected = ["Asset_Constraint"]

        self.assertListEqual(result, result_excpected)

    def test_GetTag(self):
        asset_object = utilities.create_example_dagbaseobject()

        tag = asset_object.GetTag("Asset_Constraint")

        # assert resulting instance
        self.assertIsInstance(tag, dag.DagBaseTag)

        # assert resulting name
        result = tag.GetName()
        result_expected = "Asset_Constraint"

        self.assertEqual(result, result_expected)

    def test_GetRecursive(self):
        asset_object = utilities.create_example_recursive_dagbaseobject()

        result = []

        for child in asset_object.GetRecursive("Spine_*_Joint"):
            # assert resulting instance
            self.assertIsInstance(child, dag.DagBaseObject)

            result.append(child.GetName())

        result_expected = ["Spine_2_Joint", "Spine_3_Joint", "Spine_4_Joint"]

        self.assertListEqual(result, result_expected)


class TestDagList(unittest.TestCase):
    def test___iter__(self):
        example_list = utilities.create_example_daglist()

        result = []

        for item in example_list:
            result.append(item.GetName())

            # assert resulting instance
            self.assertIsInstance(item, dag.DagAtom)

        result_expected = [
            "BaseObject_{}_Null".format(x + 1) for x in range(0, 10)
        ]

        self.assertListEqual(result, result_expected)

    def test___getitem__(self):
        example_list = utilities.create_example_daglist()

        item = example_list[0]

        # assert resulting instance
        self.assertIsInstance(item, dag.DagAtom)

        # assert resulting name
        result = item.GetName()
        result_expected = "BaseObject_1_Null"

        self.assertEqual(result, result_expected)

    def test_Get(self):
        example_list = utilities.create_example_daglist()

        item = example_list.Get("BaseObject_2_Null")

        # assert resulting instance
        self.assertIsInstance(item, dag.DagAtom)

        # assert resulting name
        result = item.GetName()
        result_expected = "BaseObject_2_Null"

        self.assertEqual(result, result_expected)

    def test_Get_raise_DagNotFoundError(self):
        example_list = utilities.create_example_daglist()

        with self.assertRaises(dag.DagNotFoundError):
            example_list.Get("YouCanNotFindMe")

    def test_Insert(self):
        example_list = utilities.create_example_daglist()

        new_object = c4d.BaseList2D(c4d.Onull)
        new_object.SetName("NewItem_Null")

        example_list.Insert(0, dag.DagAtom(new_object))

        result = [x.GetName() for x in example_list]
        result_expected = ["NewItem_Null"] + [
            f"BaseObject_{x}_Null" for x in range(1, 11)
        ]

        self.assertListEqual(result, result_expected)

    def test_Extend(self):
        example_list = utilities.create_example_daglist()

        new_object = c4d.BaseList2D(c4d.Onull)
        new_object.SetName("NewItem_Null")

        new_list = dag.DagAtomList([dag.DagAtom(new_object)])

        example_list.Extend(new_list)

        result = example_list.Get("NewItem_Null").GetName()
        result_expected = "NewItem_Null"

        self.assertEqual(result, result_expected)

    def test_Append(self):
        example_list = utilities.create_example_daglist()

        new_object = c4d.BaseList2D(c4d.Onull)
        new_object.SetName("NewItem_Null")

        example_list.Append(dag.DagAtom(new_object))

        result = example_list.Get("NewItem_Null").GetName()
        result_expected = "NewItem_Null"

        self.assertEqual(result, result_expected)

    def test_CleanUp(self):
        example_list = utilities.create_example_daglist()

        example_list[0].Remove()

        # before clean up
        result_before_cleanup = [x.GetName() for x in example_list._items]
        result_before_cleanup_expected = [
            f"BaseObject_{x}_Null" for x in range(1, 11)
        ]

        self.assertListEqual(
            result_before_cleanup, result_before_cleanup_expected
        )

        example_list.CleanUp()

        # after clean up
        result_after_cleanup = [x.GetName() for x in example_list._items]
        result_after_cleanup_expected = [
            f"BaseObject_{x}_Null" for x in range(2, 11)
        ]

        self.assertListEqual(
            result_after_cleanup, result_after_cleanup_expected
        )


if __name__ == "__main__":
    unittest.main()
