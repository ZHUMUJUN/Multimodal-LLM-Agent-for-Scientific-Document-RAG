# 10_natural_night_sky_brightness_gaia_arxiv

## Page 1

MNRAS 000, 1–15 (2020)
Preprint 6 January 2021
Compiled using MNRAS LATEX style ﬁle v3.0
A multi-band map of the natural night sky brightness including Gaia
and Hipparcos integrated starlight
Eduard Masana,1★Josep Manel Carrasco,1 Salvador Bará,2 and Salvador J. Ribas3,1
1Departament Física Quàntica i Astrofìsica. Institut de Ciències del Cosmos (ICC-UB-IEEC), C Martí Franquès 1, Barcelona 08028, Spain
2Departmento Física Aplicada, Universidade de Santiago de Compostela, 15782 Santiago de Compostela, Galicia, Spain
3Parc Astronòmic Montsec - Ferrocarrils de la Generalitat de Catalunya. Camí del Coll d’Ares, s/n, Àger (Lleida) 25691, Spain
Accepted XXX. Received YYY; in original form ZZZ
ABSTRACT
The natural night sky brightness is a relevant input for monitoring the light pollution
evolution at observatory sites, by subtracting it from the overall sky brightness determined
by direct measurements. It is also instrumental for assessing the expected darkness of the
pristine night skies. The natural brightness of the night sky is determined by the sum of
the spectral radiances coming from astrophysical sources, including zodiacal light, and the
atmospheric airglow. The resulting radiance is modiﬁed by absorption and scattering before it
reaches the observer. Therefore, the natural night sky brightness is a function of the location,
time and atmospheric conditions. We present in this work GAMBONS (GAia Map of the
Brightness Of the Natural Sky), a model to map the natural night brightness of the sky in
cloudless and moonless nights. Unlike previous maps, GAMBONS is based on the extra-
atmospheric star radiance obtained from the Gaia catalogue. The Gaia-DR2 archive compiles
astrometric andphotometric information formore than1.6 billion starsup to𝐺= 21 magnitude.
For the brightest stars, not included in Gaia-DR2, we have used the Hipparcos catalogue
instead. After adding up to the star radiance the contributions of the diﬀuse galactic and
extragalactic light, zodiacal light and airglow, and taking into account the eﬀects of atmospheric
attenuation and scattering, the radiance detected by ground-based observers can be estimated.
This methodology can be applied to any photometric band, if appropriate transformations
from the Gaia bands are available. In particular, we present the expected sky brightness for
𝑉(Johnson), and visual photopic and scotopic passbands.
Key words: light pollution - scattering - radiative transfer - atmospheric eﬀects - instrumen-
tation: photometers - site testing
1
INTRODUCTION
The natural brightness of the night sky in diﬀerent photometric
passbands is a relevant parameter for site characterization and light
pollution research, since it allows establishing a baseline against
which to evaluate the light pollution levels experienced in urban,
periurban, rural and pristine dark sites.
Brightness, in this context, is a shortcut name for the spectral
radiance of the sky, weighted by the sensitivity function of the
photometric band, spectrally integrated over all wavelengths, and
angularly integrated within the ﬁeld-of-view of the detector.
The measurement of the night sky brightness and the atmo-
spheric conditions, in particular at sites of astronomical interest, has
a long history that continues to the present day (for example Turn-
rose (1974) for Palomar and Mount Wilson Observatories; Benn &
★E-mail: emasana@fqa.ub.edu (EM)
Ellison (1998) for La Palma; or Patat (2008) for Cerro Paranal). The
natural sources of the night sky brightness were already outlined
in Roach & Gordon (1973). The reference paper by Leinert et al.
(1998) studies and analyzes the diﬀerent sources contributing to the
sky brightness covering wavelengths from 𝜆≈100 nm (ultraviolet
domain) to 𝜆≈200 𝜇m (far infrared). It includes airglow, zodiacal
light, integrated star light, diﬀuse galactic light and extragalactic
background light, and summarizes the best estimations at the time
for all of them. A similar work can be found in Noll et al. (2012)
for the wavelength range from 𝜆≈300 to 𝜆≈920 nm, with an
extended discussion on the airglow and atmospheric extinction at
Cerro Paranal. Duriscoe (2013) evaluates the artiﬁcial contribution
to the sky brightness by subtracting the natural contributions from
the overall sky radiance measured with all-sky imaging systems.
Duriscoe (2013) used a model of integrated starlight (including dif-
fuse galactic light) constructed from images made with the same
© 2020 The Authors
arXiv:2101.01500v1  [astro-ph.IM]  5 Jan 2021

## Page 2

2
E. Masana et al.
equipment used for sky brightness observations, and modeling zo-
diacal light and airglow from previously available data.
In parallel, several models to compute the artiﬁcial light con-
tribution to the overall night sky brightness have been developed,
from the early works by Treanor (1973), Berry (1976) and Garstang
(1986, 1989, 1991), to the more recent by Cinzano & Falchi (2012),
Kocifaj (2007, 2018) and Aubé et al. (2005, 2018). The outcome
of these models are maps of the artiﬁcial brightness of the night
sky (for instance Cinzano et al. (2001) and Falchi et al. (2016)) to
which the natural brightness shall be added in order to obtain the
total one, which is the physical observable available from direct
measurements.
The publication of the Gaia-DR2 archive (Gaia Collaboration
et al. 2018), with high quality space-based global astrometric and
photometric information for more than 1.6 billion stars in all the sky
up to 𝐺= 21 mag (being 𝐺the white light magnitude observed with
Gaia in the astrometric instrument), oﬀers a unique opportunity to
improve the computation of the integrated star light, by directly
integrating the contributions of all the stars in the Gaia catalogue.
As a ﬁrst result, we present in this work the ﬁrst maps of the extra-
atmospheric brightness of the night sky in the 𝑉(Johnson) and the
human vision photopic and scotopic bands, directly obtained from
the Gaia and Hipparcos (ESA 1997; van Leeuwen 2007) catalogues.
Hipparcos is used here to extend Gaia catalogue to the bright end,
not included in Gaia-DR2. The inclusion of the remaining relevant
sources, including zodiacal light and airglow, and the corrections
due to attenuation and scattering into the ﬁeld of view, allows to
compute the radiance at ground-level at any direction of the sky and
any location and night time for the observer. This methodology can
be applied to any photometric band, if appropriate transformations
from the native Gaia bands are computed. In particular, we have
determined the sky brightness for the Johnson 𝑉and human-vision
photopic and scotopic passbands. All together constitutes the ﬁrst
version of GAMBONS model of the natural night sky brightness.
The novelty of this work is the determination of the radiance
outside the Earth’s atmosphere using Gaia and Hipparcos cata-
logues. However, a complete sky brightness model requires the
modeling of the other components, as zodiacal light, airglow or
atmospheric attenuation and scattering. We have implemented in
GAMBONS the more updated and reliable models available in the
literature for those components, as described in the next sections,
but it is not the scope of this work to discuss in detail each one of
them. On the other hand, the ﬁnal map of the night sky brightness is
highly dependent on the atmospheric conditions, including airglow.
Thus, the accuracy of the results depends on the reliability of the
atmospheric parameters used in the computation.
The Gaia and Hipparcos catalogues are over-viewed in Sec-
tion 2. Their photometric systems, as well as the other photometric
bands used in this work are described in Section 3. Section 3 also
deals with the problem of deriving the needed transformations be-
tween diﬀerent photometric bands. Section 4 describes the general
characteristics of our model. Sections 5 to 7 explain in detail the
computation of the diﬀerent sources of the natural night sky bright-
ness and the models for atmospheric attenuation and scattering.
Finally, we expose some applications of the model in Section 8.
2
THE GAIA AND HIPPARCOS CATALOGUES
Gaia (Gaia Collaboration et al. 2016) is an extremely ambitious
astrometric space mission of the scientiﬁc programme of the Euro-
pean Space Agency (ESA). Gaia measures, with very high accuracy,
the positions, motions and parallaxes of a large number of stars and
many other kinds of objects as galaxies, asteroids and quasars.
Consequently, a detailed three-dimensional map of more than
1.6 billion stars of our Galaxy (approximately 1% of the stars popu-
lating the Milky Way) is obtained. This map also includes, for almost
all the objects, information about their brightness and colour, as well
as radial velocity, and several astrophysical parameters for a large
fraction of them.
Gaia-DR2 photometry in 𝐺band is almost complete up to
𝐺≈20 mag, with a limiting magnitude slightly fainter than
𝐺= 21 mag in some areas of the sky. Gaia extends to the faint
the catalogue obtained by the Hipparcos ESA mission, launched
in 1989. Hipparcos catalogue includes information about the po-
sition, motion, brightness and colour of the sources. Although the
Gaia catalogue is several orders of magnitude more complete and
precise than Hipparcos catalogue, Gaia cannot observe very bright
objects (with 𝐺< 5 mag). For those stars, the Hipparcos catalogue
addresses the lack of Gaia data. In particular, of the 118,218 stars
in the Hipparcos catalogue (ESA 1997), 83,034 are present in the
Gaia-DR2 - Hipparcos best neighbour catalogue available on the
Gaia archive, and has therefore, Gaia data available. The details of
the Gaia-DR2 - Hipparcos cross match are given in Marrese et al.
(2019). For the 35,000 remaining stars not having Gaia information
we have used photometry from the Hipparcos catalogue. In terms of
ﬂux, the Hipparcos stars account for around 20 per cent of the total
integrated star light. After these considerations, our ﬁnal catalogue
contains 1,692,953,899 stars.
3
THE PHOTOMETRIC DATA
3.1
The Gaia photometric system
The Gaia broad band photometric system is fully described in
Jordi et al. (2010). It is composed by three diﬀerent passbands
(𝐺, 𝐺BP and 𝐺RP ). The transmission curves represented in Fig. 1
were derived by Maiz Apellaniz & Weiler (2018), as the most rep-
resentative of the Gaia-DR2 data according to the Gaia team1. 𝐺is
a panchromatic band covering the wavelength range from about 350
to 1000 nm. It is the result of the transmission of the mirrors and
the response of the instruments in Gaia. 𝐺BP (blue photometer)
and 𝐺RP (red photometer) are two broad passbands in the wave-
length ranges 330–680 nm and 640–1000 nm, respectively. The
corresponding magnitudes are obtained from the integrated ﬂux of
the low-resolution spectra of the Gaia spectrophotometer. These
photometric data allow the classiﬁcation of the sources by deriving
the astrophysical parameters, such as eﬀective temperature, grav-
ity, chemical composition and interstellar absorption. An additional
description of the photometric contents of Gaia-DR2, including
uncertainty distribution, external comparisons and colour transfor-
mations, can be found in Evans et al. (2018).
A small systematic inconsistency in the BP photometric system
was spotted by Maiz Apellaniz & Weiler (2018); Weiler (2018),
likely caused by insuﬃcient convergence of the 𝐺BP calibration
in Gaia-DR2 for bright sources. Maiz Apellaniz & Weiler (2018)
propose to mitigate this eﬀect by using two diﬀerent 𝐺BP response
curves (𝐺𝑏
BP and 𝐺𝑓
BP ) for the magnitude ranges brighter and fainter
than 𝐺= 10.87 mag, respectively.
1 https://www.cosmos.esa.int/web/gaia/dr2-known-issues
MNRAS 000, 1–15 (2020)

## Page 3

Map of the natural sky brightness
3
Figure 1. Gaia passbands transmission used in this work (Maiz Apellaniz
& Weiler 2018).
Figure 2. 𝑉Johnson (Bessell & Murphy 2012), Hipparcos (𝐻p) (Weiler
et al. 2018), 𝑉’ scotopic (CIE 1951) and 𝑉photopic (CIE 1990) passbands
transmission used in this work.
3.2
Photometry from Hipparcos catalogue
Hipparcos catalogue provides photometric magnitudes in several
passbands. Three of them, 𝐻p, 𝐵T and 𝑉T, are the three native
Hipparcos–Tycho bands. Furthermore, the catalogue compiles ex-
ternal values of the 𝑉Johnson magnitude and (𝐵−𝑉) and (𝑉−𝐼)
colours in the Johnson-Cousins system (Johnson 1963).
In this work we use 𝑉and 𝐻p magnitudes and (𝐵−𝑉) and
(𝑉−𝐼) colours to transform to other passbands, as described in
Section 3.4. The passband transmissions used here for 𝑉(Bessell
& Murphy 2012) and 𝐻p (Weiler et al. 2018) are shown in Fig. 2.
In the case of the V band, the photonic response function deﬁned
in Bessell & Murphy (2012) was transformed back to its original
energy response form, since the classical 𝑉magnitude system is
deﬁned in terms of in-band irradiances, not photon numbers.
3.3
Scotopic and photopic visual passbands
The scotopic 𝑉′(𝜆) and photopic 𝑉(𝜆) spectral responses (Fig. 2)
describe the response of the human eye fully adapted to low (<
0.005 cd m−2) and high (> 5 cd m−2) environmental luminances,
respectively. These photometric bands have been standardized by
CIE (1951, 1990). The luminance of a radiance ﬁeld seen with
photopic adaptation, in cd m−2, is obtained by multiplying the in-
tegrated radiance within the 𝑉(𝜆) band (in W m−2 sr−1) by the
photopic luminous eﬃcacy factor 𝐾m = 683 lm W−1. Similarly,
the luminance of a radiance ﬁeld seen under scotopic adaptation is
given by the radiance in the 𝑉′(𝜆) band multiplied by the scotopic
luminous eﬃcacy factor 𝐾′m = 1700 lm W−1. Mesopic sensitivity
bands can also be deﬁned for intermediate adaptation states (0.005
to 5 cd m−2) (CIE 2010). The luminance is the basic physical quan-
tity at the root of the human perception of brightness. Note that the
’visible’ 𝑉Johnson band does not provide an accurate estimation of
the visual brightness of the sky: skies with the same brightness in
𝑉Johnson may correspond to very diﬀerent luminances, depending
on the spectral composition of the sky radiance (Bará et al. 2020),
and, of course, on the adaptation state of the observer.
3.4
Transformations between passbands
The purpose of this work is to obtain the maps of the natural night
sky radiance in any photometric band, assuming that its spectral re-
sponse is known. The input data available from Gaia and Hipparcos
catalogues are not sky radiances (W m−2sr−1), but the 𝐺, 𝐺BP, 𝐺RP,
𝑉magnitudes and the (𝐵−𝑉) and (𝑉−𝐼) colours of the individual
stars. Therefore, we need to transform from these star magnitudes
and colours in their native bands to the corresponding sky radiance
in the desired target band. Let us recall that astronomical magni-
tudes are a logarithmic measure of the in-band irradiances (W m−2)
at the entrance pupil of the observing instrument. The canonical
transformation procedure consists then of three main steps: (i) in
the ﬁrst one, the catalogue magnitudes are used to compute the irra-
diances produced by each individual star in the original bands, (ii)
the star irradiances in the original bands are used to estimate the
star irradiances within the target observation band, and ﬁnally (iii)
the radiance 𝐿of any patch of the sky in the target band is given by
the sum of the irradiances contributed by all stars contained within
that patch, divided by the solid angle (in steradian) it subtends (Bará
et al. 2020). This radiance is usually called surface brightness in
the astrophysical literature.
In practice these steps can be performed in diﬀerent ways, and
in some cases they can be grouped into a single transformation. The
details depend on the available data. Note, for instance, that 𝑉John-
son is included in the Hipparcos catalogue but not in Gaia-DR2. So,
we need to transform the Gaia data from 𝐺to 𝑉. Furthermore, the
input provided by the Gaia-DR2 catalogue is given also in photons
per second within the instrument entrance pupil, which is a scaled
version of the actual in-band photon irradiance (photons s−1 m−2)
and hence of the irradiance (W m−2), being the details of this last
transformation contingent on the stars’ spectra.
In general, a transformation between two passbands (𝐴and 𝐵)
is a function of, at least, one colour. For many cases, a polynomial
expression with only one colour 𝐶, derived by subtracting the mag-
nitude in two diﬀerent passbands, is enough to obtain a good ﬁt
between 𝐴and 𝐵, in the form:
𝐴= 𝐵+
∑︁
𝑖
𝑎𝑖𝐶𝑖
(1)
Taking into account the relation 𝐴= 𝐴0 −2.5 log(𝐸A/𝐸0),
between the magnitude 𝐴and the corresponding irradiance 𝐸A,
MNRAS 000, 1–15 (2020)

## Page 4

4
E. Masana et al.
with 𝐴0 the zero point magnitude for the 𝐸0 irradiance, we can get
a relation for the ratio 𝐸A/𝐸B from equation 1:
𝐸A
𝐸B
= 𝑒
Í
𝑖𝑎𝑖𝐶𝑖
(2)
The 𝐴0 and 𝐵0 constants, as well as the conversion from com-
mon to natural logarithm are included in the 𝑒𝑎0 term.
For instance, the transformation between 𝐺and 𝑉can be ex-
pressed as function of the colour (𝐺BP -𝐺RP):
𝐸V = 𝐸G 𝑒
Í
𝑖𝑎𝑖(𝐺BP−𝐺RP)𝑖
(3)
The methodology to get the coeﬃcients 𝑎𝑖of the transforma-
tions is the same as in Jordi et al. (2010). First, the set of stellar
spectra in BaSeL-3.1 models (Westera et al. 2002) is used to com-
pute the synthetic photometry in all the bands. BaSeL-3.1 covers
a wide range of eﬀective temperature, surface gravity and stellar
metallicity including all possible evolutionary stages in the stellar
evolution. We also incorporate the eﬀect of interstellar reddening
by using a wide range of possible absorption rates (from 0 to 11
magnitudes at 550 nm) of the Gaiaand Hipparcos stars. Following
Jordi et al. (2010), a value equal to 0.03 mag has been assumed for
each synthetic magnitude of a Vega-like star. The synthetic pho-
tometry was simulated in both photons per second within the Gaia
input pupil and in W m−2, allowing the transformation of units to
be included in the ﬁt (for instance from the radiant ﬂux 𝐹G in pho-
tons per second within the Gaia input pupil to the corresponding
irradiance 𝐸V in W m−2; or from the irradiance 𝐸V to the scotopic
irradiance 𝐸Sco, both in W m−2). Finally, a minimum least squares
ﬁt is applied to get the 𝑎𝑖coeﬃcients in equation 2.
The conversion from the catalogue astronomical magnitude 𝑚
of each star to the irradiance it produces, 𝐸(W m−2), is made using
the standard deﬁnition of magnitudes,
𝐸= 𝐸r 10−0.4 𝑚
(4)
where 𝐸r is the reference irradiance associated with the ’zero-point’
of the band (𝑉or 𝐻p for Hipparcos stars), that is, the irradiance
corresponding to 𝑚= 0.0 mag, given by the integral:
𝐸r =
∫∞
0
𝑆(𝜆) 𝐸Vega(𝜆) 𝑑𝜆
(5)
where 𝐸Vega(𝜆) is the STIS003 spectral irradiance of Vega from
Bohlin & Gilliland (2004), normalized in such a way that 𝑚Vega =
0.03 mag for all the bands, and 𝑆(𝜆) is the photometric passband.
As pointed out above, the radiance 𝐿of any region of the sky
is computed as the sum of the irradiances produced by all sources
contained in that region, divided by the region’s angular extent in
steradians. This radiance can be expressed in the logarithmic scale
of magnitudes per square arcsecond within the 𝑆(𝜆) band, 𝑚S,
according to the deﬁnition:
𝐿= 𝐿r 10−0.4 𝑚S
(6)
where 𝐿r is the reference radiance given by
𝐿r = 1
𝐾
∫∞
0
𝑆(𝜆) 𝐸Vega(𝜆) 𝑑𝜆
(7)
being K=2.3504 10−11 the steradian equivalent of 1 square arcsec-
ond. The values of 𝐿r for several bands used in this work are given
in Table 2.
Figure 3. Relationship between the irradiances at diﬀerent bands used in
this work obtained using BaSeL-3.1 spectral library (Westera et al. 2002).
The colour code represents the interstellar absorption (vertical scale). The
black line is the ﬁt of equation 2 with the coeﬃcients in Table 1.
In principle, this transformation methodology can be applied
to any band, taking care to choose the colour that minimizes the
residuals of the ﬁt. For Gaia passbands this colour is (𝐺BP - GRP),
while for 𝑉, 𝐻p and human-vision bands we choose (𝑉−𝐼) or
(𝐵−𝑉), depending on the transformation. The relationships between
the diﬀerent bands used in this work are shown in Fig. 3. The 𝑎𝑖
coeﬃcients, the colours 𝐶and the 𝜎of the ﬁts for all of them are
summarized in Table 1.
4
THE MODEL
We describe in this section the general expression for the in-band
integrated radiance, 𝐿obs(𝜶, ℎ), detected by an observer in the di-
rection 𝜶= (𝑎, 𝑧) (𝑎the azimuth and 𝑧the zenith angle) relative
to its reference frame, at height ℎabove sea level. 𝐿obs(𝜶, ℎ) must
take into account all the sources contributing to the natural night sky
brightness: the integrated star light (ISL), the diﬀuse galactic light
(DGL), the extragalactic background light (EBL) and the zodiacal
light, that conform the radiance outside the Earth’s atmosphere; and
the atmospheric airglow. This extra-atmospheric radiance 𝐿0(𝜆, 𝜶)
MNRAS 000, 1–15 (2020)

## Page 5

Map of the natural sky brightness
5
Table 1. Coeﬃcients and mean standard deviations of the transformations between irradiances in diﬀerent bands, according to equation 2. 𝐸′ denotes irradiances
in photon s−1 m−2, whereas 𝐸denotes irradiance in W m−2. For the transformations from Gaia photometry, the last column shows the standard deviation for
the range (𝐺BP -𝐺RP )< 3 mag, where the most of the Gaia-DR2 stars are.
C
𝑎0
𝑎1
𝑎2
𝑎3
𝑎4
𝑎5
𝜎all(%)
𝜎Gaia(%)
𝐸G/𝐸′
G
𝐺𝑓
BP -𝐺RP
-42.474
-0.1168
-0.006034
+0.005261
-6.496 10−4
+2.521 10−5
0.5
0.4
𝐸V/𝐸′
G
𝐺𝑓
BP -𝐺RP
-43.878
+0.028640
-0.20573
+0.017942
-5.444 10−4
5.1
2.4
𝐸Sco/𝐸′
G
𝐺𝑓
BP -𝐺RP
-43.551
-0.201
-0.2284
+0.02308
-8.216 10−4
12.5
6.0
𝐸Phot/𝐸′
G
𝐺𝑓
BP -𝐺RP
-43.749
+0.04745
-0.1972
+0.01678
-5.03 10−4
3.8
2.2
𝐸G/𝐸V
(𝑉−𝐼)
1.4221
-0.14355
+ 0.22442
-0.020977
+7.827 10−4
4.3
𝐸Sco/𝐸V
(𝐵−𝑉)
0.31760
-0.34836
-0.017739
+ 0.0046171
-4.0399 10−4
5.1
𝐸Phot/𝐸Hp
(𝑉−𝐼)
-1.0155
+0.39292
-0.12037
+0.0077708
-3.2423 10−4
2.7
Table 2. Reference radiances 𝐿r based on STIS003 spectrum and 𝐺= 𝑉=
𝐻p = 0.03 mag for Vega.
Passband
𝐿r
(W m−2 sr−1)
𝐺
562.5373
𝑉
143.1685
𝐻p
426.8769
(formally including airglow) contributes to the overall map of the
sky as seen by the observer as follows:
• it produces a direct (attenuated) radiance 𝐿d(𝜆, 𝜶, ℎ)
=
𝐿0(𝜆, 𝜶) 𝑇(𝜆, 𝑧, ℎ) in the direction of observation 𝜶.
• it introduces a scattered radiance 𝐿s(𝜆, 𝜶s, 𝜶, ℎ) in the remain-
ing pixels of the sky, including the pixel 𝜶= 𝜶s itself.
𝑇(𝜆, 𝑧, ℎ) is the eﬀective atmospheric transmittance at wave-
length𝜆, accounting for the radiance reduction due to the attenuation
along the beam path from the limits of the atmosphere to the location
of the observer.
If we denote 𝐿s(𝜆, 𝜶, ℎ) as the total scattered radiance reaching
the observer when looking at the direction 𝜶:
𝐿obs(𝜆, 𝜶, ℎ) = 𝐿d(𝜆, 𝜶, ℎ) + 𝐿s(𝜆, 𝜶, ℎ)
(8)
𝐿obs(𝜶, ℎ) =
∫∞
0
𝑆(𝜆) 𝐿obs(𝜆, 𝜶, ℎ) 𝑑𝜆
(9)
The eﬀects of the atmospheric transmittance and scattering,
i.e. the computation of 𝑇(𝜆, 𝑧, ℎ) and 𝐿s(𝜆, 𝜶, ℎ), are described in
detail in Section 7.
𝐿obs(𝜆, 𝜶, ℎ) can be expressed as the sum of the radi-
ance coming from diﬀerent contributors: 𝐿obs,ISL(𝜆, 𝜶, ℎ) (in-
tegrated starlight);
𝐿obs,DGL(𝜆, 𝜶, ℎ)
(diﬀuse galactic light);
𝐿obs,EBL(𝜆, 𝜶, ℎ) (extragalactic background light); 𝐿obs,zl(𝜆, 𝜶, ℎ)
(zodiacal light); and 𝐿obs,ag(𝜆, 𝜶, ℎ) (airglow):
𝐿obs(𝜶, ℎ)
=
∑︁
∀P
 ∫∞
0
𝑆(𝜆) 𝐿obs,P (𝜆, 𝜶, ℎ) 𝑑𝜆

=
=
𝐿obs,ISL(𝜶, ℎ) + 𝐿obs,DGL(𝜶, ℎ) +
+
𝐿obs,EBL(𝜶, ℎ) + 𝐿obs,zl(𝜶, ℎ) + 𝐿obs,ag(𝜶, ℎ)
(10)
In the next sections we will ﬁrst describe in detail the compu-
tation of the extra-atmospheric radiance for each component, and
thereafter the eﬀect of the atmospheric attenuation and scattering.
Note that the diﬀerent components of the radiance are usually
given in diﬀerent coordinate systems: equatorial (𝛼, 𝛿) or galactic
(𝑙, 𝑏) coordinates for the astrophysical component; ecliptic (Λ, 𝛽)
for the zodiacal light; and horizontal (𝑎, ˆℎ) coordinates for the air-
glow and atmospheric attenuation, being ˆℎthe angular height above
the horizon. Horizontal coordinates are linked to the local reference
frame of the observer and therefore the horizontal coordinates of any
extra-terrestrial source depend on the observer position and time.
Moreover, both the airglow 𝐿ag and the atmospheric transmittance
𝑇depend only of the zenith angle 𝑧= 90 −ˆℎ. For the details about
coordinate transformation see for instance Green (1985).
5
RADIANCE OUTSIDE THE EARTH ATMOSPHERE
5.1
Integrated starlight
In the visual wavelength range, the integrated starlight (ISL) is one
of the most important contributors to the natural sky brightness.
In some circumstances, as for lines of sight towards the Galactic
Centre far from the Sun and for low solar activity, ISL can be
the brightest component. Early works on the night sky brightness
used simple models of the Galaxy to determine the ISL. Bahcall
& Soneira (1980) constructed a model with the Galaxy consisting
of an exponential disk and a power-law, spheroidal bulge, that was
widely used in the last years of the last century.
Other early approach to the problem of the ISL was to use
data from imaging photopolarimeters (IPP's) on the Pioneer 10 and
11 deep space probes (Weinberg et al. 1974). The full set of data
contains stars and background integrated light for almost all the sky
with a spatial resolution around 2◦in two bands, blue and red.
From the early 2000s, the determination of the ISL takes ad-
vantage of the emergence of large surveys, as Tycho-2, USNO-A2 or
2MASS (see for instance Melchior et al. 2007). Following this line,
the publication of Gaia-DR2 oﬀers a new opportunity to determine
the ISL from the most complete photometric survey ever published.
Before starting with the description of the use of the Gaia
data to establish the ISL, it is also worth mentioning the work of
Duriscoe (2013). He used more than 700 sky images taken from
pristine mountaintop locations to get the contribution of the stel-
lar contribution plus diﬀuse galactic and extragalactic light, after
removing the contribution from airglow and zodiacal light.
5.1.1
ISL from Gaia-DR2 and Hipparcos
With the transformations described in Section 3.4, it is possible
to calculate the irradiance produced at the top of the atmosphere
in a given passband by each and every star in our catalogues, and
then to compute the sky map of the integrated starlight by ﬁrst (a)
adding these irradiances within small elementary patches of the sky,
MNRAS 000, 1–15 (2020)

## Page 6

6
E. Masana et al.
and (b) converting them into radiances by dividing the irradiances
by the solid angle (in sr) subtended by each patch. For that, the
sky is ﬁrst tessellated into 𝑁pixels by using the HEALPix scheme
(Górski et al. 2005). We used a resolution equal to 8 and therefore
𝑁= 786432 pixels of mean area 0.05245 square degrees (equivalent
to 1.5979 10−5 sr), but the methodology could be applied to any
desired HEALPix resolution.
For each pixel we have collected all the stars in Gaia-DR2
and Hipparcos catalogues and added its irradiances for all the con-
sidered passbands. However, there are more than 300 millions of
faint sources without colour information in Gaia-DR2. In order
to not lose these stars, we have assigned to them the mean 𝐺BP -
𝐺RP colour of the stars in its surrounded area, allowing in this way
the application of the transformation described in Section 3.4. The
in-band irradiances 𝐸∗for each star are computed using equation 2
with the appropriate coeﬃcients and colour given in Table 3.4.
𝐸p =
𝑁p
∑︁
𝑘=1
𝐸∗
𝑘
(11)
where 𝐸p stands for irradiance in a given band in the pixel 𝑝, and 𝑁p
stands for the number of stars inside the pixel. This total irradiance
is divided by the solid angle Δ𝜔subtended by the pixel to obtain
the radiance outside the atmosphere from the ISL, 𝐿ISL,p(𝑙, 𝑏) =
𝐸p/Δ𝜔, with (𝑙, 𝑏) the galactic coordinates of the center of the
pixel. Following the notation introduced in Section 4, with 𝐿∗
𝑘(𝜆)
the contribution to the radiance at wavelength 𝜆of the k-th star in
the pixel, 𝐿ISL,p(𝑙, 𝑏) can be expressed as:
𝐿ISL,p(𝑙, 𝑏) =
𝑁p
∑︁
𝑘=1
∫∞
0
𝐿∗
𝑘(𝜆) 𝑆(𝜆) 𝑑𝜆
(12)
The integral in equation 12 can not be computed explicitly, as
we have not 𝐿∗
𝑘(𝜆) for each star. But it is equal to the ﬂux in 𝐺from
Gaia-DR2 transformed to in-band irradiances expressed in W m−2,
following equation 2 , and divided by the pixel solid angle, Δ𝜔.
Stars fainter than 𝐺= 20.0 mag, the approximated limit of
the Gaia −𝐷𝑅2 completeness, could contribute with some amount
of radiance to the ISL. We have used the Besançon Galaxy Model
(Robin et al. 2003, 2012) in order to estimate this lost ﬂux. The model
provides a realistic description of the stellar content of the Milky
Way, including its kinematic and dynamics, the mass distribution,
the star-formation rate and evolution of diﬀerent stellar populations.
It has been used to simulate the stars in the Milky Way up to
𝐺= 27.5 mag in a grid of patches between 0.25 and 1 square
degree distributed in a 10x10 degrees grid in (𝑙, 𝑏) over the sky.
These stars have been classiﬁed in two groups: bright stars (10.5 <
𝐺< 20.0 mag) and faint stars (21.0 < 𝐺< 27.5 mag). The
stars with 𝐺between 20.0 and 21.0 mag have been assigned to
one group or another following a probability linear distribution that
approximately reproduce the selection function of the Gaia-DR2
catalogue. Then, the ratio between the total ﬂux of both groups
was computed (Fig. 4). Only a few points on the galactic plane and
around the galactic center have a contribution from faint stars > 3
per cent. As we show in Section 8, the contribution of the Milky
Way to the total sky brightness could reach, under some conditions
and in some lines of sight, the most important contributor to the total
night sky brightness. So, we decided to correct the total radiance
𝐿ISL,p(𝑙, 𝑏) by adding the contribution of the very faint stars not
present in Gaia-DR2, computed from the ratios obtained from the
Figure 4. Ratio between ﬂux in photons sec−1 in the 𝐺band of faint stars
(20 < 𝐺< 27.5 mag) and bright stars (10.5 < 𝐺< 21 mag) obtained
using the Besançon Galaxy Model.
Besançon Galaxy Model model in order to improve the accuracy of
our model.
5.2
Background galactic light
The diﬀuse galactic light (DGL) is the diﬀuse background radiation
produced by the scattering of the starlight in the dust grains present
in the interstellar space. It contributes typically between 20 and 30
per cent of the total integrated light from the Milky Way (Leinert
et al. 1998).
DGL is very diﬃcult to map because it is masked by the light
coming from the unresolved stars and, for ground based observa-
tions, airglow and zodiacal light. Despite all this, several works to
characterize and even model the DGL in the optical range have been
done. A simple estimation of the DGL can be done using the rela-
tion between the ISL and DGL intensities in a given line of sight.
It is supported by the fact that DGL is mainly originated from the
forward scattering on interstellar grains, tracking in this way the
starlight in a given sky direction. Leinert et al. (1998) give the ratios
DGL to ISL for diﬀerent galactic latitudes based on Toller (1981).
A second and more accurate approach is to use the data from Pio-
neer probes (Arai et al. 2015). The Imaging Photopolarimeter (IPP)
instruments on Pioneer 10/11 collected data in blue (395 nm – 495
nm) and red (590 nm – 690 nm) bands. The measured radiances at
heliocentric distances greater than 3 AU are assumed as not aﬀected
by the zodiacal light. After removing the contribution of the ISL
using stellar counts or synthetic models, it is possible to get the DGL
plus the Extragalactic Background Light (the integrated radiation
from all light sources outside the Galaxy). A summary of the use
and limitations of this methodology can be found in Toller (1990).
In this work, we have adopted a diﬀerent approach. From the
early work of Laureĳs et al. (1987), several authors have pointed out
the relation between the diﬀuse emission of the dust at 100 𝜇m and
its emission at visible wavelength. The relation can be written, using
the notation in Matsuoka et al. (2011) and Kawara et al. (2017), as:
𝐼𝜈,𝑖(DGL) = 𝑏𝑖𝐼𝜈,100 −𝑐𝑖𝐼2
𝜈,100
(13)
𝐼𝜈,100 = 𝐼𝜈,SFD −0.8 MJy sr−1
(14)
where 𝐼𝜈,100 is the spectral radiance at 100 𝜇m from the In-
terstellar Medium (ISM), 𝑏𝑖and 𝑐𝑖are free parameters, and 𝐼𝜈,SFD
is the 100 𝜇m spectral radiance from the diﬀuse emission map of
Schlegel et al. (1998) (SFD hereafter). Equation 14 accounts for
MNRAS 000, 1–15 (2020)

## Page 7

Map of the natural sky brightness
7
the Extragalactic Background Light (EBL) that must be subtracted
from the SFD map. The EBL emission at 100 𝜇m is ≈0.8 MJy sr−1
(Matsuoka et al. 2011). Their optical and 100 𝜇m emissions are not
correlated.
The negative quadratic term in equation 13 reﬂects the ob-
served saturation in the DGL radiance when regions with high
100 𝜇m emission become optically thick (Ienaka et al. 2013). The
use of equation 13 is therefore limited to 𝐼𝜈,SFD<50 MJy sr−1. This
restriction applies mainly to low galactic latitudes |𝑏| ⪅30◦, where
high 100 𝜇m emission at very optical thick regions are found. In this
cases, equation 13 could give preposterous DGL radiances several
times grater than ISL ones. To avoid this, we have imposed an upper
limit in the DGL to ISL radiance ratio equal to 0.35, according with
the highest values reported by Toller (1981).
Our computation of DGL is based on the 100 𝜇m spectral
radiance SFD map. It is a combination of IRAS and COBE/DIRBE
data, with a resolution of few arcminute. It is the main source to
derive the dust temperature, opacity and extinction. Values are given
in MJy sr−1 (1MJy=10−20 W m−2 Hz−1). The zodiacal foreground
emission and bright stars have been removed from the map, but not
LMC, SMC and M31 extragalactic sources.
The coeﬃcients 𝑏𝑖and 𝑐𝑖are taken from Kawara et al. (2017),
who gives their values for several optical wavelengths from 0.23𝜇m
to 0.65𝜇m. This range of wavelengths almost fully covers the optical
bands considered in this work, allowing the interpolation of the 𝑏𝑖
and 𝑐𝑖given in Kawara et al. (2017) for the whole range and therefore
the computation of the radiance of the DGL, 𝐿DGL(𝜆), following
the same steps as for the ISL. The resultant map of the DGL in the
𝑉band is shown in Fig. 5.
5.3
Extragalactic Background Light
The Extragalactic Background Light (EBL) is a minor contributor
to the sky brightness. EBL is the sum of all extragalactic sources,
mainly resolved and unresolved galaxies and intergalactic matter. It
is assumed as isotropic. Due to its low intensity, its observation and
measurement is strongly disturbed by the zodiacal light and airglow.
In spite of its low contribution, we have included ELB in our model,
based on the data from Driver et al. (2016). In that paper, the EBL
is derived for a wide range of wavelengths, including the 𝑈𝐵𝑉𝐼
bands, from a combination of wide and deep galaxy number-count
data from the Galaxy And Mass Assembly, COSMOS/G10, Hubble
Space Telescope (HST) Early Release Science, HST UVUDF, and
various near-, mid-, and far-IR data sets from ESO, Spitzer, and
Herschel. We used the data of table 2 of the paper to interpolate at
any wavelengths in the optical range. With this procedure, we obtain
a radiance of the EBL at the 𝑉band equal to 1.1 nW m−2 sr−1.
The ﬁnal map of the radiance in 𝑉Johnson passband outside
the atmosphere including the integrated starlight, the diﬀuse galactic
light and the extragalactic background light is shown in Fig. 6. This
data, together with the radiances for the 𝐺, scotopic and photopic
passbands, is available online. A sample of the data is shown in
Table 3.
5.4
Zodiacal light
Zodiacal light is originated by the scattering of the Sun light in the
dust particles near the ecliptic plane. It represents a signiﬁcant term
of the natural night sky brightness. The zodiacal light decreases
Figure 5. Diﬀuse Galactic Light radiance in the 𝑉Johnson passband.
with the angular distance to the Sun, with the exception of the anti-
solar point, where we ﬁnd the gegenschein contribution caused by
the backward scattering of the solar light. It also decreases with
the heliocentric distance. The values for the optical emission (at
𝜆= 500 nm) of the zodiacal light at 1 A.U. were compiled by
Levasseur-Regourd & Dumont (1980) and updated by Leinert et al.
(1998). Kwon et al. (2004) presents a new set of data, with a smaller
sky coverage near the Sun than the previous work. Both sets of data
have a high degree of agreement and oﬀer conﬁdent values for the
zodiacal light brightness. In this work we have used the data given
in Leinert et al. (1998).
The spectrum of the zodiacal light is slightly reddened with
respect to the solar spectrum, and therefore a color correction must
be taken in to account when computing its radiance in other bands
diﬀerent to 𝑉. Leinert et al. (1998) accounts for the eﬀect of the
color in the zodiacal light through the factor 𝑓co, a measure of the
quotient of the zodiacal light and the solar radiance, normalized at
𝜆= 500 nm, function of the wavelength and elongation (𝜖):
𝑓co(𝜆, 𝜖) =
𝐿zl(𝜆)/𝐿⊙(𝜆)
𝐿zl(500)/𝐿⊙(500nm)
(15)
From the values of 𝑓co(𝜆, 𝜖) in Leinert et al. (1998), the zodia-
cal light spectrum at 1 A.U. can be obtained from the solar spectrum:
𝐿zl0 (𝜆, Λ, 𝛽) = 𝑓co(𝜆, 𝜖) 𝐿zl0 (500) 𝐸⊙(𝜆)
𝐸⊙(500)
(16)
where 𝐸⊙is the STIS002 spectral irradiance of the Sun from the
CALSPEC library (Bohlin et al. 2014), and the elongation can be
computed from the ecliptic coordinates (Λ, 𝛽).
As in the previous sections, the in-band radiance 𝐿zl(Λ, 𝛽) is
obtained by integrating 𝐿zl(𝜆, Λ, 𝛽) multiplied by the photometric
passband transmission 𝑆(𝜆).
The eﬀect of the variation of the visual brightness of the zodi-
acal light with the heliocentric distance of the Earth 𝑟(in A.U.) is
modelled (see Leinert et al. (1980)) by the factor 𝑓R = 𝑟−2.3.
Finally, the inﬂuence of the Earth position relative to the plane
of the interplanetary dust cloud is also taken into account for high
ecliptic latitudes (|𝛽| ≥60◦). It introduces a sinusoidal variation
of ±10 per cent in the zodiacal light brightness, having the most
extreme values when Earth is above or below this plane, and mean
values at the nodes, placed at Ω = 96◦(Leinert et al. 1998). This
factor 𝑓S takes the form:
𝑓S(𝛽) =
(
1 + 0.1 sin(ΛE −Ω),
if |𝛽| ≥60◦
1,
otherwise
(17)
MNRAS 000, 1–15 (2020)

## Page 8

8
E. Masana et al.
Figure 6. Sky map of the radiance outside the Earth atmosphere (integrated star light, diﬀuse galactic light and extragalactic background light) in the 𝑉Johnson
passband.
Table 3. Radiances (W m−2 sr−1) outside the Earth atmosphere including the integrated starlight, the diﬀuse galactic light and the extragalactic background
light for the 𝑉Johnson, 𝐺, scotopic and photopic passbands. Only the ﬁrst rows are showed. The full table is available online.
HEALPix Id
𝑙gal(◦)
𝑏gal(◦)
𝐿V
𝐿G
𝐿Sco
𝐿Phot
0
45.000
0.149
6.31994 10−8
5.27586 10−7
5.81792 10−8
1.39854 10−7
1
45.176
0.298
8.43552 10−8
5.78342 10−7
8.25604 10−8
1.57852 10−7
2
44.824
0.298
7.02885 10−8
4.89853 10−7
6.72805 10−8
1.45569 10−7
3
45.000
0.448
9.13240 10−8
7.20925 10−7
8.42789 10−8
1.65076 10−7
4
45.352
0.448
9.30920 10−8
6.45215 10−7
8.92242 10−8
1.65972 10−7
5
45.527
0.597
1.78077 10−7
1.13703 10−6
1.69802 10−7
2.41774 10−7
6
45.176
0.597
7.68996 10−8
5.58962 10−7
7.35909 10−8
1.51565 10−7
7
45.352
0.746
1.09157 10−7
7.37083 10−7
1.07517 10−7
1.79872 10−7
8
44.648
0.448
7.04502 10−8
4.98284 10−7
6.72217 10−8
1.45749 10−7
where ΛE is the ecliptic longitude of the Earth.
The in-band zodiacal radiance outside the Earth atmosphere at
a point of ecliptic coordinates (Λ, 𝛽) can then be expressed by:
𝐿zl(Λ, 𝛽) = 𝑓R 𝑓S(𝛽) 𝐿zl0 (Λ, 𝛽)
(18)
6
AIRGLOW
Aiglow is a faint light emission originated in the upper atmosphere.
It is caused by chemiluminescence, i.e. the emission of light (lu-
minescence) from the decay of excited states of the products of a
chemical reaction. In the case of the airglow, the chemiluminescence
is triggered by the high-energy solar radiation. Airglow is emitted
from several high altitude atmosphere layers, starting around 90 km
(mesopause), where the bright OI and OH emissions, together with
fainter O2 and NaD emissions, concentrate. Between ≈250 km and
≈300 km we found the emission of several OI transitions. The
airglow spectrum in the visible wavelengths is dominated by the OI
green line at 558 nm (see Hart (2019a)), the OI red lines at 630
nm and 636 nm (both produced in the layer between 200 km and
300) and the FeO pseudo-continuum around 590 nm (Saran et al.
(2011), Unterguggenberger et al. (2017)). Finally, the hydrogen at
geocorona contributes to the airglow in the 𝐻𝛼line. Other lines, like
𝐿𝛼and 𝐿𝛽are also generated in the geocorona by ﬂuorescence, but
they fall out our spectral range of interest. For a detailed analysis of
the complex processes involved in the airglow generation see Hart
(2019a) or Noll et al. (2012).
Airglow is a highly variable source of the natural night sky
brightness. The variability of the emissions due to the diﬀerent con-
stituents of the airglow (atomic and molecular O2, Na, OH, . . . ) at
diﬀerent time scales (nightly, yearly, long term, . . . ) is thoroughly
analyzed by Hart (2019a,b). For some of the main components it
can reach 100 per cent (maximum minus minimum divided by the
median). Also, airglow depends on the solar activity cycle (Patat
2008). Finally, the airglow emission could change with the geo-
graphic latitude, specially for lines originating in the mesopause
(OH, O2, Na I D, FeO or most of the green OI lines), and also with
geomagnetic latitude, in particular for ionospheric lines such as the
OI lines at 630 and 636 nm. This makes the prediction of the actual
value of the airglow emission diﬃcult to model, and it could be
considered as a free parameter if comparisons with real measure-
ments are done. The basic model described here is only intended to
provide a reference value and it shall be judiciously applied to any
particular observation.
The most common model for the airglow brightness, i.e. the in-
band integrated airglow radiance 𝐿ag(𝑧) at diﬀerent zenith angles 𝑧,
MNRAS 000, 1–15 (2020)

## Page 9

Map of the natural sky brightness
9
is the one based on the factorization of the zenith brightness 𝐿ag(0)
and the zenith angle dependence given by the van Rhĳn function
(Leinert et al. 1998):
𝐿ag(𝑧) =
𝐿ag(0)

1 −

𝑅
𝑅+𝐻
2 𝑠𝑖𝑛2𝑧
 1
2
(19)
where 𝑅= 6378 km is the Earth radius and 𝐻is the height above the
Earth’s surface of an assumed thin homogeneously emitting layer
responsible for airglow. Diﬀerent values have been quoted in the
literature for 𝐻. Here we adopt 𝐻= 87 km (Hart 2019a).In general,
the choice of 𝐻is only crucial at high zenith angles, but we need
to bear in mind that, as mentioned above, diﬀerent emissions are
originating at diﬀerent altitudes, and consequently, our choice of
𝐻could be inaccurate if strong emissions are originating at high
altitude. For more accurate results, in particular in case of strong
line emissions at diﬀerent heights, a more complex airglow model,
beyond the van Rhĳn approximation with ﬁxed H, should be used.
Some remarks should be made before applying this equation
to our calculations. First, note that equation 19 is expressed in terms
of in-band integrated radiances, 𝐿ag(𝑧), not of spectral radiances
𝐿ag(𝜆, 𝑧), although it could be deemed approximately valid (with
the same values for 𝑅and 𝐻) for 𝐿ag(𝜆, 𝑧). Second, the van Rhĳn
formulation is meant to describe the at-the-layer radiance, 𝐿ag(𝑧),
as seen at zenith angles 𝑧from the reference frame of an observer
located at sea level (ℎ= 0 m). Strictly speaking, for observers lo-
cated at heights ℎ> 0 m this equation should be slightly modiﬁed,
to take into account that regions of the airglow layer seen at zenith
angles 𝑧from sea level will appear to be at somewhat larger angles
𝑧′ = 𝑧′(𝑧, ℎ), if seen by an observer at ℎ> 0 m. However, since
for ground-based observers ℎis much smaller than 𝑅and 𝐻, this
small correction can be ignored, and equation 19 can be used to de-
scribe the at-the-layer radiance in their particular reference frames,
irrespective from ℎ.
The nadir-oriented spectral radiance at the layer, 𝐿ag(𝜆, 0),
can be determined by observational measurements or from syn-
thetic models. In the case of observational determinations, as in
Hart (2019a), some other sky radiance components can contribute
to some extent to the continuum value. For calculating the results
presented in Section 8 of this work we have used the Cerro Paranal
Advanced Sky Model (Noll et al. 2012 and Jones et al. 2013) to
get a synthetic airglow line and continuum emission spectrum. The
spectrum, computed from ESO’s SkyCalc web interface, is calcu-
lated for the Cerro Paranal altitude (2640 m above the sea level)
in the wavelength range from 350 nm to 1050 nm. For a reference
spectrum, we set the value of the Monthly Averaged Solar Radio
Flux equal to 100 sfu (1 sfu = 10−22 W m−2 s−1), the approximate
average value in the period 2009-2020 (one solar cycle) according to
the data of the Canadian Space Weather Forecast Centre (CSWFC).
This value can be set to other value for any speciﬁc application of
the model. The out-coming spectrum is shown in Fig. 7. After cor-
recting for the vertical atmospheric transmittance at Cerro Paranal
Observatory, 𝑇CPO(𝜆, 0; ℎ0), also provided by the ESO’s SkyCalc
tool, we can determine the airglow radiance at the emission layer:
𝐿layer(𝜆, 0) = 𝐿CPO
ag
(𝜆, 0; ℎ0)/𝑇CPO(𝜆, 0; ℎ0)
(20)
As stated above, the ﬁnal spectral airglow radiance is highly
spatially and temporally variable and usually it should be considered
as a free parameter. Its value could be set if more information about
Figure 7. The airglow spectrum computed with the ESO’s SkyCalc web
interface for an altitude of 2640 m. Logarithm binning 𝜆/Δ𝜆= 20000 and
Gaussian LSF convolution kernel (FWHM=10 bins).
the airglow emission is available. This issue will be discussed in
Section 8.1.
7
ATMOSPHERIC ATTENUATION AND SCATTERING
In the previous sections we have described the contributions of the
astrophysical sources to the night sky brightness. Although slightly
diﬀerent models could be adopted for the background light or the
zodiacal light, it is expected that the actual radiance outside the
Earth’s atmosphere does not diﬀer signiﬁcantly from the values
given in this work. We have also discussed the contribution of the
airglow, a highly variable source that should be considered as a free
parameter of the model.
However, in order to obtain the local map of the night sky
brightness, we need to deal with the eﬀects of the Earth atmosphere
on the outside radiance. In particular, the eﬀect of the atmospheric
attenuation and the scattering must to be added to the radiance com-
ing from the astrophysical sources. Both eﬀects are highly variable
in time, since they strongly depend on the particular atmospheric
conditions at the place and time of the observation. For the numer-
ical examples presented in Section 8 of this work we adopted some
standard values for the main atmospheric parameters. Diﬀerent at-
mospheric states will give rise to diﬀerent results.
The spectral radiance is modiﬁed by the terrestrial atmosphere
by means of two interrelated processes. On the one hand, the radi-
ance propagating toward the observer is attenuated by absorption
and scattering by the atmospheric constituents. On the other hand,
some amount of light initially propagating in diﬀerent directions
gets scattered into the observer’s line of sight, being added to the
recorded brightness. These two opposite eﬀects stem from the same
basic interaction processes at the atomic and molecular levels.
The attenuation of a beam along an atmospheric path of length
𝑑can be expressed in terms of the optical thickness 𝜏(𝑑) or, equiv-
alently, of the transmittance 𝑇(𝑑), as:
𝐿(𝑑) = 𝐿(0) 𝑒−𝜏(𝑑) = 𝐿(0) 𝑇(𝑑)
(21)
where 𝐿(0) is the initial radiance and 𝐿(𝑑) the radiance after
travelling the distance 𝑑.
Henceforth we closely follow the formulation by Kocifaj
(2007). Let us denote by 𝑘ext(ℎ′) the volume extinction coeﬃcient
at height ℎ′ above sea level, due to aerosols (A) and molecules (M),
such that:
𝑘ext(ℎ′) = 𝑘𝑀
ext(ℎ′) + 𝑘𝐴
ext(ℎ′)
(22)
MNRAS 000, 1–15 (2020)

## Page 10

10
E. Masana et al.
(which of course are wavelength-dependent). For a layered at-
mosphere as implicitly assumed in equation 21, the optical thickness
appearing in equation 22 can be computed as:
𝜏(𝑑) = 𝜏(ℎ1, ℎ2) =
∫ℎ2
ℎ1
𝑘ext(ℎ′) 𝑑ℎ′
(23)
where 𝑑ℎ′ is a function of the trajectory followed by the light
rays. Under the assumption of nearly-rectilinear propagation be-
tween atmospheric layers, at an angle 𝑧with respect to the local
zenith, we can write: 𝑑ℎ′ = 𝑀𝑀(𝑧) 𝑑ℎ, and 𝑑ℎ′ = 𝑀𝐴(𝑧) 𝑑ℎ,
where 𝑀𝑀(𝑧) and 𝑀𝐴(𝑧) are the molecular and aerosol airmasses,
respectively, corresponding to 𝑧, and 𝑑ℎis measured along the ver-
tical. Then:
𝜏(ℎ1, ℎ2) = 𝑀𝑀(𝑧)
∫ℎ2
ℎ1
𝑘𝑀
ext(ℎ) 𝑑ℎ+ 𝑀𝐴(𝑧)
∫ℎ2
ℎ1
𝑘𝐴
ext(ℎ) 𝑑ℎ
(24)
Under the assumption of exponential number density proﬁles
for molecules and aerosols, the extinction coeﬃcients take the form:
𝑘𝑀
ext(ℎ) =
𝜏𝑀
0
ℎm
𝑒−ℎ/ℎm;
𝑘𝐴
ext(ℎ) =
𝜏𝐴
0
ℎa
𝑒−ℎ/ℎa
(25)
where 𝜏𝑀
0
and 𝜏𝐴
0 are the (wavelength-dependent) molecular and
aerosol optical thicknesses of the whole atmosphere, measured
along a vertical path (𝑧=0), for which 𝑀𝑀(0) = 𝑀𝐴(0) = 1, and
ℎm and ℎa are the molecular and aerosol scale heights, respectively.
For our present calculations we have taken ℎm= 8 km and ℎa=1.54
km.
The molecular - Rayleigh component 𝜏𝑀
0 (𝜆) can be approxi-
mated analytically (Teillet 1990), with 𝜆in 𝜇m, by:
𝜏𝑀
0 (𝜆) = 0.00879 𝜆−4.09
(26)
And the aerosol component by:
𝜏𝐴
0 (𝜆) = 𝜏𝐴
0 (𝜆0)
 𝜆
𝜆0
−𝛼
(27)
being 𝛼the Ångstrom exponent.
Data on atmospheric aerosols (aerosol optical depth and
Ångstrom exponent) can be obtained from the AERONET network
https://aeronet.gsfc.nasa.gov. For the results presented be-
low, we chose 𝜏𝐴
0 (550 nm) = 0.2 and 𝛼= 1. The choice of other val-
ues will aﬀect the resulting night sky brightness, especially at high
zenith angles, where the eﬀect of atmospheric attenuation is more
signiﬁcant. For a highly accurate modelling, it is recommended to
use the available local values.
The airmasses, at a ﬁrst approximation, do not depend on
wavelength. Then, the spectral attenuation across a path at zenith
angle 𝑧, between the layers at ℎ1 and ℎ2 is:
𝑇(𝑧, 𝜆; ℎ1, ℎ2) =
exp
n
−𝑀𝑀(𝑧) 𝜏𝑀
0 (𝜆) [𝑒−ℎ1/ℎm −𝑒−ℎ2/ℎm]
−𝑀𝐴(𝑧) 𝜏𝐴
0 (𝜆) [𝑒−ℎ1/ℎa −𝑒−ℎ2/ℎa]
o
(28)
And the overall atmospheric attenuation, from ℎ1 = ℎto ℎ2 =
∞is:
𝑇(𝑧, 𝜆; ℎ) = exp
n
−𝑀𝑀(𝑧) 𝜏𝑀
0 (𝜆) 𝑒−ℎ/ℎm−𝑀𝐴(𝑧) 𝜏𝐴
0 (𝜆) 𝑒−ℎ/ℎa
o
(29)
For the airmass we use the expression of Kasten & Young
(1989), deﬁned for all zenithal distances as:
𝑀(𝑧) =
1
cos(𝑧) + 0.50572 (96.07995 −𝑧)−1.6364
(30)
with 𝑧in degrees.
Light from all other sky directions is also absorbed and scat-
tered. When interacting with the atmospheric constituents located
along the line of sight a fraction of this light gets scattered into the
observer’s ﬁeld of view, adding to the detected radiance. Denot-
ing by 𝐿0(𝜆, 𝜶s) the extra-atmospheric radiance from a diﬀerential
patch of the sky of solid angle 𝑑𝜔around the generic direction 𝜶s,
the total radiance scattered into the observer line of sight, 𝐿s(𝜆, 𝜶, ℎ)
can be calculated as
𝐿s(𝜆, 𝜶, ℎ) =
∫
Ω
Ψ(𝜆, 𝜶, 𝜶s, ℎ) 𝐿0(𝜆, 𝜶s) 𝑑𝜔
(31)
where Ψ(𝜆, 𝜶, 𝜶s, ℎ) is the function describing the spectral radiance
scattered toward the observer along the direction 𝜶, per unit 𝑑𝜔,
due to a unit amplitude radiant source located at 𝜶s (all directions
measured in the observer reference frame). The integral is extended
to the whole hemisphere above the observer, Ω. For this work we
have used the Kocifaj-Kránicz Ψ(𝜆, 𝜶, 𝜶s, ℎ) described in equa-
tion (18) of Kocifaj & Kránicz (2011) with an eﬀective scattering
phase function composed of aerosol and molecular (Rayleigh) com-
ponents weighted by the corresponding optical depths. The aerosol
scattering phase function is described by a Henyey-Greenstein func-
tion with asymmetry parameter 𝑔=0.90. The aerosol and molecular
albedos have been set to 0.85 and 1, respectively. As indicated above
regarding the aerosol optical depth, these particular values are used
to provide the examples shown in Section 8. Better estimations of
the natural night sky brightness for a given place and time could be
obtained by using the appropriate local values.
The above formulation, adopted for the Gaia-Hipparcos map,
requires performing an integration over the whole celestial hemi-
sphere for every direction of observation, 𝜶. Several simpler but
less accurate approaches have been proposed in the literature to
account for the radiance scattered into the line of sight without cal-
culating this integral. One of them is based on replacing 𝜏𝑀/𝐴
0
(𝜆)
in equation 29 by an eﬀective optical depth 𝜏𝑀/𝐴
0,eﬀ(𝜆) = 𝛾𝜏𝑀/𝐴
0
(𝜆)
with 𝛾< 1. The value of 𝛾depends on the aerosol albedo and
asymmetry parameter, and typical values are in the range 0.5-0.9
(Hong et al. 1998). This is the approach used for diﬀuse sources in
Duriscoe (2013), with 𝛾= 0.75, based on the empirical results of
Kwon (1989). It can be a practical option for obtaining reasonably
accurate results when computing time is a constraint, especially if
the night sky brightness is evaluated in sky pixels of suﬃcient size
to spatially average the contributions of the brightest stars.
8
RESULTS
In this section we outline some applications of the GAMBONS
model. The examples presented here have been calculated for par-
MNRAS 000, 1–15 (2020)

## Page 11

Map of the natural sky brightness
11
Figure 8. Comparison of GAMBONS maps (left) and SQC images (right) in 𝑉Johnson passband for Senyús (𝜆= 1◦12
′18” E, 𝜙= 42◦13
′52” N, h=1142 m,
Catalonia, Spain). The colour scale represents the sky brightness in Johnson V mag arcsec−2. Bright patches near the horizon in the SQC images are due to
light pollution. Top: 2018 August 10, 21:46 UT. Bottom: 2019 March 23, 20:28 UT.
ticular choices of the atmospheric parameters (e.g. aerosol optical
depth) and airglow zenith radiance. Quantitative comparisons with
ﬁeld measurements must take into account the actual state of the
atmosphere and the airglow at the precise time of taking them.
All-sky maps like the ones described below can be computed
for any location and time and freely downloaded from the GAM-
BONS website (http://gambons.fqa.ub.edu).
8.1
Comparison with all-sky images
As a ﬁrst application, the GAMBONS model has been used to ob-
tain all-sky maps of the brightness of the natural night sky. These
maps provide a realistic description of what one can expect to ob-
serve in pristine locations free from light pollution sources, under
diﬀerent atmospheric conditions. The multi-band capability of the
GAMBONS approach allows to generate all-sky images in several
bands.
The maps presented in this section were calculated for diﬀerent
photometric bands and are displayed in diﬀerent units. In light
pollution studies it is still frequent to work in the classical Johnson
𝑉band, reporting the brightness (i.e., the in-band radiances) in
the logarithmic scale of magnitudes per square arcsecond. Let us
remind that a region of the sky is said to have a brightness of
𝑚V magnitudes per square arcsecond if each square arcsecond of
its visual ﬁeld gives rise -at the entrance pupil of the observing
instrument- to the same irradiance a star of magnitude 𝑚= 𝑚V
would produce Bará et al. (2020). In this section we use the 𝑉band
as deﬁned in Section 3.2. The magnitudes per square arcsecond are
then calculated from the in-band radiances 𝐿(in W m−2 sr−1) as
𝑚V = −2.5 𝑙𝑜𝑔10(𝐿/𝐿r)
(32)
with 𝐿r = 143.1685 W m−2 sr−1 as indicated in Table 2.
For human visual observations, the quantity of choice is the
luminance, measured in SI units cd m−2, corresponding to the pho-
topic, mesopic, or scotopic adaptation states of the eye.
The all-sky images captured with some speciﬁc devices can
be compared with the GAMBONS maps. One of these devices is
the Sky Quality Camera (SQC) from Euromix Ltd. (Slovenia), a
commercial DSLR (Digital Single-Lens Reﬂex) camera with ﬁsh-
eye lens to evaluate the night sky brightness in the whole sky. This
kind of devices are a versatile solution to measure the night sky
brightness (see Hänel et al. (2018)), providing directional informa-
tion. The SQC software allows processing raw all-sky images and
provides diﬀerent products, including calibrated data in the 𝑉band
(Jechow et al. 2018) or (Vandersteen et al. 2020)). In Fig. 8 we show
the comparison of two of those images with our model. The images
MNRAS 000, 1–15 (2020)

## Page 12

12
E. Masana et al.
Figure 9. All sky luminance map (𝜇cd m−2) for observers with scotopic
(top) and photopic (bottom) luminance adaptation. 2019 March 23, 20:28
TU, Senyús (𝜆= 1◦12
′18” E, 𝜙= 42◦13
′52” N, h=1142 m, Catalonia,
Spain).
were taken by one of the authors (SJR) from Senyús (𝜆= 1◦12
′18”
E, 𝜙= 42◦13
′52” N, h=1142 m), a pristine dark site with very low
light pollution near the Montsec Protected Area (Catalonia, Spain)
at two diﬀerent epochs. The agreement between the SQC data and
the model is fairly good. The main features of the sky (zodiacal
light, clearly visible in the image of the bottom panel in the West
direction, or Milky way) in these SQC images are coincident with
those predicted by GAMBONS.
Note that this is a qualitative comparison. As mentioned in
Section 6, the radiance of the airglow is very variable both in short
and large time scales, and for many practical applications it may be
considered as a free parameter. We have used the value of the Solar
Radio Flux from the Canadian Space Weather Forecast Centre to
get the airglow spectra for the both epochs, but it could not account
for local or very short variations of the airglow radiance. The same
applies to the atmospheric parameters related with the attenuation.
After some tests, the best match is obtained with 𝜏𝐴
0 = 0.15 and
𝛼= 1. Furthermore, SQC images record light pollution, and its
𝑉band could not coincide with the 𝑉Johnson band used in this
work, as it is derived from the RGB image taken with a DSLR
camera. This could introduce some diﬀerences between SQC and
GAMBONS values, function of the colour of the sky.
The GAMBONS model can also be used to determine the
Table 4. Mean contributions to zenith natural night sky brightness for a
latitude equal to 40° N.
Component
Mean radiances
Percentage
(nW m−2 sr−1)
(%)
Airglow
165
47.7
Zodiacal Light
95
27.5
Integrated Star Light
75
21.7
Diﬀuse Galactic Light
10
2.9
Extragalactic Background Light
0.8
≈0.2
amount of artiﬁcial light polluting the night sky. As in the previous
case, it requires the ﬁtting of the parameters not available from direct
measurements, as e.g. the airglow, and in some cases the aerosol
properties, if they are unknown. The ﬁt could be laborious due to
the complex spatial features of the actual airglow and attenuation.
The model can be easily extended to other photometric bands used
in light pollution studies, as e.g. the SQM and TESS-W (Bará et al.
2019) or RGB (Sánchez de Miguel et al. 2019; Kolláth et al. 2020).
Both topics will be addressed in forthcoming papers. By way of
example, in Fig. 9 we show the visual scotopic and photopic all
sky maps for the same location and date. They are expressed in
luminance units 𝜇cd m−2.
8.2
Relative contributions to the night sky brightness
The model allows to compute the expected contribution of the dif-
ferent sources (ISL, DGL+ELB, zodiacal light and airglow) to the
total night sky brightness (moonless and cloudless) under diﬀerent
conditions (i.e. diﬀerent locations, times or airglow intensities). The
contribution also depends on the extent of the ﬁeld of view that we
consider. We refer here as zenith values to the average radiance in
a circular region of radius 10 degrees around the zenith with no
weights applied to the diﬀerent points.
We have run the model for a mid latitude location (𝜙= 40◦)
and the atmospheric conditions given in Section 7 and the reference
(constant) airglow spectrum described in Section 6, and averaged
the contribution of the diﬀerent sources over a year. The model
was run in one hour intervals during the astronomical night (i.e.
Sun more than 18 degrees below the horizon). The result for the
𝑉band is shown in Table 4. Note that these values are sensitive to
the airglow intensity, which is highly variable.
The contributions also depend on the observer latitude, as
shown in Fig. 10. Zodiacal light has a larger impact in locations
close to the Equator when we observe near the zenith, as the plane
of the ecliptic reaches greater heights above the horizon at these
latitudes.
Finally, the radiances are also a function of the observation
time. The presence or absence of the Milky Way and the height of
the ecliptic above the horizon are the two main factors that modulate
the relative contributions to the sky brightness throughout the year.
As shown in Fig. 11, for the midnight radiance around the zenith
for an observer at mid latitudes, the Milky Way could become the
brightness component. As it can be observed in both ﬁgures, we
assume a constant airglow radiance, regardless of the location and
time.
8.3
Seasonal variation of the zenith sky brightness
For a given location, the natural night sky brightness is highly
dependent on the observing time. As we have already mentioned, the
MNRAS 000, 1–15 (2020)

## Page 13

Map of the natural sky brightness
13
Figure 10. Annual average radiance at midnight in the Johnson 𝑉band at
zenith for the diﬀerent contributors to the natural sky brightness as function
of the observer latitude.
Figure 11. Midnight radiance at zenith in the Johnson 𝑉band for the
diﬀerent contributors to the natural sky brightness as function of the day of
the year for an observer at latitude equal to 40° N.
presence or absence of the Milky Way or the altitude of the ecliptic
plane above the horizon strongly determine the brightness of the sky.
We must bear this in mind when trying to characterize the darkness
of a given place. According to our model, for zenith measurements,
the natural variation of the night sky brightness along the year due
to the variation of the astrophysical contributions can reach more
than 0.6 magnitudes. As an example, Fig. 12 shows the variation
of the 𝑉magnitude around the zenith (i.e. a 10 degrees circular
region around it) for an observer at 𝜙= 40° latitude and h=1000
m.a.s.l. The ﬁgure plots only the times when the height of the Sun
above the horizon is < −18°. The presence of the Milky Way in
two diﬀerent epochs of the year is clearly visible. The zodiacal light
is also modulated by the position of the Earth above the ecliptic
plane and the Sun–Earth distance. The variation is smoother if a
wider area of the sky is considered. But even for relatively large
ﬁelds of view of tens of degrees, the variation of the natural night
sky brightness is up to several tenths of magV arcsec−2. Again, we
consider constant airglow.
Figure 12. Variation of the natural night sky brightness (magV arcsec−2 at
zenith) along the year for an observer at 𝜙= 40◦and h=1000 m.a.s.l. Note
that the colour scale is zoomed with regard to Fig. 8.
Figure 13. Darkest value of the natural night sky brightness (in magV
arcsec−2) as a function of the latitude for three diﬀerent ﬁelds of view: 10
degrees around the zenith (zenith angle 𝑧= (0, 10)); 30 degrees around the
zenith (𝑧= (0, 30)); and all-sky (𝑧= (0, 90)). The atmospheric and airglow
conditions are the ones assumed in this section.
8.4
How dark are the darkest natural night skies?
There might be a question about the darkest value the natural night
sky can attain, in absence of any source of artiﬁcial light pollution.
This value is signiﬁcant for light pollution studies, as it establishes
an upper limit to the actual measurements of the sky darkness.
Darker measurements could indicate higher atmospheric attenu-
ation or sporadic lower airglow radiances, not necessarily being
indicative of less polluted (’darker’) skies. The darkest value of the
zenith natural night sky depends on the observer latitude and the
time of observation, as well as on the atmospheric conditions, al-
titude of the observer above sea level, and airglow intensity. Due
to attenuation, less stars are expected to be perceived from sites at
lower altitudes above sea level, as well as at higher zenith angles,
as recently analyzed in Cinzano & Falchi (2020). For a given lati-
tude, using our model (with the particular airglow and atmospheric
conditions assumed in this section), we are able to determine the
minimum value of the night sky brightness (i.e. the darkest sky at
a given latitude). It is shown in Fig. 13. The darkest skies (aver-
aged over 10 degrees around the zenith) are found at mid-latitudes
in both hemispheres. The presence of the ecliptic plane near the
zenith for observers near the Equator prevents them to reach the
darkest values. This eﬀect almost disappears if we considered the
full sky dome, but it is well visible even for a wide ﬁeld of view
(0° < 𝑧< 30°).
MNRAS 000, 1–15 (2020)

## Page 14

14
E. Masana et al.
9
CONCLUSIONS
We present GAMBONS (the GAia Map of the Brightness Of the
Natural Sky) model of the natural night sky brightness. The model
considers each of the contributors to the sky brightness (i.e. the in-
tegrated star light, the diﬀuse galactic light, the extragalactic back-
ground light, the zodiacal light and the airglow), plus the atmo-
spheric attenuation and scattering into the ﬁeld-of-view. The main
novelty with respect to previous models is the use of the Gaia-
DR2 catalogue to evaluate the integrated star light. Furthermore,
the photometric data in Gaia-DR2 (𝐺, 𝐺BP and 𝐺RP bands) allow
to transform from Gaia photon ﬂuxes to radiances in any other
photometric band. In this way, GAMBONS becomes a multi-band
model to study the natural night sky brightness.
In particular, although it amounts less than the 3 per cent of the
sky brightness, we have put an eﬀort to evaluate the contribution of
the astrophysical diﬀuse light (diﬀuse galactic light plus extragalac-
tic background light), by using the relation between the emission at
100𝜇m and the optical emission. The spectrum template of the air-
glow used by GAMBONS is based on the Cerro Paranal Advanced
Sky Model, through the ESO SkyCalc tool.
Two highly variable inputs to the model are the absolute zenith
value of the airglow radiance and the aerosol properties at the time
of observation. They vary from place to place and in diﬀerent time
scales. Information on aerosol properties at a large network of mon-
itoring sites worldwide can be obtained from AERONET.
GAMBONS is expected to enable multiple applications in the
study and characterization of the natural night sky brightness. We
have pointed out several of them. In particular we have shown
the variation of the sky darkness as function of the latitude of
the observer and time, as well as the variation of the contribution
of the diﬀerent sources of natural light with these two variables.
Furthermore, GAMBONS could help, if reliable determinations
of airglow intensity and atmospheric conditions are available, to
establish a reference value of the sky darkness, for any given location
in a moonless and cloudless night, against which to evaluate the
measurements reported by the observers. In a forthcoming paper
we will deal with the use of GAMBONS to remove the natural night
sky brightness from the raw all-sky images in order to quantitatively
estimate the levels of light pollution, and to put to the test the
predictions obtained from models of atmospheric propagation of
artiﬁcial light at night.
GAMBONS and the data related are accessible via web at
http://gambons.fqa.ub.edu.
ACKNOWLEDGEMENTS
We thank Dr. M. Hart for kindly providing the airglow spectra
taken at Apache Point Observatory. We thank the reviewer for their
thorough and useful comments.
This
work
was
supported
by
the
MINECO
(Spanish
Ministry of Economy) through grant RTI2018-095076-B-C21
(MINECO/FEDER, UE). EM and JMC acknowledges ﬁnancial sup-
port from the State Agency for Research of the Spanish Ministry
of Science and Innovation through the “Unit of Excellence María
de Maeztu 2020-2023” award to the Institute of Cosmos Sciences
(CEX2019-000918-M). SB acknowledges Xunta de Galicia, grant
ED431B 2020/29. SJR thanks Cal Joanet family for allowing him to
take SQC measurements from their home in the village of Senyús.
DATA AVAILABILITY
The data underlying this article are available in the article and in its
online supplementary material.
REFERENCES
Arai T., et al., 2015, ApJ, 806, 69
Aubé M., Franchomme-Fossé L., Robert-Staehler P., Houle V., 2005, in At-
mospheric and Environmental Remote Sensing Data Processing and Uti-
lization: Numerical Atmospheric Prediction and Environmental Moni-
toring. p. 589012
Aubé M., Simoneau A., Wainscoat R., Nelson L., 2018, Monthly Notices of
the Royal Astronomical Society, 478, 1776
Bahcall J. N., Soneira R. M., 1980, ApJS, 44, 73
Bará S., Tapia C., Zamorano J., 2019, Sensors, 19, 1336
Bará S., Aubé M., Barentine J., Zamorano J., 2020, MNRAS, 493, 2429
Benn C. R., Ellison S. L., 1998, New Astron. Rev., 42, 503
Berry R. L., 1976, Journal of the Royal Astronomical Society of Canada,
70, 97
Bessell M., Murphy S., 2012, PASP, 124, 140
Bohlin R. C., Gilliland R. L., 2004, AJ, 127, 3508
Bohlin R. C., Gordon K. D., Tremblay P. E., 2014, PASP, 126, 711
CIE 1951, Proceedings of the Commission Internationale de l’Éclairage,
Vol. 1, Sec 4; Vol 3, p. 37, Bureau Central de la CIE, Paris
CIE 1990, Commission Internationale de l’Éclairage 1988 2· Spectral Lu-
minous Eﬃciency Function for Photopic Vision
CIE 2010, Commission Internationale de l’Éclairage. Recommended system
for mesopic photometry based on visual performance.
Cinzano P., Falchi F., 2012, MNRAS, 427, 3337
Cinzano P., Falchi F., 2020, J. Quant. Spectrosc. Radiative Transfer, 253,
107059
Cinzano P., Falchi F., Elvidge C. D., 2001, MNRAS, 328, 689
Driver S. P., et al., 2016, ApJ, 827, 108
Duriscoe D. M., 2013, PASP, 125, 1370
ESA 1997, The HIPPARCOS and TYCHO catalogues. Astrometric and
photometric star catalogues derived from the ESA HIPPARCOS Space
Astrometry Mission. ESA Special Publication Vol. 1200
Evans D. W., et al., 2018, A&A, 616, A4
Falchi F., et al., 2016, Science Advances, 2, e1600377
Gaia Collaboration et al., 2016, A&A, 595, A1
Gaia Collaboration et al., 2018, A&A, 616, A1
Garstang R. H., 1986, PASP, 98, 364
Garstang R. H., 1989, PASP, 101, 306
Garstang R. H., 1991, PASP, 103, 1109
Górski K. M., Hivon E., Banday A. J., Wand elt B. D., Hansen F. K.,
Reinecke M., Bartelmann M., 2005, ApJ, 622, 759
Green R. M., 1985, Spherical Astronomy
Hänel A., et al., 2018, J. Quant. Spectrosc. Radiative Transfer, 205, 278
Hart M., 2019a, PASP, 131, 015003
Hart M., 2019b, AJ, 157, 221
Hong S. S., Kwon S. M., Park Y. S., Park C., 1998, Earth, Planets, and
Space, 50, 487
Ienaka N., Kawara K., Matsuoka Y., Sameshima H., Oyabu S., Tsujimoto
T., Peterson B. A., 2013, ApJ, 767, 80
Jechow A., Ribas S. J., Domingo R. C., HÃ¶lker F., KollÃ¡th Z., Kyba C. C.,
2018, Journal of Quantitative Spectroscopy and Radiative Transfer, 209,
212
Johnson H. L., 1963, Photometric Systems. p. 204
Jones A., Noll S., Kausch W., Szyszka C., Kimeswenger S., 2013, A&A,
560, A91
Jordi C., et al., 2010, A&A, 523, A48
Kasten F., Young A. T., 1989, Appl. Opt., 28, 4735
Kawara K., Matsuoka Y., Sano K., Brand t T. D., Sameshima H., Tsumura
K., Oyabu S., Ienaka N., 2017, PASJ, 69, 31
Kocifaj M., 2007, Applied optics, 46, 3013
Kocifaj M., 2018, J. Quant. Spectrosc. Radiative Transfer, 206, 260
MNRAS 000, 1–15 (2020)

## Page 15

Map of the natural sky brightness
15
Kocifaj M., Kránicz B., 2011, Lighting Research & Technology, 43, 497
Kolláth Z., Cool A., Jechow A., Kolláth K., Száz D., Tong K. P., 2020,
J. Quant. Spectrosc. Radiative Transfer, 253, 107162
Kwon S. M., 1989, Journal of Korean Astronomical Society, 22, 141
Kwon S. M., Hong S. S., Weinberg J. L., 2004, New Astron., 10, 91
Laureĳs R. J., Mattila K., Schnur G., 1987, A&A, 184, 269
Leinert C., Richter I., Pitz E., Hanner M., 1980, in Halliday I., McIntosh
B. A., eds, Vol. 90, Solid Particles in the Solar System. pp 15–18
Leinert C., et al., 1998, A&AS, 127, 1
Levasseur-Regourd A. C., Dumont R., 1980, A&A, 84, 277
Maiz Apellaniz J., Weiler M., 2018, VizieR Online Data Catalog, pp
J/A+A/619/A180
Marrese P. M., Marinoni S., Fabrizio M., Altavilla G., 2019, A&A, 621,
A144
Matsuoka Y., Ienaka N., Kawara K., Oyabu S., 2011, ApJ, 736, 119
Melchior A. L., Combes F., Gould A., 2007, A&A, 462, 965
Noll S., Kausch W., Barden M., Jones A. M., Szyszka C., Kimeswenger S.,
Vinther J., 2012, A&A, 543, A92
Patat F., 2008, A&A, 481.2, 575
Roach F. E., Gordon J. L., 1973, The Light of the Night Sky
Robin A. C., Reylé C., Derrière S., Picaud S., 2003, A&A, 409, 523
Robin A. C., Marshall D. J., Schultheis M., Reylé C., 2012, A&A, 538, A106
Sánchez de Miguel A., Kyba C., Aubé M., Zamorano J., Cardiel N., Tapia
C., Bennie J., Gaston K. J., 2019, Remote Sensing of Environment, 224,
92–103
Saran D. V., Slanger T. G., Feng W., Plane J. M. C., 2011, Journal of
Geophysical Research (Atmospheres), 116, D12303
Schlegel D. J., Finkbeiner D. P., Davis M., 1998, ApJ, 500, 525
Teillet P. M., 1990, Appl. Opt., 29, 1897
Toller G. N., 1981, PhD thesis, State University of New York, Stony Brook.
Toller G. N., 1990, in Bowyer S., Leinert C., eds, IAU Symposium Vol. 139,
The Galactic and Extragalactic Background Radiation. p. 21
Treanor P. J., 1973, The Observatory, 93, 117
Turnrose B. E., 1974, PASP, 86, 545
Unterguggenberger S., Noll S., Feng W., Plane J. M. C., Kausch W.,
Kimeswenger S., Jones A., Moehler S., 2017, Atmospheric Chemistry
& Physics, 17, 4177
Vandersteen J., Kark S., Sorrell K., Levin N., 2020, Remote Sensing, 12,
1785
Weiler M., 2018, A&A, 617, A138
Weiler M., Jordi C., Fabricius C., Carrasco J. M., 2018, A&A, 615, A24
Weinberg J. L., Hanner M. S., Beeson D. E., DeShields L. M. I., Green
B. A., 1974, J. Geophys. Res., 79, 3665
Westera P., Samland M., Bruzual G., Buser R., 2002, The BaSeL 3.1 models:
metallicity calibration and application. p. 166
van Leeuwen F., 2007, A&A, 474, 653
This paper has been typeset from a TEX/LATEX ﬁle prepared by the author.
MNRAS 000, 1–15 (2020)
