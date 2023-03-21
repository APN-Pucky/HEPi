import urllib.request
import hepi
#
dl = hepi.load(urllib.request.urlopen(
"https://raw.githubusercontent.com/APN-Pucky/xsec/master/json/pp13_SGmodel_GGxsec_NLO%2BNLL.json"
),dimensions=2)
hepi.mapplot(dl,"gl","sq","NLO_PLUS_NLL_COMBINED",xaxis="$m_{\\tilde{g}}$ [GeV]",yaxis="$m_{\\tilde{q}}$ [GeV]" , zaxis="$\\sigma_{\\mathrm{NLO+NLL}}$ [pb]")
