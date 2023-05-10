from hepi.results import Result, add_errors, asym_to_sym_error


class NNLLFastResult(Result):
    """
    NNLL-fast Result Data.
    """

    def __init__(
        self,
        NLO,
        NLO_PDF_ERRMINUS,
        NLO_PDF_ERRPLUS,
        aNNLO_PLUS_NNLL,
        aNNLO_PLUS_NNLL_SCALE_ERRMINUS,
        aNNLO_PLUS_NNLL_SCALE_ERRPLUS,
        aNNLO_PLUS_NNLL_PDF_ERRMINUS,
        aNNLO_PLUS_NNLL_PDF_ERRPLUS,
    ):
        Result.__init__(self, None, NLO, None,aNNLO_PLUS_NNLL)
        self.NLO_NOERR= NLO
        self.NLO_PDF_ERRMINUS  =NLO_PDF_ERRMINUS
        self.NLO_PDF_ERRPLUS   =NLO_PDF_ERRPLUS
        self.NLO_PDF = asym_to_sym_error(NLO, NLO_PDF_ERRMINUS, NLO_PDF_ERRPLUS)

        self.aNNLO_PLUS_NNLL_NOERR = aNNLO_PLUS_NNLL

        self.aNNLO_PLUS_NNLL_SCALE_ERRMINUS=aNNLO_PLUS_NNLL_SCALE_ERRMINUS
        self.aNNLO_PLUS_NNLL_SCALE_ERRPLUS =aNNLO_PLUS_NNLL_SCALE_ERRPLUS
        self.aNNLO_PLUS_NNLL_SCALE        = asym_to_sym_error(aNNLO_PLUS_NNLL, aNNLO_PLUS_NNLL_SCALE_ERRMINUS, aNNLO_PLUS_NNLL_SCALE_ERRPLUS)

        self.aNNLO_PLUS_NNLL_PDF_ERRMINUS  =aNNLO_PLUS_NNLL_PDF_ERRMINUS
        self.aNNLO_PLUS_NNLL_PDF_ERRPLUS   =aNNLO_PLUS_NNLL_PDF_ERRPLUS
        self.aNNLO_PLUS_NNLL_PDF           = asym_to_sym_error(aNNLO_PLUS_NNLL, aNNLO_PLUS_NNLL_PDF_ERRMINUS, aNNLO_PLUS_NNLL_PDF_ERRPLUS)

        self.aNNLO_PLUS_NNLL_ERRMINUS = -add_errors(aNNLO_PLUS_NNLL_SCALE_ERRMINUS, aNNLO_PLUS_NNLL_PDF_ERRMINUS)
        self.aNNLO_PLUS_NNLL_ERRPLUS= add_errors(aNNLO_PLUS_NNLL_SCALE_ERRPLUS, aNNLO_PLUS_NNLL_PDF_ERRPLUS)
        self.aNNLO_PLUS_NNLL = asym_to_sym_error(aNNLO_PLUS_NNLL, self.aNNLO_PLUS_NNLL_ERRMINUS, self.aNNLO_PLUS_NNLL_ERRPLUS) 


