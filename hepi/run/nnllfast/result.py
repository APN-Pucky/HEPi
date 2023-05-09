from hepi.results import Result


class NNLLFastResult(Result):
    """
    NNLL-fast Result Data.
    """

    def __init__(
        self,
        NLO,
        aNNLO_PLUS_NNLL,
        aNNLO_PLUS_NNLL_SCALE_ERRMINUS,
        aNNLO_PLUS_NNLL_SCALE_ERRPLUS,
        aNNLO_PLUS_NNLL_PDF_ERRMINUS,
        aNNLO_PLUS_NNLL_PDF_ERRPLUS,
    ):
        Result.__init__(self, None, NLO, None,aNNLO_PLUS_NNLL)
        self.aNNLO_PLUS_NNLL_SCALE_ERRMINUS=aNNLO_PLUS_NNLL_SCALE_ERRMINUS
        self.aNNLO_PLUS_NNLL_SCALE_ERRPLUS =aNNLO_PLUS_NNLL_SCALE_ERRPLUS
        self.aNNLO_PLUS_NNLL_PDF_ERRMINUS  =aNNLO_PLUS_NNLL_PDF_ERRMINUS
        self.aNNLO_PLUS_NNLL_PDF_ERRPLUS   =aNNLO_PLUS_NNLL_PDF_ERRPLUS
