import unittest

from aiot_core import CommandStabilizer, command_for_prediction


class CommandLogicTests(unittest.TestCase):
    def test_only_confident_mapped_class_turns_relay_on(self):
        mapping = {"freshapples": "1"}
        self.assertEqual(command_for_prediction("freshapples", 0.60, 0.60, mapping), "1")
        self.assertEqual(command_for_prediction("freshapples", 0.59, 0.60, mapping), "0")
        self.assertEqual(command_for_prediction("unknown", 0.99, 0.60, mapping), "0")

    def test_stabilizer_emits_only_stable_state_changes(self):
        filter_ = CommandStabilizer(min_consecutive_frames=3)
        self.assertEqual([filter_.update("1") for _ in range(3)], [None, None, "1"])
        self.assertEqual([filter_.update("1") for _ in range(4)], [None] * 4)
        self.assertEqual([filter_.update("0") for _ in range(3)], [None, None, "0"])

    def test_stabilizer_rejects_invalid_configuration(self):
        with self.assertRaises(ValueError):
            CommandStabilizer(min_consecutive_frames=0)


if __name__ == "__main__":
    unittest.main()
