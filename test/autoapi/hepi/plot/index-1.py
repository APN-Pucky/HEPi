import urllib.request
import hepi
dl = hepi.load(urllib.request.urlopen(
"https://raw.githubusercontent.com/fuenfundachtzig/xsec/master/json/pp13_hino_NLO%2BNLL.json"
))
hepi.plot(dl,"N1","NLO_PLUS_NLL",xaxis="$m_{\\tilde{\\chi}_1^0}$ [GeV]")
