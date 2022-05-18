import urllib.request
import hepi
dl = hepi.load(urllib.request.urlopen(
"https://raw.githubusercontent.com/fuenfundachtzig/xsec/master/json/pp13_hinosplit_N2N1_NLO%2BNLL.json"
),dimensions=2)
hepi.mapplot(dl,"N1","N2","NLO_PLUS_NLL",xaxis="$m_{\\tilde{\\chi}_1^0}$",yaxis="$m_{\\tilde{\\chi}_2^0}$" , zaxis="$\\sigma_{\\mathrm{NLO+NLL}}$")
