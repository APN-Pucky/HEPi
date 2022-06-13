from hepi.results import Result


class NLLFastResult(Result):
    """
    (N)NLL-fast Result Data.
    """

    def __init__(self, lo, nlo, nlo_plus_nll, scale_err_up, scale_err_down,
                 pdf_err_up, pdf_err_down):
        Result.__init__(self, lo, nlo, nlo_plus_nll)
        self.scale_err_up = scale_err_up
        self.scale_err_down = scale_err_down
        self.pdf_err_up = pdf_err_up
        self.pdf_err_down = pdf_err_down
