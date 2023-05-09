from hepi.results import Result


class NLLFastResult(Result):
    """
    (N)NLL-fast Result Data.
    """

    def __init__(
        self,
        LO,
        NLO,
        NLO_PLUS_NLL,
        NLO_PLUS_NLL_SCALE_ERRMINUS,
        NLO_PLUS_NLL_SCALE_ERRPLUS,
        NLO_PLUS_NLL_PDF_ERRMINUS,
        NLO_PLUS_NLL_PDF_ERRPLUS,
    ):
        Result.__init__(self, LO, NLO, NLO_PLUS_NLL)
        self.NLO_PLUS_NLL_SCALE_ERRMINUS=NLO_PLUS_NLL_SCALE_ERRMINUS
        self.NLO_PLUS_NLL_SCALE_ERRPLUS=NLO_PLUS_NLL_SCALE_ERRPLUS
        self.NLO_PLUS_NLL_PDF_ERRMINUS=NLO_PLUS_NLL_PDF_ERRMINUS
        self.NLO_PLUS_NLL_PDF_ERRPLUS=NLO_PLUS_NLL_PDF_ERRPLUS
