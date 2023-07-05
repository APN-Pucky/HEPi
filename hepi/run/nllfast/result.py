from hepi.results import Result, add_errors, asym_to_sym_error


class NLLFastResult(Result):
    """
    (N)NLL-fast Result Data.
    """

    def __init__(
        self,
        LO,
        NLO,
        NLO_PDF_ERRMINUS,
        NLO_PDF_ERRPLUS,
        NLO_PLUS_NLL,
        NLO_PLUS_NLL_SCALE_ERRMINUS,
        NLO_PLUS_NLL_SCALE_ERRPLUS,
        NLO_PLUS_NLL_PDF_ERRMINUS,
        NLO_PLUS_NLL_PDF_ERRPLUS,
    ):
        Result.__init__(self, LO, NLO, NLO_PLUS_NLL)
        self.LO_NOERR= LO
        self.NLO_NOERR= NLO
        self.NLO_PDF_ERRMINUS=NLO_PDF_ERRMINUS
        self.NLO_PDF_ERRPLUS =NLO_PDF_ERRPLUS
        self.NLO_PDF = asym_to_sym_error(NLO, NLO_PDF_ERRMINUS, NLO_PDF_ERRPLUS)

        self.NLO_PLUS_NLL_NOERR = NLO_PLUS_NLL

        self.NLO_PLUS_NLL_SCALE_ERRMINUS=NLO_PLUS_NLL_SCALE_ERRMINUS
        self.NLO_PLUS_NLL_SCALE_ERRPLUS=NLO_PLUS_NLL_SCALE_ERRPLUS
        self.NLO_PLUS_NLL_SCALE=asym_to_sym_error(NLO_PLUS_NLL, NLO_PLUS_NLL_SCALE_ERRMINUS, NLO_PLUS_NLL_SCALE_ERRPLUS)

        self.NLO_PLUS_NLL_PDF_ERRMINUS=NLO_PLUS_NLL_PDF_ERRMINUS
        self.NLO_PLUS_NLL_PDF_ERRPLUS=NLO_PLUS_NLL_PDF_ERRPLUS
        self.NLO_PLUS_NLL_PDF=asym_to_sym_error(NLO_PLUS_NLL, NLO_PLUS_NLL_PDF_ERRMINUS, NLO_PLUS_NLL_PDF_ERRPLUS)

        self.NLO_PLUS_NLL_ERRMINUS=-add_errors(NLO_PLUS_NLL_PDF_ERRMINUS, NLO_PLUS_NLL_SCALE_ERRMINUS)
        self.NLO_PLUS_NLL_ERRPLUS=add_errors(NLO_PLUS_NLL_PDF_ERRPLUS, NLO_PLUS_NLL_SCALE_ERRPLUS)
        self.NLO_PLUS_NLL = asym_to_sym_error(NLO_PLUS_NLL, self.NLO_PLUS_NLL_ERRMINUS, self.NLO_PLUS_NLL_ERRPLUS)


