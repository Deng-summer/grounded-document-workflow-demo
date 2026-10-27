import unittest

from workflow import preview_draft, retrieve, split_document


class WorkflowTest(unittest.TestCase):
    def test_retrieval_prefers_relevant_passage(self):
        passages = split_document("sample", "Appointments can be rescheduled online.\n\nInvoices are payable within 30 days.")
        result = retrieve("When is an invoice payable?", passages)
        self.assertEqual(result[0].citation, "sample#p2")

    def test_preview_cites_only_retrieved_evidence(self):
        passages = split_document("sample", "The technician confirms the appointment.")
        result = preview_draft("Who confirms the appointment?", passages)
        self.assertEqual(result["citations"], ["sample#p1"])
        self.assertEqual(result["mode"], "preview")

    def test_no_match_does_not_invent_answer(self):
        passages = split_document("sample", "The technician confirms the appointment.")
        self.assertEqual(retrieve("insurance premium", passages), [])


if __name__ == "__main__":
    unittest.main()
