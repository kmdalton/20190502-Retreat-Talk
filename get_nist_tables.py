from urllib.request import urlopen
from bs4 import BeautifulSoup
from time import sleep
from io import StringIO
import pandas as pd


df = None

for Z in range(1, 93):
    try:
        url = "https://physics.nist.gov/PhysRefData/XrayMassCoef/ElemTab/z{:02d}.html".format(Z)
        text = urlopen(url).read()
        soup = BeautifulSoup(text, features='lxml')
        with open('mass_coeff/{:02d}.txt'.format(Z), 'w') as out:
            out.write(soup.pre.prettify())

        data = pd.read_csv(
            StringIO(
                ''.join([i for i in soup.pre.prettify().split('\n') if len(i.split()) == 3 and '>' not in i])
            ), 
            delim_whitespace=True, 
            names = ["Energy (MeV)", "mu/rho (cm2/g)", "mu_en/rho (cm2/g)"]
        )

        data['Z'] = Z
        df = pd.concat((df, data))
        #sleep(1) #be kind to NIST
    except:
        print(f"Failed at parsing z={Z}")

df.to_csv('mass_coefficients.csv')
