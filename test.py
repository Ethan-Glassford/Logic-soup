
import os

from run import example_theory

def test_theory():
    T = example_theory()

    assert len(T.vars()) > 10, "Only %d variables -- your theory is likely not sophisticated enough for the course project." % len(T.vars())
    assert T.size() > 50, "Only %d in the formula -- your theory is likely not sophisticated enough for the course project." % T.size()
    assert not T.valid(), "Theory is valid (every assignment is a solution). Something is likely wrong with the constraints."
    assert not T.negate().valid(), "Theory is inconsistent (no solutions exist). Something is likely wrong with the constraints."

def file_checks(stage):
    proofs_jp = os.path.isfile(os.path.join('.','documents',stage,'proofs.jp'))
    modelling_report_docx = os.path.isfile(os.path.join('.','documents',stage,'modelling_report.docx'))
    modelling_report_pptx = os.path.isfile(os.path.join('.','documents',stage,'modelling_report.pptx'))
    report_txt = os.path.isfile(os.path.join('.','documents',stage,'report.txt'))
    report_pdf = os.path.isfile(os.path.join('.','documents',stage,'report.pdf'))

    assert proofs_jp, "Missing proofs.jp in your %s folder." % stage
    assert modelling_report_docx or modelling_report_pptx or (report_txt and report_pdf), \
            "Missing your report (Word, PowerPoint, or OverLeaf) in your %s folder" % stage

def test_draft_files():
    file_checks('draft')

def test_final_files():
    file_checks('final')
