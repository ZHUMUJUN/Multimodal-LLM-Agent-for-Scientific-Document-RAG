# 12_space_objects_artificial_night_sky_brightness_arxiv

## Page 1

arXiv:2103.17125v2  [astro-ph.IM]  1 Apr 2021
MNRAS 000, 1–6 (2015)
Preprint 2 April 2021
Compiled using MNRAS LATEX style ﬁle v3.0
The proliferation of space objects is a rapidly increasing source of
artiﬁcial night sky brightness
M. Kocifaj,1,2⋆F. Kundracik,2 J. C. Barentine,3,4 S. Bar´a,5
1ICA, Slovak Academy of Sciences, D´ubravsk´a cesta 9, 845 03 Bratislava, Slovakia
2Department of Experimental Physics, FMPI, Comenius University, Mlynsk´a dolina, 842 48 Bratislava, Slovakia
3International Dark-Sky Association, 3223 N. 1st Ave, Tucson, AZ 85710 USA
4Consortium for Dark Sky Studies, University of Utah, 375 S 1530 E, RM 235 ARCH, Salt Lake City, Utah 84112-0730 USA
5Departamento de F´ısica Aplicada, Universidade de Santiago de Compostela, E-15782 Santiago de Compostela, Galicia, Spain
Accepted XXX. Received YYY; in original form ZZZ
ABSTRACT
The population of artiﬁcial satellites and space debris orbiting the Earth imposes
non-negligible constraints on both space operations and ground-based optical and ra-
dio astronomy. The ongoing deployment of several satellite ‘mega-constellations’ in the
2020s represents an additional threat that raises signiﬁcant concerns. The expected
severity of its unwanted consequences is still under study, including radio interference
and information loss by satellite streaks appearing in science images. In this Letter,
we report a new skyglow eﬀect produced by space objects: increased night sky bright-
ness caused by sunlight reﬂected and scattered by that large set of orbiting bodies
whose direct radiance is a diﬀuse component when observed with the naked eye or
with low angular resolution photometric instruments. According to our preliminary
estimates, the zenith luminance of this additional light pollution source may have al-
ready reached ∼20 µcd m−2, which amounts to an approximately 10 percent increase
over the brightness of the night sky determined by natural sources of light. This is the
critical limit adopted in 1979 by the International Astronomical Union for the light
pollution level not to be exceeded at the sites of astronomical observatories.
Key words: light pollution – methods: statistical – methods: data analysis
1
INTRODUCTION
Artiﬁcial satellites orbiting the Earth have been a concern of
astronomers since the launch of the ﬁrst such object, Sputnik
1, in 1957. As of 1 January 2021, some 3,372 satellites are
in orbit (UCS 2021) along with many tens of thousands of
pieces of space debris; we refer to both satellites and space
debris here as “space objects.”
The orbital altitudes of space objects range from a few
hundred kilometres in the case of objects in Low-Earth Or-
bit (LEO) to beyond the 35,786-km height deﬁning geosyn-
chronous orbits. At such altitudes, space objects remain di-
rectly illuminated by sunlight as seen from the night side
of the Earth; consequently, they appear in images obtained
with ground-based telescopes as streaks of various lengths
and apparent brightness depending on the orbital parame-
ters of the objects. Because the streaks are often comparable
to or brighter than objects of astrophysical interest, their
presence tends to compromise astronomical data and poses
the threat of irretrievable loss of information.
⋆E-mail: kocifaj@savba.sk
The number of space objects orbiting Earth is expected
to increase by more than an order of magnitude in the next
decade due to the launches of ﬂeets of new, large ’constella-
tions’ of communications satellites. While astronomers can
often plan observations around the presence of bright space
objects in their telescopes’ ﬁelds of view by predicting their
apparent positions on the night sky using databases of or-
bital elements, the expected increase in the space object pop-
ulation signiﬁcantly increases the probability that any par-
ticular observation will be aﬀected by streaks. Hainaut at al.
(2020) and Tyson et al. (2020) recently explored the ex-
pected impacts of large satellite constellations on both opti-
cal and near-infrared astronomical observations, ﬁnding that
ultra-wide imaging exposures made with large survey tele-
scopes will be most aﬀected, with up to 40% of science ex-
posures aﬀected by streaks assuming the largest expected
numbers of new satellites and an overall loss of ∼1% of sci-
ence pixels.
To date there is little information in the literature as
to the contribution of space objects to the diﬀuse brightness
of the night sky, as opposed to the eﬀect of discrete streaks
that add systematic errors to astronomical data. While the
© 2015 The Authors

## Page 2

2
M. Kocifaj et al.
Figure 1. A simpliﬁed illustrative view of space debris orbiting
the Earth and directly illuminated by sunlight. Planes I and II
are for the Sun and the Earth, respectively, while the parameters
used are described in the main text. The drawing is not to any
particular scale.
night sky luminance signal due to sunlight reﬂected from
space objects and propagating in the Earth’s atmosphere is
expected to be small, it is otherwise unknown how its con-
tribution to diﬀuse night sky brightness (NSB) compares to
natural sources of light in the night sky that ultimately de-
termine the sky luminance over ‘pristine’ locations nearly
devoid of anthropogenic skyglow, such as the sites of astro-
nomical research observatories.
We decided to estimate the present-day diﬀuse NSB
contribution from space objects, before the ongoing deploy-
ment of large communication satellite constellations increase
in order to benchmark future NSB observations in these pris-
tine places. In the current work, we describe the geometry
of the situation and model the diﬀuse NSB speciﬁcally at-
tributable to sunlight reﬂected from space objects, estab-
lishing lower limits for the space object contribution based
on expectations for coming launches and the potential for
orbital crowding to generate new sources of space debris.
This paper is organised as follows. We develop the requi-
site theory, establish the expected spectral radiance of space
objects in the observer’s zenith, and compute the zenith
night sky luminance contribution from space objects in Sec-
tion 2. We present the results of our calculations and discuss
their implications in Section 3. Finally, we draw conclusions
from this work and speculate on future prospects in Sec-
tion 4.
2
SKY BRIGHTNESS DUE TO SPACE OBJECTS
Due to their high altitudes, objects in orbit around the Earth
can be visible after the onset of astronomical night; i.e., for
solar depression angles ≥18◦. For instance, objects at al-
titudes between 1000–2000 kilometres can be directly illu-
minated by sunlight and observed in the zenith even when
the depression angle of the solar disc is 30-40◦. The lower
the minimum altitude of light rays, the more such rays di-
verge due to atmospheric refraction; see the quantity h0 in
Fig. 1. Depending on beam trajectory, the angle of refrac-
tion is 1′ at an altitude of 30 km, 10′ at h0 ≈15 km, and
approaches 1◦for rays entering the lower troposphere (Link
1969). Satellites illuminated by such low rays are normally
dark or even invisible because of exceptional atmospheric
extinction of sunlight.
Since the deﬂection of the light beam is extremely low,
most space objects orbiting the Earth are either directly
illuminated by sunlight or disappear once they cross into the
geometrical shadow of the Earth.1 A few objects moving in a
‘transition zone’ between positions unaﬀected by the Earth’s
atmosphere and those obstructed by the Earth contribute
negligibly to the diﬀuse brightness of the night sky, and thus
are not considered in the following analysis. The transition
zone is deﬁned by the angle of refraction, which normally
does not exceed 1◦. The objects traversing the sky from
the twilight region into the Earth’s shadow are constantly
illuminated by sunlight and seen in the visual ﬁeld of 90◦or
more; thus, the number of objects in the transition zone is
about 1% of all objects we can see in the night sky.
2.1
Spectral radiance
The spectral irradiance (W m−2 nm−1) at a point N located
at an altitude h above the Earth’s surface is
Eλ(γ)
=
2b0,λ
Z γ+RS
γ−RS
T Ext
λ
(ρ) ǫ0(ρ) dρ ,
(1)
where b0,λ is the average radiance of the Sun (W m−2 nm−1
sr−1), λ is the wavelength of radiation, γ is the angular dis-
tance measured from the centre of the Earth between the
position of an illuminated object (in point N) and the cen-
tre of the Earth’s shadow (in point M), RS is the angular
radius of the solar disc, ρ is the angular distance ranging
from γ −RS to γ + RS,and ǫ0 is the maximum opening an-
gle at an angular distance of ρ, i.e.,the angle between centre
of solar disc and the limb (consult Fig. 1). The transmission
coeﬃcient T Ext
λ
characterizes attenuation of sunlight in the
atmosphere due to extinction (see, e.g., Kocifaj and Horvath
2005). In the absence of the terrestrial atmosphere, or for
high-altitude beams with h0 ∼
> 60 km (Link 1969), Eq. (1)
reduces to
E0,λ
=
2b0,λ
Z γ+RS
γ−RS
ǫ0(ρ) dρ = b0,λπR2
S ,
(2)
with πR2
S being the solid angle subtended by the solar disc
in steradians.
Of all photons entering the point N, a small fraction
is intercepted by space objects and redirected toward the
Earth. The redirection is dominated by scattering in the case
of debris objects smaller than or comparable to the wave-
lengths of visible light. For larger macroscopic objects to
which the principles of geometric optics are applicable, direct
reﬂection of light dominates the redirection. The amount of
redirection is proportional to E0,λ
Pλ(θ)
4π kλ(h), where Pλ(θ) is
scattering phase function normalized to 4π, and θ is the scat-
tering angle, i.e., the angle between the incident beam and
the scattered beam. Conservation of energy requires that
R Pλ(θ)
4π dω = 1, where dω = 2π sin(θ)dθ is the elementary
solid angle.
1 The geometrical shadow of the Earth neglects refraction eﬀects
from the terrestrial atmosphere.
MNRAS 000, 1–6 (2015)

## Page 3

Space objects are a new skyglow threat
3
100
1000
10000
10
-8
10
-7
10
-6
10
-5
10
-4
Spatial Density (1/km
3
)
Altitude (km)
Figure 2. Spatial density of space objects larger than 1 mm as a
function of altitude. Dots are data published by Bendisch et al.
(2004), while the solid line represents our ﬁtted model.
Artiﬁcial satellites and pieces of space debris have di-
verse shapes and are oriented randomly in the line of sight,
scattering and reﬂecting light in a complex manner. How-
ever, the number of orbital objects is large, and statistical
averaging over a large sample size yields results similar to
those for equally sized spherical objects. Since most space
objects are very large compared to the wavelengths of visi-
ble light, they scatter light strictly in the geometrical optics
regime. The resulting optical signal therefore depends much
more strongly on an object’s geometric cross section rather
than on its morphology.
The volume scattering coeﬃcient kλ(h) can be com-
puted from Mie theory (see, e.g., Hergert and Wriedt 2012)
by treating a given object as a sphere of radius of r:
kλ(h)
=
π
Z ∞
0
r2n(r, h) Qλ,sca(r) dr,
(3)
where Qλ,sca(r) is the scattering eﬃciency factor for an ob-
ject of radius r illuminated by monochromatic light of wave-
length λ. The function n(r, h)dr is the number of objects of
radius r →r + dr per cubic meter such that n(r, h) is ex-
pressed in units of m−4. For objects larger than the typical
observational wavelengths Qλ,sca ≈1 to 2.
The spectral radiance due to the reﬂection of sunlight
in all space objects in Earth orbit along the line of sight z,
detected by an observer at ground level is
Lλ(z)
=
e−τλ/ cos z
cos z
E0,λ
Z ∞
h1
Pλ(θ)
4π
kλ(h) dh,
(4)
where τλ is the optical thickness of Earth’s atmosphere,
z is the zenith angle of observation, and h1 is the mini-
mum orbital altitude of space objects. The latter parame-
ter is normally a few hundred kilometers (see Fig. 2), but
the lower integration limit can also be asymptotically ex-
tended to h1 = 0 km assuming that both the number
density of space objects and kλ(h) approach zero near the
Earth’s surface. Space objects with arbitrary shapes reﬂect
sunlight more or less isotropically, resulting in Pλ(θ)/4π ≈
1/4π (Shendeleva 2017). Substituting the approximate ex-
pressions into Eq. (4), we found for the theoretical spectral
radiance in the zenith (z = 0◦)
Lλ(z)
=
E0,λe−τλ
2
Z ∞
h=h1
Z ∞
r=0
r2 n(r, h) dr dh. (5)
10
-6
10
-5
10
-4
10
-3
10
-2
10
-1
10
0
10
1
10
0
10
2
10
4
10
6
10
8
10
10
10
12
10
14
Number of objects found within 
1600 km of the Earth's surface (-)
Diameter (m)
Figure 3. Logarithmic relationship between cumulative num-
ber and sizes of LEO objects. Dots are data published by
National Research Council (1995) while the solid line is the ana-
lytic ﬁt. The data shown are for objects within 1600 kilometres
of the Earth’s surface.
2.2
Zenith sky luminance: An estimate
It follows from Eq. (5) that the number distribution of space
objects is the only otherwise unknown quantity required to
calculate these objects’ contribution to total diﬀuse night
sky brightness. We combined a number of works to esti-
mate this function, assuming n(r, h) = R(r)H(h). The func-
tion R(r) models the size distribution (m−1), while H(h) is
the number concentration of space objects (number m−3).
The cumulative number of LEO objects larger than a given
size has been known for decades (National Research Council
1995). The rate at which the cumulative number of objects,
N(r), declines with increasing size is roughly constant on a
log scale, which allows for the simple logarithmic approx-
imation log N(r) = a log(2r) + b (Fig. 3), where 2r is the
characteristic diameter of objects in meters, and a = −1.98
and b = 2.32 are dimensionless scaling constants.
In Fig. 3, N(r) = n0
R 5m
r
R(r)dr, where n0 = 1.64×1014
is the dimensionless coeﬃcient of proportionality satisfying
the normalization condition
R 5m
5×10−7m R(r)dr = 1. The func-
tion H(h) is scaled to satisfy the following equation
Z 1600km
200km
4πh2H(h) dh
=
n0.
(6)
The integral form for N(r) can be easily transformed into
diﬀerential form R(r) = −1
n0
dN(r)
dr
= −
a
r n0 10a log(2r)+b.
The vertical stratiﬁcation of objects in Earth orbit was mod-
eled in accordance with Bendisch et al. (2004). We have de-
veloped an analytical formula that models the experimental
data reasonably well for altitudes h < 40000 km (Fig. 2).
Assuming h is given in metres, we found
H(h)
=
β 10A(log h−D)/[B+(log h−F )m]−C
(7)
with A=4.02, B=0.60, C=7.3, D=5.35, F=5.3, and m=5.32.
The coeﬃcient of proportionality, β=0.10, was derived from
the normalization condition (Eq. 6).
To estimate the contribution of space objects to the
diﬀuse brightness of the night sky at the zenith we
take E0,λe−τλ to be about E0,vis
≈120,000 lm m−2
(Al-Obaidi et al. 2014; Taleb and Antony 2020), a standard
value for ground-level direct solar illuminance that is consis-
tent with the top-of-the-atmosphere illuminance of 133,600
lm m−2 deduced from the 1985 Wehrli Standard Extrater-
restrial Solar Irradiance Spectrum (NREL 2010; Wehrli
1985; Neckel and Labs 1981). The scattering cross-section
MNRAS 000, 1–6 (2015)

## Page 4

4
M. Kocifaj et al.
1980
1990
2000
2010
2020
0
5000
10000
15000
20000
25000
Object Count (-)
Reference Epoch
Figure 4. Trend of the absolute number of all counted space ob-
jects. Vertical lines with dots represent data provided by ESA
(2020). The solid line is an analytical model.
of a spherical object asymptotically approaches Csca =
πr2Qsca(r) with the average value for all objects
σ
=
2π
Z 5 m
5×10−7 m
r2R(r)dr
(8)
and the contribution from the space objects to the zenith
luminance is
L
=
σαE0,vis
4π
Z 4×107 m
2×105 m
H(h)dh
=
E0,visα
2
Z 5 m
5×10−7 m
r2R(r)dr
Z 4×107 m
2×105 m
H(h)dh
≈
α 7.2 µcd m−2,
(9)
where α is the average albedo of space objects.
Due to their diﬀerent shapes and orientations, the reﬂec-
tivity of space objects can vary substantially. Many space-
craft are made of composite materials, much of them highly
reﬂective for the beneﬁt of thermal management, but other
objects can appear dark because of eﬃcient absorption.
We use the average value of α ≈0.5 in accordance with
Krutz et al. (2011).
Note that the estimate in Eq. (9) is speciﬁcally appli-
cable to conditions during the middle to late 1990s. Based
on the trend published by ESA (2020) (Fig. 4) we found
that the number of known space objects has increased by
a factor of 4.5 since the late 1990s. Therefore, we expect
that today’s contribution from space objects to zenith lumi-
nance is at least (7.2α) × 4.5 = 16.2 µcd m−2. Assuming
the above increase rate remains conserved in next few years,
the luminance may quickly approach 25 µcd m−2 in 2030.
3
DISCUSSION
Any piece of matter in Earth orbit illuminated by the Sun
reﬂects or scatters light, and can in principle be detected
and tracked as an individual moving object if it can be dis-
tinguished from neighboring ones and its radiance is above
the sensitivity threshold of one’s detector. If its angular size
is smaller than the instrument point-spread function (PSF),
what is recorded in the image is essentially the PSF with an
average irradiance directly proportional to the object radi-
ance and inversely proportional to the PSF area. The irradi-
ance detection threshold can be reached either by increasing
the telescope numerical aperture, yielding larger irradiances,
and/or by increasing the responsivity of the detector. Most
present-day instruments used for narrow-ﬁeld imaging or for
large astronomical surveys have enough performance as to
record the individual streaks produced by many of the ob-
jects orbiting Earth, excepting those of very small sizes.
The situation is diﬀerent when observing the night sky
with the unaided eye. The human eye has a PSF with per-
ceptual angular resolution of order 1′, but it has a rela-
tively small light sensitivity in comparison with long expo-
sure images, even under scotopic adaptation. Except for the
brighter ones, most Earth-orbiting objects cannot be visu-
ally detected and tracked individually, since their individual
irradiances fall below the visual detection threshold. How-
ever, if several such objects are present within the receptive
ﬁeld of a retinal ganglion cell, their combined irradiance may
well reach the threshold, and may be perceived as a diﬀuse
skyglow component.
A similar diﬀuse skyglow eﬀect arises when measur-
ing the night sky brightness with highly sensitive but very
low angular resolution detectors. Examples of these devices
are the widely used Sky Quality Meter (SQM; Cinzano
2007) and Telescope Encoder and Sky Sensor-WiFi (TESS-
W; Zamorano 2017), whose PSFs have full widths at half-
maximum of ∼20◦. In that case the radiance of even very
dim space objects may be enough to be individually de-
tected, but the low angular resolution of the instrument
unavoidably integrates the light of the many such objects
present within its ﬁeld of view without resolving each in-
dividual source. This results in an increased value of the
diﬀuse night sky brightness, similar to the one that would
be produced by light pollution from atmospheric scattering
of the radiance emitted by anthropogenic light sources on
the ground.
The estimated strength of this eﬀect, as per direct ap-
plication of Eq. (9), is currently of order 16.2 µcd m−2. Note
that this value was obtained from Eq. (9) by integrating the
contributions of the objects located toward the observer’s
local zenith with a lower integration limit of 200 km, con-
sistent with the object altitude distribution in Fig. 2 and
assuming that only one half of the cross-section of the ob-
ject is illuminated by sunlight as seen from the observer’s
position. This corresponds to the objects’ phase angle at
sunset or sunrise.
At the beginning or the end of the astronomical night,
when the Sun is at –18◦with respect to the horizon, the
Earth shadow reaches 328 km above the observer. Up to this
orbital altitude the space objects are entirely in darkness at
these moments. However, since such low-altitude orbits are
relatively little populated (Fig. 2) the total number of illumi-
nated space objects is still 99.98 per cent of the maximum.
Furthermore, at that time of the night the phase angle of
the objects located above the observer is ±72◦, so that the
fraction of their illuminated surface is 0.65, instead of 0.5.
The skyglow contribution of the space object cloud at the
beginning and end of the astronomical night is then propor-
tionally increased, reaching an estimated value of 21.1 µcd
m−2.
These luminances amount to ∼10 per cent of the natural
night sky brightness, a critical level mentioned in the 1979
resolution of the International Astronomical Union (IAU) as
the limiting acceptable value of light pollution at astronom-
ical observatory sites. According to this criterion, “. . . the
increase in sky brightness at 45◦elevation due to artiﬁcial
MNRAS 000, 1–6 (2015)

## Page 5

Space objects are a new skyglow threat
5
light scattered from clear sky should not exceed 10 per cent
of the lowest natural level in any part of the spectrum be-
tween wavelengths 300 and 1000 nm except for the spectral
line emission from low pressure sodium lamps. . . ” (Cayrel
1979). Although the original criterion refers to the bright-
ness at 45◦elevation, it is reasonable to apply it also to
zenith observations.
The concept of a ‘natural level’ of brightness is in it-
self debatable, since the natural night sky brightness in any
observation band, including the visual one, is widely vari-
able depending on the region of the sky, the location of
the observer, the state of the atmosphere and the highly
ﬂuctuating strength of the airglow, as described in, e.g.,
Masana et al. (2021) and references therein. According to
the Gaia-Hipparcos map, zenith luminance values of 200 µcd
m−2 could be taken as a reasonable ‘dark sky’ luminance
benchmark. A reference level of 22.0 mag arcsec−2 in the
Johnson V band is often quoted in the literature, subject to
the same variability factors as the luminance value.
Note that the true visual luminance of a Johnson V =
22.0 mag arcsec−2 sky is contingent on the arbitrarily chosen
deﬁnition of the V magnitude scale (AB or Vega zero-points,
Vega magnitude, etc.), and also on the spectrum of the in-
coming light. The same Johnson V magnitude may corre-
spond to very diﬀerent sky luminances depending on the
correlated colour temperature (CCT) of the sky spectrum,
as reported in Bar´a et al. (2020). Notwithstanding that, 22.0
Johnson V mag arcsec−2 corresponds to ∼200 µcd m−2 for
typical sky CCTs recorded in observatories across the world
(Bar´a et al. 2020), so both quantities can be taken as sen-
sible and practical reference values for the brightness of the
natural sky.
These results imply that diﬀuse night sky brightness
produced by artiﬁcial space objects directly illuminated by
the Sun may well have reached nowadays, and perhaps ex-
ceeded, what is considered a sustainability ‘red line’ for
ground based astronomical observatory sites. Note that the
data used in Figs. (3-4) are for detected objects only. This
means the real number of objects should be even higher
because, in principle, not all objects have been identiﬁed.
Therefore, the above estimate is a lower limit. This eﬀect
will certainly be aggravated by the planned deployment of
huge satellite ‘mega-constellations’ that will add a substan-
tial number of reﬂecting objects in large-inclination orbits at
altitudes above ∼500 km. The eﬀect of these space objects
on the diﬀuse brightness of the night sky is to be considered
in addition to the streaks of individual objects that tend
to compromise the quality of astronomical images. This is
in our opinion an issue that should be taken into account
by the astrophysical community in its eﬀorts to preserve
science-grade quality night skies.
The approach in this work is a ﬁrst approximation to
the problem, made with some simplifying assumptions. How-
ever, the results in Section 2 were derived from robust ﬁrst
principles and we believe they capture the basic physics of
this eﬀect. Our estimates refer only to the human visual
band; estimates in other bands of the optical region, includ-
ing the near-infrared, would be also informative but were
not addressed in this work.
Observational campaigns to evaluate the strength of
this eﬀect should be planned and carried out. They pose
an interesting methodological problem, since this new sky-
glow component corresponds to a diﬀuse contribution slowly
varying across the night sky, so no sharp borders between an
aﬀected and an unaﬀected area of the sky are to be expected.
If these borders between adjacent patches of the sky were
present, visual inspection could have been enough to detect
this phenomenon: the luminance contrast of a 20 µcd m−2
brighter patch over a 200 µcd m−2 background is 0.1, well
above the human detection contrast threshold for a 6◦zone
surrounded by a 200 µcd m−2 adaptation luminance ﬁeld,
which is 0.07 (Blackwell 1946). The lack of such sharp bor-
ders should prompt the community to make absolute mea-
surements and compare them with models of the natural
night sky and/or to monitor changes in night sky bright-
ness on timescales of order of a few years. Comprehensive
datasets of the present levels of skyglow in dark sites could
provide an instrumental baseline to assess the additional
contribution of the new satellite mega-constellations, and
also to monitor its evolution in forthcoming years.
4
PROSPECTS AND CONCLUSIONS
The cloud of artiﬁcial objects orbiting the Earth, composed
of both operational and decommissioned satellites, parts of
launch vehicles, fragments, and small particles, with char-
acteristic sizes ranging from micrometers to tens of meters,
reﬂect and scatter sunlight toward ground-based observers.
When imaged with high angular resolution and high sensi-
tivity detectors, many of these objects appear as individual
streaks in science images. However, when observed with rel-
atively low-sensitivity detectors like the unaided human eye,
or with low-angular-resolution photometers, their combined
eﬀect is that of a diﬀuse night sky brightness component,
much like the unresolved integrated starlight background of
the Milky Way.
According to our preliminary estimations, this newly
recognised skyglow component could have reached already a
zenith visual luminance of about 20 µcd m−2, which corre-
sponds to 10 per cent of the luminance of a typical natural
night sky, exceeding in that way the IAU’s limiting light
pollution ‘red line’ for astronomical observatory sites. Fu-
ture satellite mega-constellations are expected to increase
signiﬁcantly this light pollution source.
ACKNOWLEDGEMENTS
This work was supported by the Slovak Research and Devel-
opment Agency under contract No: APVV-18-0014. Compu-
tational work was supported by the Slovak National Grant
Agency VEGA (grant No. 2/0010/20). SB acknowledges
support by Xunta de Galicia (grant ED431B 2020/29).
DATA AVAILABILITY STATEMENT
Digitized data shown in Fig. 2-4 and the numerical solvers
used to model zenith NSB are
publicly available
on
http://davinci.fmph.uniba.sk/~kundracik1/debris. We
did not use any new data.
MNRAS 000, 1–6 (2015)

## Page 6

6
M. Kocifaj et al.
REFERENCES
Al-Obaidi K. M. et al., 2014, Front. Archit. Res. 3, 178.
Alshaibani K., 2016, Lighting Res. Technol. 48, 742.
Bar´a et al., 2020, MNRAS 493, 2429
Bendisch et al., 2004, Adv. Space Res. 34, 959
Blackwell H. R., 1946, J. Opt. Soc. Am. 36, 624
Cayrel R., 1979, Trans. Int. Astron. Union, 17, 215
Cinzano, P., 2007, Report on Sky Quality Meter, version L; Tech-
nical Report; ISTIL
ESA, 2020, ESA’s Annual Space Environment Report, GEN-DB-
LOG-00288-OPS-SD, Darmstadt, Germany
Hainaut O. R. et al., 2020, Astron. Astrophys. 636, A121.
Hergert W., Wriedt T., 2012, The Mie theory: Basics and Appli-
cations. Springer Ser. Opt. Sci. 169.
Kocifaj M., Horvath H., 2005, Appl. Opt. 44, 7378
Krutz et al., 2011, Acta Astronaut. 69, 297
Link F., 1969, Eclipse Phenomena in Astronomy. Springer.
Masana et al., 2021, MNRAS 501, 5443
National Research Council, 1995, Orbital Debris: A Technical As-
sessment. Washington, DC: The National Academies Press.
Neckel H., Labs D., 2011, Sol. Phys. 74, 231
NREL,
2021,
1985
Wehrli
Standard
Ex-
traterrestrial
Solar
Irradiance
Spectrum,
www.nrel.gov/grid/solar-resource/spectra-wehrli.html
Shendeleva M. L., 2005, J. Eur. Opt. Soc. 13:10.
Taleb H. M., Antony A. G., 2020, J. Build. Eng. 28, 101034.
Tyson J. A. et al. 2020, Astron. J. 160, 226.
UCS 2021, Union of Concerned Scientists Satellite Database,
www.ucsusa.org/resources/satellite-database
Wehrli, C. Extraterrestrial Solar Spectrum, Publication no. 615,
Physikalisch-Meteorologisches Observatorium + World Radi-
ation Center, Davos Dorf, Switzerland, July 1985.
Zamorano J. et al. 2017, Int. J. Sust. Lighting 18, 49–54.
This paper has been typeset from a TEX/LATEX ﬁle prepared by
the author.
MNRAS 000, 1–6 (2015)
